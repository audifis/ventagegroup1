/* Showroom courant (?s=…) et configuration commerciale.
   Les coordonnées propres à chaque showroom se règlent dans js/catalog.js (champs whatsapp, phone, hours, address). */
(function () {
  const V = window.VENTAGE, G = V.GROUP;
  let sid = new URLSearchParams(location.search).get("s");
  try { if (!sid) sid = sessionStorage.getItem("vg-s"); } catch (e) {}
  const S = V.SHOWROOMS.find((x) => x.id === sid);
  if (!S) { location.replace("index.html"); throw new Error("showroom inconnu"); }
  try { sessionStorage.setItem("vg-s", S.id); } catch (e) {}
  const tr0 = (s) => String(s).split("|")[0];
  window.VG_SHOWROOM = S;
  window.SODISCOM_CONFIG = {
    id: S.id, name: S.name, pro: !!S.pro, color: S.c,
    city: G.city, country: G.country,
    address: S.address || (S.area ? S.area + ", " + G.city : G.city),
    phone: S.phone || G.phone, whatsapp: S.whatsapp || G.whatsapp, email: S.email || null,
    hours: S.hours || null, currency: "XAF",
    delivery: { fee: null, note: "Frais et délais de livraison confirmés par un conseiller selon votre adresse." },
    payment: { online: false, provider: null },
    features: { newArrivals: true, promotions: true, compare: true, favorites: true },
    api: { baseUrl: null },
    tag: tr0(S.tag)
  };
  /* Couleur du showroom : remplace le rouge d'origine du thème */
  const r = document.documentElement.style;
  r.setProperty("--red", S.c);
  r.setProperty("--red-d", "color-mix(in srgb, " + S.c + " 78%, #000)");
})();
