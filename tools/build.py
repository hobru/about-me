"""Build only explicitly approved public catalogue files. No third-party dependencies."""

import argparse
from datetime import date
import json
from pathlib import Path
import re
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ("public.json", "podcast.json")
STATUSES = {"Source reviewed", "Search indexed", "Series index", "User-provided excerpt", "User-provided reference", "Needs review"}
PRIVATE_HOSTS = ("sharepoint.com", "sharepoint-df.com", "teams.microsoft.com", "outlook.office.com", "airlift.microsoft.com")


def sap_content_id(url):
    parsed = urlparse(url)
    if parsed.hostname == "community.sap.com":
        match = re.search(r"/(?:ba-p|qaq-p|ec-p|ev-p|m-p)/(\d+)(?:/|$)", parsed.path)
        if match:
            return match[1]
    return None


def validate(records):
    seen = set()
    sap_seen = set()
    required = {"id", "title", "kind", "publisher", "date", "role", "topics", "url",
                "evidenceUrl", "evidenceNote", "verification", "checked"}
    for record in records:
        missing = required - record.keys()
        if missing:
            raise ValueError(f"Missing fields: {missing}")
        if record["id"] in seen:
            raise ValueError(f"Duplicate ID: {record['id']}")
        seen.add(record["id"])
        content_id = sap_content_id(record["url"])
        if content_id:
            if content_id in sap_seen:
                raise ValueError(f"Duplicate SAP content: {content_id}")
            sap_seen.add(content_id)
        if record["verification"] not in STATUSES or not record["topics"]:
            raise ValueError(f"Invalid evidence or topics: {record['id']}")
        value = record["date"]
        if value is not None:
            if not re.fullmatch(r"\d{4}(?:-\d{2})?(?:-\d{2})?", value):
                raise ValueError(f"Invalid date precision: {value}")
            date.fromisoformat(value + {4: "-01-01", 7: "-01", 10: ""}[len(value)])
        date.fromisoformat(record["checked"])
        links = [record["url"], record["evidenceUrl"]]
        links.extend(link["url"] for link in record.get("links", []))
        for link in links:
            parsed = urlparse(link)
            host = parsed.hostname or ""
            if parsed.scheme != "https" or not host or parsed.username or parsed.password:
                raise ValueError(f"Not a public HTTPS URL: {link}")
            if any(host == private or host.endswith("." + private) for private in PRIVATE_HOSTS):
                raise ValueError(f"Internal source cannot enter the public catalogue: {host}")


def publication_records(records):
    published = []
    for record in records:
        if record["verification"] == "Needs review":
            continue
        item = record.copy()
        item["evidenceNote"] = item["evidenceNote"].replace(
            "User-provided SAP Community search excerpt", "SAP Community search listing"
        ).replace(
            "Original page not reviewed; direct SAP Community retrieval previously returned HTTP 403.",
            "Attribution follows the search listing; the original page has not been independently reviewed."
        )
        published.append(item)
    return published


def standalone(encoded):
    html = (ROOT / "site" / "index.html").read_text(encoding="utf-8")
    css = (ROOT / "site" / "style.css").read_text(encoding="utf-8")
    app = (ROOT / "site" / "app.js").read_text(encoding="utf-8")
    safe_json = encoded.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    html = html.replace('<link rel="stylesheet" href="./style.css">', f"<style>{css}</style>")
    html = html.replace('<script src="./catalogue.js" defer></script>', f"<script>window.CATALOGUE = {safe_json};</script>")
    html = html.replace('<script src="./app.js" defer></script>', f'<script defer>{app}</script>')
    # Inline scripts do not honor defer; run the app only after its DOM exists.
    app_tag = f'<script defer>{app}</script>'
    html = html.replace(app_tag, "").replace("</body>", f"{app_tag}</body>")
    html = html.replace('href="./catalogue.json" download', 'href="#" id="download" download="catalogue.json"')
    download = """<script>
      const download = document.querySelector("#download");
      download.href = URL.createObjectURL(new Blob(
        [JSON.stringify(window.CATALOGUE, null, 2)], {type: "application/json"}
      ));
    </script>"""
    html = html.replace("</body>", download + "</body>")
    html = html.replace('href="./catalogue.json"', 'href="https://www.saponazurepodcast.de/"')
    return html


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--standalone", type=Path, help="Also write a single-file HTML preview at this path.")
    args = parser.parse_args()
    records = []
    for source in SOURCES:
        records.extend(json.loads((ROOT / "data" / source).read_text(encoding="utf-8")))
    validate(records)
    research_count = len(records)
    records = publication_records(records)
    records.sort(key=lambda item: (item["date"] or "", item["id"]), reverse=True)
    payload = {"collected": "2026-11-24", "scope": "Public professional catalogue", "records": records}
    encoded = json.dumps(payload, ensure_ascii=True, indent=2)
    (ROOT / "site" / "catalogue.js").write_text("window.CATALOGUE = " + encoded + ";\n", encoding="utf-8")
    (ROOT / "site" / "catalogue.json").write_text(encoded + "\n", encoding="utf-8")
    if args.standalone:
        args.standalone.parent.mkdir(parents=True, exist_ok=True)
        args.standalone.write_text(standalone(encoded), encoding="utf-8")
        print(f"Wrote standalone preview: {args.standalone}")
    print(f"Built {len(records)} public records into site/; retained {research_count - len(records)} unresolved records in research inputs only.")


if __name__ == "__main__":
    main()
