#!/usr/bin/env python3
"""Deterministic half of the planning agent (run.sh drives the LLM half via BMAD + Understand-Anything).

  python3 agent.py --crawl-only https://moso.vn [max_pages]  -> out/corpus.md (cached; delete to re-crawl)
  python3 agent.py --render-fallback                          -> out/graph.json + out/graph.html from wiki.parse
"""
import json, re, sys, time, urllib.error, urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

OUT = Path("out"); OUT.mkdir(exist_ok=True)


def get(url, opener=urllib.request.urlopen, sleep=time.sleep):
    req = urllib.request.Request(url, headers={"User-Agent": "planning-agent", "Accept": "text/markdown"})
    for attempt in range(3):
        try:
            return opener(req, timeout=20).read().decode("utf-8", "ignore")
        except urllib.error.HTTPError as e:
            if e.code != 429 or attempt == 2:
                raise RuntimeError(f"fetch failed {url}: {e}") from e
            sleep(int(e.headers.get("Retry-After", 5)))
        except OSError as e:  # URLError, timeouts
            if attempt == 2:
                raise RuntimeError(f"fetch failed {url}: {e}") from e
            sleep(2)


def crawl(site, max_pages):
    # Understand-Anything "scan": prefer machine-readable sources (llms.txt, sitemap, markdown endpoint).
    urls = re.findall(r"<loc>([^<]+)</loc>", get(f"{site}/sitemap-static.xml"))[:max_pages] or [site]
    # ponytail: only static sitemap + 2k chars/page; per-listing crawl if listing-level detail needed
    def page(u):
        path = u.replace(site, "") or "/"
        try:
            md = get(f"{site}/api/markdown?path={path}")
        except RuntimeError as e:
            print(f"skip {path}: {e}", file=sys.stderr)
            return ""
        md = re.sub(r"\n{3,}", "\n\n", md)
        return f"\n\n=== PAGE {path} ===\n{md[:2000]}"
    with ThreadPoolExecutor(4) as ex:  # /api/markdown allows 30 req/min/IP; 429s are retried
        pages = "".join(ex.map(page, urls))
    return f"=== llms.txt ===\n{get(site + '/llms.txt')[:12000]}{pages}"


HTML = """<!doctype html><meta charset=utf-8><title>Knowledge Graph</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/vis-network/9.1.9/standalone/umd/vis-network.min.js"></script>
<style>html,body{margin:0;height:100%;font:14px system-ui;background:#fff}#g{height:100%}#i{position:fixed;top:8px;left:8px;max-width:340px;background:#fffd;padding:8px;border:1px solid #ccc}</style>
<div id=i>Click a node</div><div id=g></div><script>
const D=__DATA__,C={actor:'#e76f51',module:'#264653',feature:'#2a9d8f',requirement:'#e9c46a',entity:'#8ab17d',integration:'#9b5de5',page:'#adb5bd'};
const n=new vis.DataSet(D.nodes.map(x=>({...x,color:C[x.type]||'#999',shape:x.type=='module'?'box':'dot',font:{color:x.type=='module'?'#fff':'#222'}})));
const net=new vis.Network(g,{nodes:n,edges:D.edges.map(e=>({...e,arrows:'to',font:{size:9}}))},{physics:{solver:'forceAtlas2Based'}});
net.on('click',p=>{const x=p.nodes[0]&&n.get(p.nodes[0]);if(x)i.innerHTML=`<b>${x.label}</b> <i>${x.type}</i><br>${x.desc||''}`})
</script>"""


def fallback_graph(brief, srs):
    # Same entities/links as the wiki, rendered without Understand-Anything (for offline review).
    import wiki
    modules, features, reqs = wiki.parse(brief, srs)
    nodes = [dict(id=k, label=v, type="module") for k, v in modules.items()]
    nodes += [dict(id=k, label=n, type="feature", desc=d) for k, (n, d, _) in features.items()]
    nodes += [dict(id=k, label=f"{k} {t}", type="requirement") for k, (t, _) in reqs.items()]
    nodes += [dict(id=k, label=n, type=t) for t, g in (("actor", wiki.ACTORS), ("integration", wiki.INTEGRATIONS)) for k, (n, _) in g.items()]
    edges = [{"from": m, "to": f, "label": "contains"} for f, (_, _, m) in features.items()]
    edges += [{"from": f, "to": r, "label": "specified_by"} for r, (_, fs) in reqs.items() for f in fs]
    edges += [{"from": k, "to": f, "label": "uses"} for k, (_, fs) in wiki.ACTORS.items() for f in fs.split()]
    edges += [{"from": f, "to": k, "label": "calls"} for k, (_, fs) in wiki.INTEGRATIONS.items() for f in fs.split()]
    ids = {n["id"] for n in nodes}
    return {"nodes": nodes, "edges": [e for e in edges if e["from"] in ids and e["to"] in ids]}


if __name__ == "__main__":
    if "--render-fallback" in sys.argv:
        g = fallback_graph((OUT / "brief.md").read_text(), (OUT / "SRS.md").read_text())
        (OUT / "graph.json").write_text(json.dumps(g, ensure_ascii=False, indent=1))
        (OUT / "graph.html").write_text(HTML.replace("__DATA__", json.dumps(g, ensure_ascii=False)))
        sys.exit(print(f"fallback graph: {len(g['nodes'])} nodes, {len(g['edges'])} edges -> out/graph.html"))
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    site = (args[0] if args else "https://moso.vn").rstrip("/")
    cache = OUT / "corpus.md"
    if not cache.exists():
        cache.write_text(crawl(site, int(args[1]) if len(args) > 1 else 60))
    print(f"corpus: {cache} ({cache.stat().st_size} bytes)")
