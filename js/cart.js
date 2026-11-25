/* Panier / « Ma demande » : quantités, récapitulatif, coordonnées, envoi de la commande à un conseiller via WhatsApp.
   Aucun paiement n'est simulé. Point d'extension : remplacer submitOrder() par un appel API + prestataire de paiement. */
(function () {
  const U = SODISCOM_UI, D = SODISCOM_DATA, C = SODISCOM_CONFIG, $ = (s) => document.querySelector(s), t = U.t, tr = U.tr;
  U.mount("cart");
  const root = $("#cartroot");
  let draft = {};
  try { draft = JSON.parse(sessionStorage.getItem("ventage:draft") || "{}"); } catch (e) {}

  const fmt = U.fmt;

  function render(confirmation) {
    const lines = Store.get().cart.map((l) => ({ ...l, p: D.findProduct(l.id) }));
    if (confirmation) {
      root.innerHTML = `<section class="sec"><div class="empty"><span class="eyebrow">${U.esc(t("Demande n° {id}", { id: confirmation.id }))}</span>
        <h2 class="h2" style="margin:14px 0">Merci, <em>c'est envoyé.</em></h2>
        <p class="lead" style="margin:0 auto 22px">WhatsApp s'est ouvert avec votre demande. Si ce n'est pas le cas, utilisez le bouton ci-dessous. Un conseiller SODISCOM vous confirmera prix, disponibilité et livraison.</p>
        <div class="row" style="justify-content:center"><a class="btn btn--wa" href="${confirmation.url}" target="_blank" rel="noopener">${U.waIcon} Renvoyer sur WhatsApp</a><a class="btn btn--ghost" href="catalogue.html">Continuer mes achats</a></div></div></section>`;
      return;
    }
    if (!lines.length) {
      root.innerHTML = `<section class="sec"><div class="empty"><h2 class="h2">Votre demande est vide</h2>
        <p class="lead" style="margin:12px auto 22px">Parcourez nos univers et ajoutez les produits qui vous intéressent.</p>
        <a class="btn" href="catalogue.html">Découvrir le catalogue</a></div></section>${history()}`;
      return;
    }
    const known = lines.filter((l) => l.p.price != null);
    const subtotal = known.reduce((n, l) => n + l.p.price * l.qty, 0);
    const count = Store.cartCount();

    root.innerHTML = `<div class="cart">
      <div><h2 class="sr">Produits</h2>
        ${lines.map((l) => `<div class="line">
          <a class="line-media" href="${U.productUrl(l.p)}" aria-label="${U.esc(l.p.name)}" tabindex="-1">${U.media(l.p)}</a>
          <div><span class="eyebrow">${U.esc(D.findSub(l.p.sub).label)}</span><h3><a href="${U.productUrl(l.p)}">${U.esc(l.p.name)}</a></h3>
            <span class="note">${U.esc(t("Réf. {ref}", { ref: l.p.ref }))}${l.variant ? " · " + U.esc(l.variant) : ""}</span><br>${U.priceBlock(l.p)}</div>
          <div class="line-actions">
            <div class="qty"><button type="button" data-id="${l.id}" data-v="${U.esc(l.variant || "")}" data-d="-1" aria-label="Diminuer">−</button>
              <input value="${l.qty}" readonly aria-label="${U.esc(t("Quantité {name}", { name: l.p.name }))}"><button type="button" data-id="${l.id}" data-v="${U.esc(l.variant || "")}" data-d="1" aria-label="Augmenter">+</button></div>
            <button class="linkbtn js-rm" data-id="${l.id}" data-v="${U.esc(l.variant || "")}">Retirer</button></div></div>`).join("")}
        <div class="row" style="justify-content:space-between;margin-top:20px"><a class="linkbtn" href="catalogue.html">← Continuer mes achats</a><button class="linkbtn js-clear">Vider la demande</button></div>
      </div>

      <aside class="summary" aria-labelledby="sumtitle">
        <h2 id="sumtitle">Récapitulatif</h2>
        <div class="sumrow"><span>Articles</span><b>${count}</b></div>
        <div class="sumrow"><span>Sous-total</span><b>${known.length === lines.length ? fmt(subtotal) : known.length ? fmt(subtotal) + " + " + tr("prix sur demande") : "Prix sur demande"}</b></div>
        <div class="sumrow"><span>Livraison</span><b>${C.delivery.fee != null ? fmt(C.delivery.fee) : "À confirmer"}</b></div>
        <p class="info" style="margin-top:16px">Commande accompagnée : votre demande est envoyée à un conseiller sur WhatsApp. <b>Aucun paiement en ligne</b> — rien n'est débité.</p>

        <form class="form" id="orderform" novalidate>
          <div class="field"><label for="f-name">Nom complet</label><input id="f-name" name="name" autocomplete="name" required><span class="err">Indiquez votre nom.</span></div>
          <div class="field"><label for="f-phone">Téléphone / WhatsApp</label><input id="f-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" placeholder="+240 …" required pattern="[+0-9 ]{8,}"><span class="err">Numéro invalide.</span></div>
          <div class="field"><label for="f-mode">Réception</label><select id="f-mode" name="mode"><option value="livraison">Livraison à mon adresse</option><option value="retrait">Retrait au showroom</option></select></div>
          <div class="field" id="addrfield"><label for="f-addr">Adresse de livraison</label><textarea id="f-addr" name="address" autocomplete="street-address" placeholder="Quartier, rue, repère, ville"></textarea><span class="err">Indiquez une adresse de livraison.</span></div>
          <div class="field"><label for="f-note">Message (facultatif)</label><textarea id="f-note" name="note" placeholder="Couleur souhaitée, étage, horaires…"></textarea></div>
          <button class="btn btn--wa" type="submit">${U.waIcon} Envoyer ma demande</button>
          <p class="note" style="margin:0">En envoyant, vous ouvrez WhatsApp avec le détail de votre demande. Vous pourrez le relire avant l'envoi.</p>
        </form>
      </aside></div>${history()}`;

    const form = $("#orderform");
    for (const [k, v] of Object.entries(draft)) if (form.elements[k]) form.elements[k].value = v;
    const toggleAddr = () => { $("#addrfield").hidden = form.elements.mode.value !== "livraison"; };
    toggleAddr();
    form.addEventListener("input", (e) => { const f = e.target.closest(".field"); if (f) f.classList.remove("invalid"); draft = Object.fromEntries(new FormData(form)); try { sessionStorage.setItem("ventage:draft", JSON.stringify(draft)); } catch (e) {} });
    form.elements.mode.addEventListener("change", toggleAddr);
    form.addEventListener("submit", (e) => { e.preventDefault(); submitOrder(form, lines); });
  }

  function history() {
    const o = Store.get().orders; if (!o.length) return "";
    return `<section class="orders wrap" style="padding:0 0 80px;width:auto"><span class="eyebrow">Sur cet appareil</span><h2 class="h2" style="font-size:34px;margin:10px 0 12px">Mes demandes envoyées</h2><ul style="list-style:none;padding:0;margin:0">
      ${o.map((x) => `<li><b>${U.esc(x.id)}</b> · ${new Date(x.date).toLocaleDateString(window.I18N ? I18N.meta.loc : "fr-FR")} · ${t("{n} article(s)", { n: x.items.reduce((n, i) => n + i.qty, 0) })} — ${U.esc(x.items.map((i) => i.name).join(", "))}</li>`).join("")}</ul></section>`;
  }

  function submitOrder(form, lines) {
    let ok = true;
    const check = (name, valid) => { const f = form.elements[name].closest(".field"); f.classList.toggle("invalid", !valid); if (!valid && ok) form.elements[name].focus(); ok = ok && valid; };
    const v = Object.fromEntries(new FormData(form));
    check("name", v.name.trim().length > 1);
    check("phone", /^[+0-9 ]{8,}$/.test(v.phone.trim()));
    if (v.mode === "livraison") check("address", v.address.trim().length > 4);
    if (!ok) return;

    const id = "VG-" + Date.now().toString(36).toUpperCase().slice(-6);
    const sep = window.I18N && I18N.lang !== "fr" ? ": " : " : ";
    const items = lines.map((l) => ({ id: l.id, name: l.p.name, ref: l.p.ref, qty: l.qty, variant: l.variant }));
    const text = [
      t("Bonjour SODISCOM-GE, voici ma demande de commande ({id}) :", { id }), "",
      ...items.map((i) => `• ${i.qty} × ${i.name} (${tr("réf.")} ${i.ref})${i.variant ? " — " + i.variant : ""}`), "",
      `${tr("Nom")}${sep}${v.name.trim()}`, `${tr("Téléphone")}${sep}${v.phone.trim()}`,
      v.mode === "livraison" ? `${tr("Livraison")}${sep}${v.address.trim()}` : tr("Retrait au showroom"),
      v.note.trim() ? `${tr("Message")}${sep}${v.note.trim()}` : "", "",
      tr("Merci de me confirmer le modèle disponible, le prix total et les frais de livraison.")
    ].filter((x, i, a) => x !== "" || a[i - 1] !== "").join("\n");
    const url = U.wa(text);

    Store.addOrder({ id, date: new Date().toISOString(), items, mode: v.mode });
    Store.clearCart();
    try { sessionStorage.removeItem("ventage:draft"); } catch (e) {}
    window.open(url, "_blank", "noopener");
    render({ id, url });
    scrollTo({ top: 0, behavior: "smooth" });
  }

  root.addEventListener("click", (e) => {
    const b = e.target.closest("button"); if (!b) return;
    const v = b.dataset.v || null;
    if (b.dataset.d) { const l = Store.get().cart.find((x) => x.id === b.dataset.id && x.variant === v); if (l) Store.setQty(l.id, l.qty + +b.dataset.d, v); }
    else if (b.classList.contains("js-rm")) Store.setQty(b.dataset.id, 0, v);
    else if (b.classList.contains("js-clear")) Store.clearCart();
  });
  document.addEventListener("store:change", () => { if (!document.querySelector(".empty .btn--wa")) render(); });
  render();
})();
