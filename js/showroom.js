/* Accueil d'un showroom : même structure que la boutique d'origine, alimentée par le showroom courant. */
(function () {
  const U = SODISCOM_UI, D = SODISCOM_DATA, C = SODISCOM_CONFIG, S = VG_SHOWROOM, t = U.t, tr = U.tr, esc = U.esc;
  const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const fr = (s) => String(s).split("|")[0];
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  document.title = `${C.name} — Ventage Group · Malabo`;
  document.querySelector('meta[name="description"]').content = tr(fr(S.desc));

  /* ——— Construction des diapositives ——— */
  const rank = (p) => (!p.img ? 0 : /^dj:/.test(p.img) ? 1 : 2);
  const ph1 = (a, b) => rank(b) - rank(a);
  const promos = D.products.filter((p) => p.oldPrice).sort((a, b) => ph1(a, b) || D.discount(b) - D.discount(a));
  const pickDeal = (cat) => promos.find((p) => p.category === cat && rank(p) === 2) || D.products.find((p) => p.category === cat && rank(p) === 2) || promos.find((p) => p.category === cat && p.img) || D.products.find((p) => p.category === cat && p.img) || promos.find((p) => p.category === cat) || D.products.find((p) => p.category === cat);
  const slides = [{ img: S.photos[0], k: `${C.name} · Malabo`, l1: tr(fr(S.tag)), l2: tr(fr(S.plaque)) + ".", p: tr(fr(S.desc)),
    ctas: `<a class="btn btn--gold btn--lg" href="catalogue.html">${tr("Explorer la boutique")} <span class="arr" aria-hidden="true">→</span></a><a class="btn btn--glass btn--lg js-wa" href="#" target="_blank" rel="noopener">${tr("Parler à un conseiller")}</a>` }];
  D.categories.slice(0, 3).forEach((c, i) => {
    const d = pickDeal(c.id);
    slides.push({ img: S.photos[(i + 1) % S.photos.length], k: c.label, l1: (c.short || c.label) + ",", l2: t("chez {name}.", { name: C.name }), p: c.desc,
      ctas: `<a class="btn btn--gold btn--lg" href="catalogue.html?cat=${c.id}">${tr("Voir le rayon")} <span class="arr" aria-hidden="true">→</span></a>`, deal: d });
  });
  if (C.pro) slides.push({ img: S.photos[4 % S.photos.length], k: "Ventage Pro", l1: tr("Entreprises & projets,"), l2: tr("devis sur mesure."), p: tr("Volumes, délais, livraison : un conseiller dédié établit une proposition pour votre projet."),
    ctas: `<a class="btn btn--gold btn--lg js-wa-pro" href="#" target="_blank" rel="noopener">${tr("Demander un devis")}</a>` });

  $("#slides").innerHTML = slides.map((s, i) => `<div class="slide${i ? "" : " on"}" data-i="${i}">
      ${i ? `<span data-hero="${esc(s.img)}" data-alt="${esc(C.name)}"></span>` : U.scene(s.img, C.name, true, "(max-width:700px) 100vw, 68vw", "is-photo")}
      <div class="slide-copy wrap"><span class="kicker">${esc(s.k)}</span>
        <${i ? "h2" : "h1"} class="hero-t"><span class="ln">${esc(s.l1)}</span><span class="ln"><em>${esc(s.l2)}</em></span></${i ? "h2" : "h1"}>
        <p>${esc(s.p)}</p><div class="ctas">${s.ctas}</div></div>
      ${s.deal ? `<a class="deal" href="${U.productUrl(s.deal)}"><span class="deal-img">${U.media(s.deal)}</span><span class="deal-txt"><small>${s.deal.oldPrice ? tr("Offre du moment") : tr("Top vente")}</small><b>${esc(s.deal.name)}</b><em>${s.deal.price ? U.fmt(s.deal.price) : tr("Sur devis")}${s.deal.oldPrice ? ` <s>${U.fmt(s.deal.oldPrice)}</s>` : ""}</em></span></a>` : ""}
    </div>`).join("");
  $("#dots").innerHTML = slides.map((s, i) => `<button role="tab" aria-label="${esc(s.k)}" class="${i ? "" : "on"}" aria-selected="${!i}"><i></i></button>`).join("");

  U.mount("home");
  const hero = $("#hero");

  /* ——— Rideau d'ouverture (comme la boutique d'origine) ——— */
  $("#pl-name").textContent = C.name; $("#pl-title").textContent = tr(fr(S.plaque));
  const th = $("#theatre");
  const nav = (performance.getEntriesByType && performance.getEntriesByType("navigation")[0]) || {};
  let internal = false; try { internal = !!document.referrer && new URL(document.referrer).origin === location.origin && nav.type !== "reload" && /showroom|catalogue|produit|panier|contact/.test(document.referrer); } catch (e) {}
  let seen = false; try { seen = sessionStorage.getItem("vg-curtain-" + S.id) === "1"; sessionStorage.setItem("vg-curtain-" + S.id, "1"); } catch (e) {}
  const curtainOn = /rideau/.test(location.search + location.hash) || (!internal && !seen);
  let opened = false;
  function openCurtain() {
    if (opened) return; opened = true;
    th.classList.add("open");
    setTimeout(() => hero.classList.add("play"), 900);
    setTimeout(() => document.body.classList.remove("lock"), 1200);
    setTimeout(() => th.remove(), 3300);
  }
  if (curtainOn) {
    document.body.classList.add("lock"); th.classList.add("run");
    const tm = setTimeout(openCurtain, 2300);
    $(".theatre-skip").addEventListener("click", () => { clearTimeout(tm); openCurtain(); });
    th.addEventListener("click", (e) => { if (e.target === th || e.target.classList.contains("curtain")) { clearTimeout(tm); openCurtain(); } });
  } else { th.remove(); hero.classList.add("play"); }

  /* ——— Diaporama ——— */
  const sl = $$(".slide", hero), dots = $$(".dots button", hero), DUR = 7000;
  let cur = 0, timer, paused = false;
  hero.style.setProperty("--dur", DUR + "ms");
  const loadSlide = (i) => { const el = sl[i] && sl[i].querySelector("[data-hero]"); if (el) el.outerHTML = U.scene(el.dataset.hero, el.dataset.alt, false, "(max-width:700px) 100vw, 68vw", "is-photo"); };
  function go(n) {
    sl[cur].classList.remove("on"); dots[cur].classList.remove("on"); dots[cur].setAttribute("aria-selected", "false");
    cur = (n + sl.length) % sl.length;
    loadSlide(cur); loadSlide((cur + 1) % sl.length);
    sl[cur].classList.add("on"); dots[cur].setAttribute("aria-selected", "true");
    void dots[cur].offsetWidth; dots[cur].classList.add("on");
    schedule();
  }
  function schedule() { clearTimeout(timer); if (!paused && !reduce && sl.length > 1) timer = setTimeout(() => go(cur + 1), DUR); }
  dots.forEach((d, i) => d.addEventListener("click", () => go(i)));
  $$(".harr[data-d]", hero).forEach((b) => b.addEventListener("click", () => go(cur + +b.dataset.d)));
  $(".hpause", hero).addEventListener("click", (e) => { paused = !paused; e.currentTarget.classList.toggle("paused", paused); hero.classList.toggle("is-paused", paused); schedule(); });
  setTimeout(schedule, curtainOn ? 3000 : 0);
  setTimeout(() => loadSlide(1), 1500);
  let x0 = null;
  hero.addEventListener("touchstart", (e) => (x0 = e.touches[0].clientX), { passive: true });
  hero.addEventListener("touchend", (e) => { if (x0 == null) return; const dx = e.changedTouches[0].clientX - x0; if (Math.abs(dx) > 50) go(cur + (dx < 0 ? 1 : -1)); x0 = null; });
  document.addEventListener("visibilitychange", () => (document.hidden ? clearTimeout(timer) : schedule()));

  /* ——— WhatsApp ——— */
  const waLinks = () => {
    $$(".js-wa").forEach((a) => (a.href = U.wa("Bonjour SODISCOM-GE, je souhaite être conseillé pour un achat.")));
    $$(".js-wa-pro").forEach((a) => (a.href = U.wa("Bonjour SODISCOM-GE, je souhaite un devis pour un projet professionnel (hôtel, bureaux, résidence).")));
  };

  /* ——— Bandeau promo ——— */
  const mx = U.maxOff();
  if (mx) { $("#pb-tag").textContent = t("Semaine {name}", { name: C.name }); $("#pb-big").innerHTML = `${esc(tr("Jusqu'à"))} <b>-${mx} %</b>`; } else $("#promobar").remove();

  /* ——— Rayons ——— */
  $("#cats").innerHTML = D.categories.map((c, i) => `<a class="cat" href="catalogue.html?cat=${c.id}" data-reveal style="transition-delay:${i * 50}ms">
      <span class="cat-img">${U.pimg(c.img, "")}</span><b>${esc(c.short || c.label)}</b><small>${t("{n} articles", { n: D.products.filter((p) => p.category === c.id).length })}</small></a>`).join("") +
    (promos.length ? `<a class="cat cat--promo" href="catalogue.html?promo=1" data-reveal><span class="cat-img"><b>-${mx}%</b></span><b>Promotions</b><small>${t("{n} offres", { n: promos.length })}</small></a>` : "");

  /* ——— Colonne gauche : recherche + rayons + offres (comme le catalogue) ——— */
  const cnt = (f) => D.products.filter(f).length;
  let favN = 0; try { favN = Store.get().favs.length; } catch (e) {}
  const offers = [["catalogue.html?promo=1", "tag", "Promotions", promos.length], ["catalogue.html?sort=new", "spark", "Nouveautés", cnt((p) => p.isNew)],
    ["catalogue.html?sort=best", "star", "Meilleures ventes", cnt((p) => p.best)], ["catalogue.html?fav=1", "heart", "Mes favoris", favN]].filter((o) => o[3] || o[2] === "Mes favoris");
  $("#srside").innerHTML = `<div class="sp-head"><b>${esc(C.name)}</b><button class="sp-x js-spclose" type="button" aria-label="${esc(tr("Fermer"))}">${U.ic("close")}</button></div>
    <div class="sbox sbox--q" id="sside-q"></div>
    <div class="sbox"><h3>${esc(tr("Rayons"))}</h3><nav class="srays">${D.categories.map((c) => `<div class="sray">
        <a href="catalogue.html?cat=${c.id}"><span class="sray-ic">${U.ic(c.icon)}</span><span class="sray-l">${esc(c.label)}</span><small>${cnt((p) => p.category === c.id)}</small></a>
        ${c.subs.length > 1 ? `<button class="sray-tg" type="button" aria-expanded="false" aria-label="${esc(c.label)}">${U.ic("right")}</button>
        <div class="sray-subs" hidden>${c.subs.map((sb) => `<a href="catalogue.html?cat=${c.id}&sub=${sb.id}"><span>${esc(sb.label)}</span><small>${cnt((p) => p.sub === sb.id)}</small></a>`).join("")}</div>` : ""}</div>`).join("")}
      <div class="sray sray--all"><a href="catalogue.html"><span class="sray-ic">${U.ic("grid")}</span><span class="sray-l">${esc(tr("Tout le catalogue"))}</span><small>${D.products.length}</small></a></div></nav></div>
    <div class="sbox sbox--off"><h3>${esc(tr("Offres"))}</h3>${offers.map(([h, i, l, n]) => `<a class="soff" href="${h}"><span class="sray-ic">${U.ic(i)}</span><span class="sray-l">${esc(tr(l))}</span><small>${n}</small></a>`).join("")}</div>
    <div class="scard"><small>${esc(tr("Le showroom"))}</small><b>${esc(C.name)}</b><span>${esc(C.hours || tr("Du lundi au samedi"))}</span>
      <a class="btn btn--wa btn--sm js-wa" href="#" target="_blank" rel="noopener">${U.waIcon} ${esc(tr("Écrire au showroom"))}</a></div>`;
  U.sideSearch($("#sside-q"));
  U.sidePanel($("#srside"));
  U.catChips($("#srbar"));
  $$(".sray-tg").forEach((b) => b.addEventListener("click", () => {
    const open = b.getAttribute("aria-expanded") !== "true";
    b.setAttribute("aria-expanded", open); b.nextElementSibling.hidden = !open; b.parentElement.classList.toggle("open", open);
  }));

  /* ——— Ventes flash ——— */
  if (promos.length) {
    $("#flash").innerHTML = promos.map(U.card).join("");
    let cdTimer;
    const tick = () => {
      if (!$("#cd-h")) return clearInterval(cdTimer);
      const now = new Date(), end = new Date(now); end.setHours(23, 59, 59, 999);
      const s = Math.max(0, Math.floor((end - now) / 1000)), p = (n) => String(n).padStart(2, "0");
      $("#cd-h").textContent = p(Math.floor(s / 3600)); $("#cd-m").textContent = p(Math.floor((s % 3600) / 60)); $("#cd-s").textContent = p(s % 60);
    };
    tick(); cdTimer = setInterval(tick, 1000);
  } else $("#flash-sec").remove();

  /* ——— Bannières duo ——— */
  const duo = D.categories.slice(0, 2);
  if (duo.length) $("#duo").innerHTML = duo.map((c, i) => `<a class="banner${i ? " banner--light" : ""}" href="catalogue.html?cat=${c.id}" data-reveal><span class="banner-img">${U.scene(c.scene || c.img, "", false, "(max-width:700px) 100vw, 50vw")}</span>
      <span class="banner-copy"><small>${esc(c.label)}</small><b>${esc(c.short || c.label)}</b><em>${esc(c.desc)}</em><span class="btn ${i ? "btn--dark" : "btn--light"} btn--sm">${tr("Découvrir")}</span></span></a>`).join("");
  else $("#duo-sec").remove();
  if (duo.length === 1) $("#duo").style.gridTemplateColumns = "1fr";

  /* ——— Sélection en onglets ——— */
  $("#sel-t").innerHTML = `${esc(tr("La sélection"))} <em>${esc(C.name)}</em>`;
  const sets = [["best", "Meilleures ventes", D.products.filter((p) => p.best)], ["new", "Nouveautés", D.products.filter((p) => p.isNew)], ["promo", "Promotions", promos]]
    .concat(D.categories.slice(0, 2).map((c) => [c.id, c.short || c.label, D.products.filter((p) => p.category === c.id)])).filter((x) => x[2].length).map(([k, l, a]) => [k, l, a.slice().sort(ph1)]);
  $("#tabs").innerHTML = sets.map(([k, l], i) => `<button role="tab" aria-selected="${!i}" data-t="${k}">${esc(tr(l))}</button>`).join("");
  function showTab(k) {
    $$("#tabs button").forEach((b) => b.setAttribute("aria-selected", b.dataset.t === k));
    const g = $("#tabgrid"); g.classList.remove("swap"); void g.offsetWidth; g.classList.add("swap");
    g.innerHTML = sets.find((x) => x[0] === k)[2].slice(0, 8).map(U.card).join("");
  }
  $$("#tabs button").forEach((b) => b.addEventListener("click", () => showTab(b.dataset.t)));
  if (sets.length) showTab(sets[0][0]);

  /* ——— Le showroom : photos du lieu + coordonnées ——— */
  $("#visit-ph").innerHTML = S.photos.slice(0, 3).map((u, i) => `<button data-lb="${i}" aria-label="${esc(t("Photo {n}", { n: i + 1 }))}">${U.scene(u, C.name, false, i ? "(max-width:700px) 50vw, 20vw" : "(max-width:700px) 100vw, 40vw")}${i === 2 && S.photos.length > 3 ? `<span class="more">+${S.photos.length - 3} photos</span>` : ""}</button>`).join("");
  $("#visit-t").innerHTML = `${esc(tr("Venez nous voir"))} <em>${esc(tr("sur place."))}</em>`;
  $("#visit-p").textContent = tr(fr(S.desc));
  $("#visit-dl").innerHTML = `<div><dt>${U.ic("pin")}</dt><dd>${esc(C.name)}<br>${esc(C.address)}, ${esc(C.country)}</dd></div>
    <div><dt>${U.ic("clock")}</dt><dd>${esc(C.hours || tr("Du lundi au samedi"))}</dd></div>
    <div><dt>${U.ic("chat")}</dt><dd><a href="tel:${C.phone.replace(/\s/g, "")}">${esc(C.phone)}</a></dd></div>`;
  $("#visit-wa").innerHTML = `${U.waIcon} ${esc(tr("Écrire au showroom"))}`;
  const lb = $("#lb"), lbImg = $("img", lb); let li = 0;
  const lbShow = () => { lbImg.removeAttribute("srcset"); lbImg.dataset.orig = S.photos[li]; lbImg.src = U.opt(S.photos[li], 1920); $("#lb-cap").textContent = `${C.name} · ${li + 1} / ${S.photos.length}`; };
  $$("[data-lb]").forEach((b) => b.addEventListener("click", () => { li = +b.dataset.lb; lbShow(); lb.classList.add("on"); document.body.style.overflow = "hidden"; }));
  $(".lb-p", lb).innerHTML = U.ic("left"); $(".lb-n", lb).innerHTML = U.ic("right"); $(".lb-x", lb).innerHTML = U.ic("close");
  $(".lb-p", lb).onclick = () => { li = (li - 1 + S.photos.length) % S.photos.length; lbShow(); };
  $(".lb-n", lb).onclick = () => { li = (li + 1) % S.photos.length; lbShow(); };
  const lbClose = () => { lb.classList.remove("on"); document.body.style.overflow = ""; };
  $(".lb-x", lb).onclick = lbClose; lb.addEventListener("click", (e) => { if (e.target === lb) lbClose(); });
  document.addEventListener("keydown", (e) => { if (!lb.classList.contains("on")) return; if (e.key === "Escape") lbClose(); if (e.key === "ArrowRight") $(".lb-n", lb).click(); if (e.key === "ArrowLeft") $(".lb-p", lb).click(); });

  /* ——— Rail « tout le showroom » ——— */
  const r2 = D.products.slice().sort((a, b) => ph1(a, b) || (b.isNew - a.isNew) || (b.best - a.best)).slice(0, 24);
  if (r2.length > 4) { $("#r2-k").textContent = tr(fr(S.tag)); $("#r2-t").innerHTML = `${esc(tr("Tout l'univers"))} <em>${esc(C.name)}</em>`; $("#rail2").innerHTML = r2.map(U.card).join(""); }
  else $("#rail2-sec").remove();

  /* ——— Espace Pro ——— */
  if (C.pro) { $("#pro-block").hidden = false; $("#pro-bg").innerHTML = U.scene(S.photos[2 % S.photos.length], ""); } else $("#pro-block").remove();

  /* ——— Rails : flèches ——— */
  $$(".rail-wrap").forEach((w) => {
    const r = $(".rail", w);
    $$(".rail-btn", w).forEach((b) => b.addEventListener("click", () => r.scrollBy({ left: (b.classList.contains("next") ? 1 : -1) * r.clientWidth * 0.85, behavior: "smooth" })));
  });

  /* ——— Marques ——— */
  const bl = D.brands.filter((b) => !/^(Ventage|Amanda)/.test(b));
  if (bl.length >= 3) { const h = bl.map((b) => `<span class="brand-w" style="font-family:${["Manrope", "Playfair Display", "Georgia"][b.length % 3]}">${esc(b)}</span>`).join(""); $("#brands").innerHTML = h + h + h; }
  else $("#brands-sec").remove();

  waLinks();
  U.reveal();
})();
