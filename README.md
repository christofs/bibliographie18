[![DOI](https://zenodo.org/badge/643157716.svg)](https://zenodo.org/badge/latestdoi/643157716)

# bibliographie18: Données de la Bibliographie sur le XVIIIe siècle de Benoît Melançon

## Source des données

Benoît Melançon, voir http://mapageweb.umontreal.ca/melancon/donnees_biblios_1_550.html (page d'information) et https://doi.org/10.5683/SP3/PYYEEH (dépôt Dataverse). 

Benoît Melançon précise : "Quiconque souhaite s’approprier ces données peut le faire, sous deux conditions. 1. L’attribution de la collecte des données doit toujours être rappelée, par exemple sous la forme «Données colligées par Benoît Melançon». 2. Aucune exploitation commerciale de ces données n’est tolérée. Elles ne peuvent pas être vendues sous quelque forme que ce soit. Autrement dit, chez Creative Commons : Attribution-NonCommercial 4.0 International (CC BY-NC 4.0) — https://creativecommons.org/licenses/by-nc/4.0/." 

## Données transformées 

Transformation du format CSV en format BibTeX lisible par des outils comme Zotero en utilisant un script Python. Fichiers produits par Christof Schöch en mai 2023. 

Le résultat de la transformation peut être utilisé sur Zotero, voir : https://www.zotero.org/groups/5067408/bibliographie18. 

Quelques premières analyses des données sont disponibles ici : https://github.com/christofs/bibliographie18/tree/main/analysis

## Historique des versions

- v0.1.0 – May 21, 2023

## Nota bene 

* Pour les dates de parution, seul l'année a été retenue. 
* Le bon ordonnement des noms et prénoms des auteurs ou éditeurs est difficile, il peut donc y avoir des erreurs. 
* La source de données ne fait pas de distinction entre les URL et les DOI ; par conséquent, ils sont tous répertoriés dans le champ URL. Cependant, peu de DOI sont présents de toute manière. 
* L'information sur la langue d'une publication a été ajoutée automatiquement, avec le module lingua-py. Cette information peut être éronnée dans certains cas (et sera améliorée à la main). 
* Après transformation vers BibTex, l'outil BibTeX-tidy a été utilisée : https://flamingtempura.github.io/bibtex-tidy. 
* Les fichiers résultants de cette procédure sont disponibles dans le dossier `bibtex` et forment la base pour l'importation dans Zotero. 
* Plusieurs formats d'export de Zotero sont disponibles dans le dossier `formats`. 
* Des corrections futures des données seront uniquement faits sur Zotero, avec des mises à jours des formats d'export. 

## Statistiques 

Il y a 64403 références en tout, dont:  

- 26616 journal articles (21390 traditionnel, 5228 en ligne)
- 23084 books (17956 monographies ou éditions, et 5131 edited volumes)
- 13368 book chapters
- 5131 edited volumes
- 1296 theses
- 34 datasets / CD-roms

Notons que les corrections des données apporteront sans doute une diversification des types de publication (blog post, radio broadcast, website). 

