#!/usr/bin/env python3
"""Verify every ```text block in kit.md is byte-identical to:
  1. its prompts/*.txt file,
  2. the text in index.html's <pre> that the Copy button reads (static HTML parse),
  3. the text the Copy button's own JS function returns in a real browser
     (headless Chrome, if installed).
Then runs the merge-page tests (node tests/test_merge.mjs) and loads merge.html#demo
in headless Chrome to confirm the page renders.
Exit code 0 only if everything passes. Run: python3 verify.py
"""
import json
import re
import shutil
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FILES = ["stage-1.txt", "stage-2.txt", "stage-3-corrections.txt", "stage-4.txt", "stage-5.txt"]
CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "google-chrome", "chromium", "chromium-browser",
]


def extract_blocks(md_bytes):
    """Independent of build.py: content between a ```text line and the next ``` line."""
    return re.findall(rb"^```text\n(.*?)\n```$", md_bytes, flags=re.S | re.M)


class PreText(HTMLParser):
    """Collect decoded text inside <pre class="prompt" id="prompt-N">, plus download hrefs."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.texts, self.hrefs, self._cur = {}, [], None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "pre" and "prompt" in (a.get("class") or "").split():
            self._cur = a["id"]
            self.texts[self._cur] = ""
        if tag == "a" and "dl-link" in (a.get("class") or "").split():
            self.hrefs.append(a["href"])

    def handle_endtag(self, tag):
        if tag == "pre":
            self._cur = None

    def handle_data(self, data):
        if self._cur:
            self.texts[self._cur] += data


def browser_texts():
    chrome = next((c for c in CHROME_CANDIDATES if Path(c).exists() or shutil.which(c)), None)
    if not chrome:
        return None, "no Chrome/Chromium found"
    url = (ROOT / "index.html").as_uri() + "#verify-copy"
    r = subprocess.run([chrome, "--headless=new", "--disable-gpu", "--dump-dom", url],
                       capture_output=True, timeout=60)
    m = re.search(rb'<pre id="verify-out" hidden="">(.*?)</pre>', r.stdout, re.S)
    if not m:
        return None, "verify hook output not found in dumped DOM"
    p = PreText()
    p.feed('<pre class="prompt" id="v">' + m.group(1).decode("utf-8") + "</pre>")
    return {k: v.encode("utf-8") for k, v in json.loads(p.texts["v"]).items()}, chrome


def merge_checks(chrome):
    ok = True
    print("\nMerge page")
    node = shutil.which("node")
    if not node:
        print("  logic tests: FAIL (node not found)")
        ok = False
    else:
        r = subprocess.run([node, str(ROOT / "tests" / "test_merge.mjs")], capture_output=True, text=True, timeout=120)
        last = (r.stdout.strip().splitlines() or ["no output"])[-1]
        print(f"  logic tests: {'PASS' if r.returncode == 0 else 'FAIL'} ({last})")
        if r.returncode != 0:
            print(r.stdout + r.stderr)
            ok = False
    if chrome:
        url = (ROOT / "merge.html").as_uri() + "#demo"
        r = subprocess.run([chrome, "--headless=new", "--disable-gpu", "--virtual-time-budget=3000", "--dump-dom", url],
                           capture_output=True, timeout=60)
        m = re.search(rb'<body[^>]*data-status="([^"]+)"[^>]*>', r.stdout)
        years = re.search(rb'data-inst-years="([^"]*)"', r.stdout)
        mism = re.search(rb'data-mismatches="([^"]*)"', r.stdout)
        good = bool(m and m.group(1) == b"ready" and years and years.group(1) == b"FY2021,FY2025,FY2026"
                    and mism and int(mism.group(1)) > 0)
        print(f"  demo renders in browser: {'PASS' if good else 'FAIL'}"
              f" (status={m.group(1).decode() if m else None}, years={years.group(1).decode() if years else None},"
              f" mismatches={mism.group(1).decode() if mism else None})")
        ok &= good
    else:
        print("  demo renders in browser: SKIP (no Chrome)")
    idx = (ROOT / "index.html").read_text(encoding="utf-8")
    link = 'href="merge.html"' in idx
    print(f"  index.html links to merge.html: {'PASS' if link else 'FAIL'}")
    return ok and link


def first_diff(a, b):
    for i, (x, y) in enumerate(zip(a, b)):
        if x != y:
            return f"first difference at byte {i}"
    return f"lengths differ ({len(a)} vs {len(b)})"


def main():
    ok = True
    blocks = extract_blocks((ROOT / "kit.md").read_bytes())
    print(f"kit.md: found {len(blocks)} ```text blocks (expected {len(FILES)})")
    if len(blocks) != len(FILES):
        print("FAIL: block count mismatch")
        return 1

    parser = PreText()
    parser.feed((ROOT / "index.html").read_text(encoding="utf-8"))
    html_texts = {k: v.encode("utf-8") for k, v in parser.texts.items()}
    btexts, binfo = browser_texts()

    print(f"{'#':<3}{'file':<26}{'bytes':>7}  {'.txt':<6}{'HTML':<6}{'browser':<8}{'link':<5}")
    for n, (block, fname) in enumerate(zip(blocks, FILES), 1):
        txt = (ROOT / "prompts" / fname).read_bytes()
        res = {
            "txt": txt == block,
            "html": html_texts.get(f"prompt-{n}") == block,
            "browser": None if btexts is None else btexts.get(f"prompt-{n}") == block,
            "link": n <= len(parser.hrefs) and parser.hrefs[n - 1] == f"prompts/{fname}",
        }
        fmt = lambda v: "SKIP" if v is None else ("PASS" if v else "FAIL")
        print(f"{n:<3}{fname:<26}{len(block):>7}  {fmt(res['txt']):<6}{fmt(res['html']):<6}"
              f"{fmt(res['browser']):<8}{fmt(res['link']):<5}")
        if not res["txt"]:
            print("   .txt:", first_diff(block, txt))
        if not res["html"]:
            print("   HTML:", first_diff(block, html_texts.get(f"prompt-{n}", b"")))
        if res["browser"] is False:
            print("   browser:", first_diff(block, btexts.get(f"prompt-{n}", b"")))
        ok &= all(v is not False for v in res.values())

    print(f"Browser check: {'ran with ' + binfo if btexts is not None else 'skipped (' + binfo + ')'}")

    ok &= merge_checks(binfo if btexts is not None else None)
    print("RESULT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
