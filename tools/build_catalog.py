# -*- coding: utf-8 -*-
"""Génère js/catalog.js : showrooms, rayons, ~100 produits par showroom.
Usage : python3 tools/build_catalog.py  (depuis la racine du projet)
Sources photos : assets/img (boutique d'origine), catalogue de démo DummyJSON (cdn.dummyjson.com), pictogrammes sinon."""
import json, re, hashlib, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DJ = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "/tmp/dj.json"))
OLD = open(os.path.join(ROOT, "tools/catalog-base.js"), encoding="utf-8").read()

def block(src, start):
    i = src.index(start) + len(start) - 1; d = 0
    for j in range(i, len(src)):
        if src[j] == "[": d += 1
        elif src[j] == "]":
            d -= 1
            if d == 0: return src[i:j + 1]
SHOWROOMS_JS = block(OLD, "const SHOWROOMS = [")
SDC_JS = block(OLD, "const SDC = [")
UNIVERS_JS = block(OLD, "const UNIVERS = [")

def h(s, n=100): return int(hashlib.md5(s.encode()).hexdigest(), 16) % n
def T(fr, es=None, en=None): return "|".join([fr, es or fr, en or es or fr])
def nice(x):
    if x is None: return None
    if x < 2000: return int(round(x / 50.0) * 50) or 50
    if x < 20000: return int(round(x / 100.0) * 100)
    if x < 200000: return int(round(x / 500.0) * 500)
    return int(round(x / 5000.0) * 5000)

# ───────────── Rayons (id, label fr|es|en, icône, [(sub, label)]) ─────────────
CATS = []
def C(cid, label, icon, subs, short=None, desc=None):
    CATS.append({"id": cid, "label": label, "icon": icon, "short": short, "desc": desc or "", "subs": [list(s) for s in subs]})

# MALL
C("homme", T("Homme", "Hombre", "Men"), "shirt",
  [("polos-chemises", T("Polos, chemises & t-shirts", "Polos, camisas y camisetas", "Polos, shirts & T-shirts")), ("pantalons", T("Jeans & pantalons", "Vaqueros y pantalones", "Jeans & trousers")), ("vestes", T("Vestes & costumes", "Chaquetas y trajes", "Jackets & suits")), ("sportswear", T("Sportswear", "Ropa deportiva", "Sportswear"))], None,
  T("Polos, chemises, jeans et costumes des grandes marques.", "Polos, camisas, vaqueros y trajes de las grandes marcas.", "Polos, shirts, jeans and suits from leading brands."))
C("femme", T("Femme", "Mujer", "Women"), "dress",
  [("robes", T("Robes & ensembles", "Vestidos y conjuntos", "Dresses & sets")), ("hauts", T("Blouses & mailles", "Blusas y punto", "Blouses & knitwear")), ("vestes-f", T("Vestes & manteaux", "Chaquetas y abrigos", "Jackets & coats")), ("bas", T("Jeans, leggings & sport", "Vaqueros, leggings y deporte", "Jeans, leggings & sport"))], None,
  T("Robes, blouses, vestes et jeans pour toutes les occasions.", "Vestidos, blusas, chaquetas y vaqueros para cada ocasión.", "Dresses, blouses, jackets and jeans for every occasion."))
C("enfants", T("Enfants", "Niños", "Kids"), "baby",
  [("enfant", T("Bébé & enfant", "Bebé y niño", "Baby & kids"))], None,
  T("Ensembles, survêtements et sweats pour les petits.", "Conjuntos, chándales y sudaderas para los pequeños.", "Sets, tracksuits and sweatshirts for little ones."))
C("chaussures", T("Chaussures", "Calzado", "Shoes"), "shoe",
  [("homme", T("Homme", "Hombre", "Men")), ("femme", T("Femme", "Mujer", "Women"))], None,
  T("Sneakers, souliers et escarpins.", "Zapatillas, zapatos y tacones.", "Sneakers, dress shoes and heels."))
C("parfums", T("Parfums", "Perfumes", "Fragrance"), "perfume",
  [("homme", T("Parfums homme", "Perfumes hombre", "Men's fragrance")), ("femme", T("Parfums femme", "Perfumes mujer", "Women's fragrance"))], None,
  T("Les grands parfums, en flacons authentiques.", "Los grandes perfumes, en frascos auténticos.", "The great fragrances, authentic bottles."))
C("beaute", T("Maquillage & soins", "Maquillaje y cuidado", "Make-up & skincare"), "lipstick",
  [("maquillage", T("Maquillage", "Maquillaje", "Make-up")), ("soins-beaute", T("Soins", "Cuidado", "Skincare"))], T("Beauté", "Belleza", "Beauty"),
  T("Maquillage et soins de beauté.", "Maquillaje y cuidado de belleza.", "Make-up and beauty care."))
C("horlogerie", T("Horlogerie & optique", "Relojería y óptica", "Watches & eyewear"), "watch",
  [("montres-luxe", T("Montres", "Relojes", "Watches")), ("solaires", T("Lunettes de soleil", "Gafas de sol", "Sunglasses"))], T("Montres", "Relojes", "Watches"),
  T("Montres de prestige et lunettes de soleil.", "Relojes de prestigio y gafas de sol.", "Prestige watches and sunglasses."))
C("accessoires", T("Sacs & bijoux", "Bolsos y joyas", "Bags & jewellery"), "bagl",
  [("sacs", T("Sacs", "Bolsos", "Bags")), ("bijoux", T("Bijoux", "Joyas", "Jewellery")), ("petite-maro", T("Ceintures & petite maroquinerie", "Cinturones y marroquinería", "Belts & small leather goods"))], T("Accessoires", "Accesorios", "Accessories"),
  T("Sacs, bijoux et maroquinerie.", "Bolsos, joyas y marroquinería.", "Bags, jewellery and leather goods."))
# SUPERMERCADO
C("frais", T("Fruits, légumes & frais", "Frutas, verduras y frescos", "Fresh food"), "apple",
  [("fruits-legumes", T("Fruits & légumes", "Frutas y verduras", "Fruit & vegetables")), ("boucherie", T("Viandes & poissons", "Carnes y pescados", "Meat & fish")), ("cremerie", T("Crèmerie & œufs", "Lácteos y huevos", "Dairy & eggs")), ("boulangerie", T("Boulangerie", "Panadería", "Bakery")), ("surgeles", T("Surgelés & glaces", "Congelados y helados", "Frozen & ice cream"))], T("Frais", "Frescos", "Fresh"),
  T("Fruits, légumes, viandes et produits laitiers.", "Frutas, verduras, carnes y lácteos.", "Fruit, vegetables, meat and dairy."))
C("epicerie", T("Épicerie", "Alimentación", "Pantry"), "basket",
  [("base", T("Riz, pâtes & farines", "Arroz, pasta y harinas", "Rice, pasta & flour")), ("conserves", T("Conserves & sauces", "Conservas y salsas", "Tins & sauces")), ("petit-dej", T("Petit-déjeuner", "Desayuno", "Breakfast")), ("huiles-epices", T("Huiles & épices", "Aceites y especias", "Oils & spices")), ("biscuits", T("Biscuits, snacks & confiserie", "Galletas, snacks y dulces", "Biscuits, snacks & sweets"))], None,
  T("L'essentiel du quotidien, au meilleur prix.", "Lo esencial del día a día, al mejor precio.", "Everyday essentials at the best price."))
C("boissons", T("Boissons", "Bebidas", "Drinks"), "bottle",
  [("eaux-jus", T("Eaux & jus", "Aguas y zumos", "Water & juice")), ("sodas", T("Sodas", "Refrescos", "Soft drinks")), ("cafe-the", T("Café & thé", "Café y té", "Coffee & tea")), ("alcools", T("Bières, vins & spiritueux", "Cervezas, vinos y licores", "Beer, wine & spirits"))], None,
  T("Eaux, jus, sodas, café et thé.", "Aguas, zumos, refrescos, café y té.", "Water, juice, soft drinks, coffee and tea."))
C("entretien", T("Entretien & hygiène", "Limpieza e higiene", "Household & hygiene"), "spray",
  [("menage", T("Lessive & ménage", "Detergentes y limpieza", "Laundry & cleaning")), ("hygiene", T("Hygiène", "Higiene", "Hygiene")), ("papier", T("Papier & essuie-tout", "Papel y rollos de cocina", "Paper & kitchen roll"))], T("Entretien", "Limpieza", "Household"),
  T("Lessive, ménage et hygiène pour toute la famille.", "Detergentes, limpieza e higiene para toda la familia.", "Laundry, cleaning and hygiene for the whole family."))
C("bebe", T("Bébé", "Bebé", "Baby"), "baby",
  [("bebe-soins", T("Couches & soins", "Pañales y cuidados", "Nappies & care")), ("bebe-repas", T("Repas & biberons", "Comidas y biberones", "Feeding & bottles"))], None,
  T("Couches, soins, biberons et petits pots.", "Pañales, cuidados, biberones y potitos.", "Nappies, care, bottles and baby food."))
C("animalerie", T("Animalerie", "Mascotas", "Pet shop"), "paw",
  [("chiens", T("Chiens", "Perros", "Dogs")), ("chats", T("Chats", "Gatos", "Cats"))], None,
  T("Croquettes, pâtées, friandises et jouets pour chiens et chats.", "Pienso, comida húmeda, premios y juguetes para perros y gatos.", "Dry and wet food, treats and toys for dogs and cats."))
# KM5
C("electro", "Électroménager", "fridge", [("froid", "Réfrigérateurs & congélateurs"), ("lavage", "Lave-linge"), ("clim", "Climatisation & ventilation")], None,
  T("Froid, lavage et climatisation Inverter.", "Frío, lavado y climatización Inverter.", "Cooling, laundry and Inverter air conditioning."))
C("cuisine", "Cuisine", "pot", [("cuisson", "Fours, cuisinières & micro-ondes"), ("petit", "Petit électroménager")], None,
  T("Fours, cuisinières, micro-ondes et petit électroménager.", "Hornos, cocinas, microondas y pequeño electrodoméstico.", "Ovens, cookers, microwaves and small appliances."))
C("soin-maison", T("Entretien de la maison", "Cuidado del hogar", "Home care"), "vacuum",
  [("aspirateurs", T("Aspirateurs", "Aspiradoras", "Vacuum cleaners")), ("repassage", T("Repassage", "Planchado", "Ironing"))], T("Entretien", "Cuidado", "Home care"),
  T("Aspirateurs, fers et centrales vapeur.", "Aspiradoras, planchas y centros de planchado.", "Vacuums, irons and steam generators."))
C("eau", T("Eau & chauffe-eau", "Agua y calentadores", "Water & heating"), "tank",
  [("citernes", T("Citernes Ventage", "Depósitos Ventage", "Ventage water tanks")), ("chauffe-eau", T("Chauffe-eau", "Calentadores", "Water heaters")), ("traitement", T("Traitement de l'eau", "Tratamiento del agua", "Water treatment"))], T("Eau", "Agua", "Water"),
  T("Citernes fabriquées dans le pays, chauffe-eau et purificateurs.", "Depósitos fabricados en el país, calentadores y purificadores.", "Locally made tanks, water heaters and purifiers."))
# ELA NGUEMA
C("tv", "TV & Audio", "tv", [("smart-tv", "Smart TV"), ("audio", "Son & enceintes"), ("casques", "Casques & écouteurs"), ("gaming", "Gaming")], None,
  T("Smart TV 4K, OLED, barres de son et consoles.", "Smart TV 4K, OLED, barras de sonido y consolas.", "4K and OLED smart TVs, soundbars and consoles."))
C("literie", T("Literie Ventage", "Descanso Ventage", "Ventage bedding"), "bed",
  [("matelas", T("Matelas", "Colchones", "Mattresses")), ("lits", T("Lits & chambres", "Camas y dormitorios", "Beds & bedrooms")), ("linge", T("Linge de lit", "Ropa de cama", "Bed linen"))], T("Literie", "Descanso", "Bedding"),
  T("Matelas fabriqués dans le pays, lits et linge de maison.", "Colchones fabricados en el país, camas y ropa de cama.", "Locally made mattresses, beds and linen."))
C("sport", T("Sport & loisirs", "Deporte y ocio", "Sport & leisure"), "ball",
  [("ballons", T("Sports collectifs", "Deportes de equipo", "Team sports")), ("raquettes", T("Raquettes & batte", "Raquetas y bates", "Rackets & bats")), ("fitness", T("Fitness", "Fitness", "Fitness"))], T("Sport", "Deporte", "Sport"),
  T("Ballons, raquettes et équipement de fitness.", "Balones, raquetas y equipamiento de fitness.", "Balls, rackets and fitness equipment."))
C("bagagerie", T("Bagagerie", "Maletas", "Luggage"), "suitcase",
  [("valises", T("Valises", "Maletas", "Suitcases")), ("sacs-voyage", T("Sacs de voyage", "Bolsas de viaje", "Travel bags"))], None,
  T("Valises et sacs pour tous les voyages.", "Maletas y bolsas para todos los viajes.", "Suitcases and bags for every trip."))
# CASA
C("maison", "Mobilier maison", "sofa", [("salons", "Salons & canapés"), ("fauteuils", "Fauteuils"), ("chambres", "Chambres & literie"), ("repas", "Salle à manger"), ("deco", "Rangements & déco")], "Maison",
  T("Salons, salles à manger et décoration.", "Salones, comedores y decoración.", "Living rooms, dining and décor."))
C("pro", "Mobilier pro & hôtellerie", "building", [("bureaux", "Bureaux & réunion"), ("sieges", "Sièges & accueil"), ("hotellerie", "Hôtellerie & résidences")], "Pro",
  T("Bureaux, accueil, hôtels et résidences.", "Oficinas, recepción, hoteles y residencias.", "Offices, reception, hotels and residences."))
C("table", T("Art de la table & cuisine", "Mesa y cocina", "Tableware & kitchen"), "plate",
  [("vaisselle", T("Vaisselle & verrerie", "Vajilla y cristalería", "Tableware & glassware")), ("ustensiles", T("Ustensiles", "Utensilios", "Utensils")), ("cuisson-casa", T("Casseroles & poêles", "Ollas y sartenes", "Pots & pans"))], T("Table", "Mesa", "Tableware"),
  T("Vaisselle, ustensiles et batterie de cuisine.", "Vajilla, utensilios y batería de cocina.", "Tableware, utensils and cookware."))
C("luminaires", T("Luminaires & textiles", "Iluminación y textiles", "Lighting & textiles"), "lamp",
  [("lampes", T("Lampes & suspensions", "Lámparas y colgantes", "Lamps & pendants")), ("tapis", T("Tapis & rideaux", "Alfombras y cortinas", "Rugs & curtains"))], T("Luminaires", "Iluminación", "Lighting"),
  T("Lampes, tapis et rideaux pour finir la pièce.", "Lámparas, alfombras y cortinas para completar la estancia.", "Lamps, rugs and curtains to finish the room."))
# CONSTRUCTION
C("materiaux", T("Matériaux", "Materiales", "Building materials"), "brick",
  [("gros-oeuvre", T("Gros œuvre", "Obra gruesa", "Structural")), ("toiture", T("Toiture & bois", "Cubierta y madera", "Roofing & timber"))], None,
  T("Ciment, fer, parpaings, tôles et bois.", "Cemento, hierro, bloques, chapas y madera.", "Cement, steel, blocks, roofing and timber."))
C("carrelage", T("Carrelage & sanitaire", "Cerámica y sanitarios", "Tiles & bathroom"), "tile",
  [("sols-murs", T("Sols & murs", "Suelos y paredes", "Floor & wall tiles")), ("sanitaire", T("Sanitaire", "Sanitarios", "Sanitaryware")), ("robinetterie", T("Robinetterie", "Grifería", "Taps"))], T("Carrelage", "Cerámica", "Tiles"),
  T("Carrelage, WC, lavabos, douches et robinetterie.", "Cerámica, inodoros, lavabos, duchas y grifería.", "Tiles, toilets, basins, showers and taps."))
C("plomberie", T("Plomberie & quincaillerie", "Fontanería y ferretería", "Plumbing & hardware"), "pipe",
  [("tubes", T("Tubes & raccords", "Tubos y racores", "Pipes & fittings")), ("visserie", T("Visserie & fixation", "Tornillería y fijación", "Fixings")), ("serrurerie", T("Serrurerie", "Cerrajería", "Locks"))], T("Quincaillerie", "Ferretería", "Hardware"),
  T("Tubes PVC, raccords, visserie et serrures.", "Tubos de PVC, racores, tornillería y cerraduras.", "PVC pipes, fittings, fixings and locks."))
C("outillage", T("Outillage", "Herramientas", "Tools"), "drill",
  [("electroportatif", T("Électroportatif", "Herramienta eléctrica", "Power tools")), ("main", T("Outillage à main", "Herramienta manual", "Hand tools")), ("nettoyage", T("Nettoyage & jardin", "Limpieza y jardín", "Cleaning & garden"))], None,
  T("Outils électroportatifs, outils à main et jardin.", "Herramientas eléctricas, manuales y de jardín.", "Power tools, hand tools and garden."))
# ELECTRIC
C("electricite", T("Câbles & appareillage", "Cables y aparellaje", "Cables & wiring"), "bolt",
  [("cables", T("Câbles & gaines", "Cables y tubos", "Cables & conduit")), ("appareillage", T("Prises & interrupteurs", "Enchufes e interruptores", "Sockets & switches")), ("tableaux", T("Tableaux & protection", "Cuadros y protección", "Panels & protection"))], T("Électricité", "Electricidad", "Electrical"),
  T("Câbles, prises, interrupteurs et tableaux.", "Cables, enchufes, interruptores y cuadros.", "Cables, sockets, switches and panels."))
C("eclairage", T("Éclairage", "Iluminación", "Lighting"), "bulb",
  [("ampoules", T("Ampoules & tubes", "Bombillas y tubos", "Bulbs & tubes")), ("exterieur", T("Éclairage extérieur", "Iluminación exterior", "Outdoor lighting"))], None,
  T("Ampoules LED, réglettes, projecteurs et lampadaires.", "Bombillas LED, regletas, proyectores y farolas.", "LED bulbs, battens, floodlights and street lights."))
C("energie", T("Énergie & solaire", "Energía y solar", "Power & solar"), "sun",
  [("groupes", T("Groupes électrogènes", "Grupos electrógenos", "Generators")), ("solaire", T("Solaire", "Solar", "Solar")), ("onduleurs", T("Onduleurs & batteries", "SAI y baterías", "UPS & batteries"))], T("Énergie", "Energía", "Power"),
  T("Groupes, panneaux solaires, onduleurs et batteries.", "Grupos, paneles solares, SAI y baterías.", "Generators, solar panels, UPS and batteries."))
C("ventilation", T("Ventilation", "Ventilación", "Fans"), "fan",
  [("plafond", T("Ventilateurs de plafond", "Ventiladores de techo", "Ceiling fans")), ("pied", T("Ventilateurs sur pied", "Ventiladores de pie", "Standing fans"))], None,
  T("Ventilateurs de plafond, muraux et sur pied.", "Ventiladores de techo, pared y pie.", "Ceiling, wall and standing fans."))
# ELECTRONICS
C("mobile", "Téléphones & Tablettes", "phone", [("smartphones", "Smartphones"), ("tablettes", "Tablettes"), ("montres", "Montres connectées")], "Téléphones",
  T("Les derniers smartphones et tablettes.", "Los últimos smartphones y tabletas.", "The latest smartphones and tablets."))
C("info", "Informatique", "laptop", [("portables", "Ordinateurs portables"), ("impression", "Impression & bureautique"), ("peripheriques", T("Écrans & périphériques", "Monitores y periféricos", "Monitors & peripherals"))], None,
  T("Ordinateurs, écrans, impression et périphériques.", "Ordenadores, monitores, impresión y periféricos.", "Computers, monitors, printing and peripherals."))
C("accessoires-tech", T("Accessoires & audio", "Accesorios y audio", "Accessories & audio"), "earbuds",
  [("audio-tech", T("Audio & maison connectée", "Audio y hogar conectado", "Audio & smart home")), ("charge", T("Charge & protection", "Carga y protección", "Charging & cases")), ("photo", T("Photo & vidéo", "Foto y vídeo", "Photo & video"))], T("Accessoires", "Accesorios", "Accessories"),
  T("Écouteurs, chargeurs, coques et accessoires photo.", "Auriculares, cargadores, fundas y accesorios de foto.", "Earphones, chargers, cases and photo gear."))
C("papeterie", T("Fournitures de bureau", "Material de oficina", "Office supplies"), "pen",
  [("papier", T("Papier & classement", "Papel y archivo", "Paper & filing")), ("ecriture", T("Écriture", "Escritura", "Writing")), ("reseau", T("Réseau & stockage", "Red y almacenamiento", "Network & storage"))], T("Bureau", "Oficina", "Office"),
  T("Ramettes, classeurs, stylos, stockage et réseau.", "Resmas, archivadores, bolígrafos, almacenamiento y red.", "Paper, binders, pens, storage and networking."))
# PAINT
C("peinture", T("Peintures", "Pinturas", "Paints"), "paint",
  [("interieur", T("Intérieur", "Interior", "Interior")), ("exterieur", T("Extérieur & façade", "Exterior y fachada", "Exterior & masonry")), ("laques", T("Laques & vernis", "Lacas y barnices", "Gloss & varnish"))], None,
  T("Peintures fabriquées dans le pays, intérieur et extérieur.", "Pinturas fabricadas en el país, interior y exterior.", "Locally made paints, interior and exterior."))
C("preparation", T("Préparation des murs", "Preparación de paredes", "Surface preparation"), "trowel",
  [("enduits", T("Enduits", "Masillas", "Fillers")), ("sous-couches", T("Sous-couches & traitements", "Imprimaciones y tratamientos", "Primers & treatments"))], T("Préparation", "Preparación", "Preparation"),
  T("Enduits, sous-couches, antirouille et étanchéité.", "Masillas, imprimaciones, antióxido e impermeabilización.", "Fillers, primers, anti-rust and waterproofing."))
C("outils-peintre", T("Outils du peintre", "Herramientas de pintor", "Painting tools"), "roller",
  [("rouleaux", T("Rouleaux & pinceaux", "Rodillos y brochas", "Rollers & brushes")), ("protection", T("Protection & accessoires", "Protección y accesorios", "Protection & accessories"))], T("Outils", "Herramientas", "Tools"),
  T("Rouleaux, pinceaux, bâches et rubans.", "Rodillos, brochas, lonas y cintas.", "Rollers, brushes, dust sheets and tape."))
C("deco-murale", T("Décoration murale", "Decoración mural", "Wall décor"), "wall",
  [("papiers-peints", T("Papiers peints", "Papeles pintados", "Wallpaper")), ("effets", T("Peintures à effet", "Pinturas de efecto", "Effect paints"))], T("Déco murale", "Deco mural", "Wall décor"),
  T("Papiers peints et peintures décoratives.", "Papeles pintados y pinturas decorativas.", "Wallpaper and decorative paints."))
# PHARMACIES
C("conseil", T("Médicaments conseil", "Medicamentos sin receta", "Over-the-counter medicines"), "pill",
  [("douleur", T("Douleurs & fièvre", "Dolor y fiebre", "Pain & fever")), ("rhume", T("Rhume, toux & gorge", "Resfriado, tos y garganta", "Colds, cough & throat")), ("digestion", T("Digestion & transit", "Digestión y tránsito", "Digestion"))], T("Conseil", "Sin receta", "OTC"),
  T("Douleurs, fièvre, rhume et digestion : le conseil du pharmacien.", "Dolor, fiebre, resfriado y digestión: el consejo del farmacéutico.", "Pain, fever, colds and digestion: your pharmacist's advice."))
C("dermo", T("Dermo-cosmétique", "Dermocosmética", "Skincare"), "pill",
  [("visage", T("Visage", "Rostro", "Face")), ("corps", T("Corps & mains", "Cuerpo y manos", "Body & hands")), ("solaires", T("Solaires", "Solares", "Sun care"))], T("Soins", "Cuidados", "Skincare"),
  T("Soins visage, corps et protection solaire.", "Cuidado facial, corporal y protección solar.", "Face, body and sun care."))
C("hygiene-sante", T("Hygiène", "Higiene", "Hygiene"), "tooth",
  [("dentaire", T("Hygiène bucco-dentaire", "Higiene bucodental", "Oral care")), ("intime", T("Hygiène du corps", "Higiene corporal", "Body hygiene"))], None,
  T("Dentaire, déodorants et hygiène du corps.", "Dental, desodorantes e higiene corporal.", "Oral care, deodorants and body hygiene."))
C("complements", T("Vitamines & compléments", "Vitaminas y complementos", "Vitamins & supplements"), "capsule",
  [("vitamines", T("Vitamines & minéraux", "Vitaminas y minerales", "Vitamins & minerals")), ("forme", T("Forme & immunité", "Energía e inmunidad", "Energy & immunity")), ("phyto", T("Phyto & aromathérapie", "Fitoterapia y aromaterapia", "Herbal & aromatherapy"))], T("Compléments", "Complementos", "Supplements"),
  T("Vitamines, minéraux et compléments alimentaires.", "Vitaminas, minerales y complementos.", "Vitamins, minerals and supplements."))
C("maman-bebe", T("Maman & bébé", "Mamá y bebé", "Mother & baby"), "baby",
  [("laits", T("Laits & alimentation", "Leches y alimentación", "Milk & food")), ("soins-bebe", T("Soins & couches", "Cuidados y pañales", "Care & nappies"))], T("Bébé", "Bebé", "Baby"),
  T("Laits infantiles, couches et soins pour bébé.", "Leches infantiles, pañales y cuidados del bebé.", "Infant milk, nappies and baby care."))
C("materiel-medical", T("Matériel & premiers secours", "Material y primeros auxilios", "Medical devices & first aid"), "heart",
  [("autotest", T("Tension, glycémie, température", "Tensión, glucemia, temperatura", "BP, glucose & temperature")), ("secours", T("Premiers secours", "Primeros auxilios", "First aid")), ("moustiques", T("Anti-moustiques", "Antimosquitos", "Mosquito protection"))], T("Matériel", "Material", "Devices"),
  T("Tensiomètres, glucomètres, pansements et moustiquaires.", "Tensiómetros, glucómetros, apósitos y mosquiteras.", "Monitors, meters, dressings and mosquito nets."))
# LABS
C("hematologie", T("Hématologie & biochimie", "Hematología y bioquímica", "Haematology & chemistry"), "flask",
  [("hemato", T("Hématologie", "Hematología", "Haematology")), ("biochimie", T("Biochimie", "Bioquímica", "Biochemistry"))], T("Biologie", "Biología", "Lab tests"),
  T("NFS, glycémie, bilan rénal, hépatique et lipidique.", "Hemograma, glucemia, perfil renal, hepático y lipídico.", "Blood count, glucose, kidney, liver and lipid panels."))
C("hormones", T("Hormonologie", "Hormonas", "Hormones"), "dna",
  [("thyroide", T("Thyroïde", "Tiroides", "Thyroid")), ("fertilite", T("Fertilité & grossesse", "Fertilidad y embarazo", "Fertility & pregnancy"))], None,
  T("Thyroïde, fertilité, grossesse et marqueurs.", "Tiroides, fertilidad, embarazo y marcadores.", "Thyroid, fertility, pregnancy and markers."))
C("infectiologie", T("Infectiologie & sérologies", "Infecciosas y serologías", "Infectious disease"), "virus",
  [("paludisme", T("Paludisme & fièvres", "Malaria y fiebres", "Malaria & fevers")), ("serologies", T("Sérologies", "Serologías", "Serology")), ("urines-selles", T("Urines & selles", "Orina y heces", "Urine & stool"))], T("Infectiologie", "Infecciosas", "Infection"),
  T("Paludisme, typhoïde, hépatites, VIH, ECBU.", "Malaria, tifoidea, hepatitis, VIH, urocultivo.", "Malaria, typhoid, hepatitis, HIV, urine culture."))
C("bilans", T("Bilans & check-up", "Chequeos", "Check-ups"), "clipboard",
  [("packs", T("Bilans complets", "Chequeos completos", "Full panels")), ("entreprises", T("Entreprises & domicile", "Empresas y domicilio", "Corporate & home"))], T("Bilans", "Chequeos", "Check-ups"),
  T("Bilans prénuptial, prénatal, sportif et entreprise.", "Chequeos prenupcial, prenatal, deportivo y de empresa.", "Pre-marital, prenatal, sport and corporate check-ups."))
# TIRES
C("pneus", T("Pneumatiques", "Neumáticos", "Tyres"), "tire",
  [("tourisme", T("Tourisme", "Turismo", "Car")), ("4x4", T("4×4 & SUV", "4×4 y SUV", "4×4 & SUV")), ("utilitaire", T("Utilitaires & camions", "Utilitarios y camiones", "Vans & trucks"))], T("Pneus", "Neumáticos", "Tyres"),
  T("Pneus tourisme, 4×4, utilitaires et poids lourds.", "Neumáticos turismo, 4×4, utilitarios y camión.", "Car, 4×4, van and truck tyres."))
C("pieces", T("Pièces & batteries", "Recambios y baterías", "Parts & batteries"), "car",
  [("batteries", T("Batteries", "Baterías", "Batteries")), ("freinage", T("Freinage & filtres", "Frenos y filtros", "Brakes & filters")), ("visibilite", T("Visibilité", "Visibilidad", "Visibility"))], T("Pièces", "Recambios", "Parts"),
  T("Batteries, plaquettes, filtres, balais et ampoules.", "Baterías, pastillas, filtros, escobillas y lámparas.", "Batteries, pads, filters, wipers and bulbs."))
C("lubrifiants", T("Huiles & entretien", "Aceites y mantenimiento", "Oils & car care"), "oil",
  [("huiles", T("Huiles moteur", "Aceites de motor", "Engine oils")), ("liquides", T("Liquides & accessoires", "Líquidos y accesorios", "Fluids & accessories"))], T("Huiles", "Aceites", "Oils"),
  T("Huiles, liquides et accessoires de route.", "Aceites, líquidos y accesorios.", "Oils, fluids and road accessories."))
C("atelier", T("Atelier & motos", "Taller y motos", "Workshop & motorbikes"), "wrench",
  [("services", T("Services atelier", "Servicios de taller", "Workshop services")), ("motos", T("Motos & scooters", "Motos y scooters", "Motorbikes & scooters"))], T("Atelier", "Taller", "Workshop"),
  T("Vidange, montage, géométrie, motos et scooters.", "Cambio de aceite, montaje, alineación, motos y scooters.", "Oil change, fitting, alignment, motorbikes and scooters."))

CAT_IDS = {c["id"]: c for c in CATS}

PRODUCTS = []
def add(pid, sr, brand, name, cat, sub, img, price, old, flags, hl, specs, svg):
    if cat == "bebe-animaux":
        low = name.lower()
        if sub == "animaux": cat, sub = "animalerie", ("chats" if re.search(r"\bchat|cat |cat\b|gato", low) else "chiens")
        else: cat, sub = "bebe", ("bebe-repas" if re.search(r"biberon|lait|petits pots|céréales|potito", low) else "bebe-soins")
    assert cat in CAT_IDS, (pid, cat)
    assert sub in [s[0] for s in CAT_IDS[cat]["subs"]], (pid, cat, sub)
    PRODUCTS.append([pid, sr, brand, name, cat, sub, img, price, old, flags, hl, specs, svg])

def flags_for(pid, price):
    r = h(pid); old = None; f = ""
    if price and r < 22: old = nice(price * (1.12 + (h(pid + "x", 20) / 100.0)))
    if 22 <= r < 36: f = "new"
    if r >= 82: f = (f + " best").strip()
    return old, f

# ───────────── 1) Produits repris de la boutique d'origine (photos locales) ─────────────
SDC = json.loads(re.sub(r",\s*([\]}])", r"\1", SDC_JS))
homeOf = {"tv": "megastore-ela-nguema", "mobile": "electronics-office", "info": "electronics-office", "electro": "megastore-km5", "cuisine": "megastore-km5", "pro": "ventage-casa"}
for row in SDC:
    pid, brand, name, cat, sub, img, price, old, fl, hl, specs = row[:11]
    svg = row[11] if len(row) > 11 else None
    sr = homeOf.get(cat) or ("megastore-ela-nguema" if sub == "chambres" else "ventage-casa")
    if cat == "maison" and sub == "chambres": cat, sub = "literie", "lits"
    add(pid, sr, brand, name, cat, sub, img, price, old, fl, hl, specs, svg)

# ───────────── 2) Catalogue de démonstration photographié (DummyJSON) ─────────────
TR = {  # titre → (fr, es, en)
"Essence Mascara Lash Princess": ("Mascara Lash Princess", "Máscara Lash Princess", "Lash Princess mascara"),
"Eyeshadow Palette with Mirror": ("Palette de fards avec miroir", "Paleta de sombras con espejo", "Eyeshadow palette with mirror"),
"Powder Canister": ("Poudre libre", "Polvos sueltos", "Loose powder"),
"Red Lipstick": ("Rouge à lèvres rouge", "Pintalabios rojo", "Red lipstick"),
"Red Nail Polish": ("Vernis à ongles rouge", "Esmalte de uñas rojo", "Red nail polish"),
"Calvin Klein CK One": ("CK One Eau de Toilette", "CK One Eau de Toilette", "CK One Eau de Toilette"),
"Chanel Coco Noir Eau De": ("Coco Noir Eau de Parfum", None, None),
"Dior J'adore": ("J'adore Eau de Parfum", None, None),
"Dolce Shine Eau de": ("Dolce Shine Eau de Parfum", None, None),
"Gucci Bloom Eau de": ("Gucci Bloom Eau de Parfum", None, None),
"Annibale Colombo Bed": ("Lit capitonné Annibale Colombo", "Cama capitoné Annibale Colombo", "Annibale Colombo upholstered bed"),
"Annibale Colombo Sofa": ("Canapé Annibale Colombo", "Sofá Annibale Colombo", "Annibale Colombo sofa"),
"Bedside Table African Cherry": ("Table de chevet merisier d'Afrique", "Mesita de noche de cerezo africano", "African cherry bedside table"),
"Knoll Saarinen Executive Conference Chair": ("Fauteuil de conférence Saarinen", "Sillón de conferencia Saarinen", "Saarinen conference chair"),
"Wooden Bathroom Sink With Mirror": ("Meuble vasque bois avec miroir", "Mueble lavabo de madera con espejo", "Wooden vanity unit with mirror"),
"Apple": ("Pommes · le kg", "Manzanas · el kg", "Apples · per kg"),
"Beef Steak": ("Steak de bœuf · le kg", "Filete de ternera · el kg", "Beef steak · per kg"),
"Cat Food": ("Croquettes pour chat 2 kg", "Pienso para gatos 2 kg", "Cat food 2 kg"),
"Chicken Meat": ("Poulet entier · le kg", "Pollo entero · el kg", "Whole chicken · per kg"),
"Cooking Oil": ("Huile de cuisson 1 L", "Aceite de cocina 1 L", "Cooking oil 1 L"),
"Cucumber": ("Concombre · le kg", "Pepino · el kg", "Cucumber · per kg"),
"Dog Food": ("Croquettes pour chien 4 kg", "Pienso para perros 4 kg", "Dog food 4 kg"),
"Eggs": ("Œufs frais · plateau de 30", "Huevos frescos · bandeja de 30", "Fresh eggs · tray of 30"),
"Fish Steak": ("Pavé de poisson · le kg", "Filete de pescado · el kg", "Fish steak · per kg"),
"Green Bell Pepper": ("Poivron vert · le kg", "Pimiento verde · el kg", "Green pepper · per kg"),
"Green Chili Pepper": ("Piment vert · 250 g", "Guindilla verde · 250 g", "Green chilli · 250 g"),
"Honey Jar": ("Miel pur · pot 500 g", "Miel pura · tarro 500 g", "Pure honey · 500 g jar"),
"Ice Cream": ("Crème glacée · 1 L", "Helado · 1 L", "Ice cream · 1 L"),
"Juice": ("Jus de fruits · 1 L", "Zumo de frutas · 1 L", "Fruit juice · 1 L"),
"Kiwi": ("Kiwis · le kg", "Kiwis · el kg", "Kiwis · per kg"),
"Lemon": ("Citrons · le kg", "Limones · el kg", "Lemons · per kg"),
"Milk": ("Lait entier · 1 L", "Leche entera · 1 L", "Whole milk · 1 L"),
"Mulberry": ("Mûres · barquette 250 g", "Moras · tarrina 250 g", "Mulberries · 250 g punnet"),
"Nescafe Coffee": ("Café soluble Nescafé 200 g", "Café soluble Nescafé 200 g", "Nescafé instant coffee 200 g"),
"Potatoes": ("Pommes de terre · le kg", "Patatas · el kg", "Potatoes · per kg"),
"Protein Powder": ("Protéine en poudre 1 kg", "Proteína en polvo 1 kg", "Protein powder 1 kg"),
"Red Onions": ("Oignons rouges · le kg", "Cebollas rojas · el kg", "Red onions · per kg"),
"Rice": ("Riz blanc · 5 kg", "Arroz blanco · 5 kg", "White rice · 5 kg"),
"Soft Drinks": ("Sodas assortis · pack de 6", "Refrescos variados · pack de 6", "Assorted soft drinks · 6-pack"),
"Strawberry": ("Fraises · barquette 500 g", "Fresas · tarrina 500 g", "Strawberries · 500 g punnet"),
"Tissue Paper Box": ("Mouchoirs · boîte de 100", "Pañuelos · caja de 100", "Tissues · box of 100"),
"Water": ("Eau minérale · 1,5 L", "Agua mineral · 1,5 L", "Mineral water · 1.5 L"),
"Decoration Swing": ("Balancelle décorative", "Columpio decorativo", "Decorative swing"),
"Family Tree Photo Frame": ("Cadre photo arbre de famille", "Marco de fotos árbol familiar", "Family tree photo frame"),
"House Showpiece Plant": ("Plante décorative d'intérieur", "Planta decorativa de interior", "Indoor decorative plant"),
"Plant Pot": ("Cache-pot céramique", "Macetero de cerámica", "Ceramic plant pot"),
"Table Lamp": ("Lampe de table", "Lámpara de mesa", "Table lamp"),
"Bamboo Spatula": ("Spatule en bambou", "Espátula de bambú", "Bamboo spatula"),
"Black Aluminium Cup": ("Tasse aluminium noir", "Taza de aluminio negra", "Black aluminium cup"),
"Black Whisk": ("Fouet noir", "Batidor negro", "Black whisk"),
"Boxed Blender": ("Blender 1,5 L", "Batidora de vaso 1,5 L", "Blender 1.5 L"),
"Carbon Steel Wok": ("Wok en acier carbone", "Wok de acero al carbono", "Carbon steel wok"),
"Chopping Board": ("Planche à découper", "Tabla de cortar", "Chopping board"),
"Citrus Squeezer Yellow": ("Presse-agrumes jaune", "Exprimidor amarillo", "Yellow citrus squeezer"),
"Egg Slicer": ("Coupe-œuf", "Cortahuevos", "Egg slicer"),
"Electric Stove": ("Réchaud électrique 2 feux", "Hornillo eléctrico 2 fuegos", "Two-plate electric stove"),
"Fine Mesh Strainer": ("Passoire fine", "Colador fino", "Fine mesh strainer"),
"Fork": ("Fourchettes · lot de 6", "Tenedores · juego de 6", "Forks · set of 6"),
"Glass": ("Verres · lot de 6", "Vasos · juego de 6", "Glasses · set of 6"),
"Grater Black": ("Râpe noire", "Rallador negro", "Black grater"),
"Hand Blender": ("Mixeur plongeant", "Batidora de mano", "Hand blender"),
"Ice Cube Tray": ("Bac à glaçons", "Cubitera", "Ice cube tray"),
"Kitchen Sieve": ("Tamis de cuisine", "Tamiz de cocina", "Kitchen sieve"),
"Knife": ("Couteau de chef", "Cuchillo de chef", "Chef's knife"),
"Lunch Box": ("Boîte repas", "Fiambrera", "Lunch box"),
"Microwave Oven": ("Four micro-ondes 25 L", "Microondas 25 L", "Microwave oven 25 L"),
"Mug Tree Stand": ("Support à mugs", "Soporte para tazas", "Mug tree"),
"Pan": ("Poêle antiadhésive 28 cm", "Sartén antiadherente 28 cm", "Non-stick pan 28 cm"),
"Plate": ("Assiettes · lot de 6", "Platos · juego de 6", "Plates · set of 6"),
"Red Tongs": ("Pince de cuisine rouge", "Pinzas de cocina rojas", "Red kitchen tongs"),
"Silver Pot With Glass Cap": ("Faitout inox avec couvercle", "Olla de acero con tapa", "Stainless pot with lid"),
"Slotted Turner": ("Spatule ajourée", "Espumadera plana", "Slotted turner"),
"Spice Rack": ("Étagère à épices", "Especiero", "Spice rack"),
"Spoon": ("Cuillères · lot de 6", "Cucharas · juego de 6", "Spoons · set of 6"),
"Tray": ("Plateau de service", "Bandeja de servir", "Serving tray"),
"Wooden Rolling Pin": ("Rouleau à pâtisserie en bois", "Rodillo de madera", "Wooden rolling pin"),
"Yellow Peeler": ("Éplucheur jaune", "Pelador amarillo", "Yellow peeler"),
"New DELL XPS 13 9300 Laptop": ("Dell XPS 13 9300", None, None),
"Blue & Black Check Shirt": ("Chemise à carreaux bleu et noir", "Camisa de cuadros azul y negra", "Blue & black check shirt"),
"Gigabyte Aorus Men Tshirt": ("T-shirt homme Aorus", "Camiseta hombre Aorus", "Aorus men's T-shirt"),
"Man Plaid Shirt": ("Chemise écossaise homme", "Camisa escocesa hombre", "Men's plaid shirt"),
"Man Short Sleeve Shirt": ("Chemise manches courtes", "Camisa de manga corta", "Short-sleeve shirt"),
"Men Check Shirt": ("Chemise homme à carreaux", "Camisa de cuadros hombre", "Men's check shirt"),
"Nike Air Jordan 1 Red And Black": ("Air Jordan 1 rouge et noir", "Air Jordan 1 roja y negra", "Air Jordan 1 red and black"),
"Nike Baseball Cleats": ("Chaussures à crampons", "Zapatillas de tacos", "Baseball cleats"),
"Puma Future Rider Trainers": ("Baskets Future Rider", "Zapatillas Future Rider", "Future Rider trainers"),
"Sports Sneakers Off White & Red": ("Sneakers blanc cassé et rouge", "Zapatillas blanco roto y rojo", "Off-white & red sneakers"),
"Sports Sneakers Off White Red": ("Sneakers montantes blanc et rouge", "Zapatillas altas blanco y rojo", "High-top white & red sneakers"),
"Brown Leather Belt Watch": ("Montre bracelet cuir marron", "Reloj correa de piel marrón", "Brown leather strap watch"),
"Longines Master Collection": ("Longines Master Collection", None, None),
"Rolex Cellini Date Black Dial": ("Rolex Cellini Date cadran noir", "Rolex Cellini Date esfera negra", "Rolex Cellini Date black dial"),
"Rolex Cellini Moonphase": ("Rolex Cellini Moonphase", None, None),
"Rolex Datejust": ("Rolex Datejust", None, None),
"Rolex Submariner Watch": ("Rolex Submariner", None, None),
"Amazon Echo Plus": ("Enceinte connectée Echo Plus", "Altavoz inteligente Echo Plus", "Echo Plus smart speaker"),
"Apple Airpods": ("AirPods", None, None),
"Apple AirPods Max Silver": ("AirPods Max argent", "AirPods Max plata", "AirPods Max silver"),
"Apple Airpower Wireless Charger": ("Chargeur sans fil", "Cargador inalámbrico", "Wireless charger"),
"Apple HomePod Mini Cosmic Grey": ("HomePod mini gris sidéral", "HomePod mini gris espacial", "HomePod mini space grey"),
"Apple iPhone Charger": ("Chargeur iPhone USB-C", "Cargador iPhone USB-C", "iPhone USB-C charger"),
"Apple MagSafe Battery Pack": ("Batterie MagSafe", "Batería MagSafe", "MagSafe battery pack"),
"Apple Watch Series 4 Gold": ("Apple Watch Series 4 or", "Apple Watch Series 4 oro", "Apple Watch Series 4 gold"),
"Beats Flex Wireless Earphones": ("Écouteurs sans fil Beats Flex", "Auriculares inalámbricos Beats Flex", "Beats Flex wireless earphones"),
"iPhone 12 Silicone Case with MagSafe Plum": ("Coque silicone MagSafe iPhone 12 prune", "Funda de silicona MagSafe iPhone 12 ciruela", "iPhone 12 MagSafe silicone case, plum"),
"Monopod": ("Monopode photo", "Monopié de foto", "Camera monopod"),
"Selfie Lamp with iPhone": ("Lampe selfie", "Lámpara para selfies", "Selfie light"),
"Selfie Stick Monopod": ("Perche à selfie", "Palo selfie", "Selfie stick"),
"Generic Motorcycle": ("Moto 150 cm³", "Moto 150 cc", "150 cc motorbike"),
"Kawasaki Z800": ("Kawasaki Z800", None, None),
"MotoGP CI.H1": ("Moto sportive CI.H1", "Moto deportiva CI.H1", "CI.H1 sports bike"),
"Scooter Motorcycle": ("Scooter 125 cm³", "Scooter 125 cc", "125 cc scooter"),
"Sportbike Motorcycle": ("Moto sportive 600", "Moto deportiva 600", "600 sports bike"),
"Attitude Super Leaves Hand Soap": ("Savon mains Super Leaves", "Jabón de manos Super Leaves", "Super Leaves hand soap"),
"Olay Ultra Moisture Shea Butter Body Wash": ("Gel douche karité Ultra Moisture", "Gel de ducha karité Ultra Moisture", "Ultra Moisture shea body wash"),
"Vaseline Men Body and Face Lotion": ("Lotion corps et visage homme", "Loción cuerpo y rostro hombre", "Men's body & face lotion"),
"American Football": ("Ballon de football américain", "Balón de fútbol americano", "American football"),
"Baseball Ball": ("Balle de baseball", "Pelota de béisbol", "Baseball"),
"Baseball Glove": ("Gant de baseball", "Guante de béisbol", "Baseball glove"),
"Basketball": ("Ballon de basket", "Balón de baloncesto", "Basketball"),
"Basketball Rim": ("Panier de basket", "Canasta de baloncesto", "Basketball hoop"),
"Cricket Ball": ("Balle de cricket", "Pelota de críquet", "Cricket ball"),
"Cricket Bat": ("Batte de cricket", "Bate de críquet", "Cricket bat"),
"Cricket Helmet": ("Casque de cricket", "Casco de críquet", "Cricket helmet"),
"Cricket Wicket": ("Guichet de cricket", "Palos de críquet", "Cricket stumps"),
"Feather Shuttlecock": ("Volants en plumes", "Volantes de plumas", "Feather shuttlecocks"),
"Football": ("Ballon de football", "Balón de fútbol", "Football"),
"Golf Ball": ("Balles de golf", "Pelotas de golf", "Golf balls"),
"Iron Golf": ("Fer de golf", "Hierro de golf", "Golf iron"),
"Metal Baseball Bat": ("Batte de baseball métal", "Bate de béisbol metálico", "Metal baseball bat"),
"Tennis Ball": ("Balles de tennis · tube de 3", "Pelotas de tenis · tubo de 3", "Tennis balls · tube of 3"),
"Tennis Racket": ("Raquette de tennis", "Raqueta de tenis", "Tennis racket"),
"Volleyball": ("Ballon de volley", "Balón de voleibol", "Volleyball"),
"Black Sun Glasses": ("Lunettes de soleil noires", "Gafas de sol negras", "Black sunglasses"),
"Classic Sun Glasses": ("Lunettes de soleil classiques", "Gafas de sol clásicas", "Classic sunglasses"),
"Green and Black Glasses": ("Lunettes vert et noir", "Gafas verde y negro", "Green & black sunglasses"),
"Party Glasses": ("Lunettes fantaisie", "Gafas de fiesta", "Party sunglasses"),
"Sunglasses": ("Lunettes de soleil aviateur", "Gafas de sol aviador", "Aviator sunglasses"),
"iPad Mini 2021 Starlight": ("iPad mini lumière stellaire", "iPad mini blanco estelar", "iPad mini starlight"),
"Samsung Galaxy Tab S8 Plus Grey": ("Galaxy Tab S8+ gris", "Galaxy Tab S8+ gris", "Galaxy Tab S8+ grey"),
"Samsung Galaxy Tab White": ("Galaxy Tab blanche", "Galaxy Tab blanca", "Galaxy Tab white"),
"Blue Frock": ("Robe bleue", "Vestido azul", "Blue dress"),
"Girl Summer Dress": ("Robe d'été", "Vestido de verano", "Summer dress"),
"Gray Dress": ("Robe grise", "Vestido gris", "Grey dress"),
"Short Frock": ("Robe courte", "Vestido corto", "Short dress"),
"Tartan Dress": ("Robe tartan", "Vestido de tartán", "Tartan dress"),
"Blue Women's Handbag": ("Sac à main bleu", "Bolso azul", "Blue handbag"),
"Heshe Women's Leather Bag": ("Sac cuir Heshe", "Bolso de piel Heshe", "Heshe leather bag"),
"Prada Women Bag": ("Sac Prada", "Bolso Prada", "Prada bag"),
"White Faux Leather Backpack": ("Sac à dos blanc", "Mochila blanca", "White backpack"),
"Women Handbag Black": ("Sac à main noir", "Bolso negro", "Black handbag"),
"Black Women's Gown": ("Robe de soirée noire", "Vestido de noche negro", "Black evening gown"),
"Corset Leather With Skirt": ("Ensemble corset cuir et jupe", "Conjunto corsé de piel y falda", "Leather corset & skirt set"),
"Corset With Black Skirt": ("Corset et jupe noire", "Corsé y falda negra", "Corset with black skirt"),
"Dress Pea": ("Robe vert pois", "Vestido verde guisante", "Pea-green dress"),
"Marni Red & Black Suit": ("Tailleur Marni rouge et noir", "Traje Marni rojo y negro", "Marni red & black suit"),
"Green Crystal Earring": ("Boucles d'oreilles cristal vert", "Pendientes de cristal verde", "Green crystal earrings"),
"Green Oval Earring": ("Boucles d'oreilles ovales vertes", "Pendientes ovalados verdes", "Green oval earrings"),
"Tropical Earring": ("Boucles d'oreilles tropicales", "Pendientes tropicales", "Tropical earrings"),
"Black & Brown Slipper": ("Mules noir et marron", "Chanclas negro y marrón", "Black & brown slides"),
"Calvin Klein Heel Shoes": ("Escarpins à talons", "Zapatos de tacón", "Heeled shoes"),
"Golden Shoes Woman": ("Sandales dorées", "Sandalias doradas", "Gold sandals"),
"Pampi Shoes": ("Ballerines Pampi", "Bailarinas Pampi", "Pampi flats"),
"Red Shoes": ("Escarpins rouges", "Zapatos rojos", "Red pumps"),
"IWC Ingenieur Automatic Steel": ("IWC Ingenieur automatique acier", "IWC Ingenieur automático acero", "IWC Ingenieur automatic steel"),
"Rolex Datejust Women": ("Rolex Datejust femme", "Rolex Datejust mujer", "Rolex Datejust women's"),
"Watch Gold for Women": ("Montre dorée femme", "Reloj dorado mujer", "Women's gold watch"),
"Women's Wrist Watch": ("Montre femme bracelet", "Reloj de pulsera mujer", "Women's wristwatch"),
}
# catégorie DummyJSON → (showroom, rayon, sous-rayon, picto)
DJMAP = {
 "beauty": ("ventage-mall", "beaute", "maquillage", "lipstick"), "fragrances": ("ventage-mall", "parfums", None, "perfume"),
 "mens-shirts": ("ventage-mall", "mode", "chemises", "shirt"), "tops": ("ventage-mall", "mode", "robes", "shirt"), "womens-dresses": ("ventage-mall", "mode", "robes", "shirt"),
 "mens-shoes": ("ventage-mall", "chaussures", "homme", "shoe"), "womens-shoes": ("ventage-mall", "chaussures", "femme", "shoe"),
 "mens-watches": ("ventage-mall", "horlogerie", "montres-luxe", "watch"), "womens-watches": ("ventage-mall", "horlogerie", "montres-luxe", "watch"),
 "sunglasses": ("ventage-mall", "horlogerie", "solaires", "glasses"), "womens-bags": ("ventage-mall", "accessoires", "sacs", "bagl"), "womens-jewellery": ("ventage-mall", "accessoires", "bijoux", "gem"),
 "groceries": ("supermercado", None, None, "basket"), "furniture": ("ventage-casa", "maison", None, "sofa"), "home-decoration": ("ventage-casa", "maison", "deco", "lamp"),
 "kitchen-accessories": ("ventage-casa", "table", None, "plate"), "laptops": ("electronics-office", "info", "portables", "laptop"),
 "smartphones": ("electronics-office", "mobile", "smartphones", "phone"), "tablets": ("electronics-office", "mobile", "tablettes", "phone"),
 "mobile-accessories": ("electronics-office", "accessoires-tech", None, "earbuds"), "sports-accessories": ("megastore-ela-nguema", "sport", None, "ball"),
 "skin-care": ("amanda-pharmacies", "dermo", "corps", "pill"), "motorcycle": ("tires-auto", "atelier", "motos", "moto"),
}
GROC = {"Apple": "fruits-legumes", "Cucumber": "fruits-legumes", "Green Bell Pepper": "fruits-legumes", "Green Chili Pepper": "fruits-legumes", "Kiwi": "fruits-legumes", "Lemon": "fruits-legumes", "Mulberry": "fruits-legumes", "Potatoes": "fruits-legumes", "Red Onions": "fruits-legumes", "Strawberry": "fruits-legumes",
        "Beef Steak": "boucherie", "Chicken Meat": "boucherie", "Fish Steak": "boucherie", "Eggs": "cremerie", "Milk": "cremerie", "Ice Cream": "cremerie",
        "Cooking Oil": ("epicerie", "base"), "Rice": ("epicerie", "base"), "Honey Jar": ("epicerie", "petit-dej"), "Protein Powder": ("epicerie", "petit-dej"), "Nescafe Coffee": ("boissons", "cafe-the"),
        "Juice": ("boissons", "eaux-jus"), "Water": ("boissons", "eaux-jus"), "Soft Drinks": ("boissons", "sodas"), "Tissue Paper Box": ("entretien", "hygiene"), "Cat Food": ("bebe-animaux", "animaux"), "Dog Food": ("bebe-animaux", "animaux")}
KITCHEN_APPL = {"Boxed Blender", "Electric Stove", "Hand Blender", "Microwave Oven"}
HL = {
 "parfums": [T("Flacon vaporisateur", "Frasco vaporizador", "Spray bottle"), T("Authenticité garantie", "Autenticidad garantizada", "Guaranteed authentic")],
 "beaute": [T("Tenue longue durée", "Larga duración", "Long-lasting"), T("Testé dermatologiquement", "Testado dermatológicamente", "Dermatologically tested")],
 "mode": [T("Coupe actuelle", "Corte actual", "Modern fit"), T("Plusieurs tailles disponibles", "Varias tallas disponibles", "Several sizes available")],
 "chaussures": [T("Pointures du 36 au 46", "Tallas del 36 al 46", "Sizes 36 to 46"), T("Confort toute la journée", "Comodidad todo el día", "All-day comfort")],
 "horlogerie": [T("Garantie internationale", "Garantía internacional", "International warranty"), T("Écrin et certificat", "Estuche y certificado", "Box and papers")],
 "accessoires": [T("Finitions soignées", "Acabados cuidados", "Fine finishing"), T("Emballage cadeau offert", "Envoltorio de regalo gratis", "Free gift wrapping")],
 "frais": [T("Arrivage frais", "Llegada fresca", "Fresh delivery"), T("Prix au poids", "Precio al peso", "Priced by weight")],
 "epicerie": [T("Qualité contrôlée", "Calidad controlada", "Quality checked")], "boissons": [T("Servir frais", "Servir frío", "Serve chilled")],
 "entretien": [T("Format familial", "Formato familiar", "Family size")], "bebe-animaux": [T("Formule complète", "Fórmula completa", "Complete formula")], "bebe": [T("Formule complète", "Fórmula completa", "Complete formula")], "animalerie": [T("Formule complète", "Fórmula completa", "Complete formula")],
 "maison": [T("Livraison et montage", "Entrega y montaje", "Delivery and assembly"), T("Finitions au choix", "Acabados a elegir", "Choice of finishes")],
 "table": [T("Passe au lave-vaisselle", "Apto para lavavajillas", "Dishwasher safe"), T("Qualité professionnelle", "Calidad profesional", "Professional quality")],
 "cuisine": [T("Garantie 1 an", "Garantía 1 año", "1-year warranty")], "info": [T("Garantie constructeur", "Garantía del fabricante", "Manufacturer warranty"), T("Configuration offerte", "Configuración incluida", "Free set-up")],
 "mobile": [T("Débloqué tous opérateurs", "Libre para todos los operadores", "Unlocked for all networks"), T("Garantie constructeur", "Garantía del fabricante", "Manufacturer warranty")],
 "accessoires-tech": [T("Compatible iPhone et Android", "Compatible con iPhone y Android", "Works with iPhone and Android")],
 "sport": [T("Usage intensif", "Uso intensivo", "Built for heavy use")], "dermo": [T("Testé dermatologiquement", "Testado dermatológicamente", "Dermatologically tested")],
 "atelier": [T("Garantie et entretien en atelier", "Garantía y mantenimiento en taller", "Warranty and in-house servicing"), T("Immatriculation sur demande", "Matriculación bajo pedido", "Registration on request")],
}
MALL_REAL = {"mens-shirts", "tops", "womens-dresses", "mens-shoes", "womens-shoes", "mens-watches", "womens-watches", "sunglasses", "womens-bags", "womens-jewellery"}
for p in DJ:
    if p["category"] not in DJMAP or p["category"] in MALL_REAL: continue
    sr, cat, sub, icon = DJMAP[p["category"]]
    title = p["title"]
    if p["category"] == "groceries":
        g = GROC[title]; cat, sub = (g if isinstance(g, tuple) else ("frais", g))
    if p["category"] == "fragrances":
        sub = "homme" if title.startswith(("Calvin", "Dolce")) else "femme"
    if p["category"] == "furniture":
        sub = {"Annibale Colombo Bed": "chambres", "Annibale Colombo Sofa": "salons", "Bedside Table African Cherry": "chambres", "Knoll Saarinen Executive Conference Chair": "fauteuils", "Wooden Bathroom Sink With Mirror": "deco"}[title]
    if p["category"] == "kitchen-accessories":
        if title in KITCHEN_APPL: sr, cat, sub = "megastore-km5", "cuisine", ("cuisson" if title in ("Electric Stove", "Microwave Oven") else "petit")
        else: sub = "cuisson-casa" if title in ("Carbon Steel Wok", "Pan", "Silver Pot With Glass Cap") else ("vaisselle" if title in ("Black Aluminium Cup", "Fork", "Glass", "Plate", "Spoon", "Tray", "Mug Tree Stand") else "ustensiles")
    if p["category"] == "mobile-accessories":
        if title == "TV Studio Camera Pedestal": continue
        sub = "photo" if title in ("Monopod", "Selfie Lamp with iPhone", "Selfie Stick Monopod") else ("charge" if title in ("Apple Airpower Wireless Charger", "Apple iPhone Charger", "Apple MagSafe Battery Pack", "iPhone 12 Silicone Case with MagSafe Plum") else "audio-tech")
        if title == "Apple Watch Series 4 Gold": cat, sub = "mobile", "montres"
    if p["category"] == "sports-accessories":
        sub = "ballons" if any(k in title for k in ("Football", "Basketball", "Volleyball", "Baseball Ball", "Cricket Ball", "Cricket Wicket", "Basketball Rim")) else "raquettes"
        if title in ("Cricket Helmet", "Baseball Glove", "Golf Ball", "Iron Golf"): sub = "fitness" if title == "Cricket Helmet" else "raquettes"
    if p["category"] == "home-decoration" and title == "Table Lamp": cat, sub = "luminaires", "lampes"
    fr, es, en = TR.get(title, (title, None, None))
    name = T(fr, es, en)
    path = re.sub(r"^https://cdn\.dummyjson\.com/", "", p["thumbnail"]).rsplit("/", 1)[0]
    img = "dj:%s:%d" % (path.replace("product-images/", ""), len(p["images"]))
    pid = "dj-" + re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    price = nice(p["price"] * 600)
    old, fl = flags_for(pid, price)
    brand = p.get("brand") or ({"supermercado": "Ventage Family", "ventage-casa": "Ventage Home", "megastore-ela-nguema": "Ventage Sport"}.get(sr, "Ventage"))
    add(pid, sr, brand, name, cat, sub, img, price, old, fl, HL.get(cat, []), {}, icon)

# ───────────── 2 bis) Ventage MALL : catalogue réel (photos dans assets/mall) ─────────────
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mall_tr import MALL_TR
import subprocess
MALL = json.loads(subprocess.check_output(["node", "-e", "console.log(JSON.stringify(require(process.argv[1])))", os.path.join(ROOT, "tools/mall-products.js")]))
FIX_IMG = {"tous-camille-necklace": "brand-tous-camille", "tous-two-tone-bear-necklace": "brand-tous-two-tone-bear"}
SHOE = re.compile(r"zapat|mocas|sneaker|chaussure|derb|escarpin|sandale", re.I)
def mall_place(p):
    n, r = p["name"].lower(), p["rayon"]
    if r == "relojes": return "horlogerie", "montres-luxe", "watch"
    if r == "gafas": return "horlogerie", "solaires", "glasses"
    if r == "joyas": return "accessoires", "bijoux", "gem"
    if r == "maletas": return "bagagerie", ("sacs-voyage" if "neceser" in n else "valises"), "suitcase"
    if r == "ninos": return "enfants", "enfant", "baby"
    if r == "accesorios": return "accessoires", ("petite-maro" if re.search(r"portefeuille|porte-cartes|wallet", n) else "sacs"), "bagl"
    if SHOE.search(n): return "chaussures", ("homme" if r == "hombre" else "femme"), "shoe"
    if r == "mujer":
        if "bolso" in n: return "accessoires", "sacs", "bagl"
        if re.search(r"veste|doudoune|chaqueta|blazer|cazadora", n): return "femme", "vestes-f", "dress"
        if re.search(r"jean|legging|survêtement|vaquero", n): return "femme", "bas", "dress"
        if re.search(r"blouse|cardigan|pull|top", n): return "femme", "hauts", "dress"
        return "femme", "robes", "dress"
    if re.search(r"jean|vaquero|chino", n): return "homme", "pantalons", "shirt"
    if re.search(r"chándal|survêtement|chaqueta de chándal", n) or p["brand"] == "EA7" and "zip" in p["id"]: return "homme", "sportswear", "shirt"
    if re.search(r"americana|esmoquin|cazadora|blazer", n): return "homme", "vestes", "shirt"
    return "homme", "polos-chemises", "shirt"
HL_MALL = {"homme": HL["mode"], "femme": HL["mode"], "chaussures": HL["chaussures"], "horlogerie": HL["horlogerie"], "accessoires": HL["accessoires"],
           "bagagerie": [T("Garantie constructeur", "Garantía del fabricante", "Manufacturer warranty"), T("Roues multidirectionnelles", "Ruedas multidireccionales", "Spinner wheels")],
           "enfants": [T("Matières douces", "Tejidos suaves", "Soft fabrics"), T("Plusieurs tailles disponibles", "Varias tallas disponibles", "Several sizes available")]}
seen_img = set()
for p in MALL:
    img = FIX_IMG.get(p["id"]) or os.path.basename(p["image"])[:-5]
    if img in seen_img: continue
    seen_img.add(img)
    cat, sub, icon = mall_place(p)
    base = p["price"]; price, old = (nice(base * 0.7), base) if p.get("promo") else (base, None)
    fl = ("new" if h(p["id"]) < 18 else "") + (" best" if h(p["id"] + "b") < 22 else "")
    sizes = [s for s in (p.get("sizes") or []) if s not in ("Única",)]
    specs = {"Tailles": " · ".join(sizes)} if sizes else {}
    hl = [T("Article authentique", "Artículo auténtico", "Authentic item")] + HL_MALL.get(cat, [])[:2]
    add("vm-" + p["id"], "ventage-mall", p["brand"], MALL_TR[p["id"]], cat, sub, "vm:" + img, price, old, fl.strip(), hl, specs, icon)

# ───────────── 3) Gabarits : complètent chaque showroom jusqu'à ~100 articles ─────────────
def G(sr, cat, sub, icon, brands, tpl, variants, hl=(), specs=None, quote=False, base=None, cross=False):
    if cross:
        for b in brands: G(sr, cat, sub, icon, [b], tpl, variants, hl, specs, quote)
        return
    """tpl « fr|es|en » avec {v} ; variants = [(v_fr, v_es, v_en, prix)] ou [(v, prix)]"""
    tf, te, tn = tpl.split("|") if "|" in tpl else (tpl, tpl, tpl)
    for i, var in enumerate(variants):
        if len(var) == 2: vf = ve = vn = str(var[0]); price = var[1]
        else: vf, ve, vn, price = var
        brand = brands[i % len(brands)]
        fr, es, en = tf.replace("{v}", vf).replace("{b}", brand), te.replace("{v}", ve).replace("{b}", brand), tn.replace("{v}", vn).replace("{b}", brand)
        pid = "g-" + hashlib.md5((sr + fr).encode()).hexdigest()[:10]
        pr = None if (quote or not price) else nice(price)
        old, fl = flags_for(pid, pr)
        sp = {}
        if specs:
            for k, v in specs.items(): sp[k] = v.replace("{v}", vf) if isinstance(v, str) else v
        add(pid, sr, brand, T(fr, es, en), cat, sub, None, pr, old, fl, list(hl), sp, icon)

S = "ventage-mall"
G(S, "parfums", "homme", "perfume", ["Dior", "Chanel", "Hugo Boss", "Armani", "Yves Saint Laurent", "Paco Rabanne"], "{b} {v}", [("Sauvage Elixir 60 ml", 125000), ("Bleu de Chanel EDP 100 ml", 118000), ("Boss Bottled EDT 100 ml", 76000), ("Acqua di Giò EDP 75 ml", 89000), ("Y EDP 100 ml", 95000), ("1 Million EDT 100 ml", 82000)], HL["parfums"])
G(S, "parfums", "femme", "perfume", ["Lancôme", "Yves Saint Laurent", "Chanel", "Armani", "Dior", "Paco Rabanne"], "{b} {v}", [("La Vie est Belle EDP 100 ml", 98000), ("Libre EDP 90 ml", 105000), ("N°5 EDP 100 ml", 135000), ("Sì EDP 100 ml", 99000), ("Miss Dior EDP 100 ml", 112000), ("Olympéa EDP 80 ml", 84000)], HL["parfums"])
G(S, "beaute", "soins-beaute", "lipstick", ["Lancôme", "Clarins", "Estée Lauder", "Dior"], "{b} {v}", [("Sérum Advanced Génifique 50 ml", "Sérum Advanced Génifique 50 ml", "Advanced Génifique serum 50 ml", 68000), ("Crème Multi-Active jour 50 ml", "Crema Multi-Active día 50 ml", "Multi-Active day cream 50 ml", 42000), ("Sérum Advanced Night Repair 50 ml", "Sérum Advanced Night Repair 50 ml", "Advanced Night Repair serum 50 ml", 74000), ("Fond de teint Forever 30 ml", "Base de maquillaje Forever 30 ml", "Forever foundation 30 ml", 39000)], HL["beaute"])
pass
pass
pass
pass

S = "supermercado"
G(S, "epicerie", "base", "basket", ["Ventage Family", "Panzani", "Uncle Ben's"], T("{v}", "{v}", "{v}"), [("Riz parfumé 25 kg", "Arroz aromático 25 kg", "Fragrant rice 25 kg", 19500), ("Riz long grain 5 kg", "Arroz grano largo 5 kg", "Long-grain rice 5 kg", 5200), ("Spaghetti 500 g", "Espaguetis 500 g", "Spaghetti 500 g", 750), ("Macaroni 500 g", "Macarrones 500 g", "Macaroni 500 g", 750), ("Farine de blé 5 kg", "Harina de trigo 5 kg", "Wheat flour 5 kg", 4200), ("Semoule de maïs 1 kg", "Sémola de maíz 1 kg", "Maize meal 1 kg", 1200), ("Sucre en poudre 1 kg", "Azúcar 1 kg", "Sugar 1 kg", 1100), ("Sel iodé 1 kg", "Sal yodada 1 kg", "Iodised salt 1 kg", 450), ("Huile de palme 1 L", "Aceite de palma 1 L", "Palm oil 1 L", 1500), ("Huile d'arachide 5 L", "Aceite de cacahuete 5 L", "Groundnut oil 5 L", 9800)], HL["epicerie"])
G(S, "epicerie", "conserves", "can", ["Ventage Family", "Heinz", "Maggi"], T("{v}", "{v}", "{v}"), [("Concentré de tomate 400 g", "Concentrado de tomate 400 g", "Tomato paste 400 g", 900), ("Sardines à l'huile · lot de 3", "Sardinas en aceite · pack de 3", "Sardines in oil · pack of 3", 2400), ("Thon au naturel · lot de 3", "Atún al natural · pack de 3", "Tuna in brine · pack of 3", 3600), ("Haricots rouges 400 g", "Alubias rojas 400 g", "Red kidney beans 400 g", 850), ("Petits pois carottes 400 g", "Guisantes y zanahorias 400 g", "Peas & carrots 400 g", 900), ("Ketchup 500 g", "Kétchup 500 g", "Ketchup 500 g", 1500), ("Mayonnaise 500 g", "Mayonesa 500 g", "Mayonnaise 500 g", 1800), ("Bouillon cube · boîte de 60", "Pastillas de caldo · caja de 60", "Stock cubes · box of 60", 2200), ("Lait concentré sucré 397 g", "Leche condensada 397 g", "Sweetened condensed milk 397 g", 1100)], HL["epicerie"])
G(S, "epicerie", "petit-dej", "cup", ["Nestlé", "Kellogg's", "Ventage Family"], T("{v}", "{v}", "{v}"), [("Céréales Corn Flakes 500 g", "Cereales Corn Flakes 500 g", "Corn Flakes cereal 500 g", 3200), ("Chocolat en poudre 1 kg", "Cacao en polvo 1 kg", "Chocolate drink powder 1 kg", 4900), ("Lait en poudre 900 g", "Leche en polvo 900 g", "Powdered milk 900 g", 6500), ("Confiture de fraises 370 g", "Mermelada de fresa 370 g", "Strawberry jam 370 g", 1900), ("Pâte à tartiner 750 g", "Crema para untar 750 g", "Chocolate spread 750 g", 4800), ("Biscuits sablés · paquet familial", "Galletas · paquete familiar", "Shortbread biscuits · family pack", 1600)], HL["epicerie"])
G(S, "boissons", "eaux-jus", "bottle", ["Ventage Family", "Tropicana", "Evian"], T("{v}", "{v}", "{v}"), [("Eau minérale 12 × 1,5 L", "Agua mineral 12 × 1,5 L", "Mineral water 12 × 1.5 L", 4500), ("Eau gazeuse 6 × 1 L", "Agua con gas 6 × 1 L", "Sparkling water 6 × 1 L", 4200), ("Jus d'orange 1 L · lot de 6", "Zumo de naranja 1 L · pack de 6", "Orange juice 1 L · 6-pack", 7200), ("Jus d'ananas 1 L", "Zumo de piña 1 L", "Pineapple juice 1 L", 1300), ("Jus de mangue 1 L", "Zumo de mango 1 L", "Mango juice 1 L", 1300), ("Jus multivitaminé 1 L", "Zumo multivitamínico 1 L", "Multivitamin juice 1 L", 1400)], HL["boissons"])
G(S, "boissons", "sodas", "bottle", ["Coca-Cola", "Fanta", "Sprite", "Schweppes"], T("{b} {v}", "{b} {v}", "{b} {v}"), [("canettes 33 cl · pack de 24", "latas 33 cl · pack de 24", "33 cl cans · 24-pack", 12500), ("1,5 L · pack de 6", "1,5 L · pack de 6", "1.5 L · 6-pack", 6900), ("canettes 33 cl · pack de 24", "latas 33 cl · pack de 24", "33 cl cans · 24-pack", 12500), ("Tonic 1 L · pack de 6", "Tónica 1 L · pack de 6", "Tonic 1 L · 6-pack", 7500)], HL["boissons"])
G(S, "boissons", "cafe-the", "cup", ["Nescafé", "Lipton", "Lavazza"], T("{v}", "{v}", "{v}"), [("Café moulu 250 g", "Café molido 250 g", "Ground coffee 250 g", 3500), ("Thé noir · 100 sachets", "Té negro · 100 bolsitas", "Black tea · 100 bags", 3200), ("Café en grains 1 kg", "Café en grano 1 kg", "Coffee beans 1 kg", 12500), ("Thé vert menthe · 25 sachets", "Té verde menta · 25 bolsitas", "Mint green tea · 25 bags", 1500)], HL["boissons"])
G(S, "entretien", "menage", "spray", ["Ariel", "Omo", "Javel La Croix", "Mr Propre"], T("{v}", "{v}", "{v}"), [("Lessive en poudre 5 kg", "Detergente en polvo 5 kg", "Washing powder 5 kg", 12500), ("Lessive liquide 3 L", "Detergente líquido 3 L", "Liquid detergent 3 L", 9800), ("Eau de Javel 5 L", "Lejía 5 L", "Bleach 5 L", 3900), ("Nettoyant multi-surfaces 1 L", "Limpiador multiusos 1 L", "Multi-surface cleaner 1 L", 2100), ("Liquide vaisselle 1 L", "Lavavajillas a mano 1 L", "Washing-up liquid 1 L", 1600), ("Insecticide 400 ml", "Insecticida 400 ml", "Insect spray 400 ml", 2500), ("Sacs poubelle 50 L · 30", "Bolsas de basura 50 L · 30", "Bin bags 50 L · 30", 1800)], HL["entretien"])
G(S, "entretien", "hygiene", "soap", ["Colgate", "Dove", "Ventage Family", "Gillette"], T("{v}", "{v}", "{v}"), [("Dentifrice 100 ml · lot de 3", "Pasta de dientes 100 ml · pack de 3", "Toothpaste 100 ml · 3-pack", 3200), ("Savon de toilette · lot de 4", "Jabón de tocador · pack de 4", "Bath soap · 4-pack", 2400), ("Papier toilette · 24 rouleaux", "Papel higiénico · 24 rollos", "Toilet paper · 24 rolls", 7900), ("Rasoirs jetables · 10", "Maquinillas desechables · 10", "Disposable razors · 10", 3500), ("Shampoing 400 ml", "Champú 400 ml", "Shampoo 400 ml", 2800), ("Déodorant 150 ml", "Desodorante 150 ml", "Deodorant 150 ml", 2500)], HL["entretien"])
G(S, "bebe-animaux", "bebe", "baby", ["Pampers", "Nestlé", "Ventage Family"], T("{v}", "{v}", "{v}"), [("Couches taille 3 · 60", "Pañales talla 3 · 60", "Nappies size 3 · 60", 11500), ("Couches taille 4 · 52", "Pañales talla 4 · 52", "Nappies size 4 · 52", 11500), ("Petits pots légumes · lot de 4", "Potitos de verduras · pack de 4", "Vegetable baby food · 4-pack", 3800), ("Lingettes bébé · lot de 3", "Toallitas de bebé · pack de 3", "Baby wipes · 3-pack", 3900), ("Céréales bébé 400 g", "Cereales infantiles 400 g", "Baby cereal 400 g", 3600)], HL["bebe-animaux"])

S = "megastore-km5"
G(S, "electro", "froid", "fridge", ["Samsung", "LG", "Hisense", "Haier", "Beko"], T("Réfrigérateur {v}", "Frigorífico {v}", "Fridge, {v}"), [("combiné 340 L", "combi 340 L", "340 L fridge-freezer", 395000), ("double porte 450 L", "dos puertas 450 L", "450 L double-door", 545000), ("side-by-side 520 L", "side-by-side 520 L", "520 L side-by-side", 845000), ("table top 120 L", "bajo encimera 120 L", "120 L under-counter", 145000), ("multi-portes 560 L", "multipuerta 560 L", "560 L multi-door", 1290000), ("vitré boissons 300 L", "expositor de bebidas 300 L", "300 L glass-door drinks", 465000)], [T("Froid ventilé No Frost", "Frío No Frost", "No Frost cooling"), T("Compresseur Inverter", "Compresor Inverter", "Inverter compressor")])
G(S, "electro", "froid", "freezer", ["Haier", "Hisense", "Beko"], T("Congélateur coffre {v}", "Congelador horizontal {v}", "{v} chest freezer"), [("200 L", 215000), ("400 L", 345000), ("500 L", 415000)], [T("Conserve le froid en coupure", "Conserva el frío en cortes", "Holds cold in power cuts")])
G(S, "electro", "lavage", "washer", ["LG", "Samsung", "Beko", "Hisense"], T("Lave-linge {v}", "Lavadora {v}", "Washing machine, {v}"), [("hublot 7 kg", "carga frontal 7 kg", "7 kg front-loader", 245000), ("hublot 10 kg", "carga frontal 10 kg", "10 kg front-loader", 445000), ("top 8 kg", "carga superior 8 kg", "8 kg top-loader", 265000), ("semi-automatique 12 kg", "semiautomática 12 kg", "12 kg twin-tub", 165000), ("lavante-séchante 9 kg", "lavasecadora 9 kg", "9 kg washer-dryer", 525000)], [T("Moteur Inverter silencieux", "Motor Inverter silencioso", "Quiet Inverter motor")])
G(S, "electro", "clim", "ac", ["LG", "Samsung", "Midea", "Gree", "Hisense"], T("Climatiseur {v}", "Aire acondicionado {v}", "Air conditioner, {v}"), [("split 9 000 BTU", "split 9 000 BTU", "9,000 BTU split", 275000), ("split 24 000 BTU", "split 24 000 BTU", "24,000 BTU split", 595000), ("armoire 48 000 BTU", "de columna 48 000 BTU", "48,000 BTU floor-standing", 1450000), ("cassette 36 000 BTU", "cassette 36 000 BTU", "36,000 BTU cassette", 1150000), ("mobile 12 000 BTU", "portátil 12 000 BTU", "12,000 BTU portable", 295000)], [T("Technologie Inverter", "Tecnología Inverter", "Inverter technology"), T("Installation sur rendez-vous", "Instalación con cita", "Installation by appointment")])
G(S, "cuisine", "cuisson", "stove", ["Nasco", "Beko", "Samsung", "Midea"], T("{v}", "{v}", "{v}"), [("Cuisinière 5 feux 90 cm", "Cocina 5 fuegos 90 cm", "5-burner cooker 90 cm", 345000), ("Table de cuisson gaz 4 feux", "Placa de gas 4 fuegos", "4-burner gas hob", 125000), ("Plaque à induction 2 zones", "Placa de inducción 2 zonas", "2-zone induction hob", 89000), ("Four électrique 45 L", "Horno eléctrico 45 L", "45 L electric oven", 95000), ("Hotte aspirante 60 cm", "Campana extractora 60 cm", "60 cm cooker hood", 145000), ("Micro-ondes 30 L grill", "Microondas 30 L grill", "30 L grill microwave", 105000)], HL["cuisine"])
G(S, "cuisine", "petit", "blender", ["Moulinex", "Philips", "Tefal", "Kenwood", "Russell Hobbs"], T("{v}", "{v}", "{v}"), [("Bouilloire 1,7 L", "Hervidor 1,7 L", "1.7 L kettle", 19500), ("Friteuse sans huile 5 L", "Freidora de aire 5 L", "5 L air fryer", 75000), ("Robot pâtissier 1000 W", "Robot de repostería 1000 W", "1000 W stand mixer", 145000), ("Cuiseur à riz 1,8 L", "Arrocera 1,8 L", "1.8 L rice cooker", 29000), ("Grille-pain 2 fentes", "Tostadora 2 ranuras", "2-slice toaster", 21000), ("Machine à café expresso", "Cafetera espresso", "Espresso machine", 135000), ("Presse-agrumes électrique", "Exprimidor eléctrico", "Electric juicer", 18500), ("Robot multifonction", "Procesador de alimentos", "Food processor", 89000)], HL["cuisine"])
G(S, "soin-maison", "aspirateurs", "vacuum", ["Philips", "Samsung", "Rowenta", "Kärcher"], T("Aspirateur {v}", "Aspiradora {v}", "{v} vacuum cleaner"), [("traîneau 2000 W", "de trineo 2000 W", "2000 W cylinder", 79000), ("balai sans fil", "escoba sin cable", "cordless stick", 165000), ("robot connecté", "robot conectado", "connected robot", 225000), ("eau et poussière 20 L", "agua y polvo 20 L", "20 L wet & dry", 69000)], [T("Filtre HEPA", "Filtro HEPA", "HEPA filter")])
G(S, "soin-maison", "repassage", "iron", ["Philips", "Tefal", "Rowenta"], T("{v}", "{v}", "{v}"), [("Fer à repasser vapeur 2400 W", "Plancha de vapor 2400 W", "2400 W steam iron", 25000), ("Centrale vapeur 6 bars", "Centro de planchado 6 bar", "6-bar steam generator", 145000), ("Défroisseur vertical", "Vaporizador vertical", "Garment steamer", 45000), ("Table à repasser", "Tabla de planchar", "Ironing board", 32000)], [])
G(S, "eau", "citernes", "tank", ["Ventage"], T("Citerne d'eau Ventage {v}", "Depósito de agua Ventage {v}", "Ventage water tank, {v}"), [("500 L", 65000), ("1 000 L", 105000), ("2 000 L", 185000), ("3 000 L", 265000), ("5 000 L", 425000), ("10 000 L", 845000)], [T("Fabriquée en Guinée équatoriale", "Fabricada en Guinea Ecuatorial", "Made in Equatorial Guinea"), T("Polyéthylène anti-UV", "Polietileno anti-UV", "UV-resistant polyethylene")], {"Capacité": "{v}"})
G(S, "eau", "chauffe-eau", "heater", ["Ariston", "Thermor", "Atlantic"], T("Chauffe-eau électrique {v}", "Termo eléctrico {v}", "{v} electric water heater"), [("50 L", 95000), ("80 L", 125000), ("100 L", 145000), ("instantané 5,5 kW", "instantáneo 5,5 kW", "5.5 kW instant", 45000)], [T("Cuve émaillée", "Cuba esmaltada", "Enamelled tank")])
G(S, "eau", "traitement", "drop", ["Ventage", "Brita", "Midea"], T("{v}", "{v}", "{v}"), [("Fontaine à eau chaud/froid", "Fuente de agua fría/caliente", "Hot & cold water dispenser", 95000), ("Purificateur osmose inverse", "Purificador de ósmosis inversa", "Reverse-osmosis purifier", 185000), ("Surpresseur 1 HP", "Grupo de presión 1 HP", "1 HP booster pump", 135000), ("Pompe immergée 1 HP", "Bomba sumergible 1 HP", "1 HP submersible pump", 165000)], [])

S = "megastore-ela-nguema"
G(S, "tv", "smart-tv", "tv", ["Samsung", "LG", "Hisense", "TCL", "Sony"], T("Smart TV {v}", "Smart TV {v}", "{v} Smart TV"), [("4K 43″", 215000), ("4K 65″", 545000), ("QLED 55″", 465000), ("QLED 75″", 995000), ("4K 85″", 1650000), ("OLED 55″", 995000), ("Full HD 32″", 109000), ("4K 58″", 365000)], [T("Netflix, YouTube et Prime Video", "Netflix, YouTube y Prime Video", "Netflix, YouTube and Prime Video")])
G(S, "tv", "audio", "speaker", ["Samsung", "LG", "Sony", "JBL"], T("{v}", "{v}", "{v}"), [("Barre de son 2.1 · 300 W", "Barra de sonido 2.1 · 300 W", "2.1 soundbar · 300 W", 145000), ("Barre de son Dolby Atmos", "Barra de sonido Dolby Atmos", "Dolby Atmos soundbar", 395000), ("Home cinéma 5.1", "Cine en casa 5.1", "5.1 home cinema", 245000), ("Enceinte de soirée 800 W", "Altavoz de fiesta 800 W", "800 W party speaker", 285000), ("Enceinte Bluetooth Charge 5", "Altavoz Bluetooth Charge 5", "Charge 5 Bluetooth speaker", 115000)], [])
G(S, "tv", "gaming", "console", ["Sony", "Microsoft", "Nintendo"], T("{v}", "{v}", "{v}"), [("Manette DualSense", "Mando DualSense", "DualSense controller", 49000), ("Xbox Series X", "Xbox Series X", "Xbox Series X", 395000), ("Nintendo Switch OLED", "Nintendo Switch OLED", "Nintendo Switch OLED", 245000)], [])
G(S, "literie", "matelas", "bed", ["Ventage Home"], T("Matelas Ventage {v}", "Colchón Ventage {v}", "Ventage mattress, {v}"), [("mousse 90×190", "espuma 90×190", "foam 90×190", 65000), ("mousse 140×190", "espuma 140×190", "foam 140×190", 125000), ("ressorts 160×200", "muelles 160×200", "springs 160×200", 245000), ("ressorts 180×200", "muelles 180×200", "springs 180×200", 285000), ("orthopédique 160×200", "ortopédico 160×200", "orthopaedic 160×200", 295000), ("mémoire de forme 180×200", "viscoelástico 180×200", "memory foam 180×200", 385000), ("hôtel 200×200", "hotel 200×200", "hotel 200×200", 465000)], [T("Fabriqué en Guinée équatoriale", "Fabricado en Guinea Ecuatorial", "Made in Equatorial Guinea"), T("Garantie 5 ans", "Garantía 5 años", "5-year warranty")])
G(S, "literie", "lits", "bed", ["Ventage Home"], T("{v}", "{v}", "{v}"), [("Lit 140×190 avec chevets", "Cama 140×190 con mesitas", "140×190 bed with bedsides", 345000), ("Lit enfant 90×190", "Cama infantil 90×190", "90×190 child's bed", 145000), ("Lits superposés", "Literas", "Bunk beds", 225000), ("Sommier tapissier 160×200", "Somier tapizado 160×200", "160×200 box spring", 125000)], HL["maison"])
G(S, "literie", "linge", "pillow", ["Ventage Home"], T("{v}", "{v}", "{v}"), [("Parure de draps 160×200", "Juego de sábanas 160×200", "Sheet set 160×200", 32000), ("Couette légère 220×240", "Edredón ligero 220×240", "Light duvet 220×240", 45000), ("Oreillers · lot de 2", "Almohadas · pack de 2", "Pillows · set of 2", 19500), ("Protège-matelas 160×200", "Protector de colchón 160×200", "Mattress protector 160×200", 18000), ("Serviettes de bain · lot de 4", "Toallas de baño · pack de 4", "Bath towels · set of 4", 22000), ("Moustiquaire de lit", "Mosquitera de cama", "Bed mosquito net", 9500)], [])
G(S, "sport", "fitness", "dumbbell", ["Ventage Sport", "Decathlon"], T("{v}", "{v}", "{v}"), [("Haltères réglables 20 kg", "Mancuernas ajustables 20 kg", "Adjustable dumbbells 20 kg", 45000), ("Tapis de course 2 HP", "Cinta de correr 2 HP", "2 HP treadmill", 395000), ("Vélo d'appartement", "Bicicleta estática", "Exercise bike", 165000), ("Tapis de yoga", "Esterilla de yoga", "Yoga mat", 12500), ("Banc de musculation", "Banco de musculación", "Weight bench", 85000)], HL["sport"])
G(S, "bagagerie", "valises", "suitcase", ["Samsonite", "Delsey", "Ventage Travel"], T("Valise {v}", "Maleta {v}", "{v} suitcase"), [("cabine 55 cm", "de cabina 55 cm", "55 cm cabin", 65000), ("moyenne 68 cm", "mediana 68 cm", "68 cm medium", 85000), ("grande 78 cm", "grande 78 cm", "78 cm large", 105000), ("set de 3", "juego de 3", "set of 3", 165000)], [T("Quatre roues doubles", "Cuatro ruedas dobles", "Four double wheels")])
G(S, "bagagerie", "sacs-voyage", "bagl", ["Samsonite", "Ventage Travel"], T("{v}", "{v}", "{v}"), [("Sac de voyage 60 L", "Bolsa de viaje 60 L", "60 L travel bag", 35000), ("Sac à dos ordinateur", "Mochila para portátil", "Laptop backpack", 29000), ("Sac de sport", "Bolsa de deporte", "Sports bag", 19000)], [])

S = "ventage-casa"
G(S, "maison", "salons", "sofa", ["Ventage Home"], T("{v}", "{v}", "{v}"), [("Canapé 3 places lin beige", "Sofá 3 plazas lino beige", "Three-seater linen sofa, beige", 595000), ("Salon complet 7 places", "Salón completo 7 plazas", "Seven-seat living-room set", 1450000), ("Canapé convertible", "Sofá cama", "Sofa bed", 485000), ("Table basse marbre", "Mesa de centro de mármol", "Marble coffee table", 245000), ("Meuble TV 200 cm", "Mueble TV 200 cm", "200 cm TV unit", 285000)], HL["maison"])
G(S, "maison", "repas", "table", ["Ventage Home"], T("{v}", "{v}", "{v}"), [("Table extensible 8 places", "Mesa extensible 8 plazas", "Extending table, seats 8", 545000), ("Chaises velours · lot de 4", "Sillas de terciopelo · pack de 4", "Velvet chairs · set of 4", 265000), ("Vaisselier deux corps", "Aparador vitrina", "Glass-front dresser", 445000), ("Table ronde 4 places", "Mesa redonda 4 plazas", "Round table, seats 4", 225000)], HL["maison"])
G(S, "table", "vaisselle", "plate", ["Ventage Home", "Luminarc", "Arcopal"], T("{v}", "{v}", "{v}"), [("Service de table 30 pièces", "Vajilla de 30 piezas", "30-piece dinner set", 45000), ("Ménagère 24 pièces inox", "Cubertería 24 piezas acero", "24-piece stainless cutlery set", 29000), ("Verres à pied · lot de 6", "Copas · juego de 6", "Stemmed glasses · set of 6", 15000), ("Service à thé porcelaine", "Juego de té de porcelana", "Porcelain tea set", 32000)], HL["table"])
G(S, "table", "cuisson-casa", "pan", ["Tefal", "Ventage Home"], T("{v}", "{v}", "{v}"), [("Batterie de cuisine 10 pièces", "Batería de cocina 10 piezas", "10-piece cookware set", 95000), ("Cocotte fonte 28 cm", "Cocotte de hierro 28 cm", "28 cm cast-iron casserole", 65000), ("Autocuiseur 8 L", "Olla a presión 8 L", "8 L pressure cooker", 45000)], HL["table"])
G(S, "luminaires", "lampes", "lamp", ["Ventage Home"], T("{v}", "{v}", "{v}"), [("Lustre cristal 8 bras", "Lámpara de araña de cristal 8 brazos", "Eight-arm crystal chandelier", 245000), ("Lampadaire arc", "Lámpara de pie de arco", "Arc floor lamp", 85000), ("Suspension rotin", "Lámpara colgante de ratán", "Rattan pendant", 39000), ("Applique murale laiton", "Aplique de latón", "Brass wall light", 29000)], [])
G(S, "luminaires", "tapis", "rug", ["Ventage Home"], T("{v}", "{v}", "{v}"), [("Tapis berbère 200×300", "Alfombra bereber 200×300", "Berber rug 200×300", 145000), ("Tapis de salon 160×230", "Alfombra de salón 160×230", "Living-room rug 160×230", 85000), ("Rideaux occultants · paire", "Cortinas opacas · par", "Blackout curtains · pair", 35000), ("Voilages lin · paire", "Visillos de lino · par", "Linen sheers · pair", 25000)], [])

S = "construction"
G(S, "materiaux", "gros-oeuvre", "brick", ["Ventage Build", "Lafarge", "Dangote"], T("{v}", "{v}", "{v}"), [("Ciment CPJ 42,5 · sac 50 kg", "Cemento CPJ 42,5 · saco 50 kg", "CPJ 42.5 cement · 50 kg bag", 6500), ("Ciment CPA 52,5 · sac 50 kg", "Cemento CPA 52,5 · saco 50 kg", "CPA 52.5 cement · 50 kg bag", 7800), ("Parpaing creux 15 cm · palette", "Bloque hueco 15 cm · palé", "15 cm hollow block · pallet", 0), ("Parpaing plein 20 cm · palette", "Bloque macizo 20 cm · palé", "20 cm solid block · pallet", 0), ("Sable de rivière · la tonne", "Arena de río · la tonelada", "River sand · per tonne", 0), ("Gravier 15/25 · la tonne", "Grava 15/25 · la tonelada", "15/25 gravel · per tonne", 0), ("Treillis soudé 2,4 × 6 m", "Mallazo 2,4 × 6 m", "Welded mesh 2.4 × 6 m", 18500)], [T("Livraison sur chantier", "Entrega en obra", "Delivered to site"), T("Prix dégressif par volume", "Precio decreciente por volumen", "Volume pricing")])
G(S, "materiaux", "gros-oeuvre", "brick", ["Ventage Build"], T("Fer à béton HA {v} · barre 12 m", "Varilla corrugada HA {v} · barra 12 m", "HA {v} rebar · 12 m bar"), [("6", 2300), ("8", 3900), ("10", 5400), ("14", 10500), ("16", 13500), ("20", 21500)], [T("Acier haute adhérence", "Acero de alta adherencia", "High-bond steel")], {"Diamètre": "{v} mm"})
G(S, "materiaux", "toiture", "roof", ["Ventage Build"], T("{v}", "{v}", "{v}"), [("Tôle bac acier 3 m", "Chapa grecada 3 m", "3 m steel roofing sheet", 14500), ("Tôle aluzinc ondulée 2 m", "Chapa ondulada aluzinc 2 m", "2 m corrugated aluzinc sheet", 8900), ("Faîtière acier", "Cumbrera de acero", "Steel ridge cap", 6500), ("Chevron bois 6×8 · 4 m", "Cabrio de madera 6×8 · 4 m", "6×8 timber rafter · 4 m", 4500), ("Contreplaqué 18 mm", "Contrachapado 18 mm", "18 mm plywood", 19500), ("Pointes de toiture · 1 kg", "Clavos de cubierta · 1 kg", "Roofing nails · 1 kg", 1800)], [])
G(S, "carrelage", "sols-murs", "tile", ["Ventage Build", "Porcelanosa", "Marazzi"], T("Carrelage {v} · le m²", "Cerámica {v} · el m²", "{v} tiles · per m²"), [("grès cérame 60×60 effet marbre", "gres porcelánico 60×60 efecto mármol", "60×60 marble-effect porcelain", 14500), ("grès cérame 120×60 effet béton", "gres porcelánico 120×60 efecto cemento", "120×60 concrete-effect porcelain", 22500), ("faïence murale 30×60 blanche", "azulejo 30×60 blanco", "30×60 white wall", 9500), ("parquet céramique 20×120", "porcelánico efecto madera 20×120", "20×120 wood-effect", 16500), ("antidérapant extérieur 45×45", "antideslizante exterior 45×45", "45×45 non-slip outdoor", 11500), ("mosaïque piscine", "gresite piscina", "pool mosaic", 18500)], [T("Échantillon en showroom", "Muestra en showroom", "Samples in showroom")])
G(S, "carrelage", "sanitaire", "toilet", ["Roca", "Grohe", "Ventage Build"], T("{v}", "{v}", "{v}"), [("WC à poser complet", "Inodoro de pie completo", "Close-coupled toilet", 89000), ("Lavabo sur colonne", "Lavabo de pie", "Pedestal basin", 45000), ("Vasque à poser céramique", "Lavabo sobre encimera", "Countertop basin", 39000), ("Receveur de douche 90×90", "Plato de ducha 90×90", "90×90 shower tray", 55000), ("Paroi de douche vitrée", "Mampara de ducha", "Glass shower screen", 125000), ("Baignoire acrylique 170 cm", "Bañera acrílica 170 cm", "170 cm acrylic bath", 185000), ("Évier inox 2 bacs", "Fregadero de acero 2 senos", "Two-bowl stainless sink", 49000)], [])
G(S, "carrelage", "robinetterie", "tap", ["Grohe", "Roca"], T("{v}", "{v}", "{v}"), [("Mitigeur lavabo chromé", "Monomando lavabo cromado", "Chrome basin mixer", 39000), ("Colonne de douche thermostatique", "Columna de ducha termostática", "Thermostatic shower column", 145000), ("Mitigeur évier col de cygne", "Grifo de cocina caño alto", "Swan-neck kitchen mixer", 45000), ("Robinet extérieur laiton", "Grifo exterior de latón", "Brass outdoor tap", 9500)], [])
G(S, "plomberie", "tubes", "pipe", ["Ventage Build", "Nicoll"], T("{v}", "{v}", "{v}"), [("Tube PVC évacuation Ø100 · 4 m", "Tubo PVC evacuación Ø100 · 4 m", "Ø100 PVC waste pipe · 4 m", 9500), ("Tube PVC pression Ø32 · 6 m", "Tubo PVC presión Ø32 · 6 m", "Ø32 PVC pressure pipe · 6 m", 6500), ("Tube PPR Ø25 · 4 m", "Tubo PPR Ø25 · 4 m", "Ø25 PPR pipe · 4 m", 4500), ("Coudes PVC Ø100 · lot de 10", "Codos PVC Ø100 · pack de 10", "Ø100 PVC elbows · 10", 8500), ("Colle PVC 500 ml", "Pegamento PVC 500 ml", "PVC glue 500 ml", 4200), ("Vanne d'arrêt laiton 3/4", "Llave de paso de latón 3/4", "3/4 brass stop valve", 5500)], [])
G(S, "plomberie", "visserie", "screw", ["Fischer", "Spit", "Ventage Build"], T("{v}", "{v}", "{v}"), [("Vis à bois · boîte de 500", "Tornillos de madera · caja de 500", "Wood screws · box of 500", 6500), ("Chevilles nylon · boîte de 100", "Tacos de nailon · caja de 100", "Nylon wall plugs · box of 100", 3500), ("Pointes tête plate · 5 kg", "Clavos cabeza plana · 5 kg", "Flat-head nails · 5 kg", 7500), ("Tiges filetées M10 · lot de 10", "Varillas roscadas M10 · pack de 10", "M10 threaded rods · 10", 8500)], [])
G(S, "plomberie", "serrurerie", "lock", ["Vachette", "Yale", "Ventage Build"], T("{v}", "{v}", "{v}"), [("Serrure 3 points", "Cerradura de 3 puntos", "Three-point lock", 45000), ("Cylindre de sécurité", "Bombín de seguridad", "Security cylinder", 19000), ("Cadenas laiton 60 mm", "Candado de latón 60 mm", "60 mm brass padlock", 8500), ("Poignées de porte · paire", "Manillas de puerta · par", "Door handles · pair", 12500)], [])
G(S, "outillage", "electroportatif", "drill", ["Makita", "Bosch", "DeWalt", "Hilti"], T("{v}", "{v}", "{v}"), [("Meuleuse 125 mm 900 W", "Amoladora 125 mm 900 W", "125 mm angle grinder 900 W", 65000), ("Scie circulaire 1400 W", "Sierra circular 1400 W", "1400 W circular saw", 115000), ("Ponceuse orbitale", "Lijadora orbital", "Orbital sander", 59000), ("Poste à souder 200 A", "Soldador 200 A", "200 A welder", 145000), ("Bétonnière 160 L", "Hormigonera 160 L", "160 L cement mixer", 295000), ("Groupe de compactage", "Bandeja vibrante", "Plate compactor", 0)], [T("Garantie 2 ans", "Garantía 2 años", "2-year warranty")])
G(S, "outillage", "main", "hammer", ["Stanley", "Facom", "Ventage Build"], T("{v}", "{v}", "{v}"), [("Marteau de coffreur", "Martillo de encofrador", "Framing hammer", 9500), ("Niveau à bulle 120 cm", "Nivel de burbuja 120 cm", "120 cm spirit level", 15000), ("Mètre ruban 8 m", "Cinta métrica 8 m", "8 m tape measure", 5500), ("Coffret de douilles 94 pièces", "Juego de vasos 94 piezas", "94-piece socket set", 65000), ("Truelle et taloche", "Paleta y llana", "Trowel & float", 7500), ("Échelle aluminium 3 × 9", "Escalera de aluminio 3 × 9", "3 × 9 aluminium ladder", 125000)], [])
G(S, "outillage", "nettoyage", "shovel", ["Ventage Build", "Gardena"], T("{v}", "{v}", "{v}"), [("Brouette 90 L", "Carretilla 90 L", "90 L wheelbarrow", 45000), ("Pelle carrée", "Pala cuadrada", "Square shovel", 6500), ("Tuyau d'arrosage 25 m", "Manguera 25 m", "25 m garden hose", 19000), ("Débroussailleuse thermique", "Desbrozadora de gasolina", "Petrol brush cutter", 145000)], [])

S = "electric-store"
G(S, "electricite", "cables", "bolt", ["Nexans", "Ventage Electric"], T("{v}", "{v}", "{v}"), [("Câble 1,5 mm² · 100 m", "Cable 1,5 mm² · 100 m", "1.5 mm² cable · 100 m", 24000), ("Câble 4 mm² · 100 m", "Cable 4 mm² · 100 m", "4 mm² cable · 100 m", 62000), ("Câble 6 mm² · 100 m", "Cable 6 mm² · 100 m", "6 mm² cable · 100 m", 89000), ("Câble 16 mm² · le mètre", "Cable 16 mm² · el metro", "16 mm² cable · per metre", 2500), ("Câble souple 3G2,5 · 50 m", "Manguera 3G2,5 · 50 m", "3G2.5 flex · 50 m", 39000), ("Gaine ICTA Ø20 · 100 m", "Tubo corrugado Ø20 · 100 m", "Ø20 conduit · 100 m", 14500), ("Câble coaxial TV · 100 m", "Cable coaxial TV · 100 m", "TV coaxial cable · 100 m", 19000)], [T("Norme NF", "Norma NF", "NF standard")])
G(S, "electricite", "appareillage", "socket", ["Legrand", "Schneider"], T("{b} {v}", "{b} {v}", "{b} {v}"), [("prise 2P+T", "enchufe 2P+T", "2P+E socket", 2500), ("interrupteur va-et-vient", "conmutador", "two-way switch", 2200), ("double prise", "enchufe doble", "double socket", 4500), ("prise USB", "enchufe USB", "USB socket", 9500), ("variateur", "regulador", "dimmer", 12500), ("prise étanche IP55", "enchufe estanco IP55", "IP55 outdoor socket", 5500)], [])
G(S, "electricite", "tableaux", "panel", ["Schneider", "Legrand", "Hager"], T("{v}", "{v}", "{v}"), [("Disjoncteur 16 A", "Disyuntor 16 A", "16 A breaker", 4500), ("Disjoncteur 32 A", "Disyuntor 32 A", "32 A breaker", 5500), ("Interrupteur différentiel 40 A 30 mA", "Diferencial 40 A 30 mA", "40 A 30 mA RCD", 29000), ("Coffret 2 rangées", "Cuadro 2 filas", "Two-row consumer unit", 35000), ("Parafoudre", "Protector contra sobretensiones", "Surge protector", 39000), ("Stabilisateur de tension 5 kVA", "Estabilizador de tensión 5 kVA", "5 kVA voltage stabiliser", 165000), ("Multiprise parafoudre 6 prises", "Regleta con protección 6 tomas", "Six-way surge strip", 12500)], [])
G(S, "eclairage", "ampoules", "bulb", ["Philips", "Osram", "Ventage Electric"], T("{v}", "{v}", "{v}"), [("Ampoule LED 12 W · lot de 10", "Bombilla LED 12 W · pack de 10", "12 W LED bulb · 10-pack", 18500), ("Tube LED 120 cm · lot de 10", "Tubo LED 120 cm · pack de 10", "120 cm LED tube · 10-pack", 29000), ("Réglette LED étanche 150 cm", "Regleta LED estanca 150 cm", "150 cm waterproof LED batten", 15000), ("Spot encastrable LED · lot de 6", "Foco empotrable LED · pack de 6", "LED downlight · 6-pack", 19500), ("Dalle LED 60×60", "Panel LED 60×60", "60×60 LED panel", 14500), ("Ruban LED 5 m", "Tira LED 5 m", "5 m LED strip", 12500)], [])
G(S, "eclairage", "exterieur", "flood", ["Philips", "Ventage Electric"], T("{v}", "{v}", "{v}"), [("Projecteur LED 50 W", "Proyector LED 50 W", "50 W LED floodlight", 19500), ("Projecteur LED 200 W", "Proyector LED 200 W", "200 W LED floodlight", 65000), ("Lampadaire solaire 100 W", "Farola solar 100 W", "100 W solar street light", 85000), ("Hublot extérieur", "Aplique ojo de buey", "Bulkhead light", 9500), ("Détecteur de mouvement", "Detector de movimiento", "Motion sensor", 12000)], [])
G(S, "energie", "groupes", "gen", ["Ventage Electric", "Honda", "Perkins", "Firman"], T("Groupe électrogène {v}", "Grupo electrógeno {v}", "{v} generator"), [("3 kVA essence", "3 kVA gasolina", "3 kVA petrol", 365000), ("10 kVA diesel", "10 kVA diésel", "10 kVA diesel", 2450000), ("20 kVA diesel insonorisé", "20 kVA diésel insonorizado", "20 kVA silent diesel", 0), ("60 kVA diesel", "60 kVA diésel", "60 kVA diesel", 0), ("inverter 2 kVA", "inverter 2 kVA", "2 kVA inverter", 425000)], [T("Mise en service sur site", "Puesta en marcha in situ", "On-site commissioning")])
G(S, "energie", "solaire", "sun", ["Jinko", "Victron", "Ventage Electric"], T("{v}", "{v}", "{v}"), [("Panneau solaire 450 W", "Panel solar 450 W", "450 W solar panel", 95000), ("Panneau solaire 550 W", "Panel solar 550 W", "550 W solar panel", 115000), ("Kit solaire 1 kW", "Kit solar 1 kW", "1 kW solar kit", 0), ("Installation solaire 10 kW", "Instalación solar 10 kW", "10 kW solar installation", 0), ("Régulateur MPPT 60 A", "Regulador MPPT 60 A", "60 A MPPT controller", 145000), ("Lampe solaire portable", "Lámpara solar portátil", "Portable solar lamp", 12500)], [T("Étude gratuite", "Estudio gratuito", "Free survey")])
G(S, "energie", "onduleurs", "battery", ["APC", "Victron", "Ventage Electric"], T("{v}", "{v}", "{v}"), [("Onduleur 650 VA", "SAI 650 VA", "650 VA UPS", 65000), ("Onduleur hybride 5 kW", "Inversor híbrido 5 kW", "5 kW hybrid inverter", 845000), ("Batterie gel 200 Ah", "Batería de gel 200 Ah", "200 Ah gel battery", 245000), ("Batterie lithium 5 kWh", "Batería de litio 5 kWh", "5 kWh lithium battery", 1250000), ("Convertisseur 3000 W", "Convertidor 3000 W", "3000 W inverter", 285000)], [])
G(S, "ventilation", "plafond", "fan", ["Ventage Electric", "Binatone", "Westinghouse"], T("Ventilateur de plafond {v}", "Ventilador de techo {v}", "{v} ceiling fan"), [("56″ blanc", "56″ blanco", "56″ white", 35000), ("52″ bois avec lumière", "52″ madera con luz", "52″ wood with light", 89000), ("48″ télécommandé", "48″ con mando", "48″ remote-controlled", 55000)], [])
G(S, "ventilation", "pied", "fan", ["Binatone", "Midea", "Ventage Electric"], T("{v}", "{v}", "{v}"), [("Ventilateur sur pied 18″", "Ventilador de pie 18″", "18″ standing fan", 32000), ("Ventilateur mural 16″", "Ventilador de pared 16″", "16″ wall fan", 24000), ("Ventilateur rechargeable", "Ventilador recargable", "Rechargeable fan", 29000), ("Rafraîchisseur d'air 40 L", "Climatizador evaporativo 40 L", "40 L air cooler", 85000)], [])

S = "electronics-office"
G(S, "mobile", "smartphones", "phone", ["Samsung", "Apple", "Tecno", "Infinix", "Xiaomi", "Itel"], T("{b} {v}", "{b} {v}", "{b} {v}"), [("Galaxy A55 256 Go", "Galaxy A55 256 GB", "Galaxy A55 256 GB", 245000), ("iPhone 15 128 Go", "iPhone 15 128 GB", "iPhone 15 128 GB", 645000), ("Spark 20 Pro", "Spark 20 Pro", "Spark 20 Pro", 109000), ("Hot 40 Pro", "Hot 40 Pro", "Hot 40 Pro", 115000), ("Redmi Note 13", "Redmi Note 13", "Redmi Note 13", 145000), ("A70", "A70", "A70", 59000)], HL["mobile"])
G(S, "info", "peripheriques", "monitor", ["Dell", "HP", "Logitech", "Samsung"], T("{v}", "{v}", "{v}"), [("Écran 24″ Full HD", "Monitor 24″ Full HD", "24″ Full HD monitor", 85000), ("Écran 27″ QHD", "Monitor 27″ QHD", "27″ QHD monitor", 165000), ("Clavier souris sans fil", "Teclado y ratón inalámbricos", "Wireless keyboard & mouse", 19500), ("Webcam Full HD", "Webcam Full HD", "Full HD webcam", 35000), ("Casque micro USB", "Auriculares con micro USB", "USB headset", 25000), ("Ordinateur de bureau tout-en-un", "Ordenador todo en uno", "All-in-one desktop", 545000)], HL["info"])
G(S, "info", "impression", "printer", ["HP", "Canon", "Epson", "Brother"], T("{v}", "{v}", "{v}"), [("Imprimante laser monochrome", "Impresora láser monocromo", "Mono laser printer", 115000), ("Multifonction laser couleur", "Multifunción láser color", "Colour laser all-in-one", 295000), ("Photocopieur A3", "Fotocopiadora A3", "A3 copier", 0), ("Cartouches d'encre · pack", "Cartuchos de tinta · pack", "Ink cartridges · pack", 25000), ("Toner laser", "Tóner láser", "Laser toner", 45000)], HL["info"])
G(S, "papeterie", "papier", "pen", ["Double A", "Ventage Office", "Exacompta"], T("{v}", "{v}", "{v}"), [("Ramette A4 80 g · carton de 5", "Resma A4 80 g · caja de 5", "A4 80 g paper · box of 5", 17500), ("Classeurs à levier · lot de 10", "Archivadores de palanca · pack de 10", "Lever-arch files · 10", 15000), ("Chemises cartonnées · 100", "Carpetas de cartón · 100", "Card folders · 100", 6500), ("Cahiers 200 pages · lot de 10", "Cuadernos 200 páginas · pack de 10", "200-page notebooks · 10", 7500)], [])
G(S, "papeterie", "ecriture", "pen", ["Bic", "Stabilo", "Ventage Office"], T("{v}", "{v}", "{v}"), [("Stylos bille · boîte de 50", "Bolígrafos · caja de 50", "Ballpoint pens · box of 50", 5500), ("Surligneurs · lot de 6", "Marcadores fluorescentes · pack de 6", "Highlighters · 6", 3200), ("Agrafeuse et agrafes", "Grapadora y grapas", "Stapler & staples", 6500), ("Calculatrice de bureau", "Calculadora de oficina", "Desk calculator", 9500)], [])
G(S, "papeterie", "reseau", "router", ["TP-Link", "SanDisk", "Seagate", "Ubiquiti"], T("{v}", "{v}", "{v}"), [("Routeur Wi-Fi 6", "Router Wi-Fi 6", "Wi-Fi 6 router", 59000), ("Disque dur externe 2 To", "Disco duro externo 2 TB", "2 TB external hard drive", 55000), ("Clé USB 128 Go", "Memoria USB 128 GB", "128 GB USB stick", 9500), ("SSD 1 To", "SSD 1 TB", "1 TB SSD", 65000), ("Switch 8 ports", "Switch de 8 puertos", "8-port switch", 19500), ("Point d'accès Wi-Fi pro", "Punto de acceso Wi-Fi pro", "Pro Wi-Fi access point", 89000)], [])
G(S, "accessoires-tech", "charge", "charger", ["Anker", "Samsung", "Ventage Tech"], T("{v}", "{v}", "{v}"), [("Batterie externe 20 000 mAh", "Batería externa 20 000 mAh", "20,000 mAh power bank", 25000), ("Chargeur rapide 45 W", "Cargador rápido 45 W", "45 W fast charger", 19500), ("Câble USB-C 2 m · lot de 2", "Cable USB-C 2 m · pack de 2", "2 m USB-C cable · 2-pack", 7500), ("Verre trempé · lot de 2", "Cristal templado · pack de 2", "Tempered glass · 2-pack", 5500)], [])

S = "paint-store"
COL = [("blanc", "blanco", "white"), ("blanc cassé", "blanco roto", "off-white"), ("gris perle", "gris perla", "pearl grey"), ("beige sable", "beige arena", "sand beige"), ("bleu ciel", "azul cielo", "sky blue"), ("vert sauge", "verde salvia", "sage green"), ("jaune soleil", "amarillo sol", "sunshine yellow"), ("terracotta", "terracota", "terracotta"), ("taupe", "topo", "taupe"), ("rose poudré", "rosa empolvado", "powder pink")]
G(S, "peinture", "interieur", "paint", ["Ventage Paint"], T("Peinture intérieure mate {v} · 20 L", "Pintura interior mate {v} · 20 L", "Matt interior paint, {v} · 20 L"), [(a, b, c, 42000 + 2000 * (i % 3)) for i, (a, b, c) in enumerate(COL)], [T("Fabriquée en Guinée équatoriale", "Fabricada en Guinea Ecuatorial", "Made in Equatorial Guinea"), T("Lessivable", "Lavable", "Washable")], {"Contenance": "20 L"})
G(S, "peinture", "interieur", "paint", ["Ventage Paint"], T("Peinture satinée {v}", "Pintura satinada {v}", "Satin paint {v}"), [("5 L", 18500), ("10 L", 34000), ("20 L", 62000)], [T("Pièces humides", "Zonas húmedas", "Wet rooms")])
G(S, "peinture", "exterieur", "paint", ["Ventage Paint"], T("Peinture façade {v} · 20 L", "Pintura de fachada {v} · 20 L", "Exterior paint, {v} · 20 L"), [(a, b, c, 56000) for (a, b, c) in COL[:6]], [T("Résiste aux UV et à la pluie", "Resiste a UV y lluvia", "UV and rain resistant")], {"Contenance": "20 L"})
G(S, "peinture", "exterieur", "paint", ["Ventage Paint"], T("{v}", "{v}", "{v}"), [("Peinture toiture tôle · 20 L", "Pintura para cubiertas · 20 L", "Metal roof paint · 20 L", 68000), ("Peinture sol & garage · 10 L", "Pintura de suelos · 10 L", "Floor & garage paint · 10 L", 38000), ("Peinture piscine · 10 L", "Pintura de piscinas · 10 L", "Pool paint · 10 L", 65000), ("Peinture routière · 20 L", "Pintura vial · 20 L", "Road-marking paint · 20 L", 72000)], [])
G(S, "peinture", "laques", "brush", ["Ventage Paint", "Sikkens"], T("{v}", "{v}", "{v}"), [("Laque glycéro brillante · 2,5 L", "Esmalte brillante · 2,5 L", "Gloss enamel · 2.5 L", 19500), ("Laque acrylique satinée · 2,5 L", "Esmalte acrílico satinado · 2,5 L", "Satin acrylic enamel · 2.5 L", 21500), ("Vernis bois incolore · 2,5 L", "Barniz incoloro · 2,5 L", "Clear wood varnish · 2.5 L", 18500), ("Lasure chêne · 2,5 L", "Lasur roble · 2,5 L", "Oak wood stain · 2.5 L", 19500), ("Peinture fer antirouille · 2,5 L", "Pintura antióxido · 2,5 L", "Anti-rust metal paint · 2.5 L", 22500), ("Bombe de peinture · lot de 6", "Spray de pintura · pack de 6", "Spray paint · 6-pack", 15000)], [])
G(S, "preparation", "enduits", "trowel", ["Ventage Paint", "Toupret"], T("{v}", "{v}", "{v}"), [("Enduit de lissage · 25 kg", "Masilla de alisado · 25 kg", "Skim coat · 25 kg", 15500), ("Enduit de rebouchage · 5 kg", "Masilla de relleno · 5 kg", "Filler · 5 kg", 6500), ("Mastic acrylique · lot de 6", "Masilla acrílica · pack de 6", "Acrylic sealant · 6-pack", 9500), ("Enduit de façade · 25 kg", "Revoque de fachada · 25 kg", "Exterior render · 25 kg", 18500)], [])
G(S, "preparation", "sous-couches", "drop", ["Ventage Paint", "Sika"], T("{v}", "{v}", "{v}"), [("Sous-couche universelle · 10 L", "Imprimación universal · 10 L", "Universal primer · 10 L", 26000), ("Fixateur de fonds · 5 L", "Fijador · 5 L", "Stabilising primer · 5 L", 12500), ("Traitement anti-moisissures · 5 L", "Tratamiento antimoho · 5 L", "Anti-mould treatment · 5 L", 14500), ("Étanchéité toiture · 20 kg", "Impermeabilizante de cubiertas · 20 kg", "Roof waterproofing · 20 kg", 55000), ("Diluant · 5 L", "Disolvente · 5 L", "Thinner · 5 L", 8500)], [])
G(S, "outils-peintre", "rouleaux", "roller", ["Ventage Paint", "L'Outil Parfait"], T("{v}", "{v}", "{v}"), [("Rouleau façade 230 mm", "Rodillo de fachada 230 mm", "230 mm masonry roller", 6500), ("Rouleau laqueur 110 mm", "Rodillo lacador 110 mm", "110 mm gloss roller", 3500), ("Pinceaux plats · lot de 5", "Brochas planas · pack de 5", "Flat brushes · 5", 7500), ("Perche télescopique 3 m", "Pértiga telescópica 3 m", "3 m extension pole", 9500), ("Pistolet à peinture électrique", "Pistola de pintura eléctrica", "Electric paint sprayer", 75000)], [])
G(S, "outils-peintre", "protection", "tape", ["Tesa", "Ventage Paint"], T("{v}", "{v}", "{v}"), [("Bâche de protection 4 × 5 m", "Lona de protección 4 × 5 m", "4 × 5 m dust sheet", 3500), ("Ruban de masquage · lot de 6", "Cinta de carrocero · pack de 6", "Masking tape · 6-pack", 4500), ("Bac à peinture et grille", "Cubeta y rejilla", "Paint tray & grid", 3000), ("Combinaison de peintre", "Mono de pintor", "Painter's overalls", 5500)], [])
G(S, "deco-murale", "papiers-peints", "wall", ["Ventage Deco"], T("Papier peint {v} · rouleau", "Papel pintado {v} · rollo", "{v} wallpaper · roll"), [("intissé uni", "tejido no tejido liso", "plain non-woven", 9500), ("motif tropical", "motivo tropical", "tropical print", 12500), ("effet béton", "efecto cemento", "concrete effect", 11500), ("rayures", "rayas", "striped", 9500)], [])
G(S, "deco-murale", "effets", "paint", ["Ventage Paint"], T("{v}", "{v}", "{v}"), [("Peinture effet métal · 2 L", "Pintura efecto metal · 2 L", "Metallic effect paint · 2 L", 24500), ("Peinture effet béton ciré · 4 L", "Pintura efecto microcemento · 4 L", "Polished-concrete effect · 4 L", 32000), ("Peinture tableau noir · 1 L", "Pintura pizarra · 1 L", "Chalkboard paint · 1 L", 9500), ("Peinture pailletée · 2 L", "Pintura con purpurina · 2 L", "Glitter paint · 2 L", 14500)], [])

S = "amanda-pharmacies"
G(S, "dermo", "visage", "pill", ["Avène", "Vichy", "La Roche-Posay", "Bioderma", "CeraVe", "Nivea"], T("{b} {v}", "{b} {v}", "{b} {v}"), [("crème hydratante 50 ml", "crema hidratante 50 ml", "moisturiser 50 ml", 16500), ("sérum anti-taches 30 ml", "sérum antimanchas 30 ml", "dark-spot serum 30 ml", 24500), ("gel nettoyant 400 ml", "gel limpiador 400 ml", "cleansing gel 400 ml", 13500), ("eau micellaire 500 ml", "agua micelar 500 ml", "micellar water 500 ml", 11500), ("crème anti-rides 50 ml", "crema antiarrugas 50 ml", "anti-wrinkle cream 50 ml", 28500), ("soin anti-acné 40 ml", "tratamiento antiacné 40 ml", "anti-acne care 40 ml", 15500)], HL["dermo"])
G(S, "dermo", "corps", "pill", ["Nivea", "CeraVe", "Vaseline", "Dove"], T("{b} {v}", "{b} {v}", "{b} {v}"), [("lait corps 400 ml", "leche corporal 400 ml", "body lotion 400 ml", 7500), ("baume relipidant 400 ml", "bálsamo relipidizante 400 ml", "lipid-replenishing balm 400 ml", 14500), ("crème mains 75 ml", "crema de manos 75 ml", "hand cream 75 ml", 4500), ("huile sèche 100 ml", "aceite seco 100 ml", "dry oil 100 ml", 15500)], HL["dermo"])
G(S, "dermo", "solaires", "sun", ["Avène", "La Roche-Posay", "Bioderma"], T("{b} {v}", "{b} {v}", "{b} {v}"), [("crème solaire SPF 50+ 50 ml", "protector solar SPF 50+ 50 ml", "SPF 50+ sun cream 50 ml", 14500), ("spray solaire SPF 50 200 ml", "spray solar SPF 50 200 ml", "SPF 50 sun spray 200 ml", 19500), ("solaire enfants SPF 50+", "solar niños SPF 50+", "kids' sun care SPF 50+", 16500), ("après-soleil 200 ml", "aftersun 200 ml", "after-sun 200 ml", 11500)], HL["dermo"])
G(S, "hygiene-sante", "dentaire", "tooth", ["Sensodyne", "Elmex", "Oral-B", "Signal"], T("{b} {v}", "{b} {v}", "{b} {v}"), [("dentifrice dents sensibles", "pasta dientes sensibles", "sensitive toothpaste", 4500), ("dentifrice anti-caries", "pasta anticaries", "anti-cavity toothpaste", 3500), ("brosse à dents électrique", "cepillo eléctrico", "electric toothbrush", 39000), ("bain de bouche 500 ml", "colutorio 500 ml", "mouthwash 500 ml", 5500), ("fil dentaire", "hilo dental", "dental floss", 2500)], [])
G(S, "hygiene-sante", "intime", "soap", ["Saforelle", "Rogé Cavaillès", "Dettol", "Rexona"], T("{b} {v}", "{b} {v}", "{b} {v}"), [("gel toilette intime 250 ml", "gel íntimo 250 ml", "intimate wash 250 ml", 6500), ("savon surgras 250 g", "jabón dermatológico 250 g", "rich soap 250 g", 3500), ("gel antiseptique mains 500 ml", "gel antiséptico de manos 500 ml", "antiseptic hand gel 500 ml", 4500), ("déodorant 48 h", "desodorante 48 h", "48-hour deodorant", 3500), ("serviettes hygiéniques · 3 paquets", "compresas · 3 paquetes", "sanitary pads · 3 packs", 4500)], [])
G(S, "complements", "vitamines", "capsule", ["Amanda", "Supradyn", "Berocca", "Arkopharma"], T("{v}", "{v}", "{v}"), [("Vitamine C 1000 mg · 30 comprimés", "Vitamina C 1000 mg · 30 comprimidos", "Vitamin C 1000 mg · 30 tablets", 6500), ("Vitamine D3 · 60 gélules", "Vitamina D3 · 60 cápsulas", "Vitamin D3 · 60 capsules", 7500), ("Magnésium B6 · 60 comprimés", "Magnesio B6 · 60 comprimidos", "Magnesium B6 · 60 tablets", 8500), ("Fer + acide folique · 30", "Hierro + ácido fólico · 30", "Iron + folic acid · 30", 5500), ("Zinc · 60 comprimés", "Zinc · 60 comprimidos", "Zinc · 60 tablets", 6500), ("Oméga 3 · 60 capsules", "Omega 3 · 60 cápsulas", "Omega 3 · 60 capsules", 12500), ("Multivitamines enfants · 30", "Multivitaminas niños · 30", "Kids' multivitamins · 30", 8500)], [T("Complément alimentaire", "Complemento alimenticio", "Food supplement")])
G(S, "complements", "forme", "capsule", ["Amanda", "Arkopharma", "Berocca"], T("{v}", "{v}", "{v}"), [("Ginseng énergie · 30 gélules", "Ginseng energía · 30 cápsulas", "Ginseng energy · 30 capsules", 9500), ("Probiotiques · 30 gélules", "Probióticos · 30 cápsulas", "Probiotics · 30 capsules", 14500), ("Spiruline · 120 comprimés", "Espirulina · 120 comprimidos", "Spirulina · 120 tablets", 11500), ("Gelée royale · 20 ampoules", "Jalea real · 20 ampollas", "Royal jelly · 20 vials", 15500), ("Sommeil mélatonine · 30", "Melatonina sueño · 30", "Melatonin sleep · 30", 8500)], [T("Complément alimentaire", "Complemento alimenticio", "Food supplement")])
G(S, "maman-bebe", "laits", "baby", ["Nestlé", "Gallia", "Guigoz", "Blédina"], T("{v}", "{v}", "{v}"), [("Lait 1er âge 800 g", "Leche de inicio 800 g", "First infant milk 800 g", 14500), ("Lait 2e âge 800 g", "Leche de continuación 800 g", "Follow-on milk 800 g", 13500), ("Lait croissance 3e âge 800 g", "Leche de crecimiento 800 g", "Growing-up milk 800 g", 12500), ("Céréales bébé dès 6 mois", "Cereales bebé desde 6 meses", "Baby cereal from 6 months", 4500), ("Biberon anti-colique 260 ml", "Biberón anticólico 260 ml", "Anti-colic bottle 260 ml", 8500)], [])
G(S, "maman-bebe", "soins-bebe", "baby", ["Mustela", "Pampers", "Bepanthen", "Huggies"], T("{v}", "{v}", "{v}"), [("Couches nouveau-né · 44", "Pañales recién nacido · 44", "Newborn nappies · 44", 8500), ("Couches taille 5 · 46", "Pañales talla 5 · 46", "Nappies size 5 · 46", 11500), ("Crème change 100 g", "Crema del pañal 100 g", "Nappy cream 100 g", 6500), ("Gel lavant bébé 500 ml", "Gel de baño bebé 500 ml", "Baby wash 500 ml", 7500), ("Thermomètre de bain", "Termómetro de baño", "Bath thermometer", 4500)], [])
G(S, "materiel-medical", "autotest", "heart", ["Omron", "Accu-Chek", "Braun", "Microlife"], T("{v}", "{v}", "{v}"), [("Tensiomètre poignet", "Tensiómetro de muñeca", "Wrist blood pressure monitor", 32000), ("Lecteur de glycémie", "Glucómetro", "Blood glucose meter", 25000), ("Bandelettes glycémie · 50", "Tiras de glucemia · 50", "Glucose strips · 50", 18500), ("Oxymètre de pouls", "Pulsioxímetro", "Pulse oximeter", 15500), ("Nébuliseur", "Nebulizador", "Nebuliser", 45000), ("Pèse-personne", "Báscula", "Bathroom scale", 19500)], [])
G(S, "materiel-medical", "secours", "cross", ["Urgo", "Hansaplast", "Amanda"], T("{v}", "{v}", "{v}"), [("Trousse de premiers secours", "Botiquín de primeros auxilios", "First-aid kit", 15500), ("Pansements assortis · 40", "Tiritas surtidas · 40", "Assorted plasters · 40", 3500), ("Compresses stériles · 50", "Gasas estériles · 50", "Sterile gauze pads · 50", 4500), ("Bande de contention", "Venda de compresión", "Compression bandage", 3500), ("Alcool 70° · 250 ml", "Alcohol 70° · 250 ml", "70% alcohol · 250 ml", 2000), ("Gants d'examen · boîte de 100", "Guantes de examen · caja de 100", "Exam gloves · box of 100", 6500), ("Masques chirurgicaux · 50", "Mascarillas quirúrgicas · 50", "Surgical masks · 50", 4500)], [])
G(S, "materiel-medical", "moustiques", "mosquito", ["Cinq sur Cinq", "Ventage", "Moustidose"], T("{v}", "{v}", "{v}"), [("Répulsif tropiques 75 ml", "Repelente trópicos 75 ml", "Tropical repellent 75 ml", 8500), ("Moustiquaire imprégnée 2 places", "Mosquitera impregnada 2 plazas", "Treated double mosquito net", 12500), ("Diffuseur électrique anti-moustiques", "Difusor eléctrico antimosquitos", "Plug-in mosquito diffuser", 6500), ("Répulsif enfants 100 ml", "Repelente niños 100 ml", "Kids' repellent 100 ml", 7500)], [])

S = "amanda-labs"
LAB = [
 ("hematologie", "hemato", [("Numération formule sanguine (NFS)", "Hemograma completo", "Full blood count", 6000), ("Vitesse de sédimentation (VS)", "Velocidad de sedimentación", "Erythrocyte sedimentation rate", 3000), ("Groupe sanguin et rhésus", "Grupo sanguíneo y Rh", "Blood group & Rh", 5000), ("Taux de prothrombine (TP/INR)", "Tiempo de protrombina (TP/INR)", "Prothrombin time (PT/INR)", 7000), ("Électrophorèse de l'hémoglobine", "Electroforesis de hemoglobina", "Haemoglobin electrophoresis", 15000), ("Test d'Emmel (drépanocytose)", "Test de Emmel (drepanocitosis)", "Sickle-cell screening", 5000), ("Réticulocytes", "Reticulocitos", "Reticulocyte count", 5000), ("Ferritine", "Ferritina", "Ferritin", 12000)]),
 ("hematologie", "biochimie", [("Glycémie à jeun", "Glucemia en ayunas", "Fasting glucose", 3000), ("Hémoglobine glyquée (HbA1c)", "Hemoglobina glicosilada (HbA1c)", "HbA1c", 12000), ("Créatinine", "Creatinina", "Creatinine", 4000), ("Urée", "Urea", "Urea", 4000), ("Ionogramme sanguin", "Ionograma", "Electrolytes", 12000), ("Bilan lipidique complet", "Perfil lipídico completo", "Full lipid panel", 15000), ("Transaminases (ASAT/ALAT)", "Transaminasas (AST/ALT)", "Liver enzymes (AST/ALT)", 8000), ("Gamma-GT", "Gamma-GT", "Gamma-GT", 5000), ("Bilirubine totale et conjuguée", "Bilirrubina total y directa", "Total & direct bilirubin", 7000), ("Acide urique", "Ácido úrico", "Uric acid", 4000), ("Protéine C réactive (CRP)", "Proteína C reactiva (PCR)", "C-reactive protein (CRP)", 7000), ("Calcium", "Calcio", "Calcium", 4000), ("Vitamine D", "Vitamina D", "Vitamin D", 25000), ("Bilan rénal complet", "Perfil renal completo", "Full kidney panel", 18000), ("Bilan hépatique complet", "Perfil hepático completo", "Full liver panel", 20000)]),
 ("hormones", "thyroide", [("TSH", "TSH", "TSH", 12000), ("T3 libre", "T3 libre", "Free T3", 12000), ("T4 libre", "T4 libre", "Free T4", 12000), ("Bilan thyroïdien complet", "Perfil tiroideo completo", "Full thyroid panel", 30000), ("Anticorps anti-TPO", "Anticuerpos anti-TPO", "Anti-TPO antibodies", 18000)]),
 ("hormones", "fertilite", [("Bêta-HCG (test de grossesse)", "Beta-HCG (test de embarazo)", "Beta-hCG (pregnancy test)", 8000), ("FSH", "FSH", "FSH", 12000), ("LH", "LH", "LH", 12000), ("Prolactine", "Prolactina", "Prolactin", 12000), ("Progestérone", "Progesterona", "Progesterone", 12000), ("Œstradiol", "Estradiol", "Oestradiol", 12000), ("Testostérone", "Testosterona", "Testosterone", 14000), ("AMH (réserve ovarienne)", "AMH (reserva ovárica)", "AMH (ovarian reserve)", 35000), ("Spermogramme", "Espermiograma", "Semen analysis", 20000), ("PSA total", "PSA total", "Total PSA", 15000)]),
 ("infectiologie", "paludisme", [("Goutte épaisse (paludisme)", "Gota gruesa (malaria)", "Thick blood smear (malaria)", 3000), ("TDR paludisme", "Test rápido de malaria", "Rapid malaria test", 3000), ("Sérodiagnostic de Widal (typhoïde)", "Reacción de Widal (tifoidea)", "Widal test (typhoid)", 6000), ("Hémoculture", "Hemocultivo", "Blood culture", 18000), ("Dengue NS1 / IgG / IgM", "Dengue NS1 / IgG / IgM", "Dengue NS1 / IgG / IgM", 20000), ("Test COVID-19 antigénique", "Test antígenos COVID-19", "COVID-19 antigen test", 10000), ("PCR COVID-19", "PCR COVID-19", "COVID-19 PCR", 35000)]),
 ("infectiologie", "serologies", [("Sérologie VIH 1 et 2", "Serología VIH 1 y 2", "HIV 1 & 2 serology", 6000), ("Antigène HBs (hépatite B)", "Antígeno HBs (hepatitis B)", "HBsAg (hepatitis B)", 7000), ("Sérologie hépatite C", "Serología hepatitis C", "Hepatitis C serology", 10000), ("Sérologie syphilis (TPHA/VDRL)", "Serología sífilis (TPHA/VDRL)", "Syphilis serology (TPHA/VDRL)", 8000), ("Toxoplasmose IgG / IgM", "Toxoplasmosis IgG / IgM", "Toxoplasmosis IgG / IgM", 15000), ("Rubéole IgG / IgM", "Rubéola IgG / IgM", "Rubella IgG / IgM", 15000), ("Helicobacter pylori", "Helicobacter pylori", "Helicobacter pylori", 12000), ("Chlamydia", "Clamidia", "Chlamydia", 15000), ("Charge virale VIH", "Carga viral VIH", "HIV viral load", 45000)]),
 ("infectiologie", "urines-selles", [("ECBU (examen des urines)", "Urocultivo", "Urine culture", 8000), ("Bandelette urinaire", "Tira reactiva de orina", "Urine dipstick", 2000), ("Examen parasitologique des selles", "Examen parasitológico de heces", "Stool parasite test", 5000), ("Coproculture", "Coprocultivo", "Stool culture", 12000), ("Prélèvement vaginal", "Exudado vaginal", "Vaginal swab", 10000), ("Microalbuminurie", "Microalbuminuria", "Urine microalbumin", 10000)]),
 ("bilans", "packs", [("Bilan prénuptial", "Chequeo prenupcial", "Pre-marital check-up", 45000), ("Bilan prénatal 1er trimestre", "Chequeo prenatal 1er trimestre", "First-trimester prenatal panel", 55000), ("Bilan diabète", "Chequeo diabetes", "Diabetes check-up", 25000), ("Bilan cardiovasculaire", "Chequeo cardiovascular", "Cardiovascular check-up", 40000), ("Bilan sportif", "Chequeo deportivo", "Sports check-up", 35000), ("Bilan senior 60+", "Chequeo sénior 60+", "Senior 60+ check-up", 65000), ("Bilan femme", "Chequeo mujer", "Women's health panel", 55000), ("Bilan homme", "Chequeo hombre", "Men's health panel", 55000), ("Bilan enfant", "Chequeo infantil", "Child health panel", 30000), ("Bilan voyage", "Chequeo viajero", "Travel health panel", 35000)]),
 ("bilans", "entreprises", [("Visite d'embauche · bilan biologique", "Reconocimiento de ingreso · análisis", "Pre-employment lab panel", 25000), ("Prélèvement à domicile · Malabo", "Extracción a domicilio · Malabo", "Home sampling · Malabo", 10000), ("Campagne de dépistage en entreprise", "Campaña de cribado en empresa", "Workplace screening campaign", 0), ("Contrat annuel entreprise", "Contrato anual de empresa", "Annual corporate contract", 0), ("Résultats en ligne sécurisés", "Resultados en línea seguros", "Secure online results", 0)]),
]
for cat, sub, rows in LAB:
    icon = {"hematologie": "flask", "hormones": "dna", "infectiologie": "virus", "bilans": "clipboard"}[cat]
    G(S, cat, sub, icon, ["Amanda Labs"], T("{v}", "{v}", "{v}"), [(a, b, c, (p or 0)) for a, b, c, p in rows], [T("Résultats rapides", "Resultados rápidos", "Fast results"), T("Prélèvement sans rendez-vous le matin", "Extracción sin cita por la mañana", "Walk-in sampling in the morning")])

S = "tires-auto"
for (b, sizes, base) in [("Michelin", ["185/65 R15", "195/65 R15", "205/55 R16", "215/60 R16", "225/45 R17", "235/45 R18"], 52000), ("Bridgestone", ["175/70 R13", "185/60 R14", "195/55 R16", "205/60 R16"], 42000), ("Continental", ["195/65 R15", "215/55 R17", "225/50 R17"], 58000), ("Goodyear", ["185/65 R15", "205/55 R16", "215/65 R16"], 48000), ("Hankook", ["195/65 R15", "205/55 R16", "225/45 R17"], 38000)]:
    G(S, "pneus", "tourisme", "tire", [b], T("Pneu {b} {v}", "Neumático {b} {v}", "{b} tyre {v}"), [(s, base + i * 7000) for i, s in enumerate(sizes)], [T("Montage et équilibrage en atelier", "Montaje y equilibrado en taller", "Fitting and balancing in-house")], {"Dimension": "{v}"})
for (b, sizes, base) in [("Bridgestone", ["265/70 R16", "265/65 R17", "285/60 R18"], 98000), ("Michelin", ["245/70 R16", "265/60 R18", "275/55 R20"], 125000), ("BFGoodrich", ["235/85 R16", "265/75 R16", "285/70 R17"], 135000), ("Pirelli", ["255/55 R19", "235/55 R18"], 115000)]:
    G(S, "pneus", "4x4", "tire", [b], T("Pneu 4×4 {b} {v}", "Neumático 4×4 {b} {v}", "{b} 4×4 tyre {v}"), [(s, base + i * 9000) for i, s in enumerate(sizes)], [T("Tout-terrain", "Todoterreno", "All-terrain")], {"Dimension": "{v}"})
G(S, "pneus", "utilitaire", "tire", ["Michelin", "Bridgestone", "Continental"], T("Pneu {v}", "Neumático {v}", "{v} tyre"), [("utilitaire 195/75 R16C", "utilitario 195/75 R16C", "van 195/75 R16C", 85000), ("utilitaire 215/75 R16C", "utilitario 215/75 R16C", "van 215/75 R16C", 92000), ("camion 315/80 R22.5", "camión 315/80 R22.5", "truck 315/80 R22.5", 0), ("camion 12.00 R20", "camión 12.00 R20", "truck 12.00 R20", 0), ("moto 120/70 R17", "moto 120/70 R17", "motorbike 120/70 R17", 39000)], [])
G(S, "pieces", "batteries", "car", ["Varta", "Bosch", "Exide"], T("Batterie 12 V {v}", "Batería 12 V {v}", "12 V battery, {v}"), [("45 Ah", 55000), ("60 Ah", 68000), ("90 Ah", 98000), ("100 Ah", 115000), ("150 Ah camion", "150 Ah camión", "150 Ah truck", 165000), ("200 Ah camion", "200 Ah camión", "200 Ah truck", 215000)], [T("Test de charge offert", "Test de carga gratis", "Free charge test")])
G(S, "pieces", "freinage", "brake", ["Bosch", "Brembo", "Mann-Filter"], T("{v}", "{v}", "{v}"), [("Plaquettes de frein avant", "Pastillas de freno delanteras", "Front brake pads", 25000), ("Disques de frein · paire", "Discos de freno · par", "Brake discs · pair", 65000), ("Filtre à huile", "Filtro de aceite", "Oil filter", 5500), ("Filtre à air", "Filtro de aire", "Air filter", 8500), ("Filtre à carburant", "Filtro de combustible", "Fuel filter", 9500), ("Filtre d'habitacle", "Filtro de habitáculo", "Cabin filter", 7500)], [])
G(S, "pieces", "visibilite", "wiper", ["Bosch", "Philips", "Valeo"], T("{v}", "{v}", "{v}"), [("Balais d'essuie-glace · paire", "Escobillas limpiaparabrisas · par", "Wiper blades · pair", 12500), ("Ampoules H4 · paire", "Lámparas H4 · par", "H4 bulbs · pair", 7500), ("Kit LED H7", "Kit LED H7", "H7 LED kit", 25000), ("Rétroviseur extérieur", "Retrovisor exterior", "Door mirror", 35000)], [])
G(S, "lubrifiants", "huiles", "oil", ["Total", "Shell", "Castrol", "Mobil"], T("Huile moteur {b} {v}", "Aceite de motor {b} {v}", "{b} engine oil {v}"), [("5W-30 · 5 L", 32000), ("10W-40 · 5 L", 24000), ("15W-40 diesel · 5 L", 21000), ("5W-40 · 4 L", 29000), ("20W-50 · 4 L", 15000), ("15W-40 · 20 L", 72000)], [])
G(S, "lubrifiants", "liquides", "oil", ["Total", "Bosch", "Ventage Auto"], T("{v}", "{v}", "{v}"), [("Liquide de refroidissement · 5 L", "Anticongelante · 5 L", "Coolant · 5 L", 9500), ("Liquide de frein DOT 4", "Líquido de frenos DOT 4", "DOT 4 brake fluid", 4500), ("Lave-glace · 5 L", "Limpiaparabrisas · 5 L", "Screenwash · 5 L", 3500), ("Câbles de démarrage", "Cables de arranque", "Jump leads", 12500), ("Triangle et gilet de sécurité", "Triángulo y chaleco", "Warning triangle & vest", 9500), ("Cric hydraulique 3 t", "Gato hidráulico 3 t", "3 t hydraulic jack", 35000), ("Compresseur 12 V", "Compresor 12 V", "12 V tyre inflator", 19500)], [])
G(S, "atelier", "services", "wrench", ["Ventage Auto"], T("{v}", "{v}", "{v}"), [("Vidange + filtre", "Cambio de aceite + filtro", "Oil & filter change", 35000), ("Géométrie / parallélisme", "Alineación", "Wheel alignment", 25000), ("Équilibrage · 4 roues", "Equilibrado · 4 ruedas", "Balancing · 4 wheels", 12000), ("Diagnostic électronique", "Diagnóstico electrónico", "Electronic diagnostics", 20000), ("Recharge climatisation", "Carga de aire acondicionado", "A/C recharge", 35000), ("Réparation crevaison", "Reparación de pinchazo", "Puncture repair", 5000), ("Entretien flotte d'entreprise", "Mantenimiento de flota", "Fleet maintenance", 0)], [T("Sur rendez-vous", "Con cita previa", "By appointment")])
G(S, "atelier", "motos", "moto", ["Haojue", "Yamaha", "Honda"], T("{b} {v}", "{b} {v}", "{b} {v}"), [("125 cm³", "125 cc", "125 cc", 895000), ("Crypton 115", "Crypton 115", "Crypton 115", 845000), ("Casque intégral", "Casco integral", "Full-face helmet", 35000)], [])


# ───────────── 3 bis) Compléments pour approcher 100 articles par showroom ─────────────
S = "electric-store"
G(S, "electricite", "appareillage", "socket", ["Legrand", "Schneider", "Hager"], T("{b} {v}", "{b} {v}", "{b} {v}"), [("prise 2P+T", "enchufe 2P+T", "2P+E socket", 2500), ("interrupteur va-et-vient", "conmutador", "two-way switch", 2200), ("double prise", "enchufe doble", "double socket", 4500), ("prise USB", "enchufe USB", "USB socket", 9500), ("prise étanche IP55", "enchufe estanco IP55", "IP55 outdoor socket", 5500)], cross=True)
G(S, "electricite", "tableaux", "panel", ["Schneider", "Hager"], T("Disjoncteur {b} {v}", "Disyuntor {b} {v}", "{b} {v} breaker"), [("10 A", 4200), ("20 A", 4500), ("25 A", 4800), ("40 A", 6500), ("63 A", 9500)], cross=True)
G(S, "electricite", "cables", "bolt", ["Nexans"], T("Câble 2,5 mm² {v} · 100 m", "Cable 2,5 mm² {v} · 100 m", "2.5 mm² cable, {v} · 100 m"), [("rouge", "rojo", "red", 38000), ("bleu", "azul", "blue", 38000), ("vert-jaune", "verde-amarillo", "green-yellow", 38000), ("noir", "negro", "black", 38000)])
G(S, "eclairage", "ampoules", "bulb", ["Philips", "Osram"], T("Ampoule LED {b} {v}", "Bombilla LED {b} {v}", "{b} LED bulb {v}"), [("5 W E27", 1500), ("9 W E27", 1900), ("15 W E27", 2900), ("20 W E27", 3900), ("7 W GU10", 2500), ("30 W E40", 9500)], cross=True)
G(S, "energie", "onduleurs", "battery", ["Victron", "Ventage Electric"], T("Batterie solaire {v}", "Batería solar {v}", "{v} solar battery"), [("100 Ah", 125000), ("150 Ah", 175000)], cross=True)

S = "paint-store"
G(S, "peinture", "interieur", "paint", ["Ventage Paint"], T("Peinture intérieure mate {v} · 5 L", "Pintura interior mate {v} · 5 L", "Matt interior paint, {v} · 5 L"), [(a, b, c, 12500) for (a, b, c) in COL], [T("Fabriquée en Guinée équatoriale", "Fabricada en Guinea Ecuatorial", "Made in Equatorial Guinea")], {"Contenance": "5 L"})
G(S, "peinture", "laques", "brush", ["Ventage Paint"], T("Laque brillante {v} · 1 L", "Esmalte brillante {v} · 1 L", "Gloss paint, {v} · 1 L"), [("blanc", "blanco", "white", 8500), ("noir", "negro", "black", 8500), ("rouge vif", "rojo vivo", "bright red", 9500), ("bleu roi", "azul real", "royal blue", 9500), ("vert bouteille", "verde botella", "bottle green", 9500), ("gris anthracite", "gris antracita", "charcoal", 9500), ("jaune", "amarillo", "yellow", 9500), ("marron", "marrón", "brown", 8500)], [])
G(S, "peinture", "exterieur", "paint", ["Ventage Paint"], T("Peinture façade {v} · 20 L", "Pintura de fachada {v} · 20 L", "Exterior paint, {v} · 20 L"), [(a, b, c, 56000) for (a, b, c) in COL[6:]], [T("Résiste aux UV et à la pluie", "Resiste a UV y lluvia", "UV and rain resistant")], {"Contenance": "20 L"})
G(S, "outils-peintre", "rouleaux", "roller", ["Ventage Paint"], T("{v}", "{v}", "{v}"), [("Rouleau anti-goutte 180 mm", "Rodillo antigoteo 180 mm", "180 mm no-drip roller", 4500), ("Rouleau mousse 60 mm", "Rodillo de espuma 60 mm", "60 mm foam roller", 2500), ("Brosse à rechampir 30 mm", "Paletina 30 mm", "30 mm cutting-in brush", 2500), ("Brosse plate 70 mm", "Brocha plana 70 mm", "70 mm flat brush", 3500), ("Spalter 100 mm", "Brocha ancha 100 mm", "100 mm wide brush", 4500), ("Kit rouleau + bac", "Kit rodillo + cubeta", "Roller & tray kit", 6500)], [])
G(S, "preparation", "enduits", "trowel", ["Ventage Paint"], T("{v}", "{v}", "{v}"), [("Couteau à enduire 25 cm", "Llana de enlucir 25 cm", "25 cm taping knife", 4500), ("Papier abrasif · lot de 10", "Papel de lija · pack de 10", "Sandpaper · 10", 2500), ("Bande à joint 90 m", "Cinta de juntas 90 m", "90 m joint tape", 3500), ("Enduit hydrofuge · 15 kg", "Masilla hidrófuga · 15 kg", "Water-repellent filler · 15 kg", 14500)], [])
G(S, "deco-murale", "papiers-peints", "wall", ["Ventage Deco"], T("Papier peint {v} · rouleau", "Papel pintado {v} · rollo", "{v} wallpaper · roll"), [("feuillage", "follaje", "foliage", 12500), ("géométrique", "geométrico", "geometric", 11500), ("effet bois", "efecto madera", "wood effect", 11500), ("enfant étoiles", "infantil estrellas", "kids' stars", 9500)], [])

S = "construction"
G(S, "carrelage", "sols-murs", "tile", ["Ventage Build"], T("Carrelage {v} · le m²", "Cerámica {v} · el m²", "{v} tiles · per m²"), [("grès cérame 60×60 gris", "gres 60×60 gris", "60×60 grey porcelain", 13500), ("grès cérame 60×60 beige", "gres 60×60 beige", "60×60 beige porcelain", 13500), ("grès poli 80×80 blanc", "gres pulido 80×80 blanco", "80×80 polished white", 19500), ("faïence décor 25×40", "azulejo decorado 25×40", "25×40 décor wall", 10500), ("carreau ciment 20×20", "baldosa hidráulica 20×20", "20×20 cement tile", 17500), ("terrazzo 60×60", "terrazo 60×60", "60×60 terrazzo", 21500), ("plinthes · le mètre", "rodapié · el metro", "skirting · per metre", 2500), ("colle carrelage · 25 kg", "cemento cola · 25 kg", "tile adhesive · 25 kg", 7500)], [])
G(S, "plomberie", "tubes", "pipe", ["Ventage Build"], T("Tube PVC Ø{v} · 4 m", "Tubo PVC Ø{v} · 4 m", "Ø{v} PVC pipe · 4 m"), [("40", 3500), ("50", 4200), ("63", 5200), ("75", 6500), ("125", 12500), ("160", 18500)], [])
G(S, "outillage", "main", "hammer", ["Stanley", "Facom"], T("{v}", "{v}", "{v}"), [("Scie égoïne", "Serrucho", "Handsaw", 8500), ("Tournevis · jeu de 8", "Destornilladores · juego de 8", "Screwdriver set · 8", 12500), ("Pince multiprise", "Alicate de pico de loro", "Groove-joint pliers", 7500), ("Clé à molette", "Llave inglesa", "Adjustable wrench", 6500), ("Cutter pro", "Cúter profesional", "Utility knife", 3500), ("Cordeau de traçage", "Tiralíneas", "Chalk line", 4500), ("Équerre de maçon", "Escuadra de albañil", "Builder's square", 5500), ("Gants de chantier · 10 paires", "Guantes de obra · 10 pares", "Work gloves · 10 pairs", 7500), ("Casque de chantier", "Casco de obra", "Hard hat", 5500), ("Chaussures de sécurité", "Calzado de seguridad", "Safety boots", 25000)], [])
G(S, "carrelage", "sanitaire", "toilet", ["Roca", "Ventage Build"], T("{v}", "{v}", "{v}"), [("Meuble salle de bain 80 cm", "Mueble de baño 80 cm", "80 cm bathroom vanity", 165000), ("Miroir LED 80 cm", "Espejo LED 80 cm", "80 cm LED mirror", 65000), ("Chasse d'eau complète", "Cisterna completa", "Complete cistern", 25000), ("Abattant WC", "Tapa de inodoro", "Toilet seat", 12500), ("Chauffe-eau solaire 200 L", "Calentador solar 200 L", "200 L solar water heater", 0)], [])

S = "amanda-pharmacies"
G(S, "dermo", "visage", "pill", ["Avène", "Vichy", "La Roche-Posay", "Bioderma", "CeraVe", "Nivea"], T("{b} {v}", "{b} {v}", "{b} {v}"), [("crème hydratante 50 ml", "crema hidratante 50 ml", "moisturiser 50 ml", 16500), ("gel nettoyant 400 ml", "gel limpiador 400 ml", "cleansing gel 400 ml", 13500), ("eau micellaire 500 ml", "agua micelar 500 ml", "micellar water 500 ml", 11500)], HL["dermo"], cross=True)
G(S, "dermo", "solaires", "sun", ["Avène", "La Roche-Posay", "Bioderma"], T("{b} {v}", "{b} {v}", "{b} {v}"), [("crème solaire SPF 50+ 50 ml", "protector solar SPF 50+ 50 ml", "SPF 50+ sun cream 50 ml", 14500), ("spray solaire SPF 50 200 ml", "spray solar SPF 50 200 ml", "SPF 50 sun spray 200 ml", 19500)], HL["dermo"], cross=True)
G(S, "hygiene-sante", "dentaire", "tooth", ["Sensodyne", "Elmex", "Oral-B", "Signal"], T("{b} {v}", "{b} {v}", "{b} {v}"), [("dentifrice dents sensibles", "pasta dientes sensibles", "sensitive toothpaste", 4500), ("brosse à dents souple", "cepillo suave", "soft toothbrush", 2500)], [], cross=True)

S = "megastore-km5"
G(S, "electro", "froid", "fridge", ["Samsung", "LG", "Hisense", "Haier", "Beko"], T("Réfrigérateur {b} {v}", "Frigorífico {b} {v}", "{b} fridge, {v}"), [("combiné 340 L", "combi 340 L", "340 L fridge-freezer", 395000), ("double porte 450 L", "dos puertas 450 L", "450 L double-door", 545000), ("table top 120 L", "bajo encimera 120 L", "120 L under-counter", 145000), ("side-by-side 520 L", "side-by-side 520 L", "520 L side-by-side", 845000)], [T("Froid ventilé No Frost", "Frío No Frost", "No Frost cooling")], cross=True)
G(S, "electro", "clim", "ac", ["LG", "Samsung", "Gree"], T("Climatiseur {b} split {v}", "Aire acondicionado {b} split {v}", "{b} {v} split air conditioner"), [("12 000 BTU", 325000), ("18 000 BTU", 465000)], [T("Technologie Inverter", "Tecnología Inverter", "Inverter technology")], cross=True)

S = "amanda-labs"
G(S, "hematologie", "biochimie", "flask", ["Amanda Labs"], T("{v}", "{v}", "{v}"), [("Magnésium", "Magnesio", "Magnesium", 5000), ("Phosphore", "Fósforo", "Phosphorus", 5000), ("Albumine", "Albúmina", "Albumin", 5000), ("Protéines totales", "Proteínas totales", "Total protein", 5000), ("Phosphatases alcalines", "Fosfatasa alcalina", "Alkaline phosphatase", 5000), ("Amylase / lipase", "Amilasa / lipasa", "Amylase / lipase", 12000), ("CPK", "CPK", "CPK", 8000), ("Troponine", "Troponina", "Troponin", 18000), ("Vitamine B12", "Vitamina B12", "Vitamin B12", 20000), ("Fer sérique", "Hierro sérico", "Serum iron", 6000), ("D-dimères", "Dímero D", "D-dimer", 18000), ("Fibrinogène", "Fibrinógeno", "Fibrinogen", 7000)], [T("Résultats rapides", "Resultados rápidos", "Fast results")])
G(S, "hormones", "fertilite", "dna", ["Amanda Labs"], T("{v}", "{v}", "{v}"), [("Cortisol", "Cortisol", "Cortisol", 15000), ("Insuline", "Insulina", "Insulin", 15000), ("ACE (marqueur colon)", "CEA (marcador colon)", "CEA (bowel marker)", 20000), ("CA 125 (marqueur ovaire)", "CA 125 (marcador ovario)", "CA 125 (ovarian marker)", 22000), ("CA 15-3 (marqueur sein)", "CA 15-3 (marcador mama)", "CA 15-3 (breast marker)", 22000), ("Alpha-fœtoprotéine", "Alfafetoproteína", "Alpha-fetoprotein", 20000), ("PSA libre", "PSA libre", "Free PSA", 18000)], [T("Résultats rapides", "Resultados rápidos", "Fast results")])
G(S, "infectiologie", "serologies", "virus", ["Amanda Labs"], T("{v}", "{v}", "{v}"), [("Anticorps anti-HBs", "Anticuerpos anti-HBs", "Anti-HBs antibodies", 10000), ("Hépatite A IgM", "Hepatitis A IgM", "Hepatitis A IgM", 12000), ("Cytomégalovirus IgG / IgM", "Citomegalovirus IgG / IgM", "CMV IgG / IgM", 18000), ("Herpès IgG / IgM", "Herpes IgG / IgM", "Herpes IgG / IgM", 18000), ("ASLO", "ASLO", "ASO titre", 8000), ("Facteur rhumatoïde", "Factor reumatoide", "Rheumatoid factor", 8000)], [T("Résultats rapides", "Resultados rápidos", "Fast results")])

S = "megastore-ela-nguema"
G(S, "tv", "smart-tv", "tv", ["Samsung", "LG", "Hisense", "TCL"], T("Smart TV {b} {v}", "Smart TV {b} {v}", "{b} {v} Smart TV"), [("4K 50″", 285000), ("4K 55″", 335000), ("4K 65″", 525000)], [T("Netflix, YouTube et Prime Video", "Netflix, YouTube y Prime Video", "Netflix, YouTube and Prime Video")], cross=True)
G(S, "literie", "linge", "pillow", ["Ventage Home"], T("Parure de draps {v} · 160×200", "Juego de sábanas {v} · 160×200", "{v} sheet set · 160×200"), [("blanc", "blanco", "white", 32000), ("gris", "gris", "grey", 32000), ("bleu nuit", "azul noche", "midnight blue", 32000), ("wax imprimé", "wax estampado", "wax print", 35000)], [])

S = "tires-auto"
G(S, "pieces", "batteries", "car", ["Varta", "Bosch", "Exide"], T("Batterie {b} 12 V {v}", "Batería {b} 12 V {v}", "{b} 12 V battery, {v}"), [("60 Ah", 68000), ("75 Ah", 82000), ("100 Ah", 115000)], [T("Test de charge offert", "Test de carga gratis", "Free charge test")], cross=True)
G(S, "lubrifiants", "huiles", "oil", ["Total", "Shell", "Castrol", "Mobil"], T("Huile moteur {b} {v}", "Aceite de motor {b} {v}", "{b} engine oil {v}"), [("5W-30 · 5 L", 32000), ("15W-40 diesel · 5 L", 21000)], [], cross=True)

S = "electronics-office"
G(S, "mobile", "smartphones", "phone", ["Samsung", "Apple", "Tecno", "Infinix", "Xiaomi", "Itel", "Oppo", "Huawei"], T("{b} {v}", "{b} {v}", "{b} {v}"), [("Galaxy S24 Ultra 512 Go", "Galaxy S24 Ultra 512 GB", "Galaxy S24 Ultra 512 GB", 1045000), ("iPhone 15 Pro Max 256 Go", "iPhone 15 Pro Max 256 GB", "iPhone 15 Pro Max 256 GB", 995000), ("Camon 30", "Camon 30", "Camon 30", 165000), ("Note 40", "Note 40", "Note 40", 135000), ("Redmi 13C", "Redmi 13C", "Redmi 13C", 85000), ("P55", "P55", "P55", 69000), ("Reno 11", "Reno 11", "Reno 11", 265000), ("Nova 12", "Nova 12", "Nova 12", 245000)], HL["mobile"])
G(S, "accessoires-tech", "audio-tech", "earbuds", ["JBL", "Sony", "Oraimo", "Samsung"], T("{b} {v}", "{b} {v}", "{b} {v}"), [("écouteurs sans fil", "auriculares inalámbricos", "wireless earbuds", 39000), ("casque Bluetooth", "auriculares Bluetooth", "Bluetooth headphones", 59000), ("enceinte portable", "altavoz portátil", "portable speaker", 45000)], [])

S = "ventage-mall"
pass
pass
pass

S = "supermercado"
G(S, "frais", "fruits-legumes", "apple", ["Ventage Family"], T("{v}", "{v}", "{v}"), [("Bananes plantain · le régime", "Plátanos macho · el racimo", "Plantains · per bunch", 3500), ("Manioc · le kg", "Yuca · el kg", "Cassava · per kg", 700), ("Ignames · le kg", "Ñame · el kg", "Yams · per kg", 900), ("Avocats · le kg", "Aguacates · el kg", "Avocados · per kg", 1500), ("Tomates · le kg", "Tomates · el kg", "Tomatoes · per kg", 1200), ("Ananas pièce", "Piña unidad", "Pineapple, each", 1000), ("Mangues · le kg", "Mangos · el kg", "Mangoes · per kg", 1200)], HL["frais"])
G(S, "frais", "boucherie", "fish", ["Ventage Family"], T("{v}", "{v}", "{v}"), [("Crevettes · le kg", "Gambas · el kg", "Prawns · per kg", 9500), ("Bar entier · le kg", "Lubina entera · el kg", "Whole sea bass · per kg", 6500), ("Côtelettes d'agneau · le kg", "Chuletas de cordero · el kg", "Lamb chops · per kg", 9500), ("Saucisses · 500 g", "Salchichas · 500 g", "Sausages · 500 g", 3500)], HL["frais"])
G(S, "frais", "cremerie", "cup", ["Président", "Danone", "Ventage Family"], T("{v}", "{v}", "{v}"), [("Yaourts nature · 8", "Yogures naturales · 8", "Plain yoghurts · 8", 3200), ("Beurre doux 250 g", "Mantequilla 250 g", "Butter 250 g", 2500), ("Fromage râpé 200 g", "Queso rallado 200 g", "Grated cheese 200 g", 2900), ("Camembert 250 g", "Camembert 250 g", "Camembert 250 g", 3500)], HL["frais"])

# ───────────── 3 bis) Ventage Supermercado : ~200 articles photographiés (tools/super_products.py) ─────────────
from super_products import rows as super_rows
for name, brand, cat, sub, price, old, photo, icon in super_rows():
    fr, es, en = name.split("|")
    pid = "us-" + hashlib.md5(fr.encode()).hexdigest()[:10]
    o2, fl = flags_for(pid, price)
    hl = list(HL.get(cat, []))
    if "le kg" in fr: hl = [T("Arrivage frais", "Llegada fresca", "Fresh delivery"), T("Prix au poids", "Precio al peso", "Priced by weight")]
    add(pid, "supermercado", brand, T(fr, es, en), cat, sub, photo, price, old or o2, fl, hl, {}, icon)

# ───────────── 3 ter) Amanda Pharmacies & Labs : catalogue élargi, sans prix (tools/amanda_products.py) ─────────────
import amanda_products as AM
HL_AM = {"amanda-pharmacies": [T("Conseil du pharmacien", "Consejo del farmacéutico", "Pharmacist's advice"), T("Disponible en officine", "Disponible en farmacia", "Available in store")],
         "amanda-labs": [T("Prélèvement sur place ou à domicile", "Extracción en el centro o a domicilio", "Sample taken on site or at home"), T("Résultats en ligne sécurisés", "Resultados en línea seguros", "Secure online results")]}
for name, brand, cat, sub in AM.rows():
    sr = "amanda-labs" if brand == "Amanda Labs" else "amanda-pharmacies"
    fr = name.split("|")[0]
    pid = "am-" + hashlib.md5((sr + fr).encode()).hexdigest()[:10]
    add(pid, sr, brand, name, cat, sub, None, None, None, flags_for(pid, 1)[1], HL_AM[sr], {}, {"conseil": "pill", "complements": "capsule", "dermo": "pill", "hygiene-sante": "tooth", "maman-bebe": "baby", "materiel-medical": "heart"}.get(cat, "flask"))

S = "ventage-casa"
G(S, "maison", "deco", "lamp", ["Ventage Home"], T("{v}", "{v}", "{v}"), [("Miroir rond doré 80 cm", "Espejo redondo dorado 80 cm", "80 cm round gold mirror", 65000), ("Vase céramique", "Jarrón de cerámica", "Ceramic vase", 19500), ("Coussins velours · lot de 2", "Cojines de terciopelo · pack de 2", "Velvet cushions · set of 2", 19500), ("Tableau toile 90×60", "Cuadro en lienzo 90×60", "90×60 canvas print", 35000), ("Bougies parfumées · coffret", "Velas perfumadas · estuche", "Scented candles · gift set", 15000), ("Étagère murale bois", "Estante de pared de madera", "Wooden wall shelf", 25000)], [])
G(S, "pro", "sieges", "sofa", ["Ventage Pro"], T("{v}", "{v}", "{v}"), [("Fauteuil de bureau ergonomique", "Silla de oficina ergonómica", "Ergonomic office chair", 125000), ("Chaise visiteur · lot de 4", "Silla de confidente · pack de 4", "Visitor chairs · set of 4", 145000), ("Banquette d'accueil 3 places", "Bancada de espera 3 plazas", "Three-seat reception bench", 165000)], [])
G(S, "pro", "bureaux", "table", ["Ventage Pro"], T("{v}", "{v}", "{v}"), [("Bureau de direction 180 cm", "Mesa de dirección 180 cm", "180 cm executive desk", 345000), ("Bureau opératif 140 cm", "Mesa operativa 140 cm", "140 cm office desk", 125000), ("Armoire de rangement haute", "Armario alto de oficina", "Tall storage cabinet", 165000)], [])

# Doublons de nom dans un même showroom → on garde le premier
seen, OUT, AMI = set(), [], {}
for p in PRODUCTS:
    k = (p[1], p[3].split("|")[0])
    if k in seen: continue
    if p[1] == "supermercado" and not p[6]: continue  # supermarché : uniquement des articles photographiés
    if p[1] in ("amanda-pharmacies", "amanda-labs"):  # pharmacie et laboratoire : pas de prix affiché
        p[7] = p[8] = None
        if not p[6]:
            n = AMI.get(p[5], 0); AMI[p[5]] = n + 1; p[6] = AM.photo_for(p[5], n)
    seen.add(k); p[7] = p[7] or None; OUT.append(p)

count = {}
for p in OUT: count[p[1]] = count.get(p[1], 0) + 1
photos = {}
for p in OUT:
    if p[6]: photos[p[1]] = photos.get(p[1], 0) + 1
print("produits:", len(OUT)); print(json.dumps(count, indent=0)); print("avec photo:", json.dumps(photos))

cats_js = json.dumps([{k: v for k, v in c.items() if v is not None} for c in CATS], ensure_ascii=False, separators=(",", ":"))
prods_js = ",\n".join(json.dumps(p, ensure_ascii=False, separators=(",", ":")) for p in OUT)
head = OLD[:OLD.index("const UNIVERS = [")]
js = (head + "const UNIVERS = " + UNIVERS_JS + ";\n\n"
      "  /* Showrooms — whatsapp / phone / hours / address : par showroom (par défaut, numéro du groupe) */\n"
      "  const SHOWROOMS = " + SHOWROOMS_JS + ";\n"
      "  SHOWROOMS.forEach((s) => { s.photos = s.photos.map((p) => (/^assets\\//.test(p) ? p : W + p)); });\n\n"
      "  /* Rayons (générés par tools/build_catalog.py) */\n"
      "  const CATEGORIES = " + cats_js + ";\n"
      "  CATEGORIES.forEach((c) => (c.subs = c.subs.map((s) => s.slice())));\n\n"
      "  /* Produits : [id, showroom, marque, nom, rayon, sous-rayon, photo, prix, ancien prix, drapeaux, points forts, caractéristiques, pictogramme]\n"
      "     photo : clé assets/img, « dj:<chemin>:<n> » (catalogue de démo en ligne, n vues) ou null (pictogramme) ; prix null = sur devis */\n"
      "  const PRODUCTS = [\n" + prods_js + "\n  ];\n\n"
      "  window.VENTAGE = { W, GROUP, UNIVERS, SHOWROOMS, CATEGORIES, PRODUCTS };\n})();\n")
open(os.path.join(ROOT, "js/catalog.js"), "w", encoding="utf-8").write(js)
print("catalog.js:", len(js) // 1024, "Ko")
