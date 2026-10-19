"""Collect the reviewed Houston public source set; never attach a browser."""

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
from html.parser import HTMLParser
import http.client
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import build_opener, HTTPRedirectHandler, ProxyHandler, Request


ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "corpus"
CATALOG = ROOT / "assets" / "source-catalog.json"
HOSTS = {"spacecenter.org", "cmhouston.org", "hmns.org", "houstonzoo.org", "ridemetro.org", "visithoustontexas.com"}
EXIT_SUCCESS, EXIT_RUNTIME_ERROR, EXIT_INPUT_ERROR = 0, 1, 2
MAX_BYTES = 8 * 1024 * 1024


class SourceError(Exception):
    """A bounded source failure safe to show without response bodies."""


@contextmanager
def refresh_lock():
    """One writer owns the entire read/update/publish inventory transaction."""
    if CORPUS.is_symlink() or not CORPUS.resolve().is_relative_to(ROOT):
        raise SourceError("Corpus destination leaves this skill; restore the local corpus path.")
    CORPUS.mkdir(parents=True, exist_ok=True)
    lock_path = CORPUS / ".refresh.lock"
    try:
        descriptor = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        raise SourceError("Another refresh holds the corpus lock; wait for it to finish. After a hard interruption, verify no refresh is active before removing only corpus/.refresh.lock.") from None
    identity = os.fstat(descriptor)
    os.close(descriptor)
    try:
        yield
    finally:
        try:
            current = lock_path.lstat()
            if (current.st_dev, current.st_ino) == (identity.st_dev, identity.st_ino):
                lock_path.unlink()
        except FileNotFoundError:
            pass


def validate_url(url, expected_host=None):
    parts = urlsplit(url)
    host = (parts.hostname or "").removeprefix("www.")
    if (parts.scheme != "https" or host not in HOSTS or parts.query or parts.fragment
            or parts.username or parts.password or parts.port not in (None, 443)
            or (expected_host is not None and host != expected_host)):
        raise SourceError("URL is outside the reviewed public source boundary; verify the official catalog.")
    return host


class OfficialRedirects(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        validate_url(newurl, validate_url(req.full_url))
        return super().redirect_request(req, fp, code, msg, headers, newurl)


class PageText(HTMLParser):
    """Searchable visible text, retaining headings and table-cell boundaries."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.hidden = 0
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style", "noscript", "template"}:
            self.hidden += 1
        if not self.hidden and tag in {"p", "div", "br", "li", "tr", "td", "th", "section", "h1", "h2", "h3", "h4"}:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in {"script", "style", "noscript", "template"}:
            self.hidden = max(0, self.hidden - 1)
        if not self.hidden and tag in {"p", "div", "li", "tr", "td", "th", "section", "h1", "h2", "h3", "h4"}:
            self.parts.append("\n")

    def handle_data(self, data):
        if not self.hidden:
            self.parts.append(data)

    def text(self):
        return "\n".join(line for line in (" ".join(s.split()) for s in "".join(self.parts).splitlines()) if line) + "\n"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def atomic_write(path, data):
    if path.is_symlink() or not path.resolve().is_relative_to(ROOT):
        raise SourceError("Corpus destination leaves this skill; restore the local corpus path.")
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(data)
        os.replace(temporary, path)
    finally:
        if temporary and temporary.exists():
            temporary.unlink()


def load_catalog():
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    sources = catalog["sources"]
    ids = [source["id"] for source in sources]
    if not sources or len(ids) != len(set(ids)):
        raise SourceError("Source catalog is empty or has duplicate IDs; repair its reviewed entries.")
    for source in sources:
        if not re.fullmatch(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*", source["id"]):
            raise SourceError("Source catalog has an invalid ID; use lowercase words and hyphens.")
        validate_url(source["url"])
    return sources


def fetch(source):
    opener = build_opener(ProxyHandler({}), OfficialRedirects())
    for attempt in range(2):
        try:
            request = Request(source["url"], headers={"User-Agent": "HoustonWeekendSources/1.0 (public planning pages)", "Accept": "text/html", "Accept-Encoding": "identity"})
            with opener.open(request, timeout=25) as response:
                final_url = response.geturl()
                validate_url(final_url, validate_url(source["url"]))
                if response.headers.get_content_type() != "text/html":
                    raise SourceError("Expected a complete HTML planning page; review the source format.")
                data = response.read(MAX_BYTES + 1)
                expected_length = response.headers.get("Content-Length")
                if len(data) > MAX_BYTES or (expected_length and int(expected_length) != len(data)):
                    raise SourceError("Page size or completeness check failed; inspect the public source before retrying.")
                decoded = data.decode(response.headers.get_content_charset() or "utf-8", errors="strict")
                if "</html>" not in decoded.lower():
                    raise SourceError("HTML response is incomplete; retry after the source recovers.")
                parser = PageText()
                parser.feed(decoded)
                text = parser.text()
                if len(text) < 500 or any(marker.casefold() not in text.casefold() for marker in source["markers"]):
                    raise SourceError("Planning content markers are missing; review the public page instead of accepting a shell.")
                return data, text.encode("utf-8"), final_url
        except HTTPError as error:
            retry_after = error.headers.get("Retry-After", "1")
            retry_seconds = int(retry_after) if retry_after.isdigit() else None
            if attempt == 0 and error.code in {429, 500, 502, 503, 504} and retry_seconds is not None and retry_seconds <= 10:
                time.sleep(max(1, retry_seconds))
                continue
            raise SourceError(f"HTTP {error.code}; keep the last good copy and retry when this official page is available.") from None
        except (URLError, TimeoutError, http.client.HTTPException) as error:
            if attempt == 0:
                time.sleep(1)
                continue
            raise SourceError(f"Network retrieval failed ({type(error).__name__}); keep the last good copy and retry later.") from None
    raise SourceError("Retrieval did not complete; retry later.")


def check_entry(source, entry):
    source_id = source["id"]
    if not entry or entry.get("status") != "saved" or entry.get("url") != source["url"]:
        return {"id": source_id, "status": "failed", "reason": "Saved current source metadata is missing or failed; refresh this source ID."}
    try:
        for suffix, field in (("html", "original_sha256"), ("txt", "text_sha256")):
            path = CORPUS / "sources" / f"{source_id}.{suffix}"
            if path.is_symlink() or not path.resolve().is_relative_to(ROOT) or digest(path.read_bytes()) != entry[field]:
                raise SourceError("Saved source integrity differs; inspect the changed file before refreshing.")
        return {"id": source_id, "status": "passed", "retrieved_at": entry["retrieved_at"]}
    except (OSError, KeyError, SourceError):
        return {"id": source_id, "status": "failed", "reason": "Saved original or text is missing or changed; inspect it, then refresh this source ID."}


def run_operation(args):
    sources = load_catalog()
    requested = set(args.source or [source["id"] for source in sources])
    unknown = requested - {source["id"] for source in sources}
    if unknown:
        return {"ok": False, "error": {"message": "Unknown source ID was supplied.", "recovery": "Use IDs from assets/source-catalog.json; URLs and private values are not accepted."}}, EXIT_INPUT_ERROR
    selected = [source for source in sources if source["id"] in requested]
    if args.dry_run:
        return {"ok": True, "dry_run": True, "action": "refresh" if args.refresh else "check", "source_ids": [source["id"] for source in selected], "network": False, "writes": False}, EXIT_SUCCESS
    if args.refresh:
        with refresh_lock():
            return process_sources(args, selected)
    return process_sources(args, selected)


def process_sources(args, selected):
    """Refresh callers must hold refresh_lock before loading the inventory."""
    inventory_path = CORPUS / "inventory.json"
    inventory = json.loads(inventory_path.read_text(encoding="utf-8")) if inventory_path.exists() else {"contract_version": 1, "sources": {}}
    entries = inventory["sources"]
    results = []
    for source in selected:
        source_id = source["id"]
        if args.check:
            results.append(check_entry(source, entries.get(source_id)))
            continue
        if args.verbose and not args.quiet:
            print(f"Fetching reviewed public source: {source_id}", file=sys.stderr)
        try:
            original, text, final_url = fetch(source)
            atomic_write(CORPUS / "sources" / f"{source_id}.html", original)
            atomic_write(CORPUS / "sources" / f"{source_id}.txt", text)
            entries[source_id] = {
                **source, "status": "saved", "final_url": final_url,
                "retrieved_at": datetime.now(timezone.utc).isoformat(), "publisher_version": None,
                "representation": "complete HTTP HTML response and derived visible text; linked assets and dynamic checkout excluded",
                "original_file": f"sources/{source_id}.html", "text_file": f"sources/{source_id}.txt",
                "original_bytes": len(original), "text_bytes": len(text),
                "original_sha256": digest(original), "text_sha256": digest(text),
            }
            results.append(check_entry(source, entries[source_id]))
        except (SourceError, OSError, UnicodeError, ValueError) as error:
            previous = entries.get(source_id, {})
            entries[source_id] = {**previous, "id": source_id, "url": source["url"], "status": "failed", "attempted_at": datetime.now(timezone.utc).isoformat(), "reason": str(error) if isinstance(error, SourceError) else "Source processing failed; review the public source or local corpus permissions."}
            results.append({"id": source_id, "status": "failed", "reason": entries[source_id]["reason"]})
        if source is not selected[-1]:
            time.sleep(1)
    if args.refresh:
        atomic_write(inventory_path, (json.dumps(inventory, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    success = all(result["status"] == "passed" for result in results)
    return {"ok": success, "action": "refresh" if args.refresh else "check", "sources": results, "limits": "Local integrity is separate from current hours, live reservations, source fidelity and trip feasibility."}, EXIT_SUCCESS if success else EXIT_RUNTIME_ERROR


def build_parser():
    parser = argparse.ArgumentParser(
        description="Houston public sources: refresh selected official pages or check saved copies.",
        epilog="Examples: public_sources.py --check --json; public_sources.py --refresh --dry-run; public_sources.py --refresh --source space-guide --json. Exit 0: success; 1: source/check failure; 2: invalid input.",
    )
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--check", action="store_true", help="Check the local collection without network or writes")
    action.add_argument("--refresh", action="store_true", help="Fetch reviewed public pages into this skill's corpus")
    parser.add_argument("--source", action="append", help="Reviewed source ID; repeat for a subset")
    parser.add_argument("--json", action="store_true", help="Return one clean JSON object")
    parser.add_argument("-n", "--dry-run", action="store_true", help="Preview selected action without network or writes")
    parser.add_argument("-v", "--verbose", action="store_true", help="Explain progress on stderr")
    parser.add_argument("-q", "--quiet", action="store_true", help="Suppress progress and terminal banner")
    parser.add_argument("--no-input", action="store_true", help="Never prompt (all modes already run once and exit)")
    parser.add_argument("--no-color", action="store_true", help="Disable terminal colors")
    return parser


def main():
    args = build_parser().parse_args()
    human = sys.stdout.isatty() and not args.json and not args.no_input and not args.quiet
    color = human and not args.no_color and not os.environ.get("NO_COLOR")
    if human:
        print(("\033[94m" if color else "") + "Houston public sources" + ("\033[0m" if color else ""))
    try:
        result, exit_code = run_operation(args)
    except SourceError as error:
        result, exit_code = {"ok": False, "error": {"message": str(error), "recovery": "Resolve the named source or corpus condition before retrying; inspect an existing refresh lock before removing it."}}, EXIT_RUNTIME_ERROR
    except (OSError, ValueError, KeyError):
        result, exit_code = {"ok": False, "error": {"message": "The reviewed catalog or local corpus could not be used.", "recovery": "Check this skill's source catalog and corpus files and permissions; no private input is needed."}}, EXIT_RUNTIME_ERROR
    except KeyboardInterrupt:
        result, exit_code = {"ok": False, "error": {"message": "Source collection was interrupted; some files may have been saved.", "recovery": "Run --check, inspect failed IDs, then refresh only those IDs."}}, 130
    try:
        if args.json:
            print(json.dumps(result, ensure_ascii=False, allow_nan=False))
        else:
            label = "[OK]" if result["ok"] else "[FAILED]"
            print(("\033[92m" if result["ok"] else "\033[91m") if color else "", end="")
            print(label + ("\033[0m" if color else "") + " " + json.dumps(result, ensure_ascii=False))
    except BrokenPipeError:
        return EXIT_RUNTIME_ERROR
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
