/* Traduction FR (source) → ES, EN, AR.
   - Langue : ?lang=xx, sinon choix mémorisé, sinon langue du navigateur, sinon FR.
   - Dictionnaire : js/i18n-data.js (généré depuis i18n/translations.tsv par tools/build-i18n.py).
   - Traduit les données (produits, rayons) à la source, puis le DOM (textes + attributs), y compris le contenu ajouté ensuite.
   - Arabe : sens droite-à-gauche + polices arabes. */
(function () {
  const LANGS = {
    fr: { name: "Français", short: "FR", dir: "ltr", loc: "fr-FR" },
    es: { name: "Español", short: "ES", dir: "ltr", loc: "es-ES" },
    en: { name: "English", short: "EN", dir: "ltr", loc: "en-GB" }
  };
  const store = (k, v) => { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; } };
  function detect() {
    const q = new URLSearchParams(location.search).get("lang");
    if (LANGS[q]) { store("vg-lang", q); return q; }
    const s = store("vg-lang"); if (LANGS[s]) return s;
    const n = (navigator.languages || [navigator.language || "fr"]).map((x) => String(x).slice(0, 2)).find((x) => LANGS[x]);
    return n || "fr";
  }
  const lang = detect(), meta = LANGS[lang];
  const DICT = Object.assign({}, (window.SODISCOM_I18N_DATA || {})[lang] || {}, (window.VG_UI || {})[lang] || {}, (window.VG_DICT || {})[lang] || {});
  const CN = (window.SODISCOM_CONFIG || {}).name || "Ventage Group";
  const brand = (s) => (s.indexOf("SODISCOM") < 0 ? s : s.replace(/SODISCOM Pro/g, "Ventage Pro").replace(/SODISCOM-GE|SODISCOM/g, CN));
  const tr = (s) => {
    if (s == null) return s;
    let str = String(s); const k = str.trim();
    if (!k) return str;
    if (lang !== "fr") { const v = DICT[k]; if (v != null) str = str.replace(k, v); }
    return brand(str);
  };
  const t = (s, vars) => { let o = tr(s); if (vars) o = o.replace(/\{(\w+)\}/g, (m, k) => (vars[k] ?? m)); return o; };

  document.documentElement.lang = lang;
  document.documentElement.dir = meta.dir;
  if (false) {
    const l = document.createElement("link"); l.rel = "stylesheet";
    l.href = "https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800&family=Amiri:wght@400;700&display=swap";
    document.head.append(l);
  }

  /* Données : rayons et produits traduits une fois pour toutes */
  const D = window.SODISCOM_DATA, C = window.SODISCOM_CONFIG;
  if (D && lang !== "fr") {
    D.categories.forEach((c) => { c.label = tr(c.label); if (c.short) c.short = tr(c.short); if (c.desc) c.desc = tr(c.desc); c.subs.forEach((s) => (s.label = tr(s.label))); });
    D.products.forEach((p) => {
      p.name = tr(p.name); p.highlights = p.highlights.map(tr);
      p.specs = Object.fromEntries(Object.entries(p.specs).map(([k, v]) => [tr(k), tr(v)]));
    });
    if (C) { C.delivery.note = tr(C.delivery.note); C.country = tr(C.country); }
  }

  /* DOM : textes et attributs */
  const ATTRS = ["placeholder", "aria-label", "title", "alt"];
  const SKIP = /^(SCRIPT|STYLE|NOSCRIPT)$/;
  function walk(root) {
    if (!root) return;
    if (root.nodeType === 3) { const v = tr(root.nodeValue); if (v !== root.nodeValue) root.nodeValue = v; return; }
    if (root.nodeType !== 1 || SKIP.test(root.nodeName) || root.closest("[data-noi18n]")) return;
    const tw = document.createTreeWalker(root, NodeFilter.SHOW_ELEMENT | NodeFilter.SHOW_TEXT, {
      acceptNode: (n) => (n.nodeType === 1 && (SKIP.test(n.nodeName) || n.hasAttribute("data-noi18n")) ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT)
    });
    let n = root;
    do {
      if (n.nodeType === 3) { const v = tr(n.nodeValue); if (v !== n.nodeValue) n.nodeValue = v; }
      else for (const a of ATTRS) if (n.hasAttribute(a)) { const o = n.getAttribute(a), v = tr(o); if (v !== o) n.setAttribute(a, v); }
    } while ((n = tw.nextNode()));
  }
  {
    document.title = tr(document.title);
    const md = document.querySelector('meta[name="description"]'); if (md) md.content = tr(md.content);
    walk(document.body);
    new MutationObserver((ms) => ms.forEach((m) => {
      if (m.type === "attributes") { const o = m.target.getAttribute(m.attributeName), v = tr(o); if (v !== o) m.target.setAttribute(m.attributeName, v); }
      else m.addedNodes.forEach(walk);
    })).observe(document.body, { childList: true, subtree: true, attributes: true, attributeFilter: ATTRS });
    // titres de page posés par les scripts
    const td = Object.getOwnPropertyDescriptor(Document.prototype, "title");
    if (td && td.set) Object.defineProperty(document, "title", { get() { return td.get.call(this); }, set(v) { td.set.call(this, tr(v)); }, configurable: true });
  }

  function setLang(l) {
    if (!LANGS[l]) return; store("vg-lang", l);
    const u = new URL(location.href); u.searchParams.set("lang", l); location.href = u.toString();
  }
  window.I18N = { lang, meta, LANGS, t, tr, setLang, rtl: meta.dir === "rtl", walk };
})();
