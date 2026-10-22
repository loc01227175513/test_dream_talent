#!/usr/bin/env python3
"""Planning agent: site -> corpus -> BMAD (Analyst -> PM -> Architect) -> SRS.md + graph.json + graph.html.

Usage: python3 agent.py https://moso.vn [max_pages]
LLM = `claude -p` (Claude Code headless). Corpus is cached in out/corpus.md; delete to re-crawl.
"""
import json, re, subprocess, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

SITE = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "https://moso.vn"
MAX = int(sys.argv[2]) if len(sys.argv) > 2 else 60
OUT = Path("out"); OUT.mkdir(exist_ok=True)


def get(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "planning-agent", "Accept": "text/markdown"})
        return urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "ignore")
    except Exception as e:
        return f"<!-- fetch failed {url}: {e} -->"


def crawl():
    # Understand-Anything "scan": prefer machine-readable sources (llms.txt, sitemap, markdown endpoint).
    urls = re.findall(r"<loc>([^<]+)</loc>", get(f"{SITE}/sitemap-static.xml"))[:MAX] or [SITE]
    # ponytail: only static sitemap + 2k chars/page; per-listing crawl if listing-level detail needed
    def page(u):
        path = u.replace(SITE, "") or "/"
        md = get(f"{SITE}/api/markdown?path={path}")
        md = re.sub(r"\n{3,}", "\n\n", md)
        return f"\n\n=== PAGE {path} ===\n{md[:2000]}"
    with ThreadPoolExecutor(8) as ex:
        pages = "".join(ex.map(page, urls))
    return f"=== llms.txt ===\n{get(SITE + '/llms.txt')[:12000]}{pages}"


def llm(prompt):
    r = subprocess.run(["claude", "-p", "--output-format", "text"], input=prompt, capture_output=True, text=True, timeout=1800)
    if r.returncode:
        sys.exit(f"claude -p failed: {r.stderr or r.stdout}")
    return r.stdout.strip()


def stage(name, prompt):
    # Every stage caches to out/<name>; rerun resumes, and a human/agent can hand-edit any stage.
    f = OUT / name
    if not f.exists():
        print(f"{name}..."); f.write_text(llm(prompt))
    return f.read_text()


ANALYST = """Bạn là BMAD Analyst (Mary). Từ corpus website dưới đây, viết Product Brief tiếng Việt:
vấn đề, người dùng/persona (actor), giá trị cốt lõi, danh sách FEATURE theo module (mỗi feature: ID F-xx, tên, mô tả, URL nguồn).
Chỉ dùng sự thật có trong corpus; suy luận thì đánh dấu (giả định).\n\nCORPUS:\n{c}"""

PM = """Bạn là BMAD PM (John). Từ Product Brief, viết SRS chuẩn IEEE 830 (Markdown, tiếng Việt):
1 Giới thiệu (mục đích, phạm vi, thuật ngữ) 2 Mô tả tổng quan (actor, ràng buộc, giả định)
3 Yêu cầu chức năng: mỗi FR-xx gồm mô tả, actor, tiền điều kiện, luồng chính, acceptance criteria (Given/When/Then), truy vết F-xx
4 Yêu cầu phi chức năng (NFR-xx: hiệu năng, bảo mật, SEO/AI-crawl, khả dụng, pháp lý VN)
5 Epics & User Stories ưu tiên MoSCoW 6 Ma trận truy vết. Chỉ xuất Markdown.\n\nBRIEF:\n{b}"""

ARCH = """Bạn là BMAD Architect (Winston) kết hợp Understand-Anything. Từ SRS, dựng knowledge graph.
Chỉ xuất JSON hợp lệ, không markdown fence: {{"nodes":[{{"id","label","type","desc"}}],"edges":[{{"from","to","label"}}]}}
type ∈ actor|module|feature|requirement|entity|integration|page. Nối actor->feature (uses), module->feature (contains),
feature->requirement (specified_by), feature->entity (reads/writes), feature->integration (calls). 60-150 nodes.\n\nSRS:\n{s}"""


def graph_json(text):
    return json.loads(text[text.find("{"): text.rfind("}") + 1])


HTML = """<!doctype html><meta charset=utf-8><title>Knowledge Graph</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/vis-network/9.1.9/standalone/umd/vis-network.min.js"></script>
<style>html,body{margin:0;height:100%;font:14px system-ui;background:#fff}#g{height:100%}#i{position:fixed;top:8px;left:8px;max-width:340px;background:#fffd;padding:8px;border:1px solid #ccc}</style>
<div id=i>Click a node</div><div id=g></div><script>
const D=__DATA__,C={actor:'#e76f51',module:'#264653',feature:'#2a9d8f',requirement:'#e9c46a',entity:'#8ab17d',integration:'#9b5de5',page:'#adb5bd'};
const n=new vis.DataSet(D.nodes.map(x=>({...x,color:C[x.type]||'#999',shape:x.type=='module'?'box':'dot',font:{color:x.type=='module'?'#fff':'#222'}})));
const net=new vis.Network(g,{nodes:n,edges:D.edges.map(e=>({...e,arrows:'to',font:{size:9}}))},{physics:{solver:'forceAtlas2Based'}});
net.on('click',p=>{const x=p.nodes[0]&&n.get(p.nodes[0]);if(x)i.innerHTML=`<b>${x.label}</b> <i>${x.type}</i><br>${x.desc||''}`})
</script>"""


if __name__ == "__main__":
    cache = OUT / "corpus.md"
    if not cache.exists():
        cache.write_text(crawl())
    corpus = cache.read_text()
    brief = stage("brief.md", ANALYST.format(c=corpus))
    srs = stage("SRS.md", PM.format(b=brief))
    g = graph_json(stage("graph.raw.json", ARCH.format(s=srs)))
    ids = {x["id"] for x in g["nodes"]}
    g["edges"] = [e for e in g["edges"] if e["from"] in ids and e["to"] in ids]  # drop dangling edges
    (OUT / "graph.json").write_text(json.dumps(g, ensure_ascii=False, indent=1))
    (OUT / "graph.html").write_text(HTML.replace("__DATA__", json.dumps(g, ensure_ascii=False)))
    print(f"done: {len(g['nodes'])} nodes, {len(g['edges'])} edges -> out/")
