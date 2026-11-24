"""Import metadata from user-supplied SAP Community search-result Markdown."""

import argparse
import calendar
from datetime import date
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit, urlunsplit

from build import ROOT, sap_content_id, validate

LEGACY_IDS = {
    "12911740", "12866725", "12867710", "12868935", "12836074", "12904413",
    "12892474", "12882773", "12895313", "12871081", "12892073", "12910998",
}
LEGACY_LEADS = {"13192497", "13302481", "13181055", "13019484", "13330520"}

# These relationships were reviewed in the supplied snippets, not inferred from search matches.
MENTIONS = {
    "13187498": ("Interviewee", "Ian Thain explicitly describes interviewing Holger about API Management in SAP CodeTalk."),
    "13093775": ("Interviewee", "Ian Thain explicitly describes interviewing Holger for a SAP CodeTalk update."),
    "13080536": ("Interviewee", "Ian Thain names Holger as his CodeTalk interviewee. The excerpt also mentions an earlier interview, which is not included in this reference."),
    "13915424": ("Announced speaker", "The invitation names Holger, Rene Pajta and Tanvi Agrawal. Delivery and the event date are not established."),
    "279753": ("Announced speaker", "The invitation names Holger and Karsten Strothmann. Delivery and the event date are not established."),
    "14365782": ("Announced speaker", "Jan Matthes names Holger in a future session description. This is not a recording or proof of delivery."),
    "129276": ("Announced speaker", "The post says Holger will discuss emerging trends. Do not infer the event year from the post's displayed date."),
    "13112186": ("Session presenter mentioned in retrospective", "Carsten Boennen describes Holger's SAP Gateway for Microsoft session. The exact session date is not separately established."),
    "13157479": ("Named demo contact", "Readers are invited to ask Holger for demos. This does not establish a particular delivered talk."),
    "13138635": ("Named course instructor", "The announcement names Holger and Shoshanna Budzianowski as Microsoft Virtual Academy instructors. The linked source is a course announcement."),
    "12978327": ("Microforum mention; exact role unresolved", "The excerpt ends with Holger's name after 'Microforum'; the full session title and role remain to check."),
    "13013853": ("Announced session presenter", "The Amsterdam schedule names Holger for November 5/6 sessions. Related announcement 13029242 covers the same event, not another proven appearance."),
    "13029242": ("Announced session presenter", "The Amsterdam schedule names Holger. Related announcement 13013853 covers the same event, not another proven appearance."),
    "13518284": ("Acknowledged supporter, not article author", "Swapnil Galgali thanks Holger and others for support."),
    "13471775": ("Acknowledged supporter, not article author", "Swapnil Galgali thanks Holger and other Microsoft colleagues for support."),
    "13109016": ("Referenced author of a separate article", "The excerpt credits Holger's Excel mass-data-update blog. The linked source is a third-party reference to that blog."),
    "13035947": ("Session presenter mentioned in retrospective", "The event report explicitly refers to Holger's Microsoft and SAP expert sessions."),
    "13120030": ("Announced hands-on instructor", "Carsten Boennen's INT262 schedule names Holger and Bjoern Woppmann. Delivery is not established by the schedule."),
    "13007966": ("Named event-team participant", "Holger is listed among team members covering the event on social media; no specific talk is established."),
    "13040009": ("Session presenter mentioned in retrospective", "The report describes Holger's expert networking session on Microsoft Office applications."),
    "13298971": ("Named openSAP course-team member", "Sven Kohlhaas names Holger among the Developing Java-Based Apps on SAP HANA Cloud Platform course team."),
    "13006198": ("Referenced author, not article author", "The excerpt explicitly refers readers to Holger's SSO blogs; it does not identify their individual URLs."),
    "13352346": ("Named speaker; exact talk unresolved", "Holger is named in an Innovation Talks roundup near replay text. The exact talk and recording URL remain to check."),
    "13509583": ("Session presenter mentioned by a third party", "Kristin Aleksandrova names Mathias Klein and Holger's SAP TechEd conversion session. The linked source is an article about the session, not a recording."),
    "13527269": ("Credited demo presenter, not article author", "The article credits Holger's SAPPHIRE 2022 Microsoft booth showcase."),
    "13432914": ("Named collaborator", "Max Streifeneder describes collaboration with Holger and mentions an April 2020 livestream. The displayed January date is not the livestream date."),
    "13567919": ("Named contributor; exact role unresolved", "The excerpt lists Holger among named professionals. It does not establish an article byline or precise contribution."),
    "13476138": ("Credited example creator, not article author", "Martin Pankraz credits Holger's PowerApp and SAP ES5 custom-connector example."),
    "13461411": ("Referenced author, not article author", "The visible excerpt credits separate work to Holger; the excerpt does not identify its full title or URL."),
    "13560042": ("Co-author", "Mark Ma explicitly thanks Holger among the Microsoft colleagues who co-wrote the blog."),
    "12890274": ("Recognized SAP xApps topic leader", "The topic-leader announcement explicitly lists Holger under SAP xApps."),
    "13524917": ("Announced speaker", "Peter Spielvogel's SAP TechEd 2022 session schedule names Holger. An agenda alone does not establish delivery."),
    "14481389": ("Referenced podcast participant, not article author", "Martin Raepple says that he and Holger walk through the scenario in the SAP on Azure video podcast. This reference links to the article discussing that appearance."),
    "13384690": ("Named book co-author, not announcement author", "The SAP Learning announcement names Holger among the book's authors. This is a reference to the already catalogued book, not another book."),
    "12976880": ("Demo presenter mentioned by a third party", "The excerpt describes Holger showing Duet Enterprise at a demo pod. The displayed date belongs to the report."),
    "12925200": ("Quoted expert, not article author", "The excerpt attributes an interoperability answer to Holger."),
    "12968737": ("Credited contributor, not article author", "The excerpt explicitly credits Holger from Duet Enterprise Solution Management."),
    "12998147": ("Announced speaker, SAP Solution Management", "The announcement names Holger and Marco Heid for a 7 November 2012 webinar. Delivery and a recording remain unconfirmed."),
    "12922171": ("Named workshop contact; presenter role not verified", "The announcement names Holger as a contact for the 28 June 2012 workshop. Contact details are deliberately excluded; neither authorship nor presentation is inferred."),
}


def parse_results(text):
    results = {}
    for block in re.split(r"(?m)^## (?=\[)", text)[1:]:
        heading = re.match(r"\[([^\]\n]+)\]\((https://community\.sap\.com/[^)\n]+)\)", block)
        if not heading:
            continue
        parts = urlsplit(heading[2])
        url = urlunsplit((parts.scheme, parts.netloc, parts.path, "", ""))
        identifier = sap_content_id(url)
        if not identifier or identifier in results:
            continue
        author = re.search(r"(?m)^by (?:\[([^\]\n]+)\]\([^)\n]+\)|([^\[\n]+))", block)
        published = re.search(r"(?m)^[\s\u200e]*(\d{4}) ([A-Z][a-z]{2}) (\d{2}) ", block)
        if not author or not published:
            raise ValueError(f"Missing byline or displayed date for SAP content {identifier}")
        month = list(calendar.month_abbr).index(published[2])
        displayed_date = date(int(published[1]), month, int(published[3])).isoformat()
        results[identifier] = {
            "title": heading[1],
            "url": url,
            "author": (author[1] or author[2]).strip(),
            "holgerByline": bool(re.search(
                r"(?m)^by \[Holger-Bruchelt\]\(https://community\.sap\.com/t5/user/viewprofilepage/user-id/3494\)",
                block,
            )),
            "legacyTag": bool(re.search(r"(?im)^- \[holger bruchelt\]\(", block)),
            "date": displayed_date,
        }
    if not results:
        raise ValueError("No SAP Community search results found; input format may have changed.")
    return results


def topics_for(item):
    text = (item["title"] + " " + item["url"]).lower()
    topics = ["SAP"]
    for term, topic in (
        ("duet", "Duet"), ("duet-enterprise", "Duet Enterprise"),
        ("spnego", "SPNego"), ("sign-on", "SSO"),
        ("azure", "Azure"), ("odata", "OData"), ("gateway", "SAP Gateway"),
        ("copilot", "Copilot"), ("abap", "ABAP"), ("teched", "SAP TechEd"),
        ("dsag", "DSAG"), ("power-platform", "Power Platform"), ("microsoft", "Microsoft"),
    ):
        if term in text:
            topics.append(topic)
    return topics


def merge_results(existing, results, checked):
    date.fromisoformat(checked)
    records = [dict(record) for record in existing]
    by_content = {sap_content_id(record["url"]): record for record in records
                  if sap_content_id(record["url"])}
    added = updated = 0
    for identifier, item in results.items():
        prior = by_content.get(identifier)
        legacy = (item["author"] == "Former Member" and
                  ((identifier in LEGACY_IDS and item["legacyTag"]) or identifier in LEGACY_LEADS))
        if not (prior or item["holgerByline"] or legacy or identifier in MENTIONS):
            continue
        prefix = "User-provided SAP Community search excerpt"
        status = "User-provided excerpt"
        if item["holgerByline"]:
            role = "Co-author" if identifier == "14130760" else "Author"
            note = f"{prefix}: byline links Holger-Bruchelt to profile 3494."
            if role == "Co-author":
                note += " The snippet also names Bharath Sanmani as co-author."
            kind = "Q&A" if "/qaq-p/" in item["url"] else "Article"
        elif legacy:
            role = "Possible previous-account author; attribution unconfirmed"
            status = "Needs review"
            kind = "Article"
            attribution = ("the result carries a 'holger bruchelt' tag"
                           if item["legacyTag"] else
                           "this is a surname-search lead without visible authorship corroboration")
            note = (f"{prefix}: byline is Former Member and {attribution}. "
                    "Older posts may belong to a previous user ID; this individual post's authorship is not confirmed.")
        elif identifier in MENTIONS:
            role, relationship = MENTIONS[identifier]
            kind = "Interview" if role == "Interviewee" else "Article" if role == "Co-author" else "Mention"
            note = f"{prefix} (byline: {item['author']}): {relationship}"
            if identifier in {"12978327", "13352346", "13567919"}:
                status = "Needs review"
        else:
            role, kind = prior["role"], prior["kind"]
            note = f"{prefix}. {prior['evidenceNote']}"
        note += " Original page not reviewed; direct SAP Community retrieval previously returned HTTP 403."
        date_note = "Displayed search-result publication date, not independently verified or an event/recording date."
        if item["title"].endswith("..."):
            date_note += " Title retained as displayed, including trailing ellipsis; full title not independently reviewed."
        if prior:
            if not prior["date"]:
                prior["date"] = item["date"]
            if prior["date"] != item["date"]:
                publication_note = f"Search excerpt displays announcement publication date {item['date']}."
                date_note = prior.get("dateNote", "")
                if publication_note not in date_note:
                    date_note = f"{date_note} {publication_note}".strip()
            prior.update(evidenceNote=note, verification=status, dateNote=date_note,
                         url=item["url"], evidenceUrl=item["url"], checked=checked)
            updated += 1
        else:
            record = {
                "id": f"scn-{identifier}", "title": item["title"], "kind": kind,
                "publisher": "SAP Community / SCN", "date": item["date"], "dateNote": date_note,
                "role": role, "topics": topics_for(item), "url": item["url"],
                "evidenceUrl": item["url"], "evidenceNote": note,
                "verification": status, "checked": checked,
            }
            records.append(record)
            by_content[identifier] = record
            added += 1
    validate(records)
    return records, added, updated


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, help="User-provided Markdown file; omit to read standard input.")
    parser.add_argument("--checked", default=date.today().isoformat())
    args = parser.parse_args()
    text = args.input.read_text(encoding="utf-8") if args.input else sys.stdin.read()
    target = ROOT / "data" / "public.json"
    existing = json.loads(target.read_text(encoding="utf-8"))
    records, added, updated = merge_results(existing, parse_results(text), args.checked)
    target.write_text(json.dumps(records, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    print(f"Added {added} public records; enriched {updated} existing records. No original pages fetched.")


if __name__ == "__main__":
    main()
