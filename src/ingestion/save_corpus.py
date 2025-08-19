# save_corpus.py
# v4 — HTML→MD, optional PDF rendering, MDN & pandas fallbacks

import argparse, hashlib, json, os, platform, shutil, subprocess, sys, time
from pathlib import Path
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from readability import Document
from slugify import slugify

try:
    from markdownify import markdownify as mdify
    USE_MARKDOWNIFY = True
except Exception:
    USE_MARKDOWNIFY = False

# ----------------------- Config -----------------------
HTML_DIR = Path("data/html")
PDF_DIR  = Path("data/pdf")
MD_DIR   = Path("data/md")
META     = Path("data/metadata.jsonl")

URLS = [
    # Python
    "https://docs.python.org/3/tutorial/datastructures.html",
    "https://docs.python.org/3/howto/logging.html",
    "https://docs.python.org/3/howto/argparse.html",
    "https://peps.python.org/pep-0008/",
    "https://docs.python.org/3/reference/datamodel.html",
    # Pandas
    "https://pandas.pydata.org/docs/user_guide/10min.html",
    "https://pandas.pydata.org/docs/user_guide/merging.html",
    "https://pandas.pydata.org/docs/user_guide/groupby.html",
    # NumPy
    "https://numpy.org/doc/stable/user/absolute_beginners.html",
    "https://numpy.org/doc/stable/user/basics.indexing.html",
    # MDN (JS/TS)
    "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise",
    "https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API",
    "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/map",
    "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map",
    "https://www.typescriptlang.org/docs/handbook/2/generics.html",
    # Node.js
    "https://nodejs.org/api/fs.html",
    # DevOps
    "https://docs.docker.com/reference/dockerfile/",
    "https://kubernetes.io/docs/concepts/workloads/controllers/deployment/",
    "https://docs.github.com/actions/reference/workflow-syntax-for-github-actions",
    "https://git-scm.com/book/en/v2",
]

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; RAG-Corpus-Fetch/1.0)"}
TIMEOUT = 30
MAX_RETRIES = 3
RETRY_BACKOFF = 2  # seconds base exponent

# ----------------------- Helpers -----------------------
def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def filename_from_url(url: str) -> str:
    path = urlparse(url).path.rstrip("/").split("/")[-1] or "index"
    host = urlparse(url).netloc.replace("www.", "")
    base = slugify(f"{host}-{path}")[:120]
    return base or slugify(host)

def extract_title_from_html_str(html_str: str) -> str:
    try:
        soup = BeautifulSoup(html_str, "lxml")
        if soup.title and soup.title.string:
            return soup.title.string.strip()
    except Exception:
        pass
    return ""

def to_markdown_readability(html_bytes: bytes, encoding_hint: str | None) -> str:
    enc = encoding_hint or "utf-8"
    html_str = html_bytes.decode(enc, errors="ignore")
    try:
        doc = Document(html_str)
        article_html = doc.summary(html_partial=True)  # str
        if not article_html:
            raise ValueError("Empty readability summary")
        if USE_MARKDOWNIFY:
            return mdify(article_html, heading_style="ATX").strip()

        # simple headings/paras fallback
        soup = BeautifulSoup(article_html, "lxml")
        lines = []
        for el in soup.descendants:
            if el.name and el.name.startswith("h") and len(el.name) == 1:
                level = int(el.name[1])
                text = (el.get_text(" ", strip=True) or "").strip()
                if text:
                    lines.append("#" * min(level, 6) + " " + text)
            elif el.name in {"p", "li"}:
                text = el.get_text(" ", strip=True)
                if text:
                    lines.append(text)
        md = "\n\n".join(lines).strip()
        if md:
            return md
    except Exception:
        pass

    # full-page fallback
    soup = BeautifulSoup(html_str, "lxml")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    if USE_MARKDOWNIFY:
        return mdify(str(soup), heading_style="ATX").strip()
    paras = [p.get_text(" ", strip=True) for p in soup.find_all(["h1","h2","h3","p","li"])]
    return "\n\n".join([p for p in paras if p]).strip()

def save_metadata(record: dict):
    with META.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

# ---------- MDN & pandas fallbacks ----------
def mdn_raw_fallback(url: str) -> str | None:
    if "developer.mozilla.org" not in url:
        return None
    path = urlparse(url).path
    parts = [p for p in path.split("/") if p]
    try:
        i = parts.index("docs")
    except ValueError:
        return None
    parts = [p.lower().replace(".", "-") for p in parts[i + 1 :]]
    github_path = "/".join(["files"] + parts + ["index.md"])
    return f"https://raw.githubusercontent.com/mdn/content/main/{github_path}"

def pandas_alt_candidates(url: str) -> list[str]:
    """Try alternate stable paths + GitHub raw .rst if host DNS fails."""
    if "pandas.pydata.org" not in url:
        return []
    # Convert URL like .../docs/user_guide/10min.html to alternates
    parsed = urlparse(url)
    path = parsed.path
    alts = []
    if path.startswith("/docs/user_guide/"):
        tail = path.split("/docs/user_guide/", 1)[1]
        # alternate paths that often exist:
        alts.append(f"https://pandas.pydata.org/pandas-docs/version/stable/user_guide/{tail}")
        alts.append(f"https://pandas.pydata.org/pandas-docs/stable/user_guide/{tail}")
    # GitHub raw .rst source (best-effort)
    basename = path.rstrip("/").split("/")[-1]
    if basename.endswith(".html"):
        rst = basename[:-5] + ".rst"
        # e.g., merging.rst, groupby.rst, 10min.rst
        alts.append(f"https://raw.githubusercontent.com/pandas-dev/pandas/main/doc/source/user_guide/{rst}")
    return alts

def robust_get(url: str):
    """GET with retries + specific fallbacks. Returns (response, used_url)."""
    last_exc = None
    candidates = [url]

    # pandas alternates
    candidates.extend(pandas_alt_candidates(url))

    # MDN fallback (to GitHub raw MD)
    if "developer.mozilla.org" in url:
        fb = mdn_raw_fallback(url)
        if fb:
            candidates.append(fb)

    for candidate in candidates:
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                r = requests.get(candidate, headers=HEADERS, timeout=TIMEOUT)
                r.raise_for_status()
                if candidate != url:
                    print(f"Fallback ✓  {url}  →  {candidate}")
                return r, candidate
            except Exception as e:
                last_exc = e
                if attempt < MAX_RETRIES:
                    time.sleep(RETRY_BACKOFF ** attempt)
        # move to the next candidate
    raise last_exc

# ---------- PDF rendering via headless Chrome ----------
def find_chrome_binary() -> str | None:
    env_path = os.environ.get("CHROME_PATH")
    if env_path and Path(env_path).exists():
        return env_path

    system = platform.system().lower()
    if system == "darwin":  # macOS
        candidates = [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "/Applications/Chromium.app/Contents/MacOS/Chromium",
        ]
        for p in candidates:
            if Path(p).exists():
                return p
    elif system == "windows":
        for p in [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files\Chromium\Application\chrome.exe",
        ]:
            if Path(p).exists():
                return p
    else:  # linux
        for exe in ["google-chrome", "chromium-browser", "chromium", "chrome"]:
            p = shutil.which(exe)
            if p:
                return p
    return None

def render_pdf_with_chrome(url: str, out_pdf: Path) -> bool:
    chrome = find_chrome_binary()
    if not chrome:
        print("PDF warn: Chrome/Chromium not found. Set CHROME_PATH or install Chrome.", file=sys.stderr)
        return False
    out_pdf.parent.mkdir(parents=True, exist_ok=True)
    cmds = [
        [chrome, "--headless=new", "--disable-gpu", f"--print-to-pdf={str(out_pdf)}", url],
        [chrome, "--headless", "--disable-gpu", f"--print-to-pdf={str(out_pdf)}", url],
    ]
    for cmd in cmds:
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except subprocess.CalledProcessError:
            continue
    print(f"PDF warn: Chrome failed to render {url}", file=sys.stderr)
    return False

# ----------------------- Main -----------------------
def download_one(url: str, render_pdf: bool):
    r, used_url = robust_get(url)
    ctype = (r.headers.get("Content-Type") or "").split(";")[0].lower()
    enc = r.encoding or "utf-8"
    b = r.content
    digest = sha256_bytes(b)
    ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    base = filename_from_url(url)  # from original URL

    # 1) PDF directly from server
    if ctype == "application/pdf" or used_url.lower().endswith(".pdf"):
        out = PDF_DIR / f"{base}.pdf"
        out.write_bytes(b)
        save_metadata({
            "url": url, "downloaded_from": used_url, "saved_as": str(out),
            "content_type": "pdf", "title": "", "sha256": digest, "saved_at": ts,
            "tags": ["techdocs"]
        })
        print(f"PDF  ✓  {url}  →  {out}")
        return

    # 2) Markdown served (e.g., MDN GitHub fallback, pandas raw .rst)
    if used_url.endswith(".md") or "text/markdown" in ctype or used_url.endswith(".rst"):
        ext = ".md" if used_url.endswith(".md") else ".rst"
        out_md = MD_DIR / f"{base}{ext}"
        text = r.text
        out_md.write_text(text, encoding=enc, errors="ignore")
        save_metadata({
            "url": url, "downloaded_from": used_url, "saved_as": str(out_md),
            "content_type": "markdown" if ext == ".md" else "rst",
            "title": base.replace("-", " "), "sha256": digest, "saved_at": ts,
            "tags": ["techdocs"]
        })
        # Optional: render PDF from raw text using Chrome data URL? (skip)
        print(f"{ext.upper()[1:]}  ✓  {url}  →  {out_md}")
        return

    # 3) HTML + Markdown companion
    out_html = HTML_DIR / f"{base}.html"
    out_html.write_bytes(b)

    html_str_for_title = b.decode(enc, errors="ignore")
    title = extract_title_from_html_str(html_str_for_title) or base.replace("-", " ")

    md_text = ""
    try:
        md_text = to_markdown_readability(b, enc)
    except Exception:
        md_text = ""

    if md_text:
        out_md = MD_DIR / f"{base}.md"
        out_md.write_text(md_text, encoding="utf-8")

    save_metadata({
        "url": url, "downloaded_from": used_url, "saved_as": str(out_html),
        "content_type": "html", "title": title, "sha256": digest, "saved_at": ts,
        "tags": ["techdocs"]
    })

    msg = f"HTML ✓  {url}  →  {out_html}{'  +  md' if md_text else ''}"

    # 4) Optional: render PDF for HTML page
    if render_pdf:
        out_pdf = PDF_DIR / f"{base}.pdf"
        if render_pdf_with_chrome(used_url, out_pdf):
            msg += "  +  pdf"
        else:
            msg += "  (pdf skipped: Chrome unavailable/failed)"

    print(msg)

def main():
    parser = argparse.ArgumentParser(description="Download Tech Docs corpus")
    parser.add_argument("--pdf", action="store_true", help="Render PDFs for HTML pages via headless Chrome")
    args = parser.parse_args()

    HTML_DIR.mkdir(parents=True, exist_ok=True)
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    MD_DIR.mkdir(parents=True, exist_ok=True)
    META.parent.mkdir(parents=True, exist_ok=True)
    META.write_text("", encoding="utf-8")  # reset

    ok = fail = 0
    for u in URLS:
        try:
            download_one(u, render_pdf=args.pdf)
            ok += 1
        except Exception as e:
            print(f"ERR  ×  {u}  →  {e}", file=sys.stderr)
            fail += 1

    print(f"\nDone. OK={ok}, FAIL={fail}")
    print(f"Saved to: {HTML_DIR.resolve()}, {MD_DIR.resolve()}, {PDF_DIR.resolve()}")
    print(f"Metadata: {META.resolve()}")

if __name__ == "__main__":
    main()
