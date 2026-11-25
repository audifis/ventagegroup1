(function () {
  const U = SODISCOM_UI, C = SODISCOM_CONFIG;
  U.mount("contact");
  const tel = C.phone.replace(/\s/g, "");
  document.getElementById("contactroot").innerHTML = `
    <div class="contact-card">
      <span class="eyebrow">Showroom ${U.esc(C.name)}</span>
      <dl>
        <div><dt>Adresse</dt><dd>${U.esc(C.address)}<br>${U.esc(C.city)}, ${U.esc(C.country)}</dd></div>
        <div><dt>Téléphone</dt><dd><a href="tel:${tel}">${U.esc(C.phone)}</a></dd></div>
        ${C.email ? `<div><dt>E-mail</dt><dd><a href="mailto:${C.email}">${U.esc(C.email)}</a></dd></div>` : ""}
        ${C.hours ? `<div><dt>Horaires</dt><dd>${U.esc(C.hours)}</dd></div>` : ""}
      </dl>
      <div class="row"><a class="btn btn--wa" href="${U.wa("Bonjour SODISCOM-GE, j'ai une question.")}" target="_blank" rel="noopener">${U.waIcon} WhatsApp</a>
        <a class="btn btn--ghost" href="tel:${tel}">Appeler</a></div>
    </div>
    <div>
      <iframe class="map" title="Plan : Malabo" loading="lazy" referrerpolicy="no-referrer-when-downgrade"
        src="https://www.openstreetmap.org/export/embed.html?bbox=8.76%2C3.74%2C8.80%2C3.765&layer=mapnik"></iframe>
      <p class="note">Plan indicatif de Malabo. Pour l'itinéraire exact du showroom, demandez la localisation sur WhatsApp.</p>
    </div>`;
  document.querySelectorAll(".js-wa-pro").forEach((a) => (a.href = U.wa("Bonjour SODISCOM-GE, je représente une entreprise et souhaite un devis pour un projet d'équipement.")));
})();
