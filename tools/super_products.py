# -*- coding: utf-8 -*-
"""Ventage Supermercado : ~200 articles photographiés.
Noms et prix : relevés sur Jumia Côte d'Ivoire (FCFA) pour les produits de marque, majorés d'environ 20 %
pour le marché de Malabo ; produits frais au prix du marché. Photos : Unsplash (licence libre, usage commercial),
clé « us:photo-… » servie par images.unsplash.com (recadrage et WebP à la volée).
Format : nom fr|es|en ; marque ; rayon ; sous-rayon ; prix ; ancien prix (ou vide) ; photo"""

ROWS = r"""
Ananas pain de sucre · pièce|Piña · unidad|Pineapple, each;Ventage Family;frais;fruits-legumes;1200;;1589820296156-2454bb8a6ad1
Papaye solo · pièce|Papaya · unidad|Papaya, each;Ventage Family;frais;fruits-legumes;1300;;1526318472351-c75fcf070305
Mangues Kent · le kg|Mangos Kent · el kg|Kent mangoes · per kg;Ventage Family;frais;fruits-legumes;1800;;1553279768-865429fa0078
Mangues locales · panier 3 kg|Mangos locales · cesta 3 kg|Local mangoes · 3 kg basket;Ventage Family;frais;fruits-legumes;3500;4200;1757281096599-b9165ba74008
Pastèque · pièce|Sandía · unidad|Watermelon, each;Ventage Family;frais;fruits-legumes;2800;;1593356261955-a4be882ee52b
Citrons verts · le kg|Limas · el kg|Limes · per kg;Ventage Family;frais;fruits-legumes;1500;;1620101680155-b251043b700b
Citrons jaunes · filet 1 kg|Limones · malla 1 kg|Lemons · 1 kg net;Ventage Family;frais;fruits-legumes;2200;;1621817845389-472c0473423d
Oranges à jus · le kg|Naranjas de zumo · el kg|Juicing oranges · per kg;Ventage Family;frais;fruits-legumes;1400;;1645378193840-f4a90003285d
Bananes douces · le kg|Plátanos · el kg|Bananas · per kg;Ventage Family;frais;fruits-legumes;900;;1571771894821-ce9b6c11b08e
Bananes vertes · le régime|Plátanos verdes · el racimo|Green bananas · per bunch;Ventage Family;frais;fruits-legumes;3000;;1760696473646-ca046232002b
Avocats · lot de 4|Aguacates · pack de 4|Avocados · pack of 4;Ventage Family;frais;fruits-legumes;2000;;1671624749229-7d37826013b5
Poires · le kg|Peras · el kg|Pears · per kg;Ventage Family;frais;fruits-legumes;2800;;1615484477778-ca3b77940c25
Pêches · le kg|Melocotones · el kg|Peaches · per kg;Ventage Family;frais;fruits-legumes;3500;;1517355352485-3c18847c2f7d
Pommes rouges · le kg|Manzanas rojas · el kg|Red apples · per kg;Ventage Family;frais;fruits-legumes;2400;;1587131808575-655697d61a4e
Fruit du dragon · pièce|Pitahaya · unidad|Dragon fruit, each;Ventage Family;frais;fruits-legumes;1800;;1783749895140-29897fd142c7
Panier de fruits tropicaux|Cesta de frutas tropicales|Tropical fruit basket;Ventage Family;frais;fruits-legumes;12000;14500;1619566636858-adf3ef46400b
Noix de coco · pièce|Coco · unidad|Coconut, each;Ventage Family;frais;fruits-legumes;600;;1560769680-ba2f3767c785
Oignons rouges · le kg|Cebollas rojas · el kg|Red onions · per kg;Ventage Family;frais;fruits-legumes;1000;;1618512496248-a07fe83aa8cb
Oignons jaunes · filet 2 kg|Cebollas amarillas · malla 2 kg|Brown onions · 2 kg net;Ventage Family;frais;fruits-legumes;1700;;1518977956812-cd3dbadaaf31
Ail · filet 500 g|Ajo · malla 500 g|Garlic · 500 g net;Ventage Family;frais;fruits-legumes;1500;;1585849834908-3481231155e8
Gingembre frais · 250 g|Jengibre fresco · 250 g|Fresh ginger · 250 g;Ventage Family;frais;fruits-legumes;800;;1630623093145-f606591c2546
Pommes de terre · sac 5 kg|Patatas · saco 5 kg|Potatoes · 5 kg sack;Ventage Family;frais;fruits-legumes;4500;;1518977676601-b53f82aba655
Pommes de terre nouvelles · le kg|Patatas nuevas · el kg|New potatoes · per kg;Ventage Family;frais;fruits-legumes;1000;;1590165482129-1b8b27698780
Carottes fanes · la botte|Zanahorias con hojas · manojo|Bunched carrots;Ventage Family;frais;fruits-legumes;1200;;1598170845058-32b9d6a5da37
Carottes · le kg|Zanahorias · el kg|Carrots · per kg;Ventage Family;frais;fruits-legumes;1100;;1590868309235-ea34bed7bd7f
Poivrons tricolores · lot de 3|Pimientos tricolor · pack de 3|Mixed peppers · pack of 3;Ventage Family;frais;fruits-legumes;1800;;1774712471470-5aa92dfc94ae
Poivrons rouges · le kg|Pimientos rojos · el kg|Red peppers · per kg;Ventage Family;frais;fruits-legumes;2500;;1766537289146-f04fce265258
Piment rouge frais · 250 g|Guindilla roja fresca · 250 g|Fresh red chillies · 250 g;Ventage Family;frais;fruits-legumes;700;;1757577244288-5ef1ec654d6c
Piment habanero · 250 g|Chile habanero · 250 g|Habanero chillies · 250 g;Ventage Family;frais;fruits-legumes;900;;1788182149209-c56d0c440a37
Gombo frais · 500 g|Quimbombó fresco · 500 g|Fresh okra · 500 g;Ventage Family;frais;fruits-legumes;900;;1568640895956-e2bad65027b0
Tomates & concombres · panier|Tomates y pepinos · cesta|Tomatoes & cucumbers · basket;Ventage Family;frais;fruits-legumes;2500;;1592924802543-809bfeee53fb
Aubergines & courgettes · le kg|Berenjenas y calabacines · el kg|Aubergines & courgettes · per kg;Ventage Family;frais;fruits-legumes;1800;;1787697790048-6c657067af2b
Panier de légumes de saison|Cesta de verduras de temporada|Seasonal vegetable box;Ventage Family;frais;fruits-legumes;8500;9900;1590779033100-9f60a05a013d
Salade composée prête à servir|Ensalada mixta lista para servir|Ready-to-eat mixed salad;Ventage Family;frais;fruits-legumes;2500;;1540420773420-3366772f4999
Entrecôte de bœuf · le kg|Entrecot de ternera · el kg|Beef rib-eye · per kg;Ventage Family;frais;boucherie;11500;;1690983329845-638ec321647d
Steaks de bœuf · 2 × 200 g|Filetes de ternera · 2 × 200 g|Beef steaks · 2 × 200 g;Ventage Family;frais;boucherie;5500;;1695683948382-868cd8d516fe
Bœuf à braiser · le kg|Ternera para guisar · el kg|Braising beef · per kg;Ventage Family;frais;boucherie;7000;;1602470521006-59ab77068b0d
Viande hachée · barquette 500 g|Carne picada · bandeja 500 g|Minced beef · 500 g tray;Ventage Family;frais;boucherie;4200;;1611038333075-2efd28705f42
Émincé de bœuf · 500 g|Tiras de ternera · 500 g|Sliced beef · 500 g;Ventage Family;frais;boucherie;4500;;1602470520998-f4a52199a3d6
Colis viande famille · 3 kg|Lote de carne familiar · 3 kg|Family meat box · 3 kg;Ventage Family;frais;boucherie;22000;26000;1690983323238-0b91789e1b5a
Poulet fermier découpé · le kg|Pollo de corral troceado · el kg|Free-range chicken pieces · per kg;Ventage Family;frais;boucherie;4500;;1587593810167-a84920ea0781
Blancs de poulet · 500 g|Pechugas de pollo · 500 g|Chicken breasts · 500 g;Ventage Family;frais;boucherie;3800;;1682991136736-a2b44623eeba
Poulet entier prêt à cuire|Pollo entero listo para cocinar|Whole oven-ready chicken;Ventage Family;frais;boucherie;6500;;1672787153720-e85fe802fd9f
Dorades royales · le kg|Doradas · el kg|Gilt-head bream · per kg;Ventage Family;frais;boucherie;7500;;1510130387422-82bed34b37e9
Maquereaux frais · le kg|Caballas frescas · el kg|Fresh mackerel · per kg;Ventage Family;frais;boucherie;3500;;1576330383200-2bf325cfec52
Vivaneau rouge · le kg|Pargo rojo · el kg|Red snapper · per kg;Ventage Family;frais;boucherie;6500;;1611214774777-3d997a9d0e35
Plateau de fruits de mer|Bandeja de marisco|Seafood platter;Ventage Family;frais;boucherie;28000;;1615141982883-c7ad0e69fd62
Sardines fraîches · le kg|Sardinas frescas · el kg|Fresh sardines · per kg;Ventage Family;frais;boucherie;2500;;1498654200943-1088dd4438ae
Tilapia entier · le kg|Tilapia entera · el kg|Whole tilapia · per kg;Ventage Family;frais;boucherie;4000;;1534948216015-843149f72be3
Crevettes royales · 500 g|Langostinos · 500 g|King prawns · 500 g;Ventage Family;frais;boucherie;7500;;1548587468-971ebe4c8c3b
Salami tranché · 200 g|Salami en lonchas · 200 g|Sliced salami · 200 g;Ventage Family;frais;boucherie;2800;;1768758922609-fd805f703507
Saucisson sec · 250 g|Salchichón · 250 g|Dry-cured sausage · 250 g;Ventage Family;frais;boucherie;3200;;1769772511161-08b61a55f553
Assortiment charcuterie · 300 g|Surtido de embutidos · 300 g|Charcuterie selection · 300 g;Ventage Family;frais;boucherie;4800;;1460122109654-7e46ab4fc9b9
Lait frais entier 1 L|Leche fresca entera 1 L|Fresh whole milk 1 L;Ventage Family;frais;cremerie;1300;;1517448931760-9bf4414148c5
Lait demi-écrémé UHT · 6 × 1 L|Leche semidesnatada UHT · 6 × 1 L|Semi-skimmed UHT milk · 6 × 1 L;Ventage Family;frais;cremerie;6500;;1616534077365-f63f0d75f311
Œufs frais · boîte de 12|Huevos frescos · caja de 12|Fresh eggs · box of 12;Ventage Family;frais;cremerie;2200;;1506976785307-8732e854ad03
Œufs bruns · lot de 6|Huevos morenos · pack de 6|Brown eggs · 6-pack;Ventage Family;frais;cremerie;1200;;1498654077810-12c21d4d6dc3
Yaourt brassé nature 500 g|Yogur natural batido 500 g|Plain stirred yoghurt 500 g;Ventage Family;frais;cremerie;1900;;1571212515416-fef01fc43637
Crème fraîche épaisse 20 cl|Nata espesa 20 cl|Thick crème fraîche 20 cl;Ventage Family;frais;cremerie;1500;;1604095853918-1a1823a63dd5
Fromage à pâte dure · 250 g|Queso curado · 250 g|Hard cheese · 250 g;Ventage Family;frais;cremerie;3800;;1653150103131-25569a19958d
Beurre demi-sel 250 g|Mantequilla con sal 250 g|Salted butter 250 g;Ventage Family;frais;cremerie;2600;;1608100743854-decfbbea206e
Pain de campagne 500 g|Pan de payés 500 g|Country loaf 500 g;Ventage Family;frais;boulangerie;1200;;1599940778173-e276d4acb2bb
Pain complet aux céréales 500 g|Pan integral de cereales 500 g|Wholegrain loaf 500 g;Ventage Family;frais;boulangerie;1500;;1613929231151-d7571591259e
Pain de mie maison 600 g|Pan de molde artesano 600 g|Homemade sandwich loaf 600 g;Ventage Family;frais;boulangerie;1400;;1587912001191-0cd4f14fd89e
Miche au levain 800 g|Hogaza de masa madre 800 g|Sourdough loaf 800 g;Ventage Family;frais;boulangerie;2200;;1586657263857-346c4b712ff5
Petits pains · lot de 6|Panecillos · pack de 6|Bread rolls · 6-pack;Ventage Family;frais;boulangerie;1200;;1651604033534-e66b281f1981
Croissants au beurre · lot de 4|Cruasanes de mantequilla · pack de 4|Butter croissants · 4-pack;Ventage Family;frais;boulangerie;2000;;1555507036-ab1f4038808a
Croissants · lot de 10|Cruasanes · pack de 10|Croissants · 10-pack;Ventage Family;frais;boulangerie;4500;5200;1747459707229-7b1b7c8367e0
Viennoiseries assorties · lot de 6|Bollería variada · pack de 6|Assorted pastries · 6-pack;Ventage Family;frais;boulangerie;3600;;1597528662465-55ece5734101
Pâtisseries du jour · boîte de 6|Pasteles del día · caja de 6|Today's cakes · box of 6;Ventage Family;frais;boulangerie;6000;;1483695028939-5bb13f8648b0
Panier du boulanger · pains variés|Cesta del panadero · panes variados|Baker's basket · assorted breads;Ventage Family;frais;boulangerie;5000;;1568254183919-78a4f43a2877
Frites surgelées 2,5 kg|Patatas fritas congeladas 2,5 kg|Frozen chips 2.5 kg;Ventage Family;frais;surgeles;5500;;1615485290836-4ebcebf44aaf
Frites allumettes surgelées 1 kg|Patatas paja congeladas 1 kg|Frozen French fries 1 kg;Ventage Family;frais;surgeles;2500;;1691442152248-1c44043ef6e7
Pizza margherita surgelée 400 g|Pizza margarita congelada 400 g|Frozen margherita pizza 400 g;Ventage Family;frais;surgeles;3500;;1681290794225-cc4739bc86c0
Crevettes décortiquées surgelées 1 kg|Gambas peladas congeladas 1 kg|Frozen peeled prawns 1 kg;Ventage Family;frais;surgeles;9500;11000;1674066625481-8cffd7cf5aac
Crevettes cuites · 500 g|Gambas cocidas · 500 g|Cooked prawns · 500 g;Ventage Family;frais;surgeles;5500;;1559737558-2f5a35f4523b
Glaces assorties · bac 2 L|Helados variados · tarrina 2 L|Assorted ice cream · 2 L tub;Ventage Family;frais;surgeles;5500;;1567206563064-6f60f40a2b57
Cornets glacés · boîte de 6|Conos helados · caja de 6|Ice cream cones · box of 6;Ventage Family;frais;surgeles;4500;;1629385701021-fcd568a743e8
Gelato artisanal · pot 500 ml|Gelato artesano · tarrina 500 ml|Artisan gelato · 500 ml tub;Ventage Family;frais;surgeles;3500;;1780444122216-dad92e90090f
Colis surgelés famille|Lote de congelados familiar|Family frozen food box;Ventage Family;frais;surgeles;15000;18000;1566454825481-4e48f80aa4d7
Riz long grain thaï parfumé · sac 5 kg|Arroz tailandés aromático · saco 5 kg|Fragrant Thai long-grain rice · 5 kg;Dinor;epicerie;base;5800;;1686820740687-426a7b9b2043
Riz vietnamien jasmine · sac 5 kg|Arroz vietnamita jazmín · saco 5 kg|Vietnamese jasmine rice · 5 kg;Dinor;epicerie;base;3400;4700;1586201375761-83865001e31c
Riz basmati · sac 4,5 kg|Arroz basmati · saco 4,5 kg|Basmati rice · 4.5 kg;Ginny;epicerie;base;5100;6600;1723475158232-819e29803f4d
Riz jasmine parfumé 900 g|Arroz jazmín aromático 900 g|Fragrant jasmine rice 900 g;Delicia;epicerie;base;750;1000;1643622357625-c013987d90e7
Spaghetti · carton 40 × 200 g|Espaguetis · caja 40 × 200 g|Spaghetti · case of 40 × 200 g;Maman;epicerie;base;10000;;1551462147-ff29053bfc14
Coquillettes 500 g|Coditos 500 g|Elbow pasta 500 g;Panzani;epicerie;base;800;;1612966893103-790e549a2ab1
Penne rigate 500 g|Penne rigate 500 g|Penne rigate 500 g;Panzani;epicerie;base;900;;1606091484089-089fa86fad4f
Farine de maïs · lot de 12 × 500 g|Harina de maíz · pack 12 × 500 g|Maize flour · 12 × 500 g;Alyssa;epicerie;base;4300;6000;1549590143-d5855148a9d5
Farine de blé T55 · 1 kg|Harina de trigo T55 · 1 kg|T55 wheat flour · 1 kg;Ventage Family;epicerie;base;900;;1749169439872-7cee08d9a71b
Haricots secs · 1 kg|Alubias secas · 1 kg|Dried beans · 1 kg;Ventage Family;epicerie;base;1500;;1586770974441-93360f202c43
Sardines à l'huile végétale 125 g|Sardinas en aceite vegetal 125 g|Sardines in vegetable oil 125 g;Roch;epicerie;conserves;450;;1653174577821-9ab410d92d44
Sardines pimentées à l'huile 125 g|Sardinas picantes en aceite 125 g|Spicy sardines in oil 125 g;Roch;epicerie;conserves;500;650;1561924018-4f213bdc7364
Sardines à l'huile · carton de 50|Sardinas en aceite · caja de 50|Sardines in oil · case of 50;Roch;epicerie;conserves;22000;29500;1738618140037-09e11c8e644a
Maquereau à la tomate 425 g|Caballa en tomate 425 g|Mackerel in tomato sauce 425 g;Ventage Family;epicerie;conserves;1200;;1653174577855-50996fe588c1
Tomate concentrée 400 g|Tomate concentrado 400 g|Tomato paste 400 g;Alyssa;epicerie;conserves;600;;1626607007733-d09228471d9f
Double concentré de tomates 370 g|Doble concentrado de tomate 370 g|Double tomato concentrate 370 g;Alyssa;epicerie;conserves;500;;1584263347416-85a696b4eda7
Tomates entières pelées 800 g|Tomates enteros pelados 800 g|Whole peeled tomatoes 800 g;Sole Mio;epicerie;conserves;2000;;1619995746608-bef3de4f075a
Maïs doux sans sucre ajouté 300 g|Maíz dulce sin azúcar añadido 300 g|Sweetcorn, no added sugar 300 g;Bonduelle;epicerie;conserves;2100;2400;1612676855298-c7116c892b1a
Soupes en conserve · lot de 4|Sopas en lata · pack de 4|Canned soups · 4-pack;Campbell's;epicerie;conserves;4000;;1534483509719-3feaee7c30da
Tomato ketchup Top Down 700 g|Kétchup Top Down 700 g|Top Down tomato ketchup 700 g;Heinz;epicerie;conserves;4400;5600;1633070818236-a3e15f3e91eb
Moutarde jaune américaine 400 g|Mostaza amarilla americana 400 g|American yellow mustard 400 g;Heinz;epicerie;conserves;2200;;1528750717929-32abb73d3bd9
Moutarde au miel 250 g|Mostaza a la miel 250 g|Honey mustard 250 g;Ventage Family;epicerie;conserves;2500;;1568584952743-6e30d4f404eb
Huile d'olive vierge extra 1 L|Aceite de oliva virgen extra 1 L|Extra virgin olive oil 1 L;Ventage Family;epicerie;huiles-epices;6500;;1474979266404-7eaacbcd87c5
Huile d'olive · lot de 3 bouteilles|Aceite de oliva · pack de 3 botellas|Olive oil · 3 bottles;Ventage Family;epicerie;huiles-epices;18000;21000;1757801333112-7b89af15c7fe
Huile de cuisson · flacon verseur 1 L|Aceite de cocina · aceitera 1 L|Cooking oil · 1 L pourer;Ventage Family;epicerie;huiles-epices;1800;;1552592074-ea7a91b851b3
Épices du monde · coffret de 6|Especias del mundo · estuche de 6|World spices · set of 6;Ventage Family;epicerie;huiles-epices;7500;;1771541897176-44a3e01dc484
Mélange d'épices africaines 200 g|Mezcla de especias africanas 200 g|African spice blend 200 g;Ventage Family;epicerie;huiles-epices;1500;;1716816211590-c15a328a5ff0
Cannelle, badiane & poivre · assortiment|Canela, anís estrellado y pimienta · surtido|Cinnamon, star anise & pepper · selection;Ventage Family;epicerie;huiles-epices;3500;;1581600140682-d4e68c8cde32
Piment en poudre 100 g|Guindilla en polvo 100 g|Chilli powder 100 g;Ventage Family;epicerie;huiles-epices;900;;1506368249639-73a05d6f6488
Curry en poudre 100 g|Curry en polvo 100 g|Curry powder 100 g;Ventage Family;epicerie;huiles-epices;1000;;1596040033229-a9821ebd058d
Épices en vrac du marché · 500 g|Especias a granel del mercado · 500 g|Market loose spices · 500 g;Ventage Family;epicerie;huiles-epices;1500;;1784382265423-d5b445f04405
Cacao en poudre sans sucre · 12 sachets|Cacao en polvo sin azúcar · 12 sobres|Unsweetened cocoa powder · 12 sachets;Tafissa;epicerie;petit-dej;1200;1300;1606914469633-bd39206ea739
Céréales corn flakes 750 g|Cereales corn flakes 750 g|Corn flakes 750 g;Kellogg's;epicerie;petit-dej;3800;;1521483451569-e33803c0330c
Pétales de maïs nature 375 g|Copos de maíz 375 g|Plain corn flakes 375 g;Ventage Family;epicerie;petit-dej;2500;;1788601690871-f0fe193ec0bc
Muesli croustillant 500 g|Muesli crujiente 500 g|Crunchy muesli 500 g;Ventage Family;epicerie;petit-dej;3500;;1504308805006-0f7a5f1f0f71
Miel pur · pot 500 g|Miel pura · tarro 500 g|Pure honey · 500 g jar;Ventage Family;epicerie;petit-dej;4500;;1558642452-9d2a7deb7f62
Miel de fleurs 250 g|Miel de flores 250 g|Wildflower honey 250 g;Ventage Family;epicerie;petit-dej;2800;;1587049352824-f7e128d4ebe5
Beurre de cacahuète 340 g|Crema de cacahuete 340 g|Peanut butter 340 g;Ventage Family;epicerie;petit-dej;2800;;1691480208637-6ed63aac6694
Confiture d'abricots 370 g|Mermelada de albaricoque 370 g|Apricot jam 370 g;Ventage Family;epicerie;petit-dej;1900;;1629240830845-e4a550a6bbde
Lait en poudre 400 g|Leche en polvo 400 g|Powdered milk 400 g;Bonnet Rouge;epicerie;petit-dej;4200;;1596151163116-98a5033814c2
Lait instantané · boîte 400 g|Leche instantánea · lata 400 g|Instant milk · 400 g tin;Laity;epicerie;petit-dej;2500;2650;1685967836586-aaefdda7b517
Cookies pépites de chocolat 200 g|Cookies con pepitas de chocolate 200 g|Chocolate chip cookies 200 g;Ventage Family;epicerie;biscuits;1500;;1558961363-fa8fdf82db35
Cookies maison · boîte 400 g|Cookies caseras · caja 400 g|Homestyle cookies · 400 g box;Ventage Family;epicerie;biscuits;3200;;1576717585968-8ea8166b89b8
Sablés au beurre 250 g|Galletas de mantequilla 250 g|Butter shortbread 250 g;Ventage Family;epicerie;biscuits;1800;;1589988802149-7f9cb13a468e
Biscuits au chocolat 300 g|Galletas de chocolate 300 g|Chocolate biscuits 300 g;Ventage Family;epicerie;biscuits;2000;;1621353354739-1420ff28ead9
Cookies · boîte familiale 1 kg|Cookies · caja familiar 1 kg|Cookies · 1 kg family tub;Ventage Family;epicerie;biscuits;6500;7500;1585329678734-285d3adee73c
Chips nature 150 g|Patatas fritas clásicas 150 g|Ready salted crisps 150 g;Ventage Family;epicerie;biscuits;1500;;1641693148759-843d17ceac24
Tortilla chips 200 g|Nachos 200 g|Tortilla chips 200 g;Ventage Family;epicerie;biscuits;1800;;1699666397768-0126340e880a
Chips à l'ancienne 125 g|Patatas fritas artesanas 125 g|Kettle crisps 125 g;Ventage Family;epicerie;biscuits;1600;;1613919113640-25732ec5e61f
Tablette chocolat noir 100 g|Tableta de chocolate negro 100 g|Dark chocolate bar 100 g;Ventage Family;epicerie;biscuits;1500;;1623660053975-cf75a8be0908
Chocolat au lait 100 g|Chocolate con leche 100 g|Milk chocolate 100 g;Ventage Family;epicerie;biscuits;1400;;1614088685112-0a760b71a3c8
Barres chocolatées · assortiment de 10|Barritas de chocolate · surtido de 10|Chocolate bars · assortment of 10;Ventage Family;epicerie;biscuits;4500;;1621939514649-280e2ee25f60
Chocolat noir & blanc · duo 2 × 100 g|Chocolate negro y blanco · dúo 2 × 100 g|Dark & white chocolate · 2 × 100 g;Ventage Family;epicerie;biscuits;2800;;1599599810769-bcde5a160d32
Bonbons assortis · 8 sachets|Caramelos surtidos · 8 bolsas|Assorted sweets · 8 bags;Ventage Family;epicerie;biscuits;3500;;1619471954205-3303b9b2da87
Raisins secs 500 g|Pasas 500 g|Raisins 500 g;Ventage Family;epicerie;biscuits;2500;;1691657917109-c6e027eac44a
Mélange de noix 300 g|Mezcla de frutos secos 300 g|Mixed nuts 300 g;Ventage Family;epicerie;biscuits;4500;;1633677491262-0a51b9851f46
Noix & amandes 500 g|Nueces y almendras 500 g|Walnuts & almonds 500 g;Ventage Family;epicerie;biscuits;6500;;1648288718348-4b6d53755716
Figues séchées 500 g|Higos secos 500 g|Dried figs 500 g;Ventage Family;epicerie;biscuits;3800;4700;1629738601425-494c3d6ba3e2
Eau minérale · 6 × 1,5 L|Agua mineral · 6 × 1,5 L|Mineral water · 6 × 1.5 L;Ventage Family;boissons;eaux-jus;2800;;1788375077205-76daee0b1e51
Eau de source 1,5 L|Agua de manantial 1,5 L|Spring water 1.5 L;Ventage Family;boissons;eaux-jus;500;;1616118132534-381148898bb4
Bonbonne d'eau 19 L|Garrafa de agua 19 L|19 L water jug;Ventage Family;boissons;eaux-jus;4500;;1783309529184-75986d6e472a
Eau minérale 50 cl · pack de 12|Agua mineral 50 cl · pack de 12|Mineral water 50 cl · 12-pack;Ventage Family;boissons;eaux-jus;3000;;1561041695-d2fadf9f318c
Jus d'orange pressé 1 L|Zumo de naranja exprimido 1 L|Freshly squeezed orange juice 1 L;Pressea;boissons;eaux-jus;2200;;1782292016930-74679437f72b
100 % Passion 1 L · lot de 2|100 % Maracuyá 1 L · pack de 2|100% Passion fruit 1 L · 2-pack;Pressea;boissons;eaux-jus;4400;4800;1640213505284-21352ee0d76b
Nectar de mangue 1 L · lot de 2|Néctar de mango 1 L · pack de 2|Mango nectar 1 L · 2-pack;Pressea;boissons;eaux-jus;2950;3200;1650547001322-145ff2c0bed7
Jus d'orange · 2 L + 50 cl|Zumo de naranja · 2 L + 50 cl|Orange juice · 2 L + 50 cl;Ventage Family;boissons;eaux-jus;3200;;1782292016925-4a5b60798e0f
Smoothie fruits frais 1 L|Smoothie de frutas frescas 1 L|Fresh fruit smoothie 1 L;Ventage Family;boissons;eaux-jus;2500;;1650547002496-e7ed9df4bf3c
Coca-Cola 33 cl · pack de 6|Coca-Cola 33 cl · pack de 6|Coca-Cola 33 cl · 6-pack;Coca-Cola;boissons;sodas;3600;;1605548230624-8d2d0419c517
Coca-Cola Light 33 cl · pack de 6|Coca-Cola Light 33 cl · pack de 6|Diet Coke 33 cl · 6-pack;Coca-Cola;boissons;sodas;3600;;1600871254391-89876f6a9959
Coca-Cola Zéro 50 cl · pack de 6|Coca-Cola Zero 50 cl · pack de 6|Coca-Cola Zero 50 cl · 6-pack;Coca-Cola;boissons;sodas;4200;;1600320183466-7198f22d3c8a
Sodas assortis · 7 canettes|Refrescos variados · 7 latas|Assorted sodas · 7 cans;Ventage Family;boissons;sodas;3800;;1527960471264-932f39eb5846
Sodas · pack fête 24 canettes|Refrescos · pack fiesta 24 latas|Sodas · 24-can party pack;Ventage Family;boissons;sodas;12000;13500;1674176508097-463b009c6004
Boissons fraîches · assortiment de 12|Bebidas frías · surtido de 12|Cold drinks · assortment of 12;Ventage Family;boissons;sodas;7500;;1761281137117-42da05306117
Café en grains torréfié 500 g|Café en grano tostado 500 g|Roasted coffee beans 500 g;Ventage Family;boissons;cafe-the;6500;;1620820186187-fc32e79adb74
Café en grains intense 250 g|Café en grano intenso 250 g|Intense coffee beans 250 g;Ventage Family;boissons;cafe-the;3500;;1605170512248-d03f7f10b168
Café torréfié artisanal 500 g|Café tostado artesano 500 g|Artisan roasted coffee 500 g;Ventage Family;boissons;cafe-the;5500;;1638126687923-31912a6ee0ff
Expresso · 36 dosettes|Espresso · 36 monodosis|Espresso · 36 pods;Carte Noire;boissons;cafe-the;10700;;1643427609198-d6e51c69682c
Café 3 en 1 · 11 sachets|Café 3 en 1 · 11 sobres|3-in-1 coffee · 11 sachets;Nescafé;boissons;cafe-the;1500;;1643427577448-770e77fccdc3
Cappuccino · 8 sticks|Capuchino · 8 sticks|Cappuccino · 8 sticks;L'Or;boissons;cafe-the;4850;;1643426879831-b20d0d9e0110
Thé noir Earl Grey · 25 sachets|Té negro Earl Grey · 25 bolsitas|Earl Grey black tea · 25 bags;Ventage Family;boissons;cafe-the;1500;;1546648596-d8318bfcf491
Heineken 33 cl · pack de 6|Heineken 33 cl · pack de 6|Heineken 33 cl · 6-pack;Heineken;boissons;alcools;6500;;1618885472179-5e474019f2a9
Bière blonde 33 cl · pack de 24|Cerveza rubia 33 cl · pack de 24|Lager 33 cl · 24-pack;Ventage Family;boissons;alcools;18000;21000;1767023447884-e809b3620c16
Bière ambrée 50 cl · pack de 6|Cerveza tostada 50 cl · pack de 6|Amber beer 50 cl · 6-pack;Ventage Family;boissons;alcools;6000;;1600213903598-25be92abde40
Bière blonde 65 cl|Cerveza rubia 65 cl|Lager 65 cl;Ventage Family;boissons;alcools;1000;;1644085159285-5fd924740cb3
Vin rouge Rioja 75 cl|Vino tinto Rioja 75 cl|Rioja red wine 75 cl;Ventage Family;boissons;alcools;9500;;1610631787813-9eeb1a2386cc
Vin rouge de table 75 cl|Vino tinto de mesa 75 cl|Red table wine 75 cl;Ventage Family;boissons;alcools;5500;;1764874299343-e55d7af327cd
Vin blanc sec 75 cl|Vino blanco seco 75 cl|Dry white wine 75 cl;Ventage Family;boissons;alcools;7500;;1562601579-599dec564e06
Vins · carton découverte 6 bouteilles|Vinos · caja descubrimiento 6 botellas|Wine · 6-bottle discovery case;Ventage Family;boissons;alcools;45000;52000;1578911373434-0cb395d2cbfb
Old No.7 Tennessee whiskey 70 cl|Old No.7 whiskey de Tennessee 70 cl|Old No.7 Tennessee whiskey 70 cl;Jack Daniel's;boissons;alcools;28000;;1580537922571-ca7180cd700e
Whisky blended 70 cl|Whisky blended 70 cl|Blended whisky 70 cl;Ventage Family;boissons;alcools;15000;;1696182736807-5d21e38056ec
Whisky single malt 70 cl|Whisky single malt 70 cl|Single malt whisky 70 cl;Ventage Family;boissons;alcools;38000;;1718882301007-112132d54602
Rhum ambré 70 cl|Ron añejo 70 cl|Dark rum 70 cl;Ventage Family;boissons;alcools;12000;;1622234967875-a7971ef704c2
Spiritueux · coffret 3 bouteilles|Licores · estuche de 3 botellas|Spirits · 3-bottle gift set;Ventage Family;boissons;alcools;45000;;1691017296011-ea9532242c7e
Lessive liquide concentrée 2 L|Detergente líquido concentrado 2 L|Concentrated liquid detergent 2 L;Ariel;entretien;menage;6500;;1649005011845-ef225c89da86
Assouplissant Câlin marine 1 L|Suavizante Câlin marine 1 L|Câlin marine fabric softener 1 L;Nil;entretien;menage;1750;2000;1624372635310-01d078c05dd9
Lessive liquide couleurs 1,5 L|Detergente líquido color 1,5 L|Colour liquid detergent 1.5 L;Ventage Family;entretien;menage;3500;;1624372635277-283042097f31
Détachant textile 1 L|Quitamanchas 1 L|Stain remover 1 L;Ventage Family;entretien;menage;2200;;1624372635282-b324bcdd4907
Lessive écologique 1 L|Detergente ecológico 1 L|Eco laundry detergent 1 L;Ventage Family;entretien;menage;2800;;1610557892470-55d9e80c0bce
Nettoyant multi-surfaces spray 750 ml|Limpiador multiusos spray 750 ml|Multi-surface spray 750 ml;Ventage Family;entretien;menage;1800;;1563453392212-326f5e854473
Bactéricide formule citron 1 L|Bactericida fórmula limón 1 L|Lemon antibacterial cleaner 1 L;Super Clean;entretien;menage;900;1050;1628177142898-93e36e4e3a50
Kit ménage complet|Kit de limpieza completo|Complete cleaning kit;Ventage Family;entretien;menage;15000;18000;1759846866217-e627e4478f82
Seau & serpillière|Cubo y fregona|Mop & bucket;Ventage Family;entretien;menage;8100;9500;1779518082869-de2e1191c271
Seaux & balais · lot professionnel|Cubos y escobas · lote profesional|Buckets & brooms · pro set;Ventage Family;entretien;menage;12000;;1787205598829-e945bf8594ce
Liquide vaisselle & éponges · kit|Lavavajillas y estropajos · kit|Washing-up liquid & sponges · kit;Ventage Family;entretien;menage;2500;;1773526535649-e89045ea57c0
Gants de ménage · 3 paires|Guantes de limpieza · 3 pares|Cleaning gloves · 3 pairs;Ventage Family;entretien;menage;1500;;1627905646269-7f034dcc5738
Dentifrice protection caries 100 ml|Pasta dental anticaries 100 ml|Cavity protection toothpaste 100 ml;Colgate;entretien;hygiene;1200;;1610216690558-4aee861f4ab3
Brosses à dents souples · lot de 4|Cepillos de dientes suaves · pack de 4|Soft toothbrushes · 4-pack;Ventage Family;entretien;hygiene;2000;;1550985543-f1ea83691cd8
Brosse à dents & dentifrice · kit voyage|Cepillo y pasta de dientes · kit de viaje|Toothbrush & toothpaste · travel kit;Ventage Family;entretien;hygiene;1500;;1763048819607-ea55217cff34
Lait corporel hydratant 400 ml|Loción corporal hidratante 400 ml|Moisturising body lotion 400 ml;Ventage Family;entretien;hygiene;3500;;1643123158326-a17b8a06c45f
Crème mains nourrissante 75 ml|Crema de manos nutritiva 75 ml|Nourishing hand cream 75 ml;Ventage Family;entretien;hygiene;1800;;1643123158523-2950acbdfd68
Shampoing & après-shampoing · duo|Champú y acondicionador · dúo|Shampoo & conditioner · duo;Ventage Family;entretien;hygiene;5500;;1722872065547-515a2e6ec7bb
Soin cheveux · tube 200 ml|Tratamiento capilar · tubo 200 ml|Hair treatment · 200 ml tube;Ventage Family;entretien;hygiene;2500;;1643123158319-034f6a10aff9
Coffret soins du corps|Estuche de cuidado corporal|Body care gift set;Ventage Family;entretien;hygiene;9500;11500;1643123158300-1b08f8657fba
Gel douche · lot de 3|Gel de ducha · pack de 3|Shower gel · 3-pack;Ventage Family;entretien;hygiene;4500;;1631390179406-0bfe17e9f89d
Papier toilette · 9 rouleaux|Papel higiénico · 9 rollos|Toilet paper · 9 rolls;Style;entretien;papier;2050;;1583496597549-0fd8b25e34e2
Papier toilette · 32 rouleaux|Papel higiénico · 32 rollos|Toilet paper · 32 rolls;Ventage Family;entretien;papier;8500;9900;1631524254770-03abe3f42a0d
Papier toilette double épaisseur · 4 rouleaux|Papel higiénico doble capa · 4 rollos|2-ply toilet paper · 4 rolls;Ventage Family;entretien;papier;1000;;1584556812945-a6830379555b
Essuie-tout · 3 rouleaux|Papel de cocina · 3 rollos|Kitchen roll · 3 rolls;Style;entretien;papier;3500;4700;1598046937985-11c320dfd379
Essuie-tout maxi · 2 rouleaux|Papel de cocina maxi · 2 rollos|Maxi kitchen roll · 2 rolls;Ventage Family;entretien;papier;2500;;1584109807991-ebfcd80112a8
Biberon anti-colique 250 ml|Biberón anticólicos 250 ml|Anti-colic baby bottle 250 ml;Ventage Family;bebe-animaux;bebe;4500;;1623707430616-d9f956bcac2b
Lait de toilette bébé 500 ml|Leche limpiadora bebé 500 ml|Baby cleansing milk 500 ml;Ventage Family;bebe-animaux;bebe;3800;;1716372409137-7ad0100d57ab
Pâte à l'eau 75 ml|Pasta al agua 75 ml|Zinc nappy paste 75 ml;Biolane;bebe-animaux;bebe;4500;6400;1716372409156-b5d999f0b599
Kit naissance couches & lotion|Kit nacimiento pañales y loción|Newborn kit · nappies & lotion;Ventage Family;bebe-animaux;bebe;15000;;1716972065448-e08a46809530
Couches Baby Dry taille 5 · 48|Pañales Baby Dry talla 5 · 48|Baby Dry nappies size 5 · 48;Pampers;bebe-animaux;bebe;12400;17600;1584839404042-8bc21d240e91
Croquettes chien adulte 4 kg|Pienso perro adulto 4 kg|Adult dog food 4 kg;Ventage Family;bebe-animaux;animaux;9500;;1714068691210-073dc52c6c1d
Croquettes chien · sac 10 kg|Pienso para perros · saco 10 kg|Dog food · 10 kg sack;Ventage Family;bebe-animaux;animaux;19500;22000;1632236568054-12f36ecee2f6
Gamelle & croquettes chiot 2 kg|Comedero y pienso cachorro 2 kg|Puppy bowl & food 2 kg;Ventage Family;bebe-animaux;animaux;6500;;1565674244283-993fb27a215f
Croquettes chat stérilisé 2 kg|Pienso gato esterilizado 2 kg|Sterilised cat food 2 kg;Ventage Family;bebe-animaux;animaux;7500;;1616668983570-a971956d8928
"""

ICON = {"fruits-legumes": "basket", "boucherie": "fish", "cremerie": "cup", "boulangerie": "basket", "surgeles": "basket", "base": "basket",
        "conserves": "can", "huiles-epices": "bottle", "petit-dej": "cup", "biscuits": "basket", "eaux-jus": "bottle", "sodas": "bottle",
        "cafe-the": "cup", "alcools": "bottle", "menage": "spray", "hygiene": "soap", "papier": "soap", "bebe": "baby", "animaux": "basket"}

def rows():
    out = []
    for line in ROWS.strip().splitlines():
        name, brand, cat, sub, price, old, photo = line.split(";")
        out.append((name, brand, cat, sub, int(price), int(old) if old else None, "us:photo-" + photo, ICON[sub]))
    return out
