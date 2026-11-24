# Holger Bruchelt - professional presence catalogue

A first collection of public professional references and a working, responsive website proposal. Research started **24 November 2026**. This is a starting bibliography, **not a claim to have found every appearance or post**. It excludes unrelated personal information.

## What is collected

- **314 podcast episode records**, episodes 1-314, from the public [SAP on Azure index](https://www.saponazurepodcast.de/), spanning July 2020-November 2026. This is a series-level collection, not 314 individually confirmed appearances by Holger.
- **114 additional public references:** conference sessions, interviews, articles, a book, LinkedIn mentions, projects, profiles, and a presentation-library index. Together with the podcast index, the catalogue contains **428 records**. Related records are not necessarily unique appearances: an organizer post and its talk are separate references.
- **A separate private internal catalogue** is delivered in this Copilot session, outside this repository. No internal titles, links, decks, recordings, or source data are included in the deployable website.

### Requested sources and representative findings

| Area | Initial findings | Evidence / remaining work |
| --- | --- | --- |
| SAPinsider | [Copenhagen 2026 session](https://copenhagen.sapinsider.org/agenda/id/4597111), [speaker page](https://copenhagen.sapinsider.org/speakers/id/2647892), [2024 AI webinar](https://sapinsider.org/webinars/using-microsoft-ai-with-your-sap-solutions-today/) | The 2026 public agenda names Holger. The 2024 expert index links the webinar, but its accessible speaker block lists Robert Holland; Holger's exact role remains unconfirmed. |
| E3 Magazin | [Eine Cloud fuer SAP, 2020](https://e3mag.com/de/eine-cloud-fuer-sap/), [Einfach, schnell und kostenguenstig, 2021](https://e3mag.com/de/einfach-schnell-und-kostenguenstig/) | Both bylines and dates reviewed. English auto-translation is a related link, not another authored work. Author archive and print-only pieces still to enumerate. |
| SIT Weinheim | [2026 event and session](https://sitwhm.de), [YouTube recording](https://www.youtube.com/watch?v=tNvSRY4lvA0), [organizer LinkedIn mention](https://www.linkedin.com/posts/sitwhm_bringing-sap-ai-and-microsoft-ai-together-activity-7522960739511504896-Rrn-) | Event: 19 September 2026. Organizer post corroborates the recording. The website does not yet publish Holger's slide link. |
| Duet / Duet Enterprise | [2012 webinar announcement](https://community.sap.com/t5/technology-blog-posts-by-sap/webinar-duet-enterprise-implementation-by-campana-amp-schott-english/ba-p/12998147), installation workshop, Amsterdam/Madrid reports, original Duet and SPNego leads from 2008-2010 | Supplied excerpts enrich the known dates and roles. Original Duet posts under Former Member are possible previous-account work, not confirmed bylines. The German webinar announcement is a related source, not a second claimed appearance. Recordings remain to locate. |
| SAP Community / SCN blogs | [Beauty of OData](https://community.sap.com/t5/technology-blog-posts-by-members/beauty-of-odata/ba-p/13384175), ABAP SDK for Azure, Event Mesh, Power Platform, DevOps, MCP, podcast news, and older event posts | Imported user-supplied search excerpts with profile 3494 bylines, explicit co-author credits, third-party mentions, and separate uncertain legacy leads. Full-page review is still pending. Search-result dates and truncated titles are labelled as such. |
| Microsoft / Azure blogs | [Azure reliability article with explicit Holger co-author credit](https://techcommunity.microsoft.com/blog/reliability-and-resiliency-in-azure/from-proactive-detection-to-action-how-azure-protects-mission-critical-workloads/4569949) | Verified on Microsoft Tech Community. Main Azure Blog authorship is **not established** by this result. Relevant Azure Blog search hits had other bylines and are not claimed as Holger's work. |
| LinkedIn | Organizer posts from SIT Weinheim and Theobald Software; professional profile | Third-party mentions, not Holger-authored posts. A targeted public search for his own post URLs yielded none; a user-provided LinkedIn export or public permalinks would improve coverage. No login restrictions bypassed. |
| Other media | [Low Code with SAP podcast interview, 2022](https://www.theintelligenceagepodcast.com/low-code-with-sap-with-holger-bruchelt/), heise meets / BI-Spektrum security interview, SAP IAA Mobility interview | Podcast platforms are deduplicated as related links. Original heise audio URL and SAP video details remain to verify. |
| Presentations and books | [19-file public slide library](https://github.com/hobru/SAPonAzure/tree/master/Presentations), [Integration von SAP und Microsoft, 2018](https://www.rheinwerk-verlag.de/integration-von-sap-und-microsoft-der-praktische-leitfaden/) | Library is indexed once; guest slides are not attributed to Holger. Book publisher confirms co-authorship with Thomas Hucke. |

Other leads: ABAPConf 2026 session V5; an older `hobru2000` YouTube channel with a Duet overview playlist and an Outlook/SAP workflow walkthrough (ownership cross-link and individual URLs still to verify).

### SAP Community excerpt expansion

The supplied search pages report 188 results; the pasted text contains **187 distinct linked content IDs**, with the final page repeated. They are search matches, not 188 authored works. This pass adds **84 references** (including the SAP Community profile) and enriches **8 existing records**, rather than duplicating them.

The additions include three explicitly attributed SAP CodeTalk interviews from 2014/2016, course-team/instructor credits, conference and demo mentions, and an explicit co-author credit on the SAP RISE data-federation article. Mentions and acknowledgements are not treated as article authorship. Generic Q&A hits without a visible relationship are excluded.

**17 Former Member articles are retained as possible previous-account work:** 12 historical tagged leads (including the SPNego series and original Duet material) and 5 weaker API Management/Office/Azure leads. The user clarified that older posts can use a previous user ID. That makes Former Member a reason to investigate, not a reason to exclude a post; it does not individually confirm every match. These entries visibly say **Possible previous-account author; attribution unconfirmed** and **Needs review**. The five weaker leads have no visible authorship corroboration in the excerpt.

Direct SAP Community retrieval previously returned HTTP 403. The supplied excerpts are usable metadata evidence, but do not establish why access failed or mean the original pages were reviewed. Only metadata and original attribution notes are retained; signed-in navigation, notification counts, private-message links, and copied article text are excluded.

## Layout proposal

**Editorial personal homepage + searchable professional library**, rather than a chronological social feed:

1. **Identity and focus:** short positioning statement, SAP/Microsoft integration, AI/agents, data/security, and direct podcast/GitHub links.
2. **Selected work:** a small editorial selection of a recent talk, milestone episode, guest appearance, and historical session. `featured` flags control this; there is no invented popularity ranking.
3. **Full catalogue:** keyword search, format/year/evidence filters, newest-first ordering, incremental rendering, source links, exact roles, and expandable evidence/date notes.
4. **About and professional profiles:** draft biography based on a public publisher biography; review the wording before launch.
5. **Internal companion:** a separate authenticated SharePoint/M365 destination, not a hidden public website tab. No internal metadata is shipped with this site.

The prototype uses warm neutral surfaces, a rose accent, local system fonts, light/dark mode, keyboard-accessible controls, and a mobile layout. It deliberately avoids third-party embeds, tracking, copied articles, media downloads, and externally loaded images/fonts.

The landing page borrows hierarchy, a prominent primary action, nearby evidence, and more deliberate spacing from [elayadesign's landing-page design guide](https://github.com/elayadesign/ai-design-skills/blob/main/skills/landing-page-design/SKILL.md), as inspiration rather than a specification. It remains a personal editorial homepage, not a sales funnel: a real SIT Weinheim recording anchors the hero, catalogue counts retain their qualifications, and Listen / Read / Build shortcuts filter the existing library. There are no invented endorsements or testimonials, unnecessary signup forms, or mandatory scroll effects. The existing theme and system fonts are preserved; entrance and hover movement respect reduced-motion preferences.

## Files and maintenance

| Path | Purpose |
| --- | --- |
| `data/public.json` | Hand-curated public reference metadata with attribution and caveats |
| `data/podcast.json` | Reproducible snapshot of the public podcast index |
| `tools/import_podcast.py` | Optional network refresh of episode metadata only |
| `tools/import_sap_community.py` | Offline import of supplied SAP Community search Markdown; explicit bylines, reviewed relationship IDs, and uncertain historical leads only |
| `tools/build.py` | Offline build from two explicit public inputs |
| `site/` | Entire deployable site, including generated JS/JSON catalogue |
| `tools/test_catalogue.py` | Focused importer, schema, and public-boundary checks |

Each record carries a source URL, attribution URL, role, topics, evidence level, check date, and optional publication/event date. Date precision is preserved as year, month, day, or unknown. Event delivery is not inferred from an agenda, invitation, or file modification date.

Evidence labels:

- **Source reviewed:** relevant public page was read; this is not a guarantee of every linked asset's contents.
- **Search indexed:** evidence comes from an indexed excerpt, not a full-page review.
- **User-provided excerpt:** evidence comes from search-result metadata pasted by the user, not an independently reviewed original page.
- **Series index:** episode metadata imported from the public series index; per-episode participation and every media URL have not been independently checked.
- **Needs review:** unresolved role, attribution, or identity question stated explicitly.

Only metadata, concise original notes, and outbound links are stored. No third-party articles, slides, recordings, or transcripts are republished.

### Build and preview (PowerShell, Python 3.10+)

No package installation or server-side application is required.

```powershell
# Optional: refresh the public podcast index. Requires internet access.
python tools\import_podcast.py

# Optional: import a user-supplied search excerpt kept outside public inputs.
# Do not commit raw signed-in page copies. Review the resulting metadata.
python tools\import_sap_community.py --input .local\sap-community-search.md

# Offline build and checks
python tools\build.py
python -m unittest discover -s tools -p "test_*.py"
node --check site\app.js

# Optional: generate a portable single-file preview (not deployed automatically)
python tools\build.py --standalone .local\website-proposal.html

# Local preview; binds only to this computer
python -m http.server 8037 --bind 127.0.0.1 --directory site
```

Open `http://127.0.0.1:8037`. The generated site also works by opening `site\index.html` directly; data is loaded from a local JS asset, not a cross-origin `fetch`. Node is only needed for the optional JavaScript syntax check.

The importer rejects missing titles/dates, duplicate episode numbers, empty results, and a decrease in the existing snapshot count. Episode 16 has a malformed video link in the source index: its episode page is retained with an explicit caveat and no fabricated YouTube link. Review that at the source. Automated refresh is intentionally not enabled.

The SAP Community importer removes search tracking parameters and deduplicates repeated excerpts and existing content IDs, including migrated `m-p` / `ba-p` aliases. The build independently rejects duplicate SAP content IDs. Announcement publication dates do not overwrite existing advertised event dates. Titles ending in an ellipsis are kept as displayed rather than silently reconstructed.

The build reads only the two named public datasets and rejects known Microsoft internal source hosts in record URLs. This is a guardrail, **not a general data-loss-prevention classifier**: manually review new public records and every deployment artifact.

## Hosting options

**Recommendation: keep GitHub as the source of truth and publish the static `site` artifact to GitHub Pages; use bruchelt.de as its custom domain if desired.** The same files also work with the existing bruchelt.de web host.

### GitHub Pages

1. Review the catalogue and draft biography; keep the private internal catalogue out of Git and deployment artifacts.
2. This repository is currently private. Confirm that the account's plan supports Pages from private repositories, or choose another host. A private source repository does **not** make a published Pages site private.
3. In repository Settings > Pages, choose GitHub Actions. A future deployment workflow should build with `python tools\build.py`, run the checks above, and upload **only `site`** with the official Pages artifact action. Never upload the repository root or session artifacts.
4. Grant the deployment job only the required Pages permissions (`contents: read`, `pages: write`, `id-token: write`), use the `github-pages` environment, and deploy with the official Pages deploy action.
5. The relative asset URLs work both at a project path such as `/about-me/` and at a custom-domain root. Nothing is published by this change; no deployment workflow or remote settings were changed.

### bruchelt.de

Either upload the contents of `site` to the current web host, or configure the domain in GitHub Pages after verifying domain ownership. Only then change the relevant DNS records using GitHub's current custom-domain guidance and enable HTTPS. Decide first whether the apex or `www` name is canonical; don't overwrite existing DNS/email records. A CNAME file is deliberately not included until that decision is made.

The existing domain could not be fetched in this research environment (connection/TLS failure), so its current layout, hosting, ownership configuration, and available paths were not assessed.

Before a real public launch, review applicable German imprint/privacy requirements, accessibility, branding, and publication permissions. No legal notice or personal address has been invented.

## Next collection priorities

1. Confirm the 17 possible previous-account SCN articles using original bylines, previous user IDs, or the user's item-level confirmation. Resolve truncated titles and expand historic Duet coverage using SAP TechEd catalogs and official archives. A third-party document mirror was excluded as insufficient primary evidence.
2. Enumerate E3 author archives and SAPinsider event years, including member-only recordings through authorized access.
3. Review individual podcast appearances and public presentation bylines; link each talk to its public deck where attribution is clear.
4. Collect Holger-authored LinkedIn post permalinks from an authorized export; retain third-party mentions separately.
5. Establish exact Azure Blog authorship/contributor credits rather than treating subject-matter overlap as evidence.
6. Confirm uncertain dates, archive dead links through legitimate public archives, and review titles in their original language.
