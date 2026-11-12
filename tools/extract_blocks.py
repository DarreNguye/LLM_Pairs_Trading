"""Lift BEGIN/END blocks from QuantConnect output into the repo.

Usage (from the repo root):
    python tools/extract_blocks.py <log.txt | -> <batch folder>
    e.g. python tools/extract_blocks.py ~/Downloads/backtest_log.txt batches/B001_2026-11-07_v1/backtest
         pbpaste | python tools/extract_blocks.py - batches/B001_2026-11-07_v1      (macOS clipboard)

- Each "===== BEGIN <name> =====" ... "===== END <name> =====" block becomes <batch folder>/<name>.
- A block named pair_registry.md is APPENDED to ./pair_registry.md instead (the registry is append-only).
- Existing files are never overwritten unless --force is given (keeps results tamper-evident).
- QuantConnect log timestamps ("2025-12-31 00:00:00 :") at the start of lines are stripped.
- The token {CODE_COMMIT} is replaced with the repo's git hash, plus "(dirty)" if code/ has uncommitted changes.
  Commit code/ BEFORE running the backtest or screen, and don't change it until you've extracted.
- If a block carries src_main / src_core fingerprints (backtests do), they are compared with code/main.py and
  code/pairs_core.py; a mismatch means QuantConnect ran different code than the repo holds, and is flagged in the file.
"""
import argparse
import hashlib
import pathlib
import re
import subprocess
import sys

TS = re.compile(r"^\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}(?:\.\d+)?\s*:?\s?")   # PLACEHOLDER: adjust if QC's log prefix differs
BEGIN = re.compile(r"===== BEGIN (\S+) =====")
END = re.compile(r"===== END (\S+) =====")


def git(*args):
    '''Runs a git command in the current repo; None if git or the repo is unavailable'''
    try:
        return subprocess.run(["git", *args], capture_output=True, text=True, check=True).stdout.strip()
    except Exception:
        return None


def commit_stamp():
    '''Short hash of HEAD, with "(dirty)" if code/ has uncommitted changes'''
    head = git("rev-parse", "--short", "HEAD")
    if head is None:
        print("warning: not a git repo (or no commits yet); stamping code: unknown", file=sys.stderr)
        return "unknown"
    root = git("rev-parse", "--show-toplevel")
    dirty = git("-C", root, "status", "--porcelain", "--", "code/")
    if dirty:
        print("warning: code/ has uncommitted changes; stamp marked (dirty)", file=sys.stderr)
    return head + (" (dirty)" if dirty else "")


def fingerprint(path):
    '''Must stay identical to source_fingerprint() in code/pairs_core.py'''
    try:
        text = pathlib.Path(path).read_text(encoding="utf-8")
    except Exception:
        return "unavailable"
    text = "\n".join(line.rstrip() for line in text.replace("\r\n", "\n").split("\n")).strip("\n")
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:8]


def check_source(content):
    '''Compares src_main / src_core in a block with the repo's code files; returns a note to add, or None'''
    found = dict(re.findall(r"(src_main|src_core|src_config|src_trading): (\w+)", content))
    if not found:
        return None
    root = pathlib.Path(git("rev-parse", "--show-toplevel") or ".")
    repo = {"src_main": fingerprint(root / "code" / "main.py"), "src_core": fingerprint(root / "code" / "pairs_core.py"),
            "src_config": fingerprint(root / "code" / "screen_config.py"),
            "src_trading": fingerprint(root / "code" / "trading_config.py")}
    bad = [k for k, v in found.items() if v != "unavailable" and v != repo[k]]
    if bad:
        print(f"WARNING: QuantConnect ran different code than the repo for {', '.join(bad)} "
              f"(QC {[found[k] for k in bad]} vs repo {[repo[k] for k in bad]})", file=sys.stderr)
        return f"source_check: MISMATCH ({', '.join(bad)}) - QC code differs from repo code/"
    if "unavailable" in found.values():
        return "source_check: QC could not fingerprint its files"
    return "source_check: matches repo"


def extract(text):
    '''Returns {name: content} for every complete block in text'''
    blocks, name, buf = {}, None, []
    for raw in text.splitlines():
        line = TS.sub("", raw)
        if name is None:
            m = BEGIN.search(line)
            if m:
                name, buf = m.group(1), []
            continue
        if END.search(line):
            blocks[name] = "\n".join(buf).rstrip() + "\n"
            name = None
            continue
        buf.append(line)
    if name is not None:
        print(f"warning: block {name} has no END line (log may be cut off by the 10KB cap); skipped", file=sys.stderr)
    return blocks


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source", help="downloaded log / pasted output file, or - for stdin")
    ap.add_argument("out_dir", help="batch folder (or its backtest/ subfolder) to write files into")
    ap.add_argument("--registry", default="pair_registry.md", help="registry file to append to")
    ap.add_argument("--force", action="store_true", help="overwrite existing files")
    a = ap.parse_args()

    text = sys.stdin.read() if a.source == "-" else pathlib.Path(a.source).read_text(encoding="utf-8", errors="replace")
    blocks = extract(text)
    if not blocks:
        sys.exit("no BEGIN/END blocks found")

    out = pathlib.Path(a.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    stamp = commit_stamp()
    for name, content in blocks.items():
        content = content.replace("{CODE_COMMIT}", stamp)
        note = check_source(content)
        if note:   # goes right after the metadata line (2nd line) of a backtest file
            lines = content.split("\n")
            lines.insert(2, note)
            content = "\n".join(lines)
        if name == "pair_registry.md":
            with open(a.registry, "a", encoding="utf-8") as fh:
                fh.write("\n" + content)
            print(f"appended -> {a.registry}")
            continue
        path = out / name
        if path.exists() and not a.force:
            print(f"skipped {path} (exists; use --force to overwrite)")
            continue
        path.write_text(content, encoding="utf-8")
        print(f"wrote    -> {path}")


if __name__ == "__main__":
    main()