import copy
import json
import unittest

from build import ROOT, publication_records, standalone, validate
from import_podcast import parse_episodes, preserve_appearance_evidence
from import_sap_community import merge_results, parse_results


def episode(video="https://youtu.be/example1234", title="Episode #1 - The First One"):
    return f'''<div class="column is-one-quarter"><div class=card>
      <p class="title is-4"><a href="{video}">{title}</a></p>
      <a href="/tags/sap">SAP</a><a href="/tags/tag1">tag1</a>July 2020
      <a href="https://www.saponazurepodcast.de/episode001/">View Details</a>
      </div></div>'''


class ImportTests(unittest.TestCase):
    def test_extracts_older_title_month_and_topics(self):
        record = parse_episodes(episode(), "2026-11-24")[0]
        self.assertEqual(record["title"], "Episode #1 - The First One")
        self.assertEqual(record["date"], "2020-07")
        self.assertEqual(record["topics"], ["SAP"])
        self.assertEqual(record["url"], "https://www.saponazurepodcast.de/episode001/")

    def test_supports_both_youtube_formats(self):
        for video in ("https://youtu.be/example1234", "https://www.youtube.com/watch?v=example1234"):
            with self.subTest(video=video):
                record = parse_episodes(episode(video), "2026-11-24")[0]
                self.assertEqual(record["links"][0]["url"], video)

    def test_preserves_broken_video_as_explicit_source_issue(self):
        record = parse_episodes(episode("#ZgotmplZ"), "2026-11-24")[0]
        self.assertEqual(record["links"], [])
        self.assertIn("malformed", record["evidenceNote"])

    def test_rejects_empty_changed_or_duplicate_sources(self):
        for html in ("", episode().replace("July 2020", ""), episode() + episode()):
            with self.subTest(html=html[:40]):
                with self.assertRaises(ValueError):
                    parse_episodes(html, "2026-11-24")

    def test_refresh_preserves_individual_appearance_evidence_and_unresolved_roles(self):
        for status in ("Source reviewed", "Needs review"):
            with self.subTest(status=status):
                prior = parse_episodes(episode(), "2026-11-24")[0]
                prior.update(role="Named participant", verification=status,
                             evidenceUrl="https://example.com/author",
                             evidenceNote="Individual attribution, not a series-wide assumption.")
                original = copy.deepcopy(prior)
                refreshed = parse_episodes(episode(title="Updated source title"), "2026-11-25")
                result = preserve_appearance_evidence(refreshed, [prior])[0]
                self.assertEqual(result["title"], "Updated source title")
                for field in ("role", "verification", "evidenceUrl", "evidenceNote", "checked"):
                    self.assertEqual(result[field], prior[field])
                self.assertEqual(prior, original)


class CatalogueTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.curated = json.loads((ROOT / "data" / "public.json").read_text(encoding="utf-8"))
        cls.podcasts = json.loads((ROOT / "data" / "podcast.json").read_text(encoding="utf-8"))

    def test_real_catalogue_validates_and_snapshot_is_complete(self):
        validate(self.curated + self.podcasts)
        ids = {int(record["id"].split("-")[1]) for record in self.podcasts}
        self.assertEqual(ids, set(range(1, 315)))

    def test_rejects_internal_urls_in_primary_evidence_and_related_links(self):
        for host in ("teams.microsoft.com", "microsoft-my.sharepoint.com", "airlift.microsoft.com"):
            for field in ("url", "evidenceUrl", "links"):
                with self.subTest(host=host, field=field):
                    record = copy.deepcopy(self.curated[0])
                    record[field] = [{"label": "Private", "url": f"https://{host}/private"}] if field == "links" else f"https://{host}/private"
                    with self.assertRaisesRegex(ValueError, "Internal source"):
                        validate([record])

    def test_rejects_duplicate_ids_unsafe_urls_and_impossible_dates(self):
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            validate([self.curated[0], self.curated[0]])
        for field, value in (("url", "javascript:alert(1)"), ("date", "2026-02-31")):
            record = copy.deepcopy(self.curated[0])
            record[field] = value
            with self.assertRaises(ValueError):
                validate([record])

    def test_rejects_sap_url_alias_duplicates(self):
        first = copy.deepcopy(next(record for record in self.curated if "/ba-p/" in record["url"]))
        second = copy.deepcopy(first)
        second["id"] += "-alias"
        for alias in ("m-p", "ec-p", "ev-p"):
            with self.subTest(alias=alias):
                second["url"] = first["url"].replace("/ba-p/", f"/{alias}/") + "?search-result-uid=example"
                with self.assertRaisesRegex(ValueError, "Duplicate SAP content"):
                    validate([first, second])

    def test_public_payload_matches_inputs(self):
        payload = json.loads((ROOT / "site" / "catalogue.json").read_text(encoding="utf-8"))
        expected = [r for r in self.curated + self.podcasts if r["verification"] != "Needs review"]
        self.assertEqual({r["id"] for r in payload["records"]}, {r["id"] for r in expected})
        self.assertEqual(len(payload["records"]), len(expected))
        self.assertNotIn("Needs review", {r["verification"] for r in payload["records"]})

    def test_publication_excludes_unresolved_records_without_changing_research(self):
        ready = copy.deepcopy(self.curated[0])
        ready["evidenceNote"] = ("User-provided SAP Community search excerpt: byline names Holger. "
                                 "Original page not reviewed; direct SAP Community retrieval previously returned HTTP 403.")
        ready["dateNote"] = "Advertised event date; delivery not independently confirmed."
        pending = copy.deepcopy(ready)
        pending.update(id="unresolved-research-only", verification="Needs review")
        original = [ready, pending]
        before = copy.deepcopy(original)
        published = publication_records(original)
        self.assertEqual(original, before)
        self.assertEqual(len(published), 1)
        self.assertEqual(published[0]["verification"], ready["verification"])
        self.assertEqual(published[0]["dateNote"], ready["dateNote"])
        self.assertNotIn("403", published[0]["evidenceNote"])
        self.assertIn("not been independently reviewed", published[0]["evidenceNote"])
        encoded = json.dumps({"records": published})
        self.assertNotIn(pending["id"], standalone(encoded))

    def test_standalone_embeds_assets_and_escapes_untrusted_titles(self):
        html = standalone(json.dumps({"records": [{"title": "</script><script>alert(1)</script>"}]}))
        self.assertNotIn("</script><script>alert(1)", html)
        self.assertIn("\\u003c/script\\u003e", html)
        self.assertNotIn('src="./', html)
        self.assertNotIn('href="./', html)
        self.assertLess(html.index('id="results"'), html.index('"use strict"'))


class SapExcerptTests(unittest.TestCase):
    def result(self, identifier="13384175", author="Holger-Bruchelt", tag=""):
        byline = (f"[{author}](https://community.sap.com/t5/user/viewprofilepage/user-id/3494)"
                  if author == "Holger-Bruchelt" else author)
        return f"""## [Beauty of OData](https://community.sap.com/t5/technology-blog-posts-by-members/beauty-of-odata/ba-p/{identifier}?search-action-id=tracking)

by {byline} [Technology Blog Posts](https://community.sap.com/t5/example)

\u200e2018 Aug 13 10:38 AM

Unrelated text and page navigation are not catalogue metadata.
{tag}
"""

    def test_deduplicates_excerpt_and_preserves_byline_provenance(self):
        text = self.result()
        parsed = parse_results(text + text)
        records, added, updated = merge_results([], parsed, "2026-11-24")
        self.assertEqual((added, updated), (1, 0))
        record = records[0]
        self.assertEqual(record["date"], "2018-08-13")
        self.assertEqual(record["verification"], "User-provided excerpt")
        self.assertEqual(record["role"], "Author")
        self.assertNotIn("?", record["url"])
        self.assertNotIn("Unrelated text", record["evidenceNote"])

    def test_keeps_legacy_uncertain_and_excludes_unrelated_matches(self):
        text = (self.result("12866725", "Former Member",
                            "- [holger bruchelt](https://community.sap.com/t5/tag/holger%20bruchelt/tg-p)") +
                self.result("13192497", "Former Member") +
                self.result("99998", "Former Member") +
                self.result("99999", "Someone Else"))
        records, added, _ = merge_results([], parse_results(text), "2026-11-24")
        self.assertEqual(added, 2)
        for record in records:
            self.assertEqual(record["verification"], "Needs review")
            self.assertNotEqual(record["role"], "Author")

    def test_enrichment_preserves_event_date_and_is_repeatable(self):
        original, _, _ = merge_results([], parse_results(self.result()), "2026-11-24")
        original[0]["date"] = "2018-11-20"
        original[0]["dateNote"] = "Advertised event date; delivery unconfirmed."
        alias = self.result().replace("/ba-p/", "/m-p/")
        once, added, updated = merge_results(original, parse_results(alias), "2026-11-24")
        self.assertEqual((added, updated), (0, 1))
        self.assertEqual(once[0]["date"], "2018-11-20")
        self.assertIn("2018-08-13", once[0]["dateNote"])
        twice, added, _ = merge_results(once, parse_results(alias), "2026-11-24")
        self.assertEqual(added, 0)
        self.assertEqual(twice[0]["date"], "2018-11-20")
        self.assertEqual(once, twice)

    def test_rejects_empty_or_changed_excerpt(self):
        for text in ("", self.result().replace("2018 Aug 13 10:38 AM", "")):
            with self.subTest(text=text[:40]):
                with self.assertRaises(ValueError):
                    parse_results(text)

    def test_search_import_does_not_replace_reviewed_or_reference_evidence(self):
        records, _, _ = merge_results([], parse_results(self.result()), "2026-11-24")
        for status in ("Source reviewed", "User-provided reference"):
            with self.subTest(status=status):
                records[0].update(verification=status, evidenceNote="Item-level authorship evidence.")
                original = copy.deepcopy(records)
                merged, added, updated = merge_results(records, parse_results(self.result()), "2026-11-25")
                self.assertEqual(merged, original)
                self.assertEqual((added, updated), (0, 0))


if __name__ == "__main__":
    unittest.main()
