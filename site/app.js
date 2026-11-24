"use strict";

(() => {
  const records = window.CATALOGUE?.records;
  const results = document.querySelector("#results");
  if (!Array.isArray(records)) {
    document.querySelector("#result-count").textContent = "The catalogue could not be loaded. Reload the page or use the source catalogue download.";
    return;
  }
  const search = document.querySelector("#search");
  const kind = document.querySelector("#kind");
  const year = document.querySelector("#year");
  const evidence = document.querySelector("#evidence");
  const more = document.querySelector("#more");
  let visible = 18;
  let filtered = records;

  function element(tag, text, className) {
    const node = document.createElement(tag);
    if (text !== undefined) node.textContent = text;
    if (className) node.className = className;
    return node;
  }

  function link(label, url) {
    const node = element("a", label);
    node.href = url;
    return node;
  }

  function card(record) {
    const node = element("article", undefined, "card");
    const meta = element("div", undefined, "card-meta");
    meta.append(element("span", record.kind), element("span", record.date || "Undated"));
    const heading = element("h3");
    heading.append(link(record.title, record.url));
    const attribution = element("p", `${record.publisher} / ${record.role}`);
    const tags = element("div", undefined, "tags");
    record.topics.slice(0, 4).forEach(topic => tags.append(element("span", topic, "tag")));
    const links = element("div", undefined, "card-links");
    links.append(link("Open source \u2197", record.url));
    (record.links || []).forEach(item => links.append(link(item.label + " \u2197", item.url)));
    const details = element("details");
    details.append(element("summary", record.verification + " / source notes"));
    details.append(element("p", record.evidenceNote));
    if (record.dateNote) details.append(element("p", record.dateNote));
    details.append(link("Attribution source \u2197", record.evidenceUrl));
    details.append(element("p", `Checked ${record.checked}`));
    node.append(meta, heading, attribution, tags, links, details);
    return node;
  }

  function populate(select, values) {
    values.forEach(value => {
      const option = element("option", value);
      option.value = value;
      select.append(option);
    });
  }

  const normalize = value => value.normalize("NFKD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
  const haystacks = new Map(records.map(record => [
    record.id, normalize([record.title, record.publisher, record.role, ...record.topics, record.evidenceNote].join(" "))
  ]));
  populate(kind, [...new Set(records.map(record => record.kind))].sort());
  const years = [...new Set(records.filter(record => record.date).map(record => record.date.slice(0, 4)))].sort().reverse();
  populate(year, years);
  populate(evidence, [...new Set(records.map(record => record.verification))].sort());
  document.querySelector("#archive-range").textContent = years.length ? `${years[years.length - 1]} \u2192 ${years[0]}` : "Undated";
  document.querySelector("#episode-count").textContent = records.filter(record => record.kind === "Podcast").length;
  document.querySelector("#other-count").textContent = records.filter(record => record.kind !== "Podcast").length;
  document.querySelector("#featured").replaceChildren(...records.filter(record => record.featured).map(card));

  function render() {
    results.replaceChildren(...filtered.slice(0, visible).map(card));
    document.querySelector("#result-count").textContent = `${filtered.length} references found / showing ${Math.min(visible, filtered.length)}`;
    document.querySelector("#empty").hidden = filtered.length !== 0;
    more.hidden = visible >= filtered.length;
  }

  function filter() {
    const terms = normalize(search.value.trim()).split(/\s+/).filter(Boolean);
    filtered = records.filter(record =>
      (!kind.value || record.kind === kind.value) &&
      (!year.value || record.date?.startsWith(year.value)) &&
      (!evidence.value || record.verification === evidence.value) &&
      terms.every(term => haystacks.get(record.id).includes(term))
    );
    visible = 18;
    render();
  }
  document.querySelector("#filters").addEventListener("submit", event => event.preventDefault());
  document.querySelector("#filters").addEventListener("input", filter);
  document.querySelector("#filters").addEventListener("change", filter);
  document.querySelector("#filters").addEventListener("reset", () => {
    search.value = kind.value = year.value = evidence.value = "";
    filter();
  });
  document.querySelectorAll("[data-kind]").forEach(shortcut => {
    shortcut.addEventListener("click", () => {
      search.value = year.value = evidence.value = "";
      kind.value = shortcut.dataset.kind;
      filter();
    });
  });
  more.addEventListener("click", () => {
    const previousCount = Math.min(visible, filtered.length);
    visible += 18;
    render();
    results.children[previousCount]?.querySelector("h3 a")?.focus({ preventScroll: true });
  });
  const theme = document.querySelector("#theme");
  function updateThemeLabel() {
    const dark = document.documentElement.dataset.theme === "dark";
    theme.textContent = dark ? "Light mode" : "Dark mode";
    theme.setAttribute("aria-label", dark ? "Switch to light mode" : "Switch to dark mode");
  }
  theme.addEventListener("click", () => {
    document.documentElement.dataset.theme = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
    updateThemeLabel();
  });
  updateThemeLabel();
  render();
})();
