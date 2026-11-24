"""Import public episode metadata, not articles, transcripts, or media."""

import argparse
from datetime import datetime, timezone
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
SOURCE = "https://www.saponazurepodcast.de/"


class LinksAndText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.text = []
        self.anchor = None
        self.title = []
        self.in_title = False

    def handle_starttag(self, tag, attrs):
        if tag == "p":
            self.in_title = "title" in (dict(attrs).get("class") or "").split()
        if tag == "a":
            self.anchor = [dict(attrs).get("href") or "", []]

    def handle_endtag(self, tag):
        if tag == "p":
            self.in_title = False
        if tag == "a" and self.anchor is not None:
            self.links.append((self.anchor[0], "".join(self.anchor[1]).strip()))
            self.anchor = None

    def handle_data(self, data):
        self.text.append(data)
        if self.in_title:
            self.title.append(data)
        if self.anchor is not None:
            self.anchor[1].append(data)


def parse_episodes(html, checked):
    episodes = []
    seen = set()
    for block in re.split(r'<div class="column is-one-quarter">', html)[1:]:
        parsed = LinksAndText()
        parsed.feed(block)
        details = [
            (url, re.fullmatch(r"https://www\.saponazurepodcast\.de/episode(\d+)/", url))
            for url, _ in parsed.links
        ]
        details = [(url, match) for url, match in details if match]
        if not details:
            continue
        url, match = details[0]
        number = int(match.group(1))
        videos = [
            (link, title) for link, title in parsed.links
            if link.startswith(("https://youtu.be/", "https://www.youtube.com/watch?"))
            and title and not re.fullmatch(r"Episode #\d+", title)
        ]
        date = re.search(
            r"\b(January|February|March|April|May|June|July|August|September|October|November|December) (\d{4})\b",
            " ".join(parsed.text),
        )
        title = "".join(parsed.title).strip()
        if not title or not date or number in seen:
            raise ValueError(f"Missing or duplicate metadata for episode {number}")
        seen.add(number)
        published = datetime.strptime(date.group(), "%B %Y").strftime("%Y-%m")
        topics = [
            title for link, title in parsed.links
            if link.startswith("/tags/") and title.lower() not in {"tag1", "tag2"}
        ]
        episodes.append({
            "id": f"podcast-{number}",
            "title": title,
            "kind": "Podcast",
            "publisher": "SAP on Azure",
            "date": published,
            "dateNote": "Publication month shown by the series index; not a recording date.",
            "role": "Series creator / host",
            "topics": topics or ["SAP on Azure"],
            "url": url,
            "links": [{"label": "YouTube", "url": videos[0][0]}] if videos else [],
            "evidenceUrl": SOURCE,
            "evidenceNote": "Episode listed in the public series index. Individual participation has not been checked for every episode."
            + ("" if videos else " The source index contains a malformed video link; this entry links to the episode page instead."),
            "verification": "Series index",
            "checked": checked,
            "featured": number == 300,
        })
        if not videos:
            print(f"WARNING: Episode {number} has a malformed source video link; preserved its episode page without a video URL.")
    if not episodes:
        raise ValueError("No episodes found; the source layout may have changed.")
    return sorted(episodes, key=lambda item: int(item["id"].split("-")[1]), reverse=True)


def preserve_appearance_evidence(episodes, existing):
    previous = {record["id"]: record for record in existing}
    for episode in episodes:
        prior = previous.get(episode["id"])
        if prior and prior["verification"] != "Series index":
            for field in ("role", "evidenceUrl", "evidenceNote", "verification", "checked"):
                episode[field] = prior[field]
    return episodes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--html", type=Path, help="Use a saved public homepage instead of the network.")
    args = parser.parse_args()
    if args.html:
        html = args.html.read_text(encoding="utf-8")
    else:
        request = Request(SOURCE, headers={"User-Agent": "PersonalCatalogueResearch/1.0"})
        with urlopen(request, timeout=60) as response:
            html = response.read().decode("utf-8")
    checked = datetime.now(timezone.utc).date().isoformat()
    episodes = parse_episodes(html, checked)
    target = ROOT / "data" / "podcast.json"
    if target.exists():
        existing = json.loads(target.read_text(encoding="utf-8"))
        old_count = len(existing)
        if len(episodes) < old_count:
            raise ValueError(f"Import shrank from {old_count} to {len(episodes)}; review pagination before replacing it.")
        preserve_appearance_evidence(episodes, existing)
    target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(episodes, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    print(f"Imported {len(episodes)} episode records into {target.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
