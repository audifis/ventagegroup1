# -*- coding: utf-8 -*-
"""Amanda Pharmacies & Amanda Labs : catalogue élargi, sans prix affiché (prix en officine / tarif sur demande).
Photos : Unsplash (licence libre, usage commercial), réparties par sous-rayon.
Format des lignes : nom fr|es|en ; marque ; rayon ; sous-rayon"""

P = "photo-"
POOLS = {
  # ── Pharmacie ──
  "douleur": ["1762328494330-6bed4db5e7f9", "1631980839320-77eed020776c", "1630094539354-441ee6e76835", "1592323818181-f9b967ff537c", "1522335579687-9c718c5184d7", "1646392206581-2527b1cae5cb"],
  "rhume": ["1709294991506-f41feb81eaf6", "1635166304271-04931640a450", "1728931710064-57f73342f5f5", "1610300052051-a79c1ab1f8e8", "1774907324089-72473a9f5770", "1729949131717-a29b5dccb1e3"],
  "digestion": ["1563213126-a4273aed2016", "1592323818279-0ff7babdcb75", "1544829894-eb023ba95a38", "1571934811356-5cc061b6821f"],
  "phyto": ["1567922045116-2a00fae2ed03", "1627435601361-ec25f5b1d0e5", "1576092768241-dec231879fc3", "1648455321715-e8ed86188c0e", "1515377905703-c4788e51af15", "1605040056130-38d9faad3534", "1608571423539-e951b9b3871e"],
  "vitamines": ["1664956618021-73c47736845e", "1664216294580-079bc527ae49", "1648139346494-2b961c5a2bb7", "1664786908163-85ca46f85138", "1670850756917-8ed6c2a71e12", "1763668331599-487470fb85b2", "1664216294573-b28282de564b"],
  "forme": ["1559087316-6b27308e53f6", "1670850757263-6efc07d410f8", "1597121798359-e9ee76aa0478", "1698365140635-42894e5e63b4"],
  "visage": ["1680537260333-20fd95432044", "1599022484220-967921f2217c", "1763812770943-0b76492a38f0", "1768235146463-328c98e7234d", "1768631428503-2254505968c4", "1782506905834-b1a90c245c11", "1789334353841-1df6c2443385", "1643379850274-77d2e3703ef9", "1762583487195-41feba9a4d5a"],
  "corps": ["1632452479455-e3d5e3159b63", "1780770738499-5ade63b1f6c3", "1611072965169-e1534f6f300c", "1595432576728-94e0e94a7663"],
  "solaires": ["1623676714504-edd78728155e", "1594055103006-7871176f1a7e", "1698912198250-fb0c5ecccc6e", "1738721796993-5f42d9315689", "1721913395444-0cd6856a864c"],
  "dentaire": ["1676897288522-e8a081e71430", "1693692273603-3b9e13789298", "1693692258834-74c62f467cb7", "1702631899147-75902f6765c6"],
  "intime": ["1776105609708-3d8908ab4dc2", "1789108978116-2763682414a4"],
  "laits": ["1765031092161-a9ebe556117e", "1642055514517-7b52288890ec"],
  "soins-bebe": ["1597178938674-c4660b8843c0", "1716372409137-7ad0100d57ab"],
  "autotest": ["1615486511484-92e172cc4fe0", "1594790628624-9e563bea851d", "1683727186226-910f31a9da45", "1684156486280-ff59f07fc5bb", "1623658045230-605cb00c80d6", "1624454002429-40ed87a5ec04", "1700832082200-af7deeb63d9b"],
  "secours": ["1564144573017-8dc932e0039e", "1765996796562-ce301df337a0", "1531054601929-f1ccb3ef57f7", "1683899473390-b75e267c7aa3", "1700832082152-0416a3ee5e60"],
  "moustiques": ["1611072965169-e1534f6f300c", "1595432576728-94e0e94a7663"],
  # ── Laboratoire ──
  "hemato": ["1606206591513-adbfbdd7a177", "1697192156499-d85cfe1452c0", "1639772823849-6efbd173043c", "1631557675464-77cf8f0d9426"],
  "biochimie": ["1599556147783-7edf67c327e0", "1579154341184-22069e4614d2", "1532187863486-abf9dbad1b69", "1614935151651-0bea6508db6b", "1582560475093-ba66accbc424", "1579154204601-01588f351e67"],
  "thyroide": ["1614308459036-779d0dfe51ff", "1582719471384-894fbb16e074"],
  "fertilite": ["1631217868264-e5b90bb7e133", "1758691462878-6edc3d3da1be", "1630959305790-4c956ce6c0b6", "1562789233-495f52b583dd"],
  "paludisme": ["1630959305606-3123a081dada", "1639772823907-a716be4bdecc", "1511174511562-5f7f18b874f8"],
  "serologies": ["1581091007718-0c50d599bfd0", "1727091506038-5451111dc2fb", "1611694449252-02453c27856a", "1578308175085-444a1fbea0fe", "1581594549595-35f6edc7b762"],
  "urines-selles": ["1595154038281-4beb9195415b", "1631557676757-fcc7b1160be8", "1486825586573-7131f7991bdd"],
  "packs": ["1758691461990-03b49d969495", "1581056771107-24ca5f033842", "1584516150909-c43483ee7932"],
  "entreprises": ["1631217871099-88310a909a32", "1605781231474-f60dea478e8a"],
}

NEW = r"""
Paracétamol 500 mg · 16 comprimés|Paracetamol 500 mg · 16 comprimidos|Paracetamol 500 mg · 16 tablets;Amanda Santé;conseil;douleur
Paracétamol 1 g · 8 comprimés|Paracetamol 1 g · 8 comprimidos|Paracetamol 1 g · 8 tablets;Amanda Santé;conseil;douleur
Paracétamol effervescent 500 mg · 16|Paracetamol efervescente 500 mg · 16|Effervescent paracetamol 500 mg · 16;Amanda Santé;conseil;douleur
Ibuprofène 400 mg · 20 comprimés|Ibuprofeno 400 mg · 20 comprimidos|Ibuprofen 400 mg · 20 tablets;Amanda Santé;conseil;douleur
Ibuprofène 200 mg · 30 comprimés|Ibuprofeno 200 mg · 30 comprimidos|Ibuprofen 200 mg · 30 tablets;Amanda Santé;conseil;douleur
Paracétamol sirop enfant 100 ml|Paracetamol jarabe infantil 100 ml|Children's paracetamol syrup 100 ml;Amanda Santé;conseil;douleur
Gel anti-douleur musculaire 100 g|Gel para dolores musculares 100 g|Muscle pain relief gel 100 g;Amanda Santé;conseil;douleur
Patchs chauffants dos · 4|Parches térmicos espalda · 4|Heat patches for back · 4;Amanda Santé;conseil;douleur
Baume décontractant 30 g|Bálsamo relajante 30 g|Soothing balm 30 g;Amanda Santé;conseil;douleur
Spray froid sport 400 ml|Spray frío deportivo 400 ml|Cold spray for sports 400 ml;Amanda Santé;conseil;douleur
Pastilles gorge miel citron · 24|Pastillas garganta miel limón · 24|Honey lemon throat lozenges · 24;Amanda Santé;conseil;rhume
Sirop toux sèche 125 ml|Jarabe tos seca 125 ml|Dry cough syrup 125 ml;Amanda Santé;conseil;rhume
Sirop toux grasse 200 ml|Jarabe tos con flemas 200 ml|Chesty cough syrup 200 ml;Amanda Santé;conseil;rhume
Sirop toux enfant au miel 150 ml|Jarabe tos infantil con miel 150 ml|Children's honey cough syrup 150 ml;Amanda Santé;conseil;rhume
Spray nasal eau de mer 100 ml|Spray nasal agua de mar 100 ml|Sea-water nasal spray 100 ml;Amanda Santé;conseil;rhume
Sérum physiologique · 40 unidoses|Suero fisiológico · 40 monodosis|Saline solution · 40 single doses;Amanda Santé;conseil;rhume
Vitamine C 1000 mg effervescente · 20|Vitamina C 1000 mg efervescente · 20|Effervescent vitamin C 1000 mg · 20;Amanda Santé;conseil;rhume
Inhalateur décongestionnant|Inhalador descongestionante|Decongestant inhaler;Amanda Santé;conseil;rhume
Baume pectoral 50 g|Bálsamo pectoral 50 g|Chest rub 50 g;Amanda Santé;conseil;rhume
Spray gorge apaisant 30 ml|Spray calmante para la garganta 30 ml|Soothing throat spray 30 ml;Amanda Santé;conseil;rhume
Sels de réhydratation orale · 10 sachets|Sales de rehidratación oral · 10 sobres|Oral rehydration salts · 10 sachets;Amanda Santé;conseil;digestion
Charbon actif · 30 gélules|Carbón activado · 30 cápsulas|Activated charcoal · 30 capsules;Amanda Santé;conseil;digestion
Antiacide à croquer · 24 comprimés|Antiácido masticable · 24 comprimidos|Chewable antacid · 24 tablets;Amanda Santé;conseil;digestion
Probiotiques flore intestinale · 10 gélules|Probióticos flora intestinal · 10 cápsulas|Gut flora probiotics · 10 capsules;Amanda Santé;conseil;digestion
Fibres de psyllium 200 g|Fibra de psyllium 200 g|Psyllium fibre 200 g;Amanda Santé;conseil;digestion
Pansement gastrique · 20 sachets|Protector gástrico · 20 sobres|Stomach-lining relief · 20 sachets;Amanda Santé;conseil;digestion
Tisane digestion · 20 sachets|Infusión digestiva · 20 bolsitas|Digestion herbal tea · 20 bags;Amanda Santé;complements;phyto
Tisane sommeil · 20 sachets|Infusión para dormir · 20 bolsitas|Sleep herbal tea · 20 bags;Amanda Santé;complements;phyto
Tisane minceur · 20 sachets|Infusión adelgazante · 20 bolsitas|Slimming herbal tea · 20 bags;Amanda Santé;complements;phyto
Thé vert bio · 25 sachets|Té verde ecológico · 25 bolsitas|Organic green tea · 25 bags;Amanda Santé;complements;phyto
Huile essentielle d'eucalyptus 10 ml|Aceite esencial de eucalipto 10 ml|Eucalyptus essential oil 10 ml;Amanda Santé;complements;phyto
Huile essentielle de lavande 10 ml|Aceite esencial de lavanda 10 ml|Lavender essential oil 10 ml;Amanda Santé;complements;phyto
Huile essentielle d'arbre à thé 10 ml|Aceite esencial de árbol de té 10 ml|Tea tree essential oil 10 ml;Amanda Santé;complements;phyto
Huile de nigelle 100 ml|Aceite de comino negro 100 ml|Black seed oil 100 ml;Amanda Santé;complements;phyto
Miel de Manuka 250 g|Miel de Manuka 250 g|Manuka honey 250 g;Amanda Santé;complements;phyto
Moringa · 60 gélules|Moringa · 60 cápsulas|Moringa · 60 capsules;Amanda Santé;complements;phyto
Gingembre · 60 gélules|Jengibre · 60 cápsulas|Ginger · 60 capsules;Amanda Santé;complements;phyto
Calcium + vitamine D3 · 60 comprimés|Calcio + vitamina D3 · 60 comprimidos|Calcium + vitamin D3 · 60 tablets;Amanda Santé;complements;vitamines
Vitamine B complexe · 30 comprimés|Complejo vitamínico B · 30 comprimidos|Vitamin B complex · 30 tablets;Amanda Santé;complements;vitamines
Vitamines gommes enfants · 60|Gominolas vitaminadas infantiles · 60|Children's vitamin gummies · 60;Amanda Santé;complements;vitamines
Multivitamines adultes · 60 comprimés|Multivitaminas adultos · 60 comprimidos|Adult multivitamins · 60 tablets;Amanda Santé;complements;vitamines
Vitamines grossesse · 30 gélules|Vitaminas embarazo · 30 cápsulas|Pregnancy vitamins · 30 capsules;Amanda Santé;complements;vitamines
Collagène marin · 30 sticks|Colágeno marino · 30 sticks|Marine collagen · 30 sticks;Amanda Santé;complements;vitamines
Biotine cheveux & ongles · 60|Biotina cabello y uñas · 60|Biotin hair & nails · 60;Amanda Santé;complements;vitamines
Fortifiant énergie · 20 ampoules|Tónico energía · 20 ampollas|Energy tonic · 20 phials;Amanda Santé;complements;forme
Échinacée immunité · 30 gélules|Equinácea inmunidad · 30 cápsulas|Echinacea immunity · 30 capsules;Amanda Santé;complements;forme
Coenzyme Q10 · 30 gélules|Coenzima Q10 · 30 cápsulas|Coenzyme Q10 · 30 capsules;Amanda Santé;complements;forme
Articulations glucosamine · 60|Articulaciones glucosamina · 60|Joint glucosamine · 60;Amanda Santé;complements;forme
Sérum vitamine C éclat 30 ml|Sérum vitamina C luminosidad 30 ml|Vitamin C radiance serum 30 ml;Amanda Santé;dermo;visage
Sérum acide hyaluronique 30 ml|Sérum ácido hialurónico 30 ml|Hyaluronic acid serum 30 ml;Amanda Santé;dermo;visage
Huile visage squalane 30 ml|Aceite facial escualano 30 ml|Squalane face oil 30 ml;Amanda Santé;dermo;visage
Crème de nuit régénérante 50 ml|Crema de noche regeneradora 50 ml|Regenerating night cream 50 ml;Amanda Santé;dermo;visage
Contour des yeux 15 ml|Contorno de ojos 15 ml|Eye contour cream 15 ml;Amanda Santé;dermo;visage
Masque purifiant à l'argile 75 ml|Mascarilla purificante de arcilla 75 ml|Purifying clay mask 75 ml;Amanda Santé;dermo;visage
Beurre de karité pur 150 g|Manteca de karité pura 150 g|Pure shea butter 150 g;Amanda Santé;dermo;corps
Crème anti-vergetures 150 ml|Crema antiestrías 150 ml|Stretch-mark cream 150 ml;Amanda Santé;dermo;corps
Crème pieds secs 100 ml|Crema pies secos 100 ml|Dry feet cream 100 ml;Amanda Santé;dermo;corps
Huile corps sèche 100 ml|Aceite corporal seco 100 ml|Dry body oil 100 ml;Amanda Santé;dermo;corps
Crème solaire visage teintée SPF 50 · 40 ml|Crema solar facial con color SPF 50 · 40 ml|Tinted face sunscreen SPF 50 · 40 ml;Amanda Santé;dermo;solaires
Lait solaire famille SPF 30 · 250 ml|Leche solar familiar SPF 30 · 250 ml|Family sun lotion SPF 30 · 250 ml;Amanda Santé;dermo;solaires
Stick solaire lèvres SPF 30|Stick solar labial SPF 30|Lip sun stick SPF 30;Amanda Santé;dermo;solaires
Gel après-soleil aloe vera 200 ml|Gel aftersun aloe vera 200 ml|Aloe vera after-sun gel 200 ml;Amanda Santé;dermo;solaires
Dentifrice blancheur 75 ml|Pasta dental blanqueadora 75 ml|Whitening toothpaste 75 ml;Amanda Santé;hygiene-sante;dentaire
Brossettes interdentaires · 8|Cepillos interdentales · 8|Interdental brushes · 8;Amanda Santé;hygiene-sante;dentaire
Dentifrice enfants 2-6 ans 50 ml|Pasta dental infantil 2-6 años 50 ml|Kids' toothpaste ages 2-6 50 ml;Amanda Santé;hygiene-sante;dentaire
Gel lavant antibactérien 500 ml|Gel lavante antibacteriano 500 ml|Antibacterial body wash 500 ml;Amanda Santé;hygiene-sante;intime
Lingettes intimes · 20|Toallitas íntimas · 20|Intimate wipes · 20;Amanda Santé;hygiene-sante;intime
Coton démaquillant · 80 disques|Discos desmaquillantes · 80|Cotton pads · 80;Amanda Santé;hygiene-sante;intime
Lait de suite en poudre 400 g|Leche de continuación en polvo 400 g|Follow-on formula 400 g;Amanda Santé;maman-bebe;laits
Petits pots légumes dès 6 mois · 2|Potitos de verduras desde 6 meses · 2|Vegetable baby jars from 6 months · 2;Amanda Santé;maman-bebe;laits
Tétine physiologique 0-6 mois|Chupete fisiológico 0-6 meses|Orthodontic dummy 0-6 months;Amanda Santé;maman-bebe;soins-bebe
Lait de toilette bébé 500 ml|Leche limpiadora bebé 500 ml|Baby cleansing milk 500 ml;Amanda Santé;maman-bebe;soins-bebe
Thermomètre frontal sans contact|Termómetro frontal sin contacto|Non-contact forehead thermometer;Amanda Santé;materiel-medical;autotest
Thermomètre digital|Termómetro digital|Digital thermometer;Amanda Santé;materiel-medical;autotest
Tensiomètre bras automatique|Tensiómetro de brazo automático|Automatic upper-arm blood pressure monitor;Amanda Santé;materiel-medical;autotest
Lancettes stériles · 100|Lancetas estériles · 100|Sterile lancets · 100;Amanda Santé;materiel-medical;autotest
Test de grossesse · 2|Test de embarazo · 2|Pregnancy test · 2;Amanda Santé;materiel-medical;autotest
Stéthoscope double pavillon|Estetoscopio de doble campana|Dual-head stethoscope;Amanda Santé;materiel-medical;autotest
Désinfectant cutané 125 ml|Antiséptico cutáneo 125 ml|Skin antiseptic 125 ml;Amanda Santé;materiel-medical;secours
Bande extensible 4 m × 10 cm|Venda elástica 4 m × 10 cm|Stretch bandage 4 m × 10 cm;Amanda Santé;materiel-medical;secours
Sparadrap hypoallergénique|Esparadrapo hipoalergénico|Hypoallergenic tape;Amanda Santé;materiel-medical;secours
Trousse de secours voyage|Botiquín de viaje|Travel first-aid kit;Amanda Santé;materiel-medical;secours
Coussin chauffant / froid réutilisable|Compresa frío-calor reutilizable|Reusable hot/cold pack;Amanda Santé;materiel-medical;secours
Spray anti-moustiques zones tropicales 100 ml|Spray antimosquitos zonas tropicales 100 ml|Tropical mosquito spray 100 ml;Amanda Santé;materiel-medical;moustiques
Bracelets anti-moustiques · 2|Pulseras antimosquitos · 2|Mosquito-repellent bands · 2;Amanda Santé;materiel-medical;moustiques
Crème apaisante piqûres 40 ml|Crema calmante picaduras 40 ml|Bite soothing cream 40 ml;Amanda Santé;materiel-medical;moustiques
Acide folique (vitamine B9)|Ácido fólico (vitamina B9)|Folic acid (vitamin B9);Amanda Labs;hematologie;hemato
Temps de céphaline activée (TCA)|Tiempo de tromboplastina parcial (TTPa)|Activated partial thromboplastin time (aPTT);Amanda Labs;hematologie;hemato
Frottis sanguin|Frotis de sangre|Blood smear;Amanda Labs;hematologie;hemato
Numération des plaquettes|Recuento de plaquetas|Platelet count;Amanda Labs;hematologie;hemato
Recherche d'agglutinines irrégulières (RAI)|Anticuerpos irregulares (EAI)|Irregular antibody screening;Amanda Labs;hematologie;hemato
Test de Coombs direct|Test de Coombs directo|Direct Coombs test;Amanda Labs;hematologie;hemato
Bilan d'hémostase complet|Estudio de coagulación completo|Full coagulation panel;Amanda Labs;hematologie;hemato
Glycémie post-prandiale|Glucemia posprandial|Post-prandial blood glucose;Amanda Labs;hematologie;biochimie
Hyperglycémie provoquée par voie orale (HGPO)|Prueba de tolerancia oral a la glucosa|Oral glucose tolerance test;Amanda Labs;hematologie;biochimie
Clairance de la créatinine|Aclaramiento de creatinina|Creatinine clearance;Amanda Labs;hematologie;biochimie
LDH|LDH|LDH;Amanda Labs;hematologie;biochimie
Lactates|Lactato|Lactate;Amanda Labs;hematologie;biochimie
NT-proBNP (insuffisance cardiaque)|NT-proBNP (insuficiencia cardiaca)|NT-proBNP (heart failure);Amanda Labs;hematologie;biochimie
Homocystéine|Homocisteína|Homocysteine;Amanda Labs;hematologie;biochimie
Zinc sérique|Zinc sérico|Serum zinc;Amanda Labs;hematologie;biochimie
Cholestérol HDL / LDL|Colesterol HDL / LDL|HDL / LDL cholesterol;Amanda Labs;hematologie;biochimie
Triglycérides|Triglicéridos|Triglycerides;Amanda Labs;hematologie;biochimie
Parathormone (PTH)|Parathormona (PTH)|Parathyroid hormone (PTH);Amanda Labs;hormones;thyroide
Thyroglobuline|Tiroglobulina|Thyroglobulin;Amanda Labs;hormones;thyroide
Anticorps anti-thyroglobuline|Anticuerpos antitiroglobulina|Anti-thyroglobulin antibodies;Amanda Labs;hormones;thyroide
Calcitonine|Calcitonina|Calcitonin;Amanda Labs;hormones;thyroide
DHEA-S|DHEA-S|DHEA-S;Amanda Labs;hormones;fertilite
ACTH|ACTH|ACTH;Amanda Labs;hormones;fertilite
Hormone de croissance (GH)|Hormona del crecimiento (GH)|Growth hormone (GH);Amanda Labs;hormones;fertilite
Marqueurs sériques trisomie 21|Cribado bioquímico de trisomía 21|Down syndrome serum screening;Amanda Labs;hormones;fertilite
CA 19-9 (marqueur pancréas)|CA 19-9 (marcador páncreas)|CA 19-9 (pancreas marker);Amanda Labs;hormones;fertilite
Bêta-HCG quantitative de suivi|Beta-HCG cuantitativa de seguimiento|Follow-up quantitative beta-HCG;Amanda Labs;hormones;fertilite
Recherche de microfilaires|Búsqueda de microfilarias|Microfilariae screening;Amanda Labs;infectiologie;paludisme
Sérologie bilharziose|Serología esquistosomiasis|Schistosomiasis serology;Amanda Labs;infectiologie;paludisme
Sérologie amibiase|Serología amebiasis|Amoebiasis serology;Amanda Labs;infectiologie;paludisme
Recherche de BK (tuberculose)|Baciloscopia (tuberculosis)|AFB smear (tuberculosis);Amanda Labs;infectiologie;paludisme
QuantiFERON-TB|QuantiFERON-TB|QuantiFERON-TB;Amanda Labs;infectiologie;paludisme
Charge virale hépatite B|Carga viral hepatitis B|Hepatitis B viral load;Amanda Labs;infectiologie;serologies
Antigène HBe / anticorps anti-HBe|Antígeno HBe / anticuerpos anti-HBe|HBe antigen / anti-HBe antibodies;Amanda Labs;infectiologie;serologies
Sérologie hépatite E|Serología hepatitis E|Hepatitis E serology;Amanda Labs;infectiologie;serologies
PCR gonocoque & chlamydia|PCR gonococo y clamidia|Gonorrhoea & chlamydia PCR;Amanda Labs;infectiologie;serologies
Mycoplasmes urogénitaux|Micoplasmas urogenitales|Urogenital mycoplasma;Amanda Labs;infectiologie;serologies
Sérologie varicelle|Serología varicela|Chickenpox serology;Amanda Labs;infectiologie;serologies
Sérologie oreillons / rougeole|Serología paperas / sarampión|Mumps / measles serology;Amanda Labs;infectiologie;serologies
Antibiogramme|Antibiograma|Antibiogram;Amanda Labs;infectiologie;urines-selles
Recherche de sang occulte dans les selles|Sangre oculta en heces|Faecal occult blood test;Amanda Labs;infectiologie;urines-selles
Calprotectine fécale|Calprotectina fecal|Faecal calprotectin;Amanda Labs;infectiologie;urines-selles
Scotch-test (oxyures)|Test de Graham (oxiuros)|Sellotape test (pinworms);Amanda Labs;infectiologie;urines-selles
Protéinurie des 24 heures|Proteinuria de 24 horas|24-hour urine protein;Amanda Labs;infectiologie;urines-selles
Prélèvement streptocoque B (grossesse)|Exudado estreptococo B (embarazo)|Group B strep swab (pregnancy);Amanda Labs;infectiologie;urines-selles
Bilan fertilité du couple|Estudio de fertilidad de pareja|Couple fertility panel;Amanda Labs;bilans;packs
Bilan anémie|Estudio de anemia|Anaemia panel;Amanda Labs;bilans;packs
Bilan fatigue|Estudio de cansancio|Fatigue panel;Amanda Labs;bilans;packs
Bilan pré-opératoire|Estudio preoperatorio|Pre-operative panel;Amanda Labs;bilans;packs
Bilan fièvre (paludisme, typhoïde, NFS)|Estudio de fiebre (paludismo, tifoidea, hemograma)|Fever panel (malaria, typhoid, FBC);Amanda Labs;bilans;packs
Bilan grossesse 2e trimestre|Estudio embarazo 2.º trimestre|Second-trimester pregnancy panel;Amanda Labs;bilans;packs
Bilan dépistage IST|Estudio de cribado de ITS|STI screening panel;Amanda Labs;bilans;packs
Bilan ostéoporose|Estudio de osteoporosis|Osteoporosis panel;Amanda Labs;bilans;packs
Check-up express|Chequeo exprés|Express check-up;Amanda Labs;bilans;packs
Bilan manipulateurs alimentaires|Estudio manipuladores de alimentos|Food handler screening;Amanda Labs;bilans;entreprises
Visite médicale annuelle des salariés|Revisión médica anual de empleados|Annual staff medical check;Amanda Labs;bilans;entreprises
Dépistage paludisme en entreprise|Cribado de paludismo en empresa|Workplace malaria screening;Amanda Labs;bilans;entreprises
Tests avant voyage|Pruebas antes de viajar|Pre-travel tests;Amanda Labs;bilans;entreprises
"""

def rows():
    out = []
    for line in NEW.strip().splitlines():
        name, brand, cat, sub = line.split(";")
        out.append((name, brand, cat, sub))
    return out

def photo_for(sub, i):
    pool = POOLS.get(sub)
    return ("us:" + P + pool[i % len(pool)]) if pool else None
