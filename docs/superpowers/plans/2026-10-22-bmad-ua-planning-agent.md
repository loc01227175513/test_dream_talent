# BMAD + Understand-Anything Planning Agent — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Một lệnh `./run.sh https://moso.vn` tự động: thu thập hệ thống → chạy workflow **BMAD Method thật** (Analyst → PM → Architect) sinh SRS → chuyển tài liệu thành wiki → chạy **Understand-Anything thật** (`/understand-knowledge`) sinh knowledge graph + dashboard.

**Architecture:** Python (stdlib) làm phần deterministic: crawl, dựng wiki, kiểm tra đầu ra. Phần LLM do Claude Code headless (`claude -p`) gọi đúng các skill/command của BMAD và Understand-Anything. Mỗi stage ghi file vào `out/`; stage đã có file thì được bỏ qua (resume). Graph tự viết hiện tại (`graph.html`) giữ lại làm bản fallback / đối chiếu.

**Tech Stack:** Python 3 stdlib, Bash, Claude Code CLI, `bmad-method@6.12.4` (npx), plugin `Egonex-AI/Understand-Anything`.

**Spec:** Đề bài (nguyên văn, xem Global Constraints) + bản đã làm: `agent.py`, `out/brief.md`, `out/SRS.md`, commit `d898bd3`.

## Hiện trạng: đúng / chưa đúng

| Yêu cầu đề | Hiện trạng | Đánh giá |
|---|---|---|
| Agent **tự động** phân tích hệ thống | `agent.py` có pipeline nhưng chưa chạy end-to-end lần nào (`claude -p` OAuth hết hạn) | ⚠️ chưa chứng minh |
| Kết hợp **BMAD Method** | Chỉ nhắc tên persona trong prompt; chưa cài `bmad-method`, không dùng template/workflow | ❌ sai yêu cầu |
| Kết hợp **Understand-Anything** | Tự viết vis-network; chưa cài plugin, không có `.ua/knowledge-graph.json` | ❌ sai yêu cầu |
| Phân tích features moso.vn | 48 feature / 11 module có nguồn | ✅ |
| Xuất SRS | IEEE 830, 45 FR, 15 NFR, truy vết | ✅ (nhưng không theo template BMAD) |
| Biểu diễn knowledge graph | 125 node / 205 edge, render OK | ✅ (không phải bằng UA) |
| Trình bày / tái lập | Không README, không log chạy | ❌ |

## Global Constraints

- Đề: "Xây dựng Agent tự động phân tích hệ thống và sinh tài liệu SRS + Knowledge Graph bằng cách kết hợp BMAD Method + Understand-anything".
- Đề: "Dùng luồng đó phân tích features, xuất SRS và biểu diễn knowledge graph cho https://moso.vn/".
- BMAD: `npx bmad-method@6.12.4 install` — pin đúng version.
- Understand-Anything: `/plugin marketplace add Egonex-AI/Understand-Anything` + `/plugin install understand-anything`; output tại `.ua/knowledge-graph.json`; ngôn ngữ `--language vi`.
- Crawl tôn trọng rate limit moso.vn: `/api/markdown` 30 req/phút/IP.
- Ngôn ngữ tài liệu đầu ra: tiếng Việt.
- Không commit secrets; `out/corpus.md` được commit (dữ liệu công khai, phục vụ tái lập).

## Review Focus

1. **`claude -p` lỗi auth / lỗi giữa chừng** → pipeline phải dừng với thông báo rõ và exit ≠ 0, không ghi file rỗng làm "cache" (hiện `stage()` ghi trước khi chắc chắn thành công là đúng thứ tự, nhưng output rỗng vẫn bị lưu). Test: Task 2.
2. **Crawl vượt rate limit (HTTP 429)** → chờ theo `Retry-After` rồi thử lại, không lưu trang lỗi vào corpus. Test: Task 1.
3. **BMAD workflow hỏi tương tác** (elicitation) trong chế độ headless → prompt phải ra lệnh chế độ YOLO/không hỏi; output thiếu section bắt buộc → validator báo lỗi. Test: Task 3.
4. **Wikilink gãy** (`[[F-99]]` không có trang) → UA dựng node mồ côi; builder phải kiểm tra mọi link trỏ tới file tồn tại. Test: Task 4.
5. **Plugin UA chưa cài / không sinh `.ua/knowledge-graph.json`** → `run.sh` báo cách cài và vẫn sinh fallback `out/graph.html`. Test: Task 5.

---

## File Structure

| File | Trách nhiệm |
|---|---|
| `agent.py` (sửa) | Crawl + `stage()` cache; thêm retry 429, chặn output rỗng |
| `wiki.py` (mới) | Dựng wiki kiểu Karpathy từ `out/brief.md` + `out/SRS.md` → `wiki/` |
| `validate.py` (mới) | Kiểm tra SRS có đủ section, mọi `F-xx` trong SRS có trong brief |
| `run.sh` (mới) | Điều phối: crawl → BMAD qua `claude -p` → wiki → UA → validate |
| `prompts/bmad-*.md` (mới) | Lệnh headless gọi đúng agent/workflow BMAD |
| `tests/test_pipeline.py` (mới) | Tất cả unit test (stdlib `unittest`) |
| `README.md` (mới) | Sơ đồ luồng, cách chạy, kết quả, giới hạn |
| `_bmad/`, `.claude/` | Do installer BMAD/UA sinh — commit để tái lập |

---

### Task 1: Crawl bền vững (retry 429)

**Files:** Modify `agent.py` (hàm `get`); Test `tests/test_pipeline.py`

**Interfaces:**
- Produces: `get(url: str, opener=urllib.request.urlopen, sleep=time.sleep) -> str` — trả nội dung; ném `RuntimeError` sau 3 lần 429/lỗi mạng (không trả chuỗi `<!-- fetch failed -->` nữa). `crawl()` bỏ qua trang ném lỗi và in cảnh báo ra stderr.

- [ ] **Step 1: Viết test fail**
```python
def test_get_retries_on_429_then_succeeds(self):
    calls = []
    def opener(req, timeout):
        calls.append(1)
        if len(calls) < 2:
            raise urllib.error.HTTPError(req.full_url, 429, "x", {"Retry-After": "1"}, None)
        return io.BytesIO("ok".encode())
    slept = []
    self.assertEqual(agent.get("https://x", opener=opener, sleep=slept.append), "ok")
    self.assertEqual(slept, [1])

def test_get_raises_after_three_failures(self):
    def opener(req, timeout): raise urllib.error.URLError("down")
    with self.assertRaises(RuntimeError):
        agent.get("https://x", opener=opener, sleep=lambda s: None)
```
- [ ] **Step 2:** `python3 -m unittest tests.test_pipeline -v` → FAIL (`get()` không nhận `opener`).
- [ ] **Step 3:** Sửa `get` theo interface; thread pool trong `crawl()` giảm còn 4 worker.
- [ ] **Step 4:** Chạy lại test → PASS.
- [ ] **Step 5:** `git commit -am "fix(agent): retry 429 and fail loudly on fetch errors"`

### Task 2: Stage không lưu output rỗng / lỗi

**Files:** Modify `agent.py` (`llm`, `stage`); Test `tests/test_pipeline.py`

**Interfaces:**
- Produces: `stage(name: str, prompt: str, run=llm) -> str` — chỉ ghi `out/<name>` khi `run(prompt).strip()` khác rỗng; rỗng → `SystemExit` với message chứa `name`.

- [ ] **Step 1: Test fail**
```python
def test_stage_does_not_cache_empty_output(self):
    with self.assertRaises(SystemExit):
        agent.stage("t_empty.md", "p", run=lambda p: "  ")
    self.assertFalse((agent.OUT / "t_empty.md").exists())

def test_stage_uses_cache(self):
    (agent.OUT / "t_cached.md").write_text("cached")
    self.assertEqual(agent.stage("t_cached.md", "p", run=lambda p: 1/0), "cached")
```
- [ ] **Step 2:** Run → FAIL.
- [ ] **Step 3:** Thêm tham số `run`, kiểm tra rỗng trước khi ghi.
- [ ] **Step 4:** Run → PASS.
- [ ] **Step 5:** Commit `"fix(agent): never cache empty LLM output"`

### Task 3: Tích hợp BMAD Method thật

**Files:** Create `prompts/bmad-analyst.md`, `prompts/bmad-pm.md`, `prompts/bmad-architect.md`, `validate.py`; commit `_bmad/`, `.claude/commands|skills` do installer sinh; Test `tests/test_pipeline.py`

**Interfaces:**
- Consumes: `out/corpus.md` (Task 1).
- Produces: `out/brief.md` (product-brief BMAD), `out/SRS.md` (PRD BMAD + phụ lục IEEE 830), `out/architecture.md`; `validate.check_srs(srs: str, brief: str) -> list[str]` trả danh sách lỗi (rỗng = hợp lệ).

- [ ] **Step 1: Cài BMAD** `npx bmad-method@6.12.4 install` (chọn module BMM, IDE Claude Code, ngôn ngữ tài liệu Vietnamese). Kiểm tra: `ls _bmad` có agents `analyst`, `pm`, `architect`; ghi lại tên chính xác các command/skill sinh trong `.claude/` vào README (dùng cho Step 3).
- [ ] **Step 2: Test fail cho validator**
```python
def test_check_srs_flags_missing_section_and_unknown_feature(self):
    errs = validate.check_srs("## Functional Requirements\nFR-01 ... F-99", "F-01")
    self.assertIn("missing section: Non-Functional Requirements", errs)
    self.assertIn("unknown feature: F-99", errs)

def test_check_srs_ok_on_current_outputs(self):
    self.assertEqual(validate.check_srs(Path("out/SRS.md").read_text(), Path("out/brief.md").read_text()), [])
```
Section bắt buộc (khớp cả tiếng Việt hoặc Anh): Giới thiệu/Introduction, Yêu cầu chức năng/Functional Requirements, Yêu cầu phi chức năng/Non-Functional Requirements, Epics, Ma trận truy vết/Traceability.
- [ ] **Step 3:** Viết 3 prompt: mỗi file gọi đúng command BMAD tìm được ở Step 1 (analyst → product brief; pm → PRD; architect → architecture), chỉ định file input/output trong `out/`, ra lệnh **chạy YOLO, không hỏi lại người dùng**, giữ quy ước ID `F-xx`/`FR-xx`/`NFR-xx`, và với PM thêm phụ lục IEEE 830 + Given/When/Then.
- [ ] **Step 4:** Implement `validate.py` (`check_srs` + `__main__` in lỗi, exit 1 nếu có).
- [ ] **Step 5:** `python3 -m unittest tests.test_pipeline -v` → PASS.
- [ ] **Step 6:** Commit `"feat: integrate BMAD Method agents and SRS validator"`

### Task 4: Wiki builder cho Understand-Anything

**Files:** Create `wiki.py`; Test `tests/test_pipeline.py`

**Interfaces:**
- Consumes: `out/brief.md`, `out/SRS.md` (ID và bảng như hiện tại).
- Produces: `build_wiki(brief: str, srs: str, dest: Path) -> list[Path]` — ghi `dest/index.md` (danh mục theo category: Actors, Modules, Features, Requirements, Integrations, mỗi mục là `[[slug]]`) và mỗi entity một file `<ID>.md` có mô tả + wikilink tới entity liên quan (module→feature, feature→FR, actor→feature theo bảng `uses` hiện tại trong lịch sử script graph); `broken_links(dest: Path) -> list[str]`.

- [ ] **Step 1: Test fail**
```python
def test_build_wiki_links_feature_to_requirement(self):
    d = Path(tempfile.mkdtemp())
    wiki.build_wiki(Path("out/brief.md").read_text(), Path("out/SRS.md").read_text(), d)
    self.assertIn("[[FR-08]]", (d / "F-10.md").read_text())
    self.assertIn("[[F-10]]", (d / "M2.md").read_text())
    self.assertEqual(wiki.broken_links(d), [])
```
- [ ] **Step 2:** Run → FAIL.
- [ ] **Step 3:** Implement — tái dùng regex parse brief/SRS đã dùng để sinh `out/graph.raw.json` (feature table `| F-xx | name | desc | src |`, heading `#### FR-xx`, dòng `Truy vết:`, bảng FR trong M7/M10). Bảng actor→feature và feature→integration chuyển thành dict hằng trong `wiki.py`.
- [ ] **Step 4:** Run → PASS.
- [ ] **Step 5:** Commit `"feat: build Karpathy-pattern wiki from BMAD docs"`

### Task 5: Điều phối end-to-end + Understand-Anything

**Files:** Create `run.sh`; Modify `agent.py` (`__main__` chỉ còn crawl + fallback graph); Test: chạy thật

**Interfaces:**
- Consumes: Task 1–4.
- Produces: `./run.sh <url>` → `out/corpus.md`, `out/brief.md`, `out/SRS.md`, `out/architecture.md`, `wiki/`, `.ua/knowledge-graph.json`, `out/graph.html` (fallback), `out/run.log`.

- [ ] **Step 1: Cài UA** trong Claude Code: `/plugin marketplace add Egonex-AI/Understand-Anything` rồi `/plugin install understand-anything`. Kiểm tra `claude -p "/understand-knowledge --help"` không lỗi "unknown command".
- [ ] **Step 2:** Viết `run.sh` (`set -euo pipefail`, `tee out/run.log`): (1) `claude -p "say ok"` — fail → in "Run: claude /login" và exit 1; (2) `python3 agent.py --crawl-only "$1"`; (3) với mỗi `prompts/bmad-*.md` chưa có output: `claude -p --permission-mode acceptEdits < prompt`; (4) `python3 validate.py`; (5) `python3 wiki.py`; (6) `claude -p "/understand-knowledge wiki --language vi"`; nếu không có `.ua/knowledge-graph.json` → cảnh báo cài plugin; (7) luôn sinh fallback `out/graph.html`.
- [ ] **Step 3: Chạy thật từ đầu**: `rm -f out/brief.md out/SRS.md out/architecture.md out/graph.raw.json && ./run.sh https://moso.vn`. Expected: exit 0; `python3 validate.py` không lỗi; `python3 -c "import json;g=json.load(open('.ua/knowledge-graph.json'));print(len(g['nodes']))"` ≥ 100.
- [ ] **Step 4:** `claude` → `/understand-dashboard`, chụp màn hình dashboard vào `docs/img/ua-dashboard.png`; mở `out/graph.html` chụp `docs/img/fallback-graph.png`.
- [ ] **Step 5:** `python3 -m unittest tests.test_pipeline -v` → PASS toàn bộ.
- [ ] **Step 6:** Commit `"feat: end-to-end BMAD + Understand-Anything run for moso.vn"` (gồm `out/`, `wiki/`, `.ua/`, `run.log`, ảnh).

### Task 6: README nộp bài

**Files:** Create `README.md`

- [ ] **Step 1:** Viết README tiếng Việt gồm: sơ đồ Mermaid luồng `moso.vn → crawl (llms.txt/sitemap/markdown) → BMAD Analyst → PM → Architect → validate → wiki → Understand-Anything → graph/dashboard`; bảng ánh xạ "bước ↔ công cụ ↔ file đầu ra"; cách cài & chạy (3 lệnh); tóm tắt kết quả (số feature/FR/NFR/node/edge lấy từ lần chạy Task 5); 2 ảnh chụp; giới hạn & hướng mở rộng (crawl cấp listing, check quy hoạch, câu hỏi mở trong SRS §7).
- [ ] **Step 2:** Kiểm tra mọi link trong README trỏ tới file tồn tại: `grep -o '](\./[^)]*)' README.md` và `ls` từng path.
- [ ] **Step 3:** Commit `"docs: README for submission"`; hỏi người dùng trước khi push.

---

## Self-review
- Phủ yêu cầu đề: tự động (Task 5), BMAD thật (Task 3), UA thật (Task 4–5), features/SRS/graph moso.vn (Task 3–5), trình bày (Task 6). ✅
- Interface nhất quán: `get`, `stage`, `check_srs`, `build_wiki`, `broken_links` dùng cùng tên ở các task. ✅
- Rủi ro chặn: Task 3 Step 1 và Task 5 Step 1 cần người dùng có Claude Code đăng nhập được (`claude /login`) — đây là điều kiện tiên quyết duy nhất.
