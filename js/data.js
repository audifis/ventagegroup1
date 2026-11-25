/* Données du showroom courant, construites depuis js/catalog.js.
   Les textes « fr|es|en » sont découpés : le français sert de clé, l'espagnol et l'anglais alimentent le dictionnaire. */
(function () {
  const V = window.VENTAGE, S = window.VG_SHOWROOM;
  const DICT = (window.VG_DICT = window.VG_DICT || { es: {}, en: {} });
  const fr = (s) => {
    if (s == null || typeof s !== "string" || s.indexOf("|") < 0) return s;
    const [f, e, n] = s.split("|"); if (e) DICT.es[f] = e; if (n) DICT.en[f] = n; return f;
  };
  window.VG_FR = fr;

  const all = V.PRODUCTS.map(([id, sr, brand, name, category, sub, img, price, old, flags, hl, specs, svg]) => ({
    id, sr, brand, name: fr(name), category, sub, img, svg: svg || null,
    highlights: (hl || []).map(fr), specs: Object.fromEntries(Object.entries(specs || {}).map(([k, v]) => [fr(k), fr(v)])),
    price, oldPrice: old, isNew: /new/.test(flags), best: /best/.test(flags),
    ref: "VG-" + id.toUpperCase().replace(/[^A-Z0-9]/g, "").slice(0, 8)
  }));
  const products = all.filter((p) => p.sr === S.id);
  const used = new Set(products.map((p) => p.category)), usedSub = new Set(products.map((p) => p.sub));
  const catIds = V.CATEGORIES.filter((c) => used.has(c.id)).map((c) => c.id);
  const categories = V.CATEGORIES.filter((c) => used.has(c.id)).map((c) => ({
    id: c.id, label: fr(c.label), short: c.short ? fr(c.short) : null, icon: c.icon, desc: fr(c.desc || ""),
    img: (products.find((p) => p.category === c.id && p.img && !/^dj:/.test(p.img)) || products.find((p) => p.category === c.id && p.img) || {}).img || `ph:${S.id}:${catIds.indexOf(c.id) + 1}`,
    scene: `ph:${S.id}:${catIds.indexOf(c.id) + 1}`,
    subs: c.subs.filter(([id]) => usedSub.has(id)).map(([id, label]) => ({ id, label: fr(label) }))
  }));
  fr(S.tag); fr(S.desc); fr(S.plaque);

  window.SODISCOM_DATA = {
    showroom: S, categories, products,
    brands: [...new Set(products.map((p) => p.brand))].sort(),
    findProduct: (id) => products.find((p) => p.id === id),
    findCategory(id) { return this.categories.find((c) => c.id === id); },
    findSub(id) { for (const c of this.categories) { const s = c.subs.find((x) => x.id === id); if (s) return { ...s, parent: c }; } return null; },
    discount: (p) => (p.oldPrice && p.price ? Math.round((1 - p.price / p.oldPrice) * 100) : 0)
  };
})();
