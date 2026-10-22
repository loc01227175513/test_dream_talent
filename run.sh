#!/usr/bin/env bash
# Planning agent: crawl -> BMAD (Analyst -> PM -> Architect) -> validate -> wiki -> Understand-Anything graph.
# Usage: ./run.sh https://moso.vn [max_pages]   (stages whose output exists are skipped; delete to rerun)
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p out
exec > >(tee -a out/run.log) 2>&1
echo "== run $(date -u +%FT%TZ) $*"

claude_run() { claude -p --permission-mode acceptEdits "$@"; }

echo ok | claude -p >/dev/null 2>&1 || { echo "Claude Code not logged in. Run: claude /login"; exit 1; }

echo "== 1/5 crawl";      python3 agent.py --crawl-only "${1:-https://moso.vn}" "${2:-60}"
for s in analyst:brief.md pm:SRS.md architect:architecture.md; do
  out="out/${s#*:}"
  [ -s "$out" ] && { echo "== BMAD ${s%%:*}: cached $out"; continue; }
  echo "== 2/5 BMAD ${s%%:*} -> $out"
  claude_run < "prompts/bmad-${s%%:*}.md"
  [ -s "$out" ] || { echo "BMAD ${s%%:*} did not write $out"; exit 1; }
done

echo "== 3/5 validate";   python3 validate.py
echo "== 4/5 wiki";       python3 wiki.py wiki

echo "== 5/5 Understand-Anything"
if claude plugin list 2>/dev/null | grep -q understand-anything; then
  claude_run "/understand-knowledge wiki --language vi"
else
  echo "WARN: plugin missing. Install: claude plugin marketplace add Egonex-AI/Understand-Anything && claude plugin install understand-anything"
fi
G=$(ls .ua/knowledge-graph.json .understand-anything/knowledge-graph.json 2>/dev/null | head -1 || true)
[ -n "$G" ] && python3 -c "import json,sys;g=json.load(open(sys.argv[1]));print('UA graph:',sys.argv[1],len(g.get('nodes',[])),'nodes')" "$G" \
  || echo "WARN: no Understand-Anything graph; fallback only"

python3 agent.py --render-fallback
echo "== done"
