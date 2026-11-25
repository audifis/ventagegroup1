# Ventage Group — site commercial

- `index.html` : portail du groupe (12 showrooms, rayons, offres, FR/ES/EN, FCFA/EUR).
- `showroom.html?s=<id>` : boutique d'un showroom (même moteur que SODISCOM : rayons, catalogue, fiche produit, favoris, comparateur, panier, commande WhatsApp).
- `catalogue.html`, `produit.html`, `panier.html`, `contact.html` : pages de la boutique, toujours avec `?s=<id>`.

## Modifier le contenu
Tout est dans **`js/catalog.js`** : showrooms (nom, couleur, photos, WhatsApp, téléphone, horaires, adresse), rayons et produits.
Textes au format `"français|español|english"`.

Identifiants des showrooms : ventage-mall, supermercado, megastore-km5, megastore-ela-nguema, ventage-casa, construction,
electric-store, electronics-office, paint-store, amanda-pharmacies, amanda-labs, tires-auto.

Chaque showroom a son propre panier (stockage `ventage:<id>`) et envoie la commande à son numéro WhatsApp.

## Régénérer le catalogue
`python3 tools/build_catalog.py <products.json>` reconstruit `js/catalog.js` (≈100 produits par showroom) à partir de
`tools/catalog-base.js` (showrooms) et du catalogue de démonstration DummyJSON (`database/products.json` du dépôt Ovi/DummyJSON).

## Photos
- Produits de la boutique d'origine : `assets/img` (WebP/AVIF, plusieurs tailles).
- Photos des lieux (ventagegroup.com) et produits de démonstration (cdn.dummyjson.com) : redimensionnées à la volée en WebP par wsrv.nl ;
  si wsrv.nl ne répond pas, l'image d'origine est chargée. Pour la production, copier ces photos dans `assets/` optimisées.

## En ligne
https://ventage-group.vercel.app — déployé automatiquement par Vercel à chaque push sur `main` (dépôt audifis/ventagegroup1).
