(function () {
  const U = SODISCOM_UI, D = SODISCOM_DATA, C = SODISCOM_CONFIG, $ = (s) => document.querySelector(s), t = U.t;
  const p = D.findProduct(new URLSearchParams(location.search).get("id"));
  U.mount(p ? p.category : "");
  const root = $("#pdp");
  if (!p) {
    root.innerHTML = `<section class="sec"><div class="empty"><h1 class="h2">Produit introuvable</h1><p class="lead">Ce produit n'est plus en ligne ou le lien est incorrect.</p><a class="btn" href="catalogue.html">Voir la boutique</a></div></section>`;
    $("#related-wrap").remove(); return;
  }
  const c = D.findCategory(p.category), s = D.findSub(p.sub), d = D.discount(p);
  document.title = `${p.brand} ${p.name} — ${C.name}`;
  document.querySelector('meta[name="description"]').content = `${p.brand} ${t("{name} chez SODISCOM-GE à Malabo.", { name: p.name })} ${p.highlights.join(", ")}.`;

  // Galerie : photo produit + photos d'ambiance du même univers
  const n = U.djN(p.img);
  const views = n > 1 ? Array.from({ length: n }, (_, i) => ({ u: U.djUrl(p.img, i + 1) })) : [/^us:/.test(p.img || "") ? { u: U.remote(p.img) } : p.img ? { k: p.img } : { svg: p.svg }, { scene: c.scene }];
  const view = (v, cls = "") => v.u ? U.rimg(v.u, p.name, cls, true, [640, 1200], "(max-width:900px) 100vw, 50vw") : v.k ? U.pimg(v.k, p.name, cls, true) : v.svg ? U.studio(v.svg) : U.scene(v.scene, "", false, "(max-width:900px) 100vw, 50vw");
  const msg = (q) => t("Bonjour SODISCOM-GE, je suis intéressé(e) par : {p} (réf. {ref}){q}. Pouvez-vous me confirmer la disponibilité et la livraison ?", { p: `${p.brand} ${p.name}`, ref: p.ref, q: q > 1 ? t(", quantité {n}", { n: q }) : "" });

  root.innerHTML = `
    <nav class="crumbs crumbs--light" aria-label="Fil d'Ariane" style="padding-top:22px"><a href="showroom.html">Accueil</a><a href="catalogue.html?cat=${c.id}"><span>${U.esc(c.label)}</span></a><a href="catalogue.html?cat=${c.id}&sub=${s.id}"><span>${U.esc(s.label)}</span></a><span>${U.esc(p.name)}</span></nav>
    <div class="pdp">
      <div class="gallery">
        <div class="gal-main" id="gmain">${view(views[0])}</div>
        <div class="thumbs" role="group" aria-label="Vues">${views.map((v, i) => `<button class="${i ? "" : "on"}" data-i="${i}" aria-label="Vue ${i + 1}">${view(v)}</button>`).join("")}</div>
      </div>
      <div class="pinfo">
        <span class="pc-brand">${U.esc(p.brand)}</span>
        <h1>${U.esc(p.name)}</h1>
        <span class="pref">${U.esc(t("Réf. {ref}", { ref: p.ref }))} · ${U.esc(s.label)}</span>
        <div class="pbadges">${d ? `<span class="b b--red">-${d}%</span>` : ""}${p.isNew ? '<span class="b b--dark">Nouveau</span>' : ""}${p.best ? '<span class="b b--gold">Top vente</span>' : ""}</div>
        <div class="pbox">
          ${U.priceBlock(p, true)}
          <ul class="hl" style="margin-top:18px">${p.highlights.map((h) => `<li>${U.esc(h)}</li>`).join("")}</ul>
          <div class="buy">
            ${p.price != null || U.CARTNP ? `<div class="qty"><button type="button" data-d="-1" aria-label="Moins">−</button><input id="qty" type="number" min="1" max="99" value="1" aria-label="Quantité"><button type="button" data-d="1" aria-label="Plus">+</button></div>
            <button class="btn btn--lg" id="add">${U.ic("bag")} Ajouter au panier</button>` : ""}
            <a class="btn btn--wa btn--lg" id="ask" href="${U.wa(msg(1))}" target="_blank" rel="noopener">${U.waIcon} ${C.id === "amanda-labs" ? "Prendre rendez-vous" : p.price == null && !U.CARTNP ? "Demander un devis" : "Commander sur WhatsApp"}</a>
          </div>
          <div class="ptools"><button class="js-fav" data-id="${p.id}" aria-pressed="false">${U.ic("heart")} Favori</button><button class="js-cmp" data-id="${p.id}" aria-pressed="false">${U.ic("compare")} Comparer</button></div>
        </div>
        <div class="perks"><div>${U.ic("truck")} ${U.esc(t("Livraison & installation à {city}, sur rendez-vous", { city: C.city }))}</div><div>${U.ic("shield")} Prix et disponibilité confirmés avant tout paiement</div><div>${U.ic("pin")} ${U.esc(t("À voir au showroom : {address}", { address: C.address }))}</div></div>
        <div class="acc">
          <details open><summary>Caractéristiques</summary><div class="acc-b">${Object.keys(p.specs).length ? `<table class="specs"><tbody>${Object.entries(p.specs).map(([k, v]) => `<tr><th scope="row">${U.esc(k)}</th><td>${U.esc(v)}</td></tr>`).join("")}<tr><th scope="row">Marque</th><td>${U.esc(p.brand)}</td></tr></tbody></table>` : "Fiche technique transmise par un conseiller."}</div></details>
          <details><summary>Livraison & retrait</summary><div class="acc-b">${U.esc(C.delivery.note)} ${U.esc(t("Retrait possible au showroom, {address}.", { address: C.address }))}</div></details>
          <details><summary>Paiement</summary><div class="acc-b">Pas de paiement en ligne : votre commande est confirmée par un conseiller, qui vous indique les modalités de règlement.</div></details>
        </div>
      </div>
    </div>`;

  const qty = $("#qty");
  if (qty) {
    const cl = () => Math.max(1, Math.min(99, parseInt(qty.value, 10) || 1));
    const upd = () => { qty.value = cl(); $("#ask").href = U.wa(msg(cl())); };
    root.querySelectorAll(".qty button").forEach((b) => b.addEventListener("click", () => { qty.value = cl() + +b.dataset.d; upd(); }));
    qty.addEventListener("change", upd);
    $("#add").addEventListener("click", (e) => { Store.addToCart(p.id, cl()); U.toast(t("{name} ajouté au panier.", { name: p.name }), { href: "panier.html", label: "Voir le panier" }); e.currentTarget.classList.add("pop"); });
  }
  root.querySelectorAll(".thumbs button").forEach((b) => b.addEventListener("click", () => {
    root.querySelectorAll(".thumbs button").forEach((x) => x.classList.remove("on")); b.classList.add("on");
    $("#gmain").innerHTML = view(views[+b.dataset.i]);
  }));
  // zoom au survol (ordinateur)
  const gm = $("#gmain");
  if (matchMedia("(hover:hover)").matches) {
    gm.addEventListener("mousemove", (e) => { const r = gm.getBoundingClientRect(), img = gm.querySelector("img"); if (!img) return; img.style.transformOrigin = `${((e.clientX - r.left) / r.width) * 100}% ${((e.clientY - r.top) / r.height) * 100}%`; gm.classList.add("zoom"); });
    gm.addEventListener("mouseleave", () => gm.classList.remove("zoom"));
  }
  document.dispatchEvent(new CustomEvent("store:change"));

  const rel = D.products.filter((x) => x.id !== p.id && x.sub === p.sub).concat(D.products.filter((x) => x.id !== p.id && x.sub !== p.sub && x.category === p.category)).concat(D.products.filter((x) => x.category !== p.category && x.best)).slice(0, 10);
  $("#related").innerHTML = rel.map(U.card).join("");
  document.querySelectorAll(".rail-wrap").forEach((w) => w.querySelectorAll(".rail-btn").forEach((b) => b.addEventListener("click", () => { const r = w.querySelector(".rail"); r.scrollBy({ left: (b.classList.contains("next") ? 1 : -1) * (window.I18N && I18N.rtl ? -1 : 1) * r.clientWidth * 0.85, behavior: "smooth" }); })));

  const ld = document.createElement("script"); ld.type = "application/ld+json";
  ld.textContent = JSON.stringify({ "@context": "https://schema.org", "@type": "Product", name: p.name, sku: p.ref, brand: { "@type": "Brand", name: p.brand }, description: p.highlights.join(". "), ...(p.img ? { image: (U.vm(p.img) ? new URL(`assets/mall/${U.vm(p.img)}.webp`, location.href).href : null) || U.remote(p.img) || new URL(`assets/img/${p.img}-640.webp`, location.href).href } : {}), ...(p.price ? { offers: { "@type": "Offer", priceCurrency: "XAF", price: p.price } } : {}) });
  document.head.append(ld);
})();
