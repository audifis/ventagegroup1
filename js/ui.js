/* Composants partagés : en-tête e-commerce (recherche instantanée, catégories), barre mobile, pied de page,
   cartes produit, images responsives, rendus studio SVG, toasts, comparateur. */
(function () {
  const C = window.SODISCOM_CONFIG, D = window.SODISCOM_DATA, S = window.VG_SHOWROOM, V = window.VENTAGE;
  const VGF = window.VG_FR || ((s) => s);
  const L = window.I18N || { t: (s, v) => s.replace(/\{(\w+)\}/g, (m, k) => v[k]), tr: (s) => s, meta: { loc: "fr-FR" }, lang: "fr", LANGS: {}, rtl: false };
  const t = L.t, tr = L.tr;
  const $ = (s, r = document) => r.querySelector(s);
  const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const wa = (msg) => `https://wa.me/${C.whatsapp}?text=${encodeURIComponent(tr(msg))}`;
  const fmt = (v) => new Intl.NumberFormat(L.meta.loc).format(v).replace(/ /g, " ") + " FCFA";
  const productUrl = (p) => `produit.html?id=${encodeURIComponent(p.id)}`;

  /* ——— Images ——— */
  // Chemin d'une image optimisée (la version autonome hors-ligne fournit window.__IMGMAP)
  const phot = (k) => { const m = /^ph:([\w-]+):(\d+)$/.exec(k || ""); if (!m) return null; const s = V.SHOWROOMS.find((x) => x.id === m[1]); return s ? s.photos[+m[2] % s.photos.length] : null; };
  /* Photos en ligne : catalogue de démo (dj:<chemin>:<n>) et photos des lieux, redimensionnées en WebP via wsrv.nl */
  const DJB = "https://cdn.dummyjson.com/product-images/";
  const djN = (k) => { const m = /^dj:(.+):(\d+)$/.exec(k || ""); return m ? +m[2] : 0; };
  const djUrl = (k, i = 1) => { const m = /^dj:(.+):(\d+)$/.exec(k || ""); return m ? `${DJB}${m[1]}/${i}.webp` : null; };
  const remote = (k) => (/^(https?:|assets\/)/.test(k || "") ? k : phot(k) || djUrl(k));
  const opt = (u, w) => !/^https?:/.test(u) ? u : `https://wsrv.nl/?url=${encodeURIComponent(u.replace(/^https?:\/\//, ""))}&w=${w}&output=webp&q=76&we`;
  const rimg = (u, alt, cls = "", eager = false, widths = [400, 800], sizes = "(max-width:600px) 46vw, 300px") =>
    `<img class="${cls} is-photo" src="${opt(u, widths[0])}" srcset="${widths.map((w) => `${opt(u, w)} ${w}w`).join(", ")}" sizes="${sizes}" data-orig="${u}" alt="${esc(alt)}" ${eager ? 'fetchpriority="high"' : 'loading="lazy"'} decoding="async">`;
  document.addEventListener("error", (e) => { const i = e.target; if (i.tagName !== "IMG") return; if (i.dataset.orig && i.getAttribute("src") !== i.dataset.orig) { i.removeAttribute("srcset"); i.src = i.dataset.orig; } else i.style.visibility = "hidden"; }, true);
  const src = (k, s) => remote(k) || (window.__IMGMAP ? (__IMGMAP[`${k}-${s}`] || __IMGMAP[`${k}-${{ 640: 320, 1920: 960 }[s] || s}`] || "") : `assets/img/${k}-${s}.webp`);
  const vm = (k) => (/^vm:(.+)$/.exec(k || "") || [])[1];
  const pimg = (key, alt, cls = "", eager = false) => vm(key) ? `<img class="${cls} is-photo" src="assets/mall/${vm(key)}-400.webp" srcset="assets/mall/${vm(key)}-400.webp 400w, assets/mall/${vm(key)}.webp 600w" sizes="(max-width:600px) 46vw, 300px" alt="${esc(alt)}" width="600" height="800" ${eager ? 'fetchpriority="high"' : 'loading="lazy"'} decoding="async">` : remote(key) ? rimg(remote(key), alt, cls, eager) :
    `<img class="${cls}" src="${src(key, 320)}" srcset="${src(key, 320)} 320w, ${src(key, 640)} 640w" sizes="(max-width:600px) 46vw, 300px" alt="${esc(alt)}" width="640" height="640" ${eager ? 'fetchpriority="high"' : 'loading="lazy"'} decoding="async">`;
  // Photos d'ambiance : AVIF (≈ -45 %) avec WebP en secours, 3 largeurs ; `sizes` = largeur affichée
  const scene = (key, alt = "", eager = false, sizes = "100vw", cls = "") => {
    if (remote(key) && !/^https?:/.test(remote(key))) return `<img class="${cls} is-photo" src="${remote(key)}" alt="${esc(alt)}" ${eager ? 'fetchpriority="high"' : 'loading="lazy"'} decoding="async">`;
    if (remote(key)) return rimg(remote(key), alt, cls, eager, [960, 1600, 2400], sizes);
    const set = (ext) => [960, 1440, 1920].map((w) => `assets/img/${key}-${w}.${ext} ${w}w`).join(", ");
    const img = `<img class="${cls}" src="${src(key, 960)}" ${window.__IMGMAP ? "" : `srcset="${set("webp")}"`} sizes="${sizes}" alt="${esc(alt)}" width="1920" height="1080" ${eager ? 'fetchpriority="high"' : 'loading="lazy"'} decoding="async">`;
    return window.__IMGMAP ? img : `<picture><source type="image/avif" srcset="${set("avif")}" sizes="${sizes}">${img}</picture>`;
  };

  /* Rendus studio vectoriels (produits sans photo libre de droits) */
  const RENDERS = {
    ac: `<svg viewBox="0 0 400 400"><defs><linearGradient id="acb" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff"/><stop offset=".7" stop-color="#eef0f3"/><stop offset="1" stop-color="#cfd3da"/></linearGradient><linearGradient id="acs" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2b2f36"/><stop offset="1" stop-color="#0f1115"/></linearGradient></defs><ellipse cx="200" cy="292" rx="150" ry="10" fill="#000" opacity=".08"/><rect x="40" y="130" width="320" height="110" rx="26" fill="url(#acb)" stroke="#d9dce2"/><rect x="40" y="214" width="320" height="26" rx="10" fill="url(#acs)"/><path d="M70 220h260" stroke="#8a9099" stroke-width="2" opacity=".6"/><rect x="290" y="156" width="40" height="8" rx="4" fill="#d6dae0"/><circle cx="318" cy="186" r="4" fill="#4cc38a"/><text x="70" y="168" font-family="Manrope,Arial" font-size="14" font-weight="700" fill="#9aa1ab" letter-spacing="3">INVERTER</text><path d="M120 262c0 14-8 20-8 32M200 262c0 14 8 20 8 32M280 262c0 14-8 20-8 32" stroke="#9ad0ff" stroke-width="3" fill="none" stroke-linecap="round" opacity=".7"/></svg>`,
    fan: `<svg viewBox="0 0 400 400"><defs><radialGradient id="fg" cx=".5" cy=".45"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#dfe3e8"/></radialGradient></defs><ellipse cx="200" cy="362" rx="80" ry="10" fill="#000" opacity=".1"/><rect x="193" y="200" width="14" height="150" rx="6" fill="#cfd4db"/><ellipse cx="200" cy="352" rx="70" ry="14" fill="#e9ecf0" stroke="#cdd2d9"/><circle cx="200" cy="150" r="110" fill="url(#fg)" stroke="#cfd4db" stroke-width="3"/><g stroke="#c3c9d1" stroke-width="2" fill="none">${Array.from({ length: 12 }, (_, i) => `<line x1="200" y1="150" x2="${200 + 108 * Math.cos(i * Math.PI / 6)}" y2="${150 + 108 * Math.sin(i * Math.PI / 6)}"/>`).join("")}<circle cx="200" cy="150" r="70"/></g><g fill="#5b9bd5" opacity=".85"><path d="M200 150c-10-40 10-80 40-82-10 30-14 60-40 82z"/><path d="M200 150c40-8 78 14 78 44-28-10-58-14-78-44z"/><path d="M200 150c-30 28-74 26-88 0 30 0 62-6 88 0z"/></g><circle cx="200" cy="150" r="16" fill="#1f2a37"/></svg>`,
    freezer: `<svg viewBox="0 0 400 400"><defs><linearGradient id="fz" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#e3e6eb"/></linearGradient></defs><ellipse cx="200" cy="320" rx="160" ry="12" fill="#000" opacity=".1"/><rect x="45" y="150" width="310" height="165" rx="12" fill="url(#fz)" stroke="#cfd4db" stroke-width="2"/><rect x="40" y="128" width="320" height="34" rx="10" fill="#f7f8fa" stroke="#cfd4db" stroke-width="2"/><rect x="170" y="150" width="60" height="10" rx="5" fill="#9aa1ab"/><rect x="290" y="190" width="40" height="14" rx="4" fill="#1f2a37"/><circle cx="300" cy="197" r="2.5" fill="#4cc38a"/><path d="M60 300h280" stroke="#c9ced6" stroke-width="3"/></svg>`,
    stove: `<svg viewBox="0 0 400 400"><defs><linearGradient id="st" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f2f3f5"/><stop offset="1" stop-color="#d6dae0"/></linearGradient></defs><ellipse cx="200" cy="362" rx="130" ry="10" fill="#000" opacity=".1"/><rect x="80" y="70" width="240" height="40" rx="6" fill="#1b1e24"/><g fill="#2c313a" stroke="#555c66"><circle cx="140" cy="90" r="14"/><circle cx="185" cy="90" r="10"/><circle cx="225" cy="90" r="12"/><circle cx="265" cy="90" r="14"/></g><rect x="80" y="110" width="240" height="245" rx="8" fill="url(#st)" stroke="#c4c9d1"/><g fill="#1b1e24">${[120, 160, 200, 240, 280].map((x) => `<circle cx="${x}" cy="135" r="8"/>`).join("")}</g><rect x="100" y="160" width="200" height="150" rx="8" fill="#14171c"/><rect x="112" y="172" width="176" height="126" rx="6" fill="#2a2f37" opacity=".9"/><path d="M118 180l40 0" stroke="#fff" stroke-width="3" opacity=".25"/><rect x="120" y="152" width="160" height="6" rx="3" fill="#aab0b9"/></svg>`
  };
  const SI = {
    shirt: '<path d="M8 3l-5 3 2 5 3-1v11h8V10l3 1 2-5-5-3c-.5 1.7-2 3-4 3S8.5 4.7 8 3z"/>',
    perfume: '<rect x="5" y="9" width="14" height="12" rx="3"/><path d="M9 9V6h6v3M10 6V3h4v3M9 15h6"/>',
    glasses: '<circle cx="6.5" cy="14" r="3.5"/><circle cx="17.5" cy="14" r="3.5"/><path d="M10 14c.6-.8 3.4-.8 4 0M3 14l1-7h2M21 14l-1-7h-2"/>',
    watch: '<circle cx="12" cy="12" r="6"/><path d="M12 9v3l2 1.5M9 6.5L10 2h4l1 4.5M9 17.5L10 22h4l1-4.5"/>',
    bagl: '<path d="M4 8h16l-1.5 13h-13z"/><path d="M8 8V6a4 4 0 018 0v2"/>',
    basket: '<path d="M3 10h18l-2 10H5z"/><path d="M8 10l3-6M16 10l-3-6M9 14v3M15 14v3M12 14v3"/>',
    bottle: '<path d="M10 2h4v3l2 3v13a1 1 0 01-1 1H9a1 1 0 01-1-1V8l2-3z"/><path d="M8 12h8M8 17h8"/>',
    spray: '<rect x="7" y="10" width="10" height="11" rx="2"/><path d="M9 10V7h6v3M15 7h3l2-2M12 14v3"/>',
    brick: '<rect x="3" y="5" width="18" height="14" rx="1"/><path d="M3 9.7h18M3 14.3h18M9 5v4.7M15 5v4.7M6 9.7v4.6M12 9.7v4.6M18 9.7v4.6M9 14.3V19M15 14.3V19"/>',
    drill: '<path d="M3 7h12v6H3zM15 9h4M19 10h2M8 13l-1 8h4l1-8"/>',
    bolt: '<path d="M13 2L4 14h7l-1 8 9-12h-7z"/>',
    bulb: '<path d="M9 18h6M10 21h4M12 3a6 6 0 00-4 10.5c.7.7 1 1.5 1 2.5h6c0-1 .3-1.8 1-2.5A6 6 0 0012 3z"/>',
    sun: '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2M5 5l1.5 1.5M17.5 17.5L19 19M5 19l1.5-1.5M17.5 6.5L19 5"/>',
    paint: '<rect x="3" y="3" width="15" height="7" rx="1.5"/><path d="M18 6h3v6h-9v3"/><rect x="10" y="15" width="4" height="7" rx="1"/>',
    pill: '<rect x="2.5" y="8.5" width="19" height="7" rx="3.5" transform="rotate(-45 12 12)"/><path d="M9.5 9.5l5 5"/>',
    cross: '<path d="M9 3h6v6h6v6h-6v6H9v-6H3V9h6z"/>',
    heart: '<path d="M12 20s-8-5-8-11a4 4 0 018-1 4 4 0 018 1c0 6-8 11-8 11z"/><path d="M7 11h3l1-2 2 4 1-2h3"/>',
    flask: '<path d="M9 3h6M10 3v6L4.5 19a1.5 1.5 0 001.3 2h12.4a1.5 1.5 0 001.3-2L14 9V3M7 15h10"/>',
    tire: '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4"/><path d="M12 3v5M12 16v5M3 12h5M16 12h5"/>',
    car: '<path d="M5 16v-5l2-5h10l2 5v5M3 16h18v3H3zM5 11h14"/><circle cx="7.5" cy="13.5" r=".8"/><circle cx="16.5" cy="13.5" r=".8"/>',
    oil: '<path d="M4 10h9l4 3 4-2-2 6H4z"/><path d="M7 10V7h4v3"/>',
    tag: '<path d="M3 12V4h8l10 10-8 8z"/><circle cx="7.5" cy="8" r="1.4"/>'
  };
  Object.assign(SI, {"shoe": "<path d=\"M3 16c0-3 1-7 2-9 2 0 3 2 5 3 3 1 6 1 9 3 2 1 2 3 2 3H3z\"/><path d=\"M3 19h18\"/>", "lipstick": "<path d=\"M9 21h6V11H9z\"/><path d=\"M10 11V6l4-3v8\"/>", "gem": "<path d=\"M6 3h12l3 6-9 12L3 9z\"/><path d=\"M3 9h18M9 3l3 18 3-18\"/>", "apple": "<path d=\"M12 7c-2-2-7-1-7 5 0 4 3 9 5 9 1 0 1.5-.5 2-.5s1 .5 2 .5c2 0 5-5 5-9 0-6-5-7-7-5z\"/><path d=\"M12 7c0-2 1-4 3-4\"/>", "can": "<rect x=\"6\" y=\"4\" width=\"12\" height=\"16\" rx=\"2\"/><path d=\"M6 8h12M6 16h12\"/>", "cup": "<path d=\"M4 8h13v6a5 5 0 01-5 5H9a5 5 0 01-5-5z\"/><path d=\"M17 10h2a2 2 0 010 4h-2M8 3v2M12 3v2\"/>", "soap": "<rect x=\"3\" y=\"10\" width=\"18\" height=\"9\" rx=\"4\"/><circle cx=\"8\" cy=\"6\" r=\"2\"/><circle cx=\"14\" cy=\"5\" r=\"1.5\"/>", "baby": "<circle cx=\"12\" cy=\"10\" r=\"6\"/><path d=\"M10 10h.01M14 10h.01M10 13c1 1 3 1 4 0M12 4c0-1 1-1 1-1\"/><path d=\"M7 20c1-2 3-3 5-3s4 1 5 3\"/>", "fish": "<path d=\"M3 12c3-5 9-6 13-2l5-3v10l-5-3c-4 4-10 3-13-2z\"/><circle cx=\"8\" cy=\"11\" r=\".8\"/>", "vacuum": "<path d=\"M14 3l-6 14\"/><rect x=\"4\" y=\"17\" width=\"8\" height=\"4\" rx=\"1\"/><circle cx=\"17\" cy=\"18\" r=\"3\"/><path d=\"M12 19h2\"/>", "iron": "<path d=\"M3 17h18c0-6-4-9-9-9H8l-1-3h9\"/><path d=\"M3 17l2-5\"/>", "heater": "<rect x=\"7\" y=\"2\" width=\"10\" height=\"18\" rx=\"5\"/><path d=\"M10 22v-2M14 22v-2M10 9c1 1 1 2 0 3M14 9c1 1 1 2 0 3\"/>", "drop": "<path d=\"M12 3s7 7 7 12a7 7 0 01-14 0c0-5 7-12 7-12z\"/>", "speaker": "<rect x=\"6\" y=\"2\" width=\"12\" height=\"20\" rx=\"2\"/><circle cx=\"12\" cy=\"15\" r=\"3\"/><circle cx=\"12\" cy=\"6.5\" r=\"1.5\"/>", "console": "<path d=\"M6 8h12a4 4 0 014 4v2a4 4 0 01-7 2l-1-1h-4l-1 1a4 4 0 01-7-2v-2a4 4 0 014-4z\"/><path d=\"M7 11v3M5.5 12.5h3M16 12h.01M18 13h.01\"/>", "pillow": "<path d=\"M4 7c4-2 12-2 16 0 1 3 1 7 0 10-4 2-12 2-16 0-1-3-1-7 0-10z\"/>", "dumbbell": "<path d=\"M6 7v10M3 9v6M18 7v10M21 9v6M6 12h12\"/>", "suitcase": "<rect x=\"5\" y=\"6\" width=\"14\" height=\"14\" rx=\"2\"/><path d=\"M9 6V3h6v3M9 10v6M15 10v6M8 20v1M16 20v1\"/>", "ball": "<circle cx=\"12\" cy=\"12\" r=\"9\"/><path d=\"M12 7l4 3-1.5 5h-5L8 10z\"/><path d=\"M12 3v4M21 10l-5 0M17 20l-2.5-5M7 20l2.5-5M3 10h5\"/>", "plate": "<circle cx=\"12\" cy=\"12\" r=\"9\"/><circle cx=\"12\" cy=\"12\" r=\"5\"/>", "pan": "<circle cx=\"9\" cy=\"12\" r=\"7\"/><path d=\"M16 12h6\"/>", "lamp": "<path d=\"M8 3h8l3 8H5z\"/><path d=\"M12 11v8M8 21h8\"/>", "rug": "<rect x=\"4\" y=\"5\" width=\"16\" height=\"14\" rx=\"1\"/><path d=\"M8 9l4 3-4 3M16 9l-4 3 4 3M4 3v2M8 3v2M12 3v2M16 3v2M20 3v2M4 19v2M8 19v2M12 19v2M16 19v2M20 19v2\"/>", "roof": "<path d=\"M2 12l10-8 10 8\"/><path d=\"M5 10v10h14V10\"/><path d=\"M9 20v-5h6v5\"/>", "tile": "<rect x=\"3\" y=\"3\" width=\"8\" height=\"8\"/><rect x=\"13\" y=\"3\" width=\"8\" height=\"8\"/><rect x=\"3\" y=\"13\" width=\"8\" height=\"8\"/><rect x=\"13\" y=\"13\" width=\"8\" height=\"8\"/>", "toilet": "<path d=\"M6 3h6v7H6z\"/><path d=\"M4 10h14a4 4 0 01-4 6l1 5H8l1-4a6 6 0 01-5-7z\"/>", "tap": "<path d=\"M4 8h10a4 4 0 014 4v2\"/><path d=\"M9 8V5M6 5h6\"/><path d=\"M18 17v.01M18 20v.01\"/>", "pipe": "<path d=\"M3 7h9a3 3 0 013 3v11\"/><path d=\"M3 11h8v10\"/><path d=\"M3 5v8M17 19h-6\"/>", "screw": "<path d=\"M9 3h6l-1 3h-4z\"/><path d=\"M12 6v15M10 9l4 1M10 12l4 1M10 15l4 1M10 18l4 1\"/>", "lock": "<rect x=\"5\" y=\"10\" width=\"14\" height=\"11\" rx=\"2\"/><path d=\"M8 10V7a4 4 0 018 0v3M12 14v3\"/>", "hammer": "<path d=\"M14 4l6 6-3 3-6-6z\"/><path d=\"M11 7l-8 8 3 3 8-8\"/>", "shovel": "<path d=\"M14 3l7 7M17.5 6.5L9 15\"/><path d=\"M9 15l-5 1-1 4 4-1 1-5\"/>", "socket": "<rect x=\"3\" y=\"3\" width=\"18\" height=\"18\" rx=\"3\"/><circle cx=\"12\" cy=\"12\" r=\"5\"/><path d=\"M10 11v2M14 11v2\"/>", "panel": "<rect x=\"4\" y=\"3\" width=\"16\" height=\"18\" rx=\"1\"/><path d=\"M4 9h16M8 9v5M11 9v5M14 9v5M17 9v5\"/>", "flood": "<rect x=\"3\" y=\"5\" width=\"12\" height=\"10\" rx=\"1\"/><path d=\"M9 15v4M5 19h8M17 7l4-2M17 10h4M17 13l4 2\"/>", "gen": "<rect x=\"3\" y=\"7\" width=\"18\" height=\"11\" rx=\"1\"/><path d=\"M7 18v2M17 18v2M12 9l-2 4h4l-2 4\"/>", "battery": "<rect x=\"3\" y=\"7\" width=\"16\" height=\"10\" rx=\"2\"/><path d=\"M21 10v4M7 12h3M8.5 10.5v3M13 12h3\"/>", "earbuds": "<path d=\"M7 4a3 3 0 00-3 3v3a3 3 0 006 0V7\"/><path d=\"M7 13v7M17 4a3 3 0 013 3v3a3 3 0 01-6 0V7\"/><path d=\"M17 13v7\"/>", "monitor": "<rect x=\"3\" y=\"4\" width=\"18\" height=\"12\" rx=\"1\"/><path d=\"M12 16v4M8 20h8\"/>", "router": "<rect x=\"3\" y=\"13\" width=\"18\" height=\"7\" rx=\"1\"/><path d=\"M7 13l-1-6M17 13l1-6M7 16.5h.01M10 16.5h.01\"/>", "pen": "<path d=\"M15 4l5 5L9 20H4v-5z\"/><path d=\"M13 6l5 5\"/>", "charger": "<rect x=\"6\" y=\"8\" width=\"12\" height=\"13\" rx=\"2\"/><path d=\"M9 8V3M15 8V3M12 12l-1.5 3h3L12 18\"/>", "trowel": "<path d=\"M3 14l8-8 7 7-8 8z\"/><path d=\"M14 10l4-4 3 3\"/>", "roller": "<rect x=\"3\" y=\"3\" width=\"15\" height=\"6\" rx=\"1.5\"/><path d=\"M18 6h3v5h-9v3\"/><path d=\"M12 14v7\"/>", "wall": "<rect x=\"3\" y=\"3\" width=\"18\" height=\"18\" rx=\"1\"/><path d=\"M3 9c4 2 8-2 12 0s4 2 6 0M3 15c4 2 8-2 12 0s4 2 6 0\"/>", "tape": "<circle cx=\"10\" cy=\"12\" r=\"7\"/><circle cx=\"10\" cy=\"12\" r=\"3\"/><path d=\"M17 12h4v7H10\"/>", "brush": "<path d=\"M8 3h8v8H8zM8 11h8l-1 3H9z\"/><path d=\"M12 14v7\"/>", "tooth": "<path d=\"M7 3c-3 0-4 3-3 6s1 5 2 9c.5 2 2 2 2.5 0L10 14h4l1.5 4c.5 2 2 2 2.5 0 1-4 1-6 2-9s0-6-3-6c-2 0-3 1-5 1S9 3 7 3z\"/>", "capsule": "<rect x=\"3\" y=\"8\" width=\"18\" height=\"8\" rx=\"4\"/><path d=\"M12 8v8\"/>", "mosquito": "<ellipse cx=\"12\" cy=\"13\" rx=\"2\" ry=\"5\"/><path d=\"M12 8V4M10 11L4 7M14 11l6-4M10 14l-6 2M14 14l6 2M11 18l-2 3M13 18l2 3\"/>", "dna": "<path d=\"M7 3c0 6 10 6 10 12s-10 3-10 6M17 3c0 6-10 6-10 12s10 3 10 6\"/><path d=\"M9 7h6M9 17h6\"/>", "virus": "<circle cx=\"12\" cy=\"12\" r=\"5\"/><path d=\"M12 3v4M12 17v4M3 12h4M17 12h4M5.6 5.6l2.9 2.9M15.5 15.5l2.9 2.9M5.6 18.4l2.9-2.9M15.5 8.5l2.9-2.9\"/>", "clipboard": "<rect x=\"5\" y=\"4\" width=\"14\" height=\"17\" rx=\"2\"/><path d=\"M9 4V2h6v2M9 10h6M9 14h6M9 18h3\"/>", "brake": "<circle cx=\"12\" cy=\"12\" r=\"9\"/><circle cx=\"12\" cy=\"12\" r=\"3\"/><path d=\"M19 7a9 9 0 010 10\"/>", "wiper": "<path d=\"M3 18a12 12 0 0118 0\"/><path d=\"M12 18L6 8\"/>", "wrench": "<path d=\"M14 6a4 4 0 00-5 5l-6 6 3 3 6-6a4 4 0 005-5l-2 2-3-3z\"/>", "moto": "<circle cx=\"5\" cy=\"17\" r=\"3\"/><circle cx=\"19\" cy=\"17\" r=\"3\"/><path d=\"M5 17l4-6h5l3 6M14 11l2-4h3M9 11h-3\"/>", "blender": "<path d=\"M7 3h10l-2 11H9z\"/><rect x=\"7\" y=\"14\" width=\"10\" height=\"7\" rx=\"1\"/><path d=\"M12 17.5h.01\"/>", "freezer": "<rect x=\"3\" y=\"8\" width=\"18\" height=\"12\" rx=\"1.5\"/><path d=\"M3 11h18M10 8V6h4v2\"/>", "ac": "<rect x=\"2\" y=\"5\" width=\"20\" height=\"8\" rx=\"2\"/><path d=\"M6 10h12M7 16c0 2-1 3-1 3M12 16v3M17 16c0 2 1 3 1 3\"/>", "stove": "<rect x=\"4\" y=\"3\" width=\"16\" height=\"18\" rx=\"1.5\"/><path d=\"M4 8h16\"/><rect x=\"7\" y=\"11\" width=\"10\" height=\"7\" rx=\"1\"/>", "fan": "<circle cx=\"12\" cy=\"9\" r=\"6\"/><path d=\"M12 15v6M8 21h8M12 9l3-3M12 9l-4-1M12 9l1 4\"/>", "washer": "<rect x=\"4\" y=\"2\" width=\"16\" height=\"20\" rx=\"2\"/><circle cx=\"12\" cy=\"13\" r=\"5\"/><path d=\"M4 6h16\"/>", "table": "<path d=\"M3 9h18M5 9v11M19 9v11M3 9l2-4h14l2 4\"/>", "printer": "<path d=\"M7 9V3h10v6\"/><rect x=\"3\" y=\"9\" width=\"18\" height=\"8\" rx=\"2\"/><path d=\"M7 14h10v7H7z\"/>", "tv": "<rect x=\"2\" y=\"4\" width=\"20\" height=\"13\" rx=\"1.5\"/><path d=\"M8 21h8M12 17v4\"/>", "phone": "<rect x=\"7\" y=\"2\" width=\"10\" height=\"20\" rx=\"2.5\"/><path d=\"M11 18h2\"/>", "laptop": "<rect x=\"4\" y=\"5\" width=\"16\" height=\"11\" rx=\"1.5\"/><path d=\"M2 19h20\"/>", "bed": "<path d=\"M3 18V6M3 13h18v5M21 13a3 3 0 00-3-3h-8v3\"/><circle cx=\"6.5\" cy=\"10.5\" r=\"1.5\"/>", "sofa": "<path d=\"M4 11V8a3 3 0 013-3h10a3 3 0 013 3v3\"/><path d=\"M2 13a2 2 0 014 0v2h12v-2a2 2 0 014 0v5H2zM5 18v2M19 18v2\"/>", "building": "<path d=\"M4 21V5l8-2v18M12 8h8v13M7 8h2M7 12h2M7 16h2M15 12h2M15 16h2\"/>", "fridge": "<rect x=\"5\" y=\"2\" width=\"14\" height=\"20\" rx=\"2\"/><path d=\"M5 10h14M8 6v1.5M8 13v3\"/>", "pot": "<path d=\"M4 10h16v6a4 4 0 01-4 4H8a4 4 0 01-4-4z\"/><path d=\"M2 10h20M9 6c0-1 1-2 3-2s3 1 3 2\"/>"});
  SI.dress = '<path d="M9 3h6l-1 4 4 14H6l4-14z"/><path d="M9 3c0 2 6 2 6 0"/>';
  SI.tank = '<rect x="5" y="5" width="14" height="16" rx="3"/><path d="M5 10h14M5 15h14M10 2h4v3h-4z"/>';
  const studio = (k) => RENDERS[k] ? `<div class="studio">${RENDERS[k]}</div>` : `<div class="studio studio--ic"><svg viewBox="0 0 24 24" aria-hidden="true">${SI[k] || SI.tag}</svg></div>`;
  const media = (p, cls = "", eager = false) => p.img ? pimg(p.img, p.name, cls, eager) : studio(p.svg);

  /* Pictos de ligne */
  const P = { star: '<path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1L3.2 9.5l6.1-.9z"/>', spark: '<path d="M12 3v5M12 16v5M3 12h5M16 12h5M6.3 6.3l2.5 2.5M15.2 15.2l2.5 2.5M6.3 17.7l2.5-2.5M15.2 8.8l2.5-2.5"/>',
    search: '<circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/>', heart: '<path d="M12 20s-7-4.4-7-10a4 4 0 017-2.6A4 4 0 0119 10c0 5.6-7 10-7 10z"/>',
    bag: '<path d="M5 8h14l-1 12H6z"/><path d="M9 8a3 3 0 016 0"/>', menu: '<path d="M4 7h16M4 12h16M4 17h16"/>', close: '<path d="M6 6l12 12M18 6L6 18"/>',
    compare: '<path d="M8 4v16M16 4v16M4 8h8M12 16h8"/>', arrow: '<path d="M5 12h14M13 6l6 6-6 6"/>', left: '<path d="M15 6l-6 6 6 6"/>', right: '<path d="M9 6l6 6-6 6"/>',
    home: '<path d="M4 11l8-7 8 7v9h-5v-6H9v6H4z"/>', grid: '<rect x="4" y="4" width="7" height="7" rx="1.5"/><rect x="13" y="4" width="7" height="7" rx="1.5"/><rect x="4" y="13" width="7" height="7" rx="1.5"/><rect x="13" y="13" width="7" height="7" rx="1.5"/>',
    pin: '<path d="M12 21s-6-5.5-6-11a6 6 0 0112 0c0 5.5-6 11-6 11z"/><circle cx="12" cy="10" r="2.2"/>', truck: '<path d="M3 7h11v9H3zM14 10h4l3 3v3h-7"/><circle cx="7" cy="18" r="1.8"/><circle cx="17" cy="18" r="1.8"/>',
    shield: '<path d="M12 3l7 3v5c0 5-3 8-7 10-4-2-7-5-7-10V6z"/><path d="M9 12l2 2 4-4"/>', chat: '<path d="M4 5h16v11H9l-5 4z"/>', tool: '<path d="M14 6a4 4 0 00-5 5l-5 5 3 3 5-5a4 4 0 005-5l-2 2-3-3z"/>',
    tv: '<rect x="3" y="5" width="18" height="12" rx="1.5"/><path d="M9 21h6M12 17v4"/>', phone: '<rect x="7" y="2.5" width="10" height="19" rx="2.2"/><path d="M11 18.5h2"/>',
    laptop: '<rect x="5" y="5" width="14" height="10" rx="1"/><path d="M2.5 18.5h19"/>', fridge: '<rect x="6" y="2.5" width="12" height="19" rx="1.8"/><path d="M6 9.5h12M9 5.5v2M9 12v3"/>',
    pot: '<path d="M4 10h16v6a4 4 0 01-4 4H8a4 4 0 01-4-4z"/><path d="M2 10h20M9 6c0-1 1-2 3-2s3 1 3 2"/>', sofa: '<path d="M5 11V8a2 2 0 012-2h10a2 2 0 012 2v3"/><path d="M3 12a2 2 0 014 0v2h10v-2a2 2 0 014 0v5H3z"/><path d="M5 17v2M19 17v2"/>',
    building: '<path d="M4 21V5l8-2v18M12 8h8v13M7 8h2M7 12h2M7 16h2M15 12h2M15 16h2"/>', tag: '<path d="M3 12V4h8l10 10-8 8z"/><circle cx="7.5" cy="8" r="1.4"/>',
    globe: '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3.2 3 14.8 0 18M12 3c-3 3.2-3 14.8 0 18"/>', clock: '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>', play: '<path d="M8 5l11 7-11 7z"/>', pause: '<path d="M8 5v14M16 5v14"/>'
  };
  Object.keys(SI).forEach((k) => { if (!P[k]) P[k] = SI[k]; });
  const ic = (n, cls = "") => `<svg class="ic ${cls}" viewBox="0 0 24 24" aria-hidden="true">${P[n] || ""}</svg>`;
  const waIcon = '<svg class="ic ic-fill" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 00-8.6 15.1L2 22l5-1.3A10 10 0 1012 2zm0 18.2a8.2 8.2 0 01-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1112 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 01-3.3-2.9c-.3-.4.3-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 00-.7.3 3 3 0 00-.9 2.2 5.2 5.2 0 001.1 2.8 11.9 11.9 0 004.6 4c1.7.7 2.4.8 3.2.7a2.8 2.8 0 001.8-1.3 2.3 2.3 0 00.2-1.3c-.1-.1-.2-.2-.4-.3z"/></svg>';

  /* ——— Prix ——— */
  function priceBlock(p, big = false) {
    if (p.price == null) return `<div class="pr${big ? " pr--big" : ""}"><b>Sur devis</b></div>`;
    const d = D.discount(p);
    return `<div class="pr${big ? " pr--big" : ""}"><b>${fmt(p.price)}</b>${p.oldPrice ? `<s>${fmt(p.oldPrice)}</s>` : ""}${big && d ? `<span class="save">${esc(t("Vous économisez {x}", { x: fmt(p.oldPrice - p.price) }))}</span>` : ""}</div>`;
  }

  /* ——— Carte produit ——— */
  function card(p) {
    const d = D.discount(p), fav = Store.isFav(p.id);
    return `<article class="pc" data-id="${p.id}">
      <a class="pc-media" href="${productUrl(p)}" tabindex="-1" aria-label="${esc(p.name)}">${media(p)}</a>
      <div class="pc-badges">${d ? `<span class="b b--red">-${d}%</span>` : ""}${p.isNew ? '<span class="b b--dark">Nouveau</span>' : ""}${p.best && !d ? '<span class="b b--gold">Top vente</span>' : ""}</div>
      <button class="pc-fav js-fav${fav ? " on" : ""}" data-id="${p.id}" aria-pressed="${fav}" aria-label="${esc(t("Favori : {name}", { name: p.name }))}">${ic("heart")}</button>
      <div class="pc-body">
        <span class="pc-brand">${esc(p.brand)}</span>
        <h3 class="pc-name"><a href="${productUrl(p)}">${esc(p.name)}</a></h3>
        ${priceBlock(p)}
      </div>
      <div class="pc-actions">
        ${p.price == null ? `<a class="btn btn--sm btn--line" href="${productUrl(p)}">Demander un devis</a>` : `<button class="btn btn--sm js-add" data-id="${p.id}">${ic("bag")} Ajouter</button>`}
        <button class="pc-cmp js-cmp${Store.inCompare(p.id) ? " on" : ""}" data-id="${p.id}" aria-pressed="${Store.inCompare(p.id)}" aria-label="${esc(t("Comparer {name}", { name: p.name }))}" title="Comparer">${ic("compare")}</button>
      </div></article>`;
  }

  /* ——— En-tête ——— */
  function header(active) {
    const mega = D.categories.map((c) => `<div class="mega-col"><a class="mega-h" href="catalogue.html?cat=${c.id}">${ic(c.icon)} ${esc(c.label)}</a>
        ${c.subs.map((s) => `<a href="catalogue.html?cat=${c.id}&sub=${s.id}">${esc(s.label)}</a>`).join("")}</div>`).join("");
    return `<a class="skip" href="#main">Aller au contenu</a>
    <div class="topbar"><div class="wrap topbar-in">
      <span class="vg-top"><a class="vg-back" data-portal href="index.html">${ic("left")} Ventage Group</a>
        <span class="srswitch"><button class="srs-btn" aria-haspopup="true" aria-expanded="false">${ic("grid")} <span>Nos 12 showrooms</span></button>
          <span class="srs-menu" role="menu">${V.UNIVERS.map((u) => `<span class="srs-g"><small>${esc(tr(VGF(u.label)))}</small>${V.SHOWROOMS.filter((s) => s.u === u.id).map((s) => `<a role="menuitem" class="${s.id === S.id ? "on" : ""}" href="showroom.html?s=${s.id}"><i style="background:${s.c}"></i>${esc(s.name)}</a>`).join("")}</span>`).join("")}</span></span>
        <span class="tb-addr">${ic("pin")} ${esc(C.address)}</span></span>
      <span class="tb-mid">${ic("truck")} ${esc(t("Livraison & installation à {city}", { city: C.city }))}</span>
      <span class="tb-right">${C.pro ? `<a href="contact.html#pro">${ic("building")} Espace Pro</a>` : ""}<a href="tel:${C.phone.replace(/\s/g, "")}">${ic("chat")} ${esc(C.phone)}</a></span>
    </div></div>
    <header class="hdr"><div class="wrap hdr-in">
      <button class="hbtn burger" aria-label="Ouvrir le menu" aria-controls="drawer" aria-expanded="false">${ic("menu")}</button>
      <a class="brand vg-brand" href="showroom.html" aria-label="${esc(C.name)}"><img src="assets/ventage-check.png" alt="" width="40" height="44"><span><b>${esc(C.name)}</b><small>Ventage Group</small></span></a>
      <form class="search" action="catalogue.html" role="search" autocomplete="off"><input type="hidden" name="s" value="${C.id}">
        <label class="sr" for="q-top">Rechercher</label>
        <input id="q-top" name="q" type="search" placeholder="Rechercher un produit, une marque…" aria-autocomplete="list" aria-controls="suggest">
        <button class="search-go" aria-label="Lancer la recherche">${ic("search")}</button>
        <div class="suggest" id="suggest" role="listbox" hidden></div>
      </form>
      <nav class="hdr-tools" aria-label="Mon espace">
        <a class="hbtn" href="catalogue.html?fav=1" aria-label="Mes favoris">${ic("heart")}<span>Favoris</span><i class="badge js-fav-count"></i></a>
        <a class="hbtn" href="panier.html" aria-label="Mon panier">${ic("bag")}<span>Panier</span><i class="badge js-cart-count"></i></a>
        <div class="lang" data-noi18n><button class="hbtn lang-btn" aria-haspopup="true" aria-expanded="false" aria-label="Langue / Language">${ic("globe")}<span>${esc((L.LANGS[L.lang] || {}).short || "FR")}</span></button>
          <div class="lang-menu" role="menu">${Object.entries(L.LANGS).map(([k, v]) => `<button role="menuitem" class="js-lang${k === L.lang ? " on" : ""}" data-l="${k}" lang="${k}">${esc(v.name)}</button>`).join("")}</div></div>
        <a class="btn btn--wa btn--sm hdr-wa" href="${wa("Bonjour SODISCOM-GE, je souhaite parler à un conseiller.")}" target="_blank" rel="noopener">${waIcon} Conseiller</a>
      </nav>
    </div></header>
    <nav class="catnav" aria-label="Catégories"><div class="wrap catnav-in">
      <div class="allcats"><button class="allcats-btn" aria-expanded="false" aria-controls="mega">${ic("menu")} Toutes les catégories</button>
        <div class="mega" id="mega"><div class="mega-grid">${mega}</div>
          <a class="mega-promo" href="catalogue.html?promo=1">${scene(S.photos[1])}<span><small>Offres du moment</small><b>${maxOff() ? esc(t("Jusqu'à -{n} %", { n: maxOff() })) : esc(C.name)}</b><em>Voir les promotions →</em></span></a></div></div>
      <ul class="catlinks">${D.categories.map((c) => `<li><a class="${active === c.id ? "on" : ""}" href="catalogue.html?cat=${c.id}">${ic(c.icon)} ${esc(c.short || c.label)}</a></li>`).join("")}</ul>
      <a class="promo-pill" href="catalogue.html?promo=1">${ic("tag")} Promotions</a>
    </div></nav>
    <div class="drawer" id="drawer" hidden><div class="drawer-panel" role="dialog" aria-label="Menu">
      <div class="drawer-top"><span class="vg-brand vg-brand--dark"><img src="assets/ventage-check.png" alt="" height="30"><span><b>${esc(C.name)}</b><small>Ventage Group</small></span></span><button class="hbtn drawer-close" aria-label="Fermer le menu">${ic("close")}</button></div>
      ${D.categories.map((c) => `<details><summary>${ic(c.icon)} ${esc(c.label)}</summary><a href="catalogue.html?cat=${c.id}">Tout voir</a>${c.subs.map((s) => `<a href="catalogue.html?cat=${c.id}&sub=${s.id}">${esc(s.label)}</a>`).join("")}</details>`).join("")}
      <div class="drawer-langs" data-noi18n>${Object.entries(L.LANGS).map(([k, v]) => `<button class="js-lang${k === L.lang ? " on" : ""}" data-l="${k}" lang="${k}">${esc(v.name)}</button>`).join("")}</div>
      <a class="drawer-link gold" href="catalogue.html?promo=1">${ic("tag")} Promotions</a>
      ${C.pro ? `<a class="drawer-link" href="contact.html#pro">${ic("building")} Espace Pro</a>` : ""}
      <a class="drawer-link" data-portal href="index.html">${ic("left")} Ventage Group · 12 showrooms</a>
      <a class="drawer-link" href="contact.html">${ic("pin")} Showroom & contact</a>
      <a class="btn btn--wa" href="${wa("Bonjour SODISCOM-GE, je souhaite parler à un conseiller.")}" target="_blank" rel="noopener">${waIcon} Parler à un conseiller</a>
    </div></div>`;
  }

  function footer() {
    return `<section class="services"><div class="wrap services-in">
      <div>${ic("truck")}<b>Livraison & installation</b><span>À domicile ou en entreprise, sur rendez-vous</span></div>
      <div>${ic("chat")}<b>Conseil d'expert</b><span>Un conseiller répond sur WhatsApp</span></div>
      <div>${ic("shield")}<b>Prix confirmé avant achat</b><span>Aucun paiement en ligne requis</span></div>
      <div>${ic("building")}<b>Particuliers & pros</b><span>Hôtels, bureaux, résidences : devis sur mesure</span></div>
    </div></section>
    <footer class="ftr"><div class="wrap">
      <div class="ftr-top">
        <div class="ftr-brand"><a data-portal href="index.html"><img src="assets/logo-ventage-w.png" alt="Ventage Group" width="230" height="40" loading="lazy"></a>
          <p><b style="color:#fff;display:block;margin-bottom:4px">${esc(C.name)}</b>${esc(tr(S.desc.split("|")[0]))}</p>
          <a class="btn btn--wa btn--sm" href="${wa("Bonjour SODISCOM-GE !")}" target="_blank" rel="noopener">${waIcon} WhatsApp</a></div>
        <div><b>Rayons</b>${D.categories.map((c) => `<a href="catalogue.html?cat=${c.id}">${esc(c.label)}</a>`).join("")}</div>
        <div><b>Acheter</b><a href="catalogue.html?promo=1">Promotions</a><a href="catalogue.html?sort=new">Nouveautés</a><a href="catalogue.html?fav=1">Mes favoris</a><a href="panier.html">Mon panier</a><a href="contact.html#faq">Comment commander</a></div>
        <div><b>Showroom</b><address>${esc(C.address)}<br>${esc(C.country)}</address><a href="tel:${C.phone.replace(/\s/g, "")}">${esc(C.phone)}</a>${C.email ? `<a href="mailto:${C.email}">${esc(C.email)}</a>` : ""}${C.pro ? '<a href="contact.html#pro">Espace professionnels</a>' : ""}<a data-portal href="index.html">Tous les showrooms Ventage</a></div>
      </div>
      <div class="ftr-bottom"><span>© ${new Date().getFullYear()} ${esc(C.name)}</span>
        <span>Ventage Group · ${esc(C.city)}, ${esc(C.country)}</span></div>
    </div></footer>
    <nav class="tabbar" aria-label="Navigation mobile">
      <a href="showroom.html" data-t="home">${ic("home")}<span>Accueil</span></a>
      <button class="js-open-drawer" data-t="cats">${ic("grid")}<span>Rayons</span></button>
      <button class="js-search-focus" data-t="search">${ic("search")}<span>Rechercher</span></button>
      <a href="panier.html" data-t="cart">${ic("bag")}<span>Panier</span><i class="badge js-cart-count"></i></a>
      <a class="tab-wa" href="${wa("Bonjour SODISCOM-GE, je souhaite parler à un conseiller.")}" target="_blank" rel="noopener">${waIcon}<span>WhatsApp</span></a>
    </nav>
    <a class="wa-float" href="${wa("Bonjour SODISCOM-GE, je souhaite parler à un conseiller.")}" target="_blank" rel="noopener" aria-label="WhatsApp ${esc(C.name)}">${waIcon}<span>Un conseiller</span></a>
    <div class="cmpbar" id="cmpbar" hidden></div>
    <div class="toast" id="toast" role="status" aria-live="polite"></div>
    <dialog class="dlg" id="cmpdlg" aria-label="Comparer"></dialog>`;
  }

  /* ——— Recherche instantanée ——— */
  const norm = (s) => String(s).toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "");
  function searchProducts(q, n = 6) {
    const t = norm(q).split(/\s+/).filter(Boolean);
    if (!t.length) return [];
    return D.products.map((p) => {
      const hay = norm([p.brand, p.name, D.findSub(p.sub).label, D.findCategory(p.category).label].join(" "));
      return { p, ok: t.every((w) => hay.includes(w)), s: t.reduce((a, w) => a + (norm(p.name).includes(w) ? 2 : 0) + (norm(p.brand).startsWith(w) ? 3 : 0), 0) };
    }).filter((x) => x.ok).sort((a, b) => b.s - a.s).slice(0, n).map((x) => x.p);
  }
  function bindSearch() {
    const input = $("#q-top"), box = $("#suggest"); let sel = -1;
    const render = () => {
      const q = input.value.trim(), res = searchProducts(q);
      const cats = q ? D.categories.flatMap((c) => c.subs.map((s) => ({ c, s }))).filter(({ s, c }) => norm(s.label + " " + c.label).includes(norm(q))).slice(0, 3) : [];
      if (!q) { box.hidden = true; return; }
      box.innerHTML = (cats.length ? `<div class="sg-cats">${cats.map(({ c, s }) => `<a href="catalogue.html?cat=${c.id}&sub=${s.id}">${ic("grid")} ${esc(s.label)}</a>`).join("")}</div>` : "") +
        (res.length ? res.map((p) => `<a class="sg-item" role="option" href="${productUrl(p)}"><span class="sg-img">${media(p)}</span><span><small>${esc(p.brand)}</small>${esc(p.name)}</span><b>${p.price ? fmt(p.price) : "Sur devis"}</b></a>`).join("") +
          `<a class="sg-all" href="catalogue.html?q=${encodeURIComponent(q)}">${esc(t("Voir tous les résultats pour « {q} »", { q }))} →</a>`
          : `<p class="sg-empty">${esc(t("Aucun produit pour « {q} ».", { q }))} <a href="${wa(tr("Bonjour, je cherche :") + " " + q)}" target="_blank" rel="noopener">Demander à un conseiller</a></p>`);
      box.hidden = false; sel = -1;
    };
    input.addEventListener("input", render);
    input.addEventListener("focus", render);
    input.addEventListener("keydown", (e) => {
      const items = [...box.querySelectorAll(".sg-item")]; if (!items.length) return;
      if (e.key === "ArrowDown" || e.key === "ArrowUp") { e.preventDefault(); sel = (sel + (e.key === "ArrowDown" ? 1 : -1) + items.length) % items.length; items.forEach((x, i) => x.classList.toggle("on", i === sel)); }
      if (e.key === "Enter" && sel >= 0) { e.preventDefault(); items[sel].click(); }
    });
    document.addEventListener("click", (e) => { if (!e.target.closest(".search")) box.hidden = true; });
  }

  /* ——— Recherche de la colonne gauche (accueil showroom + catalogue) ——— */
  function sideSearch(box, onLive) {
    box.innerHTML = `<form class="ssearch" action="catalogue.html" role="search" autocomplete="off"><input type="hidden" name="s" value="${esc(C.id)}">
      <label class="sr" for="q-side">${esc(tr("Rechercher"))}</label><input id="q-side" name="q" type="search" placeholder="${esc(tr("Rechercher un article…"))}">
      <button aria-label="${esc(tr("Rechercher"))}">${ic("search")}</button></form><div class="ssug" hidden></div>`;
    const f = box.querySelector("form"), i = f.querySelector("#q-side"), sg = box.querySelector(".ssug");
    if (onLive) {
      let tm; i.addEventListener("input", () => { clearTimeout(tm); tm = setTimeout(() => onLive(i.value.trim()), 180); });
      f.addEventListener("submit", (e) => { e.preventDefault(); clearTimeout(tm); onLive(i.value.trim()); });
      return i;
    }
    i.addEventListener("input", () => {
      const q = i.value.trim(), r = searchProducts(q, 5);
      if (!q) { sg.hidden = true; return; }
      sg.innerHTML = r.length ? r.map((p) => `<a href="${productUrl(p)}"><span class="ssug-img">${media(p)}</span><span><small>${esc(p.brand)}</small>${esc(p.name)}</span></a>`).join("") +
        `<a class="ssug-all" href="catalogue.html?q=${encodeURIComponent(q)}">${esc(t("Voir tous les résultats pour « {q} »", { q }))} →</a>`
        : `<p class="ssug-empty">${esc(t("Aucun produit pour « {q} ».", { q }))} <a href="${wa(tr("Bonjour, je cherche :") + " " + q)}" target="_blank" rel="noopener">${esc(tr("Demander à un conseiller"))}</a></p>`;
      sg.hidden = false;
    });
    return i;
  }

  /* ——— Toast, compteurs, comparateur ——— */
  let tt;
  function toast(msg, link) {
    const t = $("#toast"); t.innerHTML = esc(tr(msg)) + (link ? ` <a href="${link.href}">${esc(tr(link.label))}</a>` : "");
    t.classList.add("show"); clearTimeout(tt); tt = setTimeout(() => t.classList.remove("show"), 3200);
  }
  function counts() {
    const n = Store.cartCount(), f = Store.get().favs.length;
    document.querySelectorAll(".js-cart-count").forEach((e) => { e.textContent = n || ""; e.hidden = !n; });
    document.querySelectorAll(".js-fav-count").forEach((e) => { e.textContent = f || ""; e.hidden = !f; });
    document.querySelectorAll(".js-fav").forEach((b) => { const on = Store.isFav(b.dataset.id); b.classList.toggle("on", on); b.setAttribute("aria-pressed", on); });
    document.querySelectorAll(".js-cmp").forEach((b) => { const on = Store.inCompare(b.dataset.id); b.classList.toggle("on", on); b.setAttribute("aria-pressed", on); });
    const bar = $("#cmpbar"), ids = Store.get().compare; if (!bar) return;
    bar.hidden = !ids.length;
    if (ids.length) bar.innerHTML = `<div class="wrap cmpbar-in"><div class="cmp-thumbs">${ids.map((id) => { const p = D.findProduct(id); return `<span>${media(p)}</span>`; }).join("")}</div>
      <span><b>${ids.length}/3</b> produits à comparer</span><button class="btn btn--sm js-cmp-open" ${ids.length < 2 ? "disabled" : ""}>Comparer</button><button class="linkbtn js-cmp-clear">Vider</button></div>`;
  }
  function compareDialog() {
    const dlg = $("#cmpdlg"), ps = Store.get().compare.map(D.findProduct), keys = [...new Set(ps.flatMap((p) => Object.keys(p.specs)))];
    const row = (l, f) => `<tr><th scope="row">${l}</th>${ps.map((p) => `<td>${f(p)}</td>`).join("")}</tr>`;
    dlg.innerHTML = `<div class="dlg-head"><h2>Comparer</h2><button class="hbtn js-dlg-close" aria-label="Fermer">${ic("close")}</button></div><div class="tscroll"><table class="cmp"><thead><tr><td></td>${ps.map((p) => `<th scope="col"><span class="cmp-img">${media(p)}</span><small>${esc(p.brand)}</small><a href="${productUrl(p)}">${esc(p.name)}</a></th>`).join("")}</tr></thead><tbody>
      ${row("Prix", (p) => priceBlock(p))}${keys.map((k) => row(esc(k), (p) => esc(p.specs[k] || "—"))).join("")}${row("", (p) => p.price ? `<button class="btn btn--sm js-add" data-id="${p.id}">Ajouter</button>` : "")}</tbody></table></div>`;
    dlg.showModal();
  }

  /* ——— Événements globaux ——— */
  const openDrawer = () => { $("#drawer").hidden = false; document.body.style.overflow = "hidden"; const b = $(".burger"); if (b) b.setAttribute("aria-expanded", "true"); };
  const closeDrawer = () => { const d = $("#drawer"); if (d) d.hidden = true; document.body.style.overflow = ""; const b = $(".burger"); if (b) b.setAttribute("aria-expanded", "false"); };
  document.addEventListener("click", (e) => {
    if (e.target.id === "drawer") return closeDrawer();
    if (e.target.id === "cmpdlg") return e.target.close();
    const t = e.target.closest("button, a"); if (!t || !t.closest(".lang")) { const lm = $(".lang.open"); if (lm) lm.classList.remove("open"); } if (!t) { const m = $(".allcats.open"); if (m && !e.target.closest(".allcats")) m.classList.remove("open"); return; }
    const c = t.classList;
    if (c.contains("js-add")) { Store.addToCart(t.dataset.id); toast(L.t("{name} ajouté au panier.", { name: D.findProduct(t.dataset.id).name }), { href: "panier.html", label: "Voir le panier" }); t.classList.add("pop"); setTimeout(() => t.classList.remove("pop"), 500); }
    else if (c.contains("js-fav")) toast(Store.toggleFav(t.dataset.id) ? "Ajouté aux favoris." : "Retiré des favoris.");
    else if (c.contains("js-cmp")) { if (!Store.toggleCompare(t.dataset.id)) toast("3 produits maximum dans le comparateur."); }
    else if (c.contains("js-cmp-clear")) Store.clearCompare();
    else if (c.contains("js-cmp-open")) compareDialog();
    else if (c.contains("js-dlg-close")) t.closest("dialog").close();
    else if (c.contains("burger") || c.contains("js-open-drawer")) openDrawer();
    else if (c.contains("drawer-close")) closeDrawer();
    else if (c.contains("js-search-focus")) { scrollTo({ top: 0, behavior: "smooth" }); setTimeout(() => $("#q-top").focus(), 250); }
    else if (c.contains("js-lang")) L.setLang && L.setLang(t.dataset.l);
    else if (c.contains("lang-btn")) { const m = t.parentElement; m.classList.toggle("open"); t.setAttribute("aria-expanded", m.classList.contains("open")); }
    else if (c.contains("srs-btn")) { const m = t.parentElement; m.classList.toggle("open"); t.setAttribute("aria-expanded", m.classList.contains("open")); }
    else if (c.contains("allcats-btn")) { const m = t.parentElement; m.classList.toggle("open"); t.setAttribute("aria-expanded", m.classList.contains("open")); }
  });
  document.addEventListener("keydown", (e) => { if (e.key === "Escape") { closeDrawer(); const s = $("#suggest"); if (s) s.hidden = true; const m = $(".allcats.open"); if (m) m.classList.remove("open"); } });
  document.addEventListener("store:change", counts);

  function reveal() {
    const els = document.querySelectorAll("[data-reveal]:not(.in)");
    if (!("IntersectionObserver" in window) || matchMedia("(prefers-reduced-motion: reduce)").matches) { els.forEach((e) => e.classList.add("in")); return; }
    const io = new IntersectionObserver((es) => es.forEach((en) => { if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); } }), { rootMargin: "0px 0px -6% 0px" });
    els.forEach((e) => io.observe(e));
  }

  function maxOff() { return Math.max(0, ...D.products.map(D.discount)); }
  /* Liens internes : gardent le showroom courant (?s=…) ; index.html = portail du groupe */
  function fixA(a) {
    const h = a.getAttribute("href"); if (!h || a.hasAttribute("data-portal")) return;
    const m = /^([\w-]+\.html)(\?[^#]*)?(#.*)?$/.exec(h); if (!m || m[1] === "index.html") return;
    const q = new URLSearchParams((m[2] || "").slice(1)); if (q.has("s")) return;
    const rest = q.toString(); a.setAttribute("href", `${m[1]}?s=${C.id}${rest ? "&" + rest : ""}${m[3] || ""}`);
  }
  const fixAll = (r) => { if (r.nodeType !== 1) return; if (r.matches("a[href]")) fixA(r); r.querySelectorAll("a[href]").forEach(fixA); };
  const url = (h) => { const a = document.createElement("a"); a.setAttribute("href", h); fixA(a); return a.getAttribute("href"); };
  fixAll(document.body);
  new MutationObserver((ms) => ms.forEach((m) => m.type === "attributes" ? fixA(m.target) : m.addedNodes.forEach(fixAll))).observe(document.body, { childList: true, subtree: true, attributes: true, attributeFilter: ["href"] });
  document.addEventListener("click", (e) => { if (!e.target.closest(".srswitch")) { const s = document.querySelector(".srswitch.open"); if (s) s.classList.remove("open"); } });

  function mount(active) {
    $("#site-header").outerHTML = header(active);
    $("#site-footer").outerHTML = footer();
    const tab = { home: "home", cart: "cart" }[document.body.dataset.page]; if (tab) { const el = document.querySelector(`.tabbar [data-t="${tab}"]`); if (el) el.classList.add("on"); }
    const h = $(".hdr"), fl = $(".wa-float");
    const onScroll = () => { h.classList.toggle("scrolled", scrollY > 40); fl.classList.toggle("is-hidden", scrollY < 500); };
    addEventListener("scroll", onScroll, { passive: true }); onScroll();
    bindSearch(); counts(); reveal();
  }

  window.SODISCOM_UI = { vm, url, maxOff, remote, opt, rimg, djN, djUrl, t, tr, src, mount, card, media, pimg, scene, studio, ic, waIcon, wa, esc, fmt, priceBlock, productUrl, toast, reveal, searchProducts, sideSearch, norm };
})();
