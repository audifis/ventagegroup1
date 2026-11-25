(function () {
  const U = SODISCOM_UI, D = SODISCOM_DATA, $ = (s) => document.querySelector(s), t = U.t, tr = U.tr;
  const P = new URLSearchParams(location.search);
  const st = {
    cat: P.get("cat") || "", sub: P.get("sub") || "", q: P.get("q") || "", fav: P.get("fav") === "1", promo: P.get("promo") === "1",
    brands: (P.get("brand") || "").split(",").filter(Boolean), min: +P.get("min") || "", max: +P.get("max") || "", sort: P.get("sort") || "pertinence"
  };
  U.mount(st.cat);

  const SORTS = [["pertinence", "Pertinence"], ["best", "Meilleures ventes"], ["new", "Nouveautés"], ["price-asc", "Prix croissant"], ["price-desc", "Prix décroissant"], ["promo", "Meilleures remises"]];
  $("#sort").innerHTML = SORTS.map(([v, l]) => `<option value="${v}"${v === st.sort ? " selected" : ""}>${l}</option>`).join("");

  const base = () => D.products.filter((p) => (!st.cat || p.category === st.cat) && (!st.sub || p.sub === st.sub));
  function list() {
    const t = st.q ? U.searchProducts(st.q, 999).map((p) => p.id) : null;
    let l = base().filter((p) =>
      (!t || t.includes(p.id)) && (!st.fav || Store.isFav(p.id)) && (!st.promo || p.oldPrice) &&
      (!st.brands.length || st.brands.includes(p.brand)) &&
      (!st.min || (p.price ?? 0) >= st.min) && (!st.max || (p.price ?? Infinity) <= st.max));
    const pr = (p) => p.price ?? Infinity;
    if (st.sort === "pertinence") l.sort((a, b) => (b.img ? (/^dj:/.test(b.img) ? 1 : 2) : 0) - (a.img ? (/^dj:/.test(a.img) ? 1 : 2) : 0));
    if (st.sort === "best") l.sort((a, b) => b.best - a.best);
    if (st.sort === "new") l.sort((a, b) => b.isNew - a.isNew);
    if (st.sort === "price-asc") l.sort((a, b) => pr(a) - pr(b));
    if (st.sort === "price-desc") l.sort((a, b) => (b.price ?? -1) - (a.price ?? -1));
    if (st.sort === "promo") l.sort((a, b) => D.discount(b) - D.discount(a));
    return l;
  }

  function filters() {
    const n = (f) => D.products.filter(f).length;
    const link = (label, q, on, c, cls = "") => `<a class="${cls}${on ? " on" : ""}" href="catalogue.html${q}">${label}<small>${c}</small></a>`;
    const brandsHere = [...new Set(base().map((p) => p.brand))].sort();
    $("#fpanel-in").innerHTML = `
      <div class="fpanel-close"><b style="font-size:20px">Filtres</b><button class="btn btn--sm btn--dark js-fclose">${t("Voir {n} résultats", { n: list().length })}</button></div>
      <div class="fbox"><h3>Rayons</h3>${link("Tout le catalogue", "", !st.cat, D.products.length)}
        ${D.categories.map((c) => link(`<span class="fcat">${U.ic(c.icon)}${U.esc(c.label)}</span>`, `?cat=${c.id}`, st.cat === c.id && !st.sub, n((p) => p.category === c.id)) +
          (st.cat === c.id ? c.subs.map((s) => link(U.esc(s.label), `?cat=${c.id}&sub=${s.id}`, st.sub === s.id, n((p) => p.sub === s.id), "sub")).join("") : "")).join("")}</div>
      <div class="fbox"><h3>Offres</h3><label class="toggle"><input type="checkbox" id="f-promo" ${st.promo ? "checked" : ""}><span>En promotion</span><small>${base().filter((p) => p.oldPrice).length}</small></label>
        <label class="toggle"><input type="checkbox" id="f-fav" ${st.fav ? "checked" : ""}><span>Mes favoris</span><small>${Store.get().favs.length}</small></label></div>
      <div class="fbox"><h3>Prix (FCFA)</h3><div class="price-in"><input id="f-min" type="number" inputmode="numeric" placeholder="Min" value="${st.min || ""}" aria-label="Prix minimum"><input id="f-max" type="number" inputmode="numeric" placeholder="Max" value="${st.max || ""}" aria-label="Prix maximum"></div></div>
      <div class="fbox"><h3>Marques</h3>${brandsHere.map((b) => `<label><input type="checkbox" class="f-brand" value="${U.esc(b)}" ${st.brands.includes(b) ? "checked" : ""}><span>${U.esc(b)}</span><small>${base().filter((p) => p.brand === b).length}</small></label>`).join("")}</div>`;
  }

  function head() {
    const c = D.findCategory(st.cat), s = st.sub && D.findSub(st.sub);
    const title = st.fav ? tr("Mes favoris") : st.promo && !c ? tr("Promotions") : s ? s.label : c ? c.label : st.q ? t("Résultats pour « {q} »", { q: st.q }) : tr("Toute la boutique");
    $("#ttl").textContent = title; document.title = `${title} — ${SODISCOM_CONFIG.name}`;
    $("#crumbs").innerHTML = `<a href="showroom.html">Accueil</a><a href="catalogue.html"><span>Boutique</span></a>` + (c ? `<a href="catalogue.html?cat=${c.id}"><span>${U.esc(c.label)}</span></a>` : "") + (s ? `<span>${U.esc(s.label)}</span>` : "");
    $("#catbanner").innerHTML = c ? `<div class="catbanner">${U.scene(c.scene, "")}<div><b>${U.esc(s ? s.label : c.label)}</b><span>${U.esc(t("{n} articles · conseil et livraison à Malabo", { n: D.products.filter((p) => p.category === c.id).length }))}</span></div></div>` : "";
  }

  function render() {
    const l = list();
    $("#count").textContent = t(l.length > 1 ? "{n} articles" : "{n} article", { n: l.length });
    const chips = [
      ...st.brands.map((b) => [b, () => (st.brands = st.brands.filter((x) => x !== b))]),
      st.promo && ["En promotion", () => (st.promo = false)], st.fav && ["Favoris", () => (st.fav = false)],
      st.min && [t("Min {v}", { v: U.fmt(st.min) }), () => (st.min = "")], st.max && [t("Max {v}", { v: U.fmt(st.max) }), () => (st.max = "")],
      st.q && [`« ${st.q} »`, () => (st.q = "")]
    ].filter(Boolean);
    $("#chips").innerHTML = chips.map(([l], i) => `<span class="chip">${U.esc(l)}<button data-i="${i}" aria-label="${U.esc(t("Retirer le filtre {f}", { f: l }))}">×</button></span>`).join("");
    $("#chips").querySelectorAll("button").forEach((b) => (b.onclick = () => { chips[+b.dataset.i][1](); update(); }));
    $("#results").innerHTML = l.length ? l.map(U.card).join("") : `<div class="empty" style="grid-column:1/-1"><h2 class="h2">${st.fav ? "Aucun favori" : "Aucun résultat"}</h2>
      <p class="lead">${st.fav ? "Touchez le cœur d'un produit pour le retrouver ici." : "Modifiez vos filtres, ou demandez directement à un conseiller : nos arrivages changent souvent."}</p>
      <a class="btn" href="catalogue.html">Toute la boutique</a></div>`;
  }

  function sync() {
    const p = new URLSearchParams();
    if (st.cat) p.set("cat", st.cat); if (st.sub) p.set("sub", st.sub); if (st.q) p.set("q", st.q);
    if (st.fav) p.set("fav", "1"); if (st.promo) p.set("promo", "1"); if (st.brands.length) p.set("brand", st.brands.join(","));
    if (st.min) p.set("min", st.min); if (st.max) p.set("max", st.max); if (st.sort !== "pertinence") p.set("sort", st.sort);
    history.replaceState(null, "", U.url("catalogue.html" + (p.toString() ? "?" + p : "")));
  }
  function update() {
    filters(); head(); render(); sync();
    const qs = $("#q-side"); if (qs && document.activeElement !== qs) qs.value = st.q;
    const qt = $("#q-top"); if (qt && document.activeElement !== qt) qt.value = st.q;
  }
  U.sideSearch($("#fsearch"), (q) => { st.q = q; update(); });

  $("#fpanel").addEventListener("change", (e) => {
    const t = e.target;
    if (t.id === "f-promo") st.promo = t.checked;
    else if (t.id === "f-fav") st.fav = t.checked;
    else if (t.classList.contains("f-brand")) st.brands = [...document.querySelectorAll(".f-brand:checked")].map((x) => x.value);
    else if (t.id === "f-min") st.min = +t.value || "";
    else if (t.id === "f-max") st.max = +t.value || "";
    update();
  });
  $("#fsearch").insertAdjacentHTML("beforebegin", `<div class="sp-head"><b>${U.esc(tr("Rayons & filtres"))}</b><button class="sp-x js-spclose" type="button" aria-label="${U.esc(tr("Fermer"))}">${U.ic("close")}</button></div>`);
  const sp = U.sidePanel($("#fpanel"));
  $("#fpanel").addEventListener("click", (e) => { if (e.target.closest(".js-fclose")) sp.close(); });
  $("#ftoggle").addEventListener("click", sp.open);
  U.catChips($("#srbar"), st.cat);
  $("#sort").addEventListener("change", (e) => { st.sort = e.target.value; render(); sync(); });
  const qt = $("#q-top"); if (qt) qt.value = st.q;
  document.addEventListener("store:change", () => { if (st.fav) render(); });
  update();
})();
