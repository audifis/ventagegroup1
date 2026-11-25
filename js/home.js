(function () {
  const U = SODISCOM_UI, D = SODISCOM_DATA, $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
  U.mount("home");
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const hero = $("#hero");

  /* ——— Rideau de théâtre : à chaque chargement (rechargement, arrivée depuis l'extérieur) ;
     pas quand on revient à l'accueil depuis une autre page du site. ?rideau le force toujours. ——— */
  const th = $("#theatre");
  const nav = (performance.getEntriesByType && performance.getEntriesByType("navigation")[0]) || {};
  let internal = false; try { internal = !!document.referrer && new URL(document.referrer).origin === location.origin && nav.type !== "reload"; } catch (e) {}
  if (window.__route) internal = !!window.__routeInternal; // version autonome : navigation interne
  const curtainOn = /rideau/.test(location.search + location.hash) || !internal;
  let opened = false;
  function openCurtain() {
    if (opened) return; opened = true;
    th.classList.add("open");
    setTimeout(() => hero.classList.add("play"), 900);
    setTimeout(() => document.body.classList.remove("lock"), 1200);
    setTimeout(() => th.remove(), 3300);
  }
  if (curtainOn) {
    document.body.classList.add("lock");
    th.classList.add("run");
    const t = setTimeout(openCurtain, 2300);
    $(".theatre-skip").addEventListener("click", () => { clearTimeout(t); openCurtain(); });
    th.addEventListener("click", (e) => { if (e.target === th || e.target.classList.contains("curtain")) { clearTimeout(t); openCurtain(); } });
  } else { th.remove(); hero.classList.add("play"); }

  /* ——— Diaporama ——— */
  const slides = $$(".slide", hero), dots = $$(".dots button", hero), DUR = 7000;
  let cur = 0, timer, paused = false;
  hero.style.setProperty("--dur", DUR + "ms");
  // Diapositives cachées : leur photo n'est chargée qu'au moment utile
  function heroPic(k, alt) {
    const set = (ext) => [960, 1440, 1920].map((w) => `assets/img/${k}-${w}.${ext} ${w}w`).join(", ");
    if (window.__IMGMAP) return `<picture><img src="${U.src(k, 960)}" alt="${U.esc(U.tr(alt))}"></picture>`;
    return `<picture><source media="(max-width:700px)" type="image/avif" srcset="assets/img/${k}-m.avif"><source media="(max-width:700px)" srcset="assets/img/${k}-m.webp"><source type="image/avif" srcset="${set("avif")}" sizes="100vw"><img src="assets/img/${k}-1440.webp" srcset="${set("webp")}" sizes="100vw" alt="${U.esc(U.tr(alt))}" width="1920" height="1080" decoding="async"></picture>`;
  }
  const loadSlide = (i) => { const el = slides[i] && slides[i].querySelector("[data-hero]"); if (el) el.outerHTML = heroPic(el.dataset.hero, el.dataset.alt); };
  function go(n) {
    slides[cur].classList.remove("on"); dots[cur].classList.remove("on"); dots[cur].setAttribute("aria-selected", "false");
    cur = (n + slides.length) % slides.length;
    loadSlide(cur); loadSlide((cur + 1) % slides.length);
    slides[cur].classList.add("on"); dots[cur].setAttribute("aria-selected", "true");
    void dots[cur].offsetWidth; dots[cur].classList.add("on");
    schedule();
  }
  function schedule() { clearTimeout(timer); if (!paused && !reduce) timer = setTimeout(() => go(cur + 1), DUR); }
  dots.forEach((d, i) => d.addEventListener("click", () => go(i)));
  $$(".harr[data-d]", hero).forEach((b) => b.addEventListener("click", () => go(cur + +b.dataset.d)));
  $(".hpause", hero).addEventListener("click", (e) => { paused = !paused; e.currentTarget.classList.toggle("paused", paused); e.currentTarget.setAttribute("aria-label", paused ? "Lecture" : "Pause"); hero.classList.toggle("is-paused", paused); schedule(); });
  setTimeout(schedule, curtainOn ? 3000 : 0);
  if (document.readyState === "complete") setTimeout(() => loadSlide(1), 1500);
  else addEventListener("load", () => setTimeout(() => loadSlide(1), 1500));
  // glisser au doigt
  let x0 = null;
  hero.addEventListener("touchstart", (e) => (x0 = e.touches[0].clientX), { passive: true });
  hero.addEventListener("touchend", (e) => { if (x0 == null) return; const dx = e.changedTouches[0].clientX - x0; if (Math.abs(dx) > 50) go(cur + ((dx < 0) !== !!(window.I18N && I18N.rtl) ? 1 : -1)); x0 = null; });
  document.addEventListener("visibilitychange", () => (document.hidden ? clearTimeout(timer) : schedule()));
  // cartes « offre » des slides
  $$("[data-p]", hero).forEach((el) => { const p = D.findProduct(el.dataset.p); if (p) el.innerHTML = U.media(p); });
  $$("[data-price]", hero).forEach((el) => { const p = D.findProduct(el.dataset.price); if (p) el.innerHTML = `${U.fmt(p.price)}${p.oldPrice ? ` <s>${U.fmt(p.oldPrice)}</s>` : ""}`; });

  /* Liens WhatsApp */
  $$(".js-wa").forEach((a) => (a.href = U.wa("Bonjour SODISCOM-GE, je souhaite être conseillé pour un achat.")));
  $$(".js-wa-pro").forEach((a) => (a.href = U.wa("Bonjour SODISCOM-GE, je souhaite un devis pour un projet professionnel (hôtel, bureaux, résidence).")));

  /* Images de fond des bannières */
  $$("[data-scene]").forEach((el) => (el.innerHTML = U.scene(el.dataset.scene, "", false, el.closest(".tile:not(.tile--xl)") ? "(max-width:700px) 100vw, 33vw" : "(max-width:700px) 100vw, 50vw")));

  /* ——— Rayons ——— */
  $("#cats").innerHTML = D.categories.map((c, i) => `<a class="cat" href="catalogue.html?cat=${c.id}" data-reveal style="transition-delay:${i * 50}ms">
      <span class="cat-img">${U.pimg(c.img, "")}</span><b>${U.esc(c.short || c.label)}</b><small>${U.t("{n} articles", { n: D.products.filter((p) => p.category === c.id).length })}</small></a>`).join("") +
    `<a class="cat cat--promo" href="catalogue.html?promo=1" data-reveal><span class="cat-img"><b>-20%</b></span><b>Promotions</b><small>${U.t("{n} offres", { n: D.products.filter((p) => p.oldPrice).length })}</small></a>`;

  /* ——— Ventes flash ——— */
  const promos = D.products.filter((p) => p.oldPrice).sort((a, b) => D.discount(b) - D.discount(a));
  $("#flash").innerHTML = promos.map(U.card).join("");
  let cdTimer;
  const tick = () => {
    if (!$("#cd-h")) return clearInterval(cdTimer);
    const now = new Date(), end = new Date(now); end.setHours(23, 59, 59, 999);
    let s = Math.max(0, Math.floor((end - now) / 1000));
    const p = (n) => String(n).padStart(2, "0");
    $("#cd-h").textContent = p(Math.floor(s / 3600)); $("#cd-m").textContent = p(Math.floor((s % 3600) / 60)); $("#cd-s").textContent = p(s % 60);
  };
  tick(); cdTimer = setInterval(tick, 1000);

  /* ——— Rails : flèches ——— */
  $$(".rail-wrap").forEach((w) => {
    const r = $(".rail", w);
    $$(".rail-btn", w).forEach((b) => b.addEventListener("click", () => r.scrollBy({ left: (b.classList.contains("next") ? 1 : -1) * (window.I18N && I18N.rtl ? -1 : 1) * r.clientWidth * 0.85, behavior: "smooth" })));
  });

  /* ——— Onglets ——— */
  const sets = {
    best: D.products.filter((p) => p.best), new: D.products.filter((p) => p.isNew),
    promo: promos, maison: D.products.filter((p) => p.category === "maison")
  };
  function showTab(t) {
    $$("#tabs button").forEach((b) => b.setAttribute("aria-selected", b.dataset.t === t));
    const g = $("#tabgrid"); g.classList.remove("swap"); void g.offsetWidth; g.classList.add("swap");
    g.innerHTML = sets[t].slice(0, 8).map(U.card).join("");
  }
  $$("#tabs button").forEach((b) => b.addEventListener("click", () => showTab(b.dataset.t)));
  showTab("best");

  /* ——— Shop the look ——— */
  const card = $("#spotcard"), spots = $$(".spot");
  const lookItems = spots.map((s) => D.findProduct(s.dataset.p));
  $("#looklist").innerHTML = lookItems.map((p, i) => `<a class="look-item" href="${U.productUrl(p)}" data-i="${i}"><span class="li-img">${U.media(p)}</span><span><small>${U.esc(p.brand)}</small>${U.esc(p.name)}</span><b>${U.fmt(p.price)}</b></a>`).join("");
  spots.forEach((s, i) => {
    s.addEventListener("click", (e) => {
      e.stopPropagation(); const p = lookItems[i];
      spots.forEach((x) => x.classList.toggle("on", x === s));
      card.innerHTML = `<span class="sc-img">${U.media(p)}</span><span class="sc-txt"><small>${U.esc(p.brand)}</small><b>${U.esc(p.name)}</b>${U.priceBlock(p)}</span><a class="btn btn--sm" href="${U.productUrl(p)}">Voir</a>`;
      card.style.left = `min(max(${s.style.left} , 140px), calc(100% - 150px))`; card.style.top = `calc(${s.style.top} - 12px)`;
      card.hidden = false;
    });
  });
  document.addEventListener("click", (e) => { if (!e.target.closest(".spot-card")) { card.hidden = true; spots.forEach((x) => x.classList.remove("on")); } });

  /* ——— High-tech ——— */
  $("#techrail").innerHTML = D.products.filter((p) => ["mobile", "info"].includes(p.category) || p.sub === "casques").map(U.card).join("");

  /* ——— Marques (défilement continu) ——— */
  const bl = D.brands.filter((b) => !/SODISCOM/.test(b)).map((b) => `<span class="brand-w" style="font-family:${["Manrope", "Playfair Display", "Georgia"][b.length % 3]}">${U.esc(b)}</span>`).join("");
  $("#brands").innerHTML = bl + bl;

  U.reveal();
})();
