#!/usr/bin/env python3
"""Build index.html and prompts/*.txt from kit.md.

Prompt text (every ```text block) is copied byte-for-byte; it is only
HTML-escaped for embedding, never reflowed or trimmed.
Run: python3 build.py
"""
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROMPT_FILES = [
    "stage-1.txt",
    "stage-2.txt",
    "stage-3-corrections.txt",
    "stage-4.txt",
    "stage-5.txt",
]
PROMPT_LABELS = [
    "Stage 1 prompt",
    "Stage 2 prompt",
    "Stage 3 correction prompt",
    "Stage 4 prompt",
    "Stage 5 prompt",
]


def inline(s):
    """Escape HTML, then render `code` and **bold**."""
    parts = re.split(r"(`[^`]*`)", s)
    out = []
    for p in parts:
        if len(p) >= 2 and p.startswith("`") and p.endswith("`"):
            out.append("<code>" + html.escape(p[1:-1], quote=False) + "</code>")
        else:
            e = html.escape(p, quote=False)
            e = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", e)
            out.append(e)
    return "".join(out)


def slugify(s, used):
    base = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-") or "section"
    slug, n = base, 2
    while slug in used:
        slug, n = f"{base}-{n}", n + 1
    used.add(slug)
    return slug


def split_row(line):
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [c.strip() for c in line.split("|")]


def convert(md):
    """Return (title, body_html, toc_entries, prompts)."""
    lines = md.split("\n")
    out, toc, prompts, used = [], [], [], set()
    title = "Prompt Kit"
    i = 0
    while i < len(lines):
        line = lines[i]

        # Fenced code block
        if line.startswith("```"):
            lang = line[3:].strip()
            j = i + 1
            while j < len(lines) and lines[j] != "```":
                j += 1
            body = "\n".join(lines[i + 1 : j])
            if lang == "text":
                n = len(prompts)
                prompts.append(body)
                fname = PROMPT_FILES[n]
                label = PROMPT_LABELS[n]
                out.append(
                    f'<figure class="prompt-box">'
                    f'<div class="prompt-bar"><span class="prompt-label">{html.escape(label)}</span>'
                    f'<span class="prompt-actions">'
                    f'<button type="button" class="copy-btn" data-target="prompt-{n + 1}">Copy</button>'
                    f'<a class="dl-link" href="prompts/{fname}" download="{fname}">Download .txt</a>'
                    f"</span></div>"
                    # No newline after the opening tag: browsers drop one leading newline in <pre>.
                    f'<pre class="prompt" id="prompt-{n + 1}">{html.escape(body, quote=False)}</pre>'
                    f"</figure>"
                )
            else:
                out.append(f"<pre class=\"code\">{html.escape(body, quote=False)}</pre>")
            i = j + 1
            continue

        # Headings
        m = re.match(r"^(#{1,6}) (.*)$", line)
        if m:
            level, text = len(m.group(1)), m.group(2).strip()
            if level == 1:
                title = text
                out.append(f"<h1>{inline(text)}</h1>")
            else:
                slug = slugify(text, used)
                if level in (2, 3):
                    toc.append((level, slug, text))
                out.append(f'<h{level} id="{slug}">{inline(text)}</h{level}>')
            i += 1
            continue

        # Tables
        if line.startswith("|") and i + 1 < len(lines) and re.match(r"^\|\s*:?-+", lines[i + 1]):
            head = split_row(line)
            i += 2
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append(split_row(lines[i]))
                i += 1
            t = ['<div class="table-wrap"><table><thead><tr>']
            t += [f"<th>{inline(c)}</th>" for c in head]
            t.append("</tr></thead><tbody>")
            for r in rows:
                t.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>")
            t.append("</tbody></table></div>")
            out.append("".join(t))
            continue

        # Lists (ordered / unordered / checklist), with indented continuation items
        if re.match(r"^(\d+\. |- )", line):
            ordered = bool(re.match(r"^\d+\. ", line))
            items = []
            while i < len(lines) and re.match(r"^(\d+\. |- )", lines[i]):
                text = re.sub(r"^(\d+\. |- )", "", lines[i])
                items.append(text)
                i += 1
            tag = "ol" if ordered else "ul"
            is_check = all(t.startswith("[ ] ") or t.startswith("[x] ") for t in items)
            cls = ' class="checklist"' if is_check else ""
            lis = []
            for t in items:
                if is_check:
                    checked = " checked" if t.startswith("[x]") else ""
                    lis.append(f'<li><label><input type="checkbox"{checked}> {inline(t[4:])}</label></li>')
                else:
                    lis.append(f"<li>{inline(t)}</li>")
            out.append(f"<{tag}{cls}>" + "".join(lis) + f"</{tag}>")
            continue

        # Blank line
        if not line.strip():
            i += 1
            continue

        # Paragraph
        para = []
        while i < len(lines) and lines[i].strip() and not re.match(r"^(#|```|\||\d+\. |- )", lines[i]):
            para.append(lines[i])
            i += 1
        out.append(f"<p>{inline(' '.join(para))}</p>")
    return title, "\n".join(out), toc, prompts


CSS = r"""
:root{--bg:#fbfbfa;--fg:#1f2328;--muted:#5d6670;--line:#d9dde1;--panel:#f2f4f6;--code-bg:#f5f6f7;--accent:#0b5cad;--accent-fg:#fff;--ok:#1a7f37;--th:#eef1f4}
@media (prefers-color-scheme:dark){:root{--bg:#121417;--fg:#e4e7ea;--muted:#9aa4ae;--line:#30363d;--panel:#1a1e23;--code-bg:#171b20;--accent:#5aa2f0;--accent-fg:#0b1220;--ok:#4cc26a;--th:#1f242a}}
*{box-sizing:border-box}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
a{color:var(--accent)}
.layout{display:grid;grid-template-columns:260px minmax(0,1fr);gap:40px;max-width:1180px;margin:0 auto;padding:0 24px}
nav.toc{position:sticky;top:0;align-self:start;max-height:100vh;overflow:auto;padding:28px 0 28px;font-size:14px}
nav.toc details{border:0}
nav.toc summary{font-weight:600;cursor:pointer;list-style:none;margin-bottom:8px;color:var(--muted);text-transform:uppercase;letter-spacing:.04em;font-size:12px}
nav.toc summary::-webkit-details-marker{display:none}
nav.toc ul{list-style:none;margin:0;padding:0}
nav.toc li{margin:0}
nav.toc a{display:block;padding:4px 10px;border-left:2px solid var(--line);color:var(--fg);text-decoration:none}
nav.toc a:hover{background:var(--panel)}
nav.toc a.active{border-left-color:var(--accent);color:var(--accent);font-weight:600}
nav.toc li.l3 a{padding-left:24px;color:var(--muted);font-size:13px}
main{min-width:0;padding:28px 0 80px;max-width:820px}
h1{font-size:1.9rem;line-height:1.25;margin:.2em 0 .3em}
h2{font-size:1.4rem;margin:2.2em 0 .6em;padding-top:.6em;border-top:1px solid var(--line)}
h3{font-size:1.12rem;margin:1.8em 0 .5em}
h2,h3{scroll-margin-top:16px}
main>p:nth-of-type(1){color:var(--muted)}
code{font:0.9em ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;background:var(--code-bg);border:1px solid var(--line);border-radius:4px;padding:.05em .3em}
ul,ol{padding-left:1.4em}
li{margin:.3em 0}
ul.checklist{list-style:none;padding-left:0}
ul.checklist label{display:flex;gap:.6em;align-items:flex-start}
ul.checklist input{margin-top:.35em;flex:none;width:1.05em;height:1.05em}
.table-wrap{overflow-x:auto;margin:1em 0;border:1px solid var(--line);border-radius:6px}
table{border-collapse:collapse;width:100%;font-size:14px}
th,td{text-align:left;vertical-align:top;padding:8px 10px;border-bottom:1px solid var(--line)}
th{background:var(--th);font-weight:600}
tr:last-child td{border-bottom:0}
.prompt-box{margin:1.2em 0 1.6em;border:1px solid var(--line);border-radius:8px;overflow:hidden;background:var(--code-bg)}
.prompt-bar{display:flex;flex-wrap:wrap;gap:8px;align-items:center;justify-content:space-between;padding:8px 10px;background:var(--panel);border-bottom:1px solid var(--line)}
.prompt-label{font-weight:600;font-size:14px}
.prompt-actions{display:flex;gap:8px;align-items:center}
.copy-btn,.dl-link{font:600 13px/1 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;padding:8px 12px;border-radius:6px;cursor:pointer;text-decoration:none;min-height:34px;display:inline-flex;align-items:center}
.copy-btn{background:var(--accent);color:var(--accent-fg);border:1px solid var(--accent)}
.copy-btn.copied{background:var(--ok);border-color:var(--ok)}
.dl-link{border:1px solid var(--line);color:var(--fg);background:var(--bg)}
pre.prompt,pre.code{margin:0;padding:14px 16px;max-height:32rem;overflow:auto;white-space:pre-wrap;overflow-wrap:anywhere;font:13px/1.55 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;color:var(--fg);tab-size:4}
.skip{position:absolute;left:-999px}.skip:focus{left:8px;top:8px;background:var(--bg);padding:6px;z-index:10}
footer{color:var(--muted);font-size:13px;margin-top:3em;border-top:1px solid var(--line);padding-top:1em}
@media (max-width:860px){
 .layout{display:block;padding:0 16px}
 nav.toc{position:sticky;top:0;z-index:5;max-height:none;overflow:visible;padding:0;margin:0 -16px;background:var(--bg);border-bottom:1px solid var(--line)}
 nav.toc summary{margin:0;padding:12px 16px;font-size:13px}
 nav.toc summary::after{content:" \25BE"}
 nav.toc details[open] ul{max-height:60vh;overflow:auto;padding:0 16px 12px}
 main{padding-top:16px}
 h1{font-size:1.5rem}
 h2,h3{scroll-margin-top:56px}
 pre.prompt{max-height:24rem;font-size:12.5px}
}
@media print{nav.toc,.prompt-actions{display:none}.layout{display:block}pre.prompt{max-height:none}}
"""

JS = r"""
(function(){
  // The exact text a Copy button copies: the <pre>'s textContent (HTML entities decoded, nothing trimmed).
  function promptText(id){ return document.getElementById(id).textContent; }
  window.promptText = promptText;

  function fallbackCopy(text){
    var ta = document.createElement('textarea');
    ta.value = text; ta.setAttribute('readonly','');
    ta.style.position='fixed'; ta.style.top='-1000px';
    document.body.appendChild(ta); ta.select();
    var ok = false; try { ok = document.execCommand('copy'); } catch(e) {}
    document.body.removeChild(ta); return ok;
  }
  function flash(btn, msg){
    btn.textContent = msg; btn.classList.add('copied');
    setTimeout(function(){ btn.textContent='Copy'; btn.classList.remove('copied'); }, 1600);
  }
  document.querySelectorAll('.copy-btn').forEach(function(btn){
    btn.addEventListener('click', function(){
      var text = promptText(btn.getAttribute('data-target'));
      if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(text).then(function(){ flash(btn,'Copied'); },
          function(){ flash(btn, fallbackCopy(text) ? 'Copied' : 'Copy failed'); });
      } else {
        flash(btn, fallbackCopy(text) ? 'Copied' : 'Copy failed');
      }
    });
  });

  // Highlight the current section in the table of contents.
  var links = Array.prototype.slice.call(document.querySelectorAll('nav.toc a'));
  var map = {}; links.forEach(function(a){ map[a.getAttribute('href').slice(1)] = a; });
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(e){
        if (e.isIntersecting) {
          links.forEach(function(a){ a.classList.remove('active'); });
          var a = map[e.target.id]; if (a) a.classList.add('active');
        }
      });
    }, {rootMargin:'0px 0px -75% 0px'});
    document.querySelectorAll('main h2[id], main h3[id]').forEach(function(h){ io.observe(h); });
  }
  // On phones, close the contents menu after picking a section.
  var det = document.querySelector('nav.toc details');
  links.forEach(function(a){ a.addEventListener('click', function(){
    if (window.matchMedia('(max-width:860px)').matches) det.open = false; }); });
  function syncToc(){ det.open = !window.matchMedia('(max-width:860px)').matches; }
  syncToc(); window.matchMedia('(max-width:860px)').addEventListener('change', syncToc);

  // Verification hook used by verify.py (headless browser): index.html#verify-copy
  if (location.hash === '#verify-copy') {
    var out = {};
    document.querySelectorAll('pre.prompt').forEach(function(p){ out[p.id] = promptText(p.id); });
    var v = document.createElement('pre'); v.id = 'verify-out'; v.hidden = true;
    v.textContent = JSON.stringify(out);
    document.body.appendChild(v);
  }
})();
"""


def main():
    md = (ROOT / "kit.md").read_text(encoding="utf-8")
    title, body, toc, prompts = convert(md)
    if len(prompts) != len(PROMPT_FILES):
        raise SystemExit(f"Expected {len(PROMPT_FILES)} text blocks, found {len(prompts)}")

    pdir = ROOT / "prompts"
    pdir.mkdir(exist_ok=True)
    for name, text in zip(PROMPT_FILES, prompts):
        (pdir / name).write_bytes(text.encode("utf-8"))

    toc_html = "".join(
        f'<li class="l{lvl}"><a href="#{slug}">{inline(text)}</a></li>' for lvl, slug, text in toc
    )
    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light dark">
<title>{html.escape(title)}</title>
<style>{CSS}</style>
</head>
<body>
<a class="skip" href="#content">Skip to content</a>
<div class="layout">
<nav class="toc" aria-label="Table of contents"><details open><summary>Contents</summary><ul>{toc_html}</ul></details></nav>
<main id="content">
{body}
<footer>Built from kit.md. Prompts are reproduced byte-for-byte; the Copy button and the .txt downloads contain identical text.</footer>
</main>
</div>
<script>{JS}</script>
</body>
</html>
"""
    (ROOT / "index.html").write_text(page, encoding="utf-8")
    print(f"Wrote index.html and {len(prompts)} prompt files.")


if __name__ == "__main__":
    main()
