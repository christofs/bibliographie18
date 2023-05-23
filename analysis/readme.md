# Analyses of the 'Bibliographie: XVIIIe' dataset 

The analyses are based on the RDF version of the data (currently, v0.1.0, May 20, 2023) and have been performed by Christof Schöch. 

Note that all numbers can be expected to shift slighly as the process of cleaning the data proceeds. Collaborative authorship / editorship as well as the publication types will most likely be most affected by corrections. 


## Distribution of publications per year 

The dataset contains 64169 publication years, with 87 different publication years recorded (some of them are errors). Here, only data starting in 1986 is shown (the bibliography was launched in 1992). 

![](/analysis/figures/pubyear_counts.png)


## Distribution of publication types in the dataset

There are 64397 instances of publication type (each entry has one), with just 6 different types of publication types. This number results from the original bibliography's data model, but the labels used below are Zotero's labels. The exception to this rule is that the distinction between monographs and edited volumes is lost in Zotero, which considers both to be books.  

- journalArticle: 26615
- book (monographs and edited volumes): 23083
- bookSection: 13368
- thesis: 1296
- dataset: 34
- webpage: 1


## Most frequently occurring person names 

There are 94321 mentions of person names in the dataset, in total, for 31026 different person names. 

The person names occurring most frequently in the dataset, irrespective of context or function, are the following, with the number of occurrence of their names: 

- Porret, Michel: 439
- Berchtold, Jacques: 388
- Delon, Michel: 383
- Voltaire: 346
- Seth, Catriona: 306
- Herman, Jan: 280
- Pelckmans, Paul: 267
- Moureau, François: 255
- Sermain, Jean-Paul: 240
- Bourdin, Philippe: 235


## Most frequently occurring publisher names

There are 37781 mentions of publisher names in the dataset, in total, for 5705 different publisher names. 

The publisher names occurring most frequently in the dataset, irrespective of context or function, are the following, with the number of occurrence of their names: 

- Classiques Garnier: 2354
- Honoré Champion: 1349
- Presses universitaires de Rennes: 1306
- Peter Lang: 706
- L’Harmattan: 691
- Voltaire Foundation: 682
- Droz: 552
- Presses universitaires de France: 540
- Gallimard: 523
- Cambridge University Press: 459


## Prevalence of collaboration in the dataset 

There are 56860 publications in the bibliography that have an author role (for instance monographs, journal articles and book chapters). Shown here is the number of authors in each of these publications. Single authorship is the norm, dual authorship is not uncommon, anything beyond this is exceedingly rare. 

- 1 author: 53488 (94.1%)
- 2 authors: 3361 (5.9%)
- 3 authors: 9 (0.02 %)
- 4 authors: 2 (0.004%)

There are 17135 publications in the bibliography that have an editor role (for instance edited volumes, proceedings, special issues, textual editions, etc.). Shown here is the number of editors in each of these publications. Dual editorship is the most common case, but single editorship and triple editorship are also very common. Higher numbers of editors are rarer. 

- 1 editor: 5558 (32.4%)
- 2 editors: 7743 (45.2%)
- 3 editors: 2638 (15.4%)
- 4 editors: 904 (5.3%)
- 5 editors: 256 (1.5%)
- 6 editors: 35 (0.2%)
- 11 (!) editors: (0.01%)


## Co-editor networks 

As shown above, editorship is an area of particularly intense collaboration in the community of Dix-huitiémistes, based on the data in the bibliography. The following is an initial, experimental attempt to elucidate the data using network visualization. 

The following shows a network of the top 20 co-editors and all of their co-editors, resulting in 148 different co-editor pairs. Each node is one editor, and each time two people have co-edited a publication, a link between them is created. The more co-editorships a person accumulates, the larger the node. The more co-editorships two people share, the thicker the edge connecting them. For this visualization, the full data of collaborations for edited volumes and editions has been massively reduced. Different parameters may strongly affect the results. See the full coeditor data in the `data` folder for more details.  

![Network showing the top 20 co-editors and all of their co-editors, created using Gephi.](figures/coeditors_top2.svg)

This figure is available also as a [zoom-able image file](https://raw.githubusercontent.com/christofs/bibliographie18/main/analysis/figures/coeditors_top2.svg) and [with somewhat friendlier colors but no community detection](https://raw.githubusercontent.com/christofs/bibliographie18/main/analysis/figures/coeditors_top1.svg).  

We basically see three key co-editor networks (the different colors are based on an algorithmic community or cluster detection): 

- Porret, Rosset, Majeur, Farkas, Baczko et al. 
- Sermain, Herman, Pelckmans, Escola, Omacini, Peeters, Paschoud, Berchtold et al. 
- Leuwers, Bourdin, Biard, Simien, Serna, Antoine et al. 
- Smaller clusters with Didier and Neefs as well around Kolving and Mortier. 

Some initial observations: While Porret appears to be the most productive co-editor overall, this is achived with some frequent, but also with a large number of less frequent coeditors. Inversely, the most intense collaboration appears to be between Herman and Pelckmans, who seem to avoid one-off collaborations. Finally, Rosset also functions as a bridge linking Porret and Baczko on the one hand, and Herman and Pelckmans on the other hand, and their respective coeditor networks. No similar bridge exists towards the Leuwers et al. network. The smaller Didier cluster is also connected to Sermain.  

