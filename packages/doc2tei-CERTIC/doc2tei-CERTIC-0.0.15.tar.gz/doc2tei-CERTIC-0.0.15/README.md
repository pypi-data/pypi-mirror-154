# XSL-TEI-Circe

Description du pipeline de traitement Circé pour la conversion de fichiers stylés (formats `.docx`, `.odt`) en XML-TEI (schéma Métopes-OpenEdition).



[toc]

## 1. Conversion en Flat XML

```bash
soffice  --invisible --convert-to xml:'OpenDocument Text Flat XML' --outdir file
```



## 2. Pipeline de traitement XSL

### Point d'étapes et modules communs Métopes/OpenEdition

- campagne de tests

- scripts de conversion

Les différents modules et les choix d'encodage (convergence/divergence) sont documentés dans ce dépôt : https://git.unicaen.fr/fnso/i-fair-ir/schema-tei.

> bibliographie de fin d'unité, `teiHeader/titleStmt`, mots-clés, entretien



### 2.1 [`cleanup`]

Date(s) : 27/01/2021, 09/02/2021

**Objectif** : produire une arborescence facile à parser

- Nettoyage du fichier (suppression des éléments non utiles)
- Ajout du niveau 
  - pour le titre du document
  - pour les styles particuliers qui doivent véhiculer un niveau de titre (*Titre-section-biblio*, *Titre-section-annexe*)
- Remplacement des raccourcis par les noms de styles appliqués
- Liste
    - typologie
    - conversion en Unicode des puces 
- Encadrés : insertion de milestone début/fin
- Sens de composition : propriétés
- Images : 
    - contrôle du format
    - liens relatifs

Référent : Edith Cannet



> - raccourcis de styles
> - suppression des éléments non utiles



### 2.2 [`normalise`]

Date(s) : 23/02/2021


Principe : module de normalisation [bas niveau et procédural] : lister ce qui n’est pas normé et créer des régularités d’annotation **neutres au niveau sémantique** (soit : identifier les traitements pas ou peu dépendant du système de stylage initial) 

—> normalisation du XML

1. enrichissements typos [CR]
   - italic, gras, exposant, indice, souligné, barré, double enrichissements
   - voir commentaire *infra*
2. figures : [EC]
   - ramène à une structure identique les données quelque soit la méthode de stylage (OE ou Métopes) ;
   - groupe les éléments par bloc figure ;
   - images/graphic : inline, images block, hiéroglyphes, équations mode image
3. marqueurs d’index [EC]
4. séquences maths : équations mode code [CR]

> intégré à 1.

5. identifiants d’éléments [EC]
   - ancres, références croisés
6. sens de composition [PyB] 
   - évaluer l'information depuis le traitement de texte
   - évaluer la langue

> pré-traitement générique dans les pass 1 et 2.

7. liste [EC]
8. notes [CR]



> **Typo** 
>
> - les enrichissements typographiques sont gérés par la pass de cleanup 
> - la micro-typo (gestion des espaces) pourra être intrégrée dans une commande XXE, au moment de l'établissement du texte en XML



> - gestion des variations de stylage
> - normalisation des noms de styles

### 2.3 [`enrich`]

Traitement générique pour les attributs de langue.

> - répartition des informations (`@xml:lang`)


### 2.4 [`control`]

- Contrôle de la hiérarchie des titres
- Contrôle des styles présents dans le fichier


### 2.5 [`floatingText`]

- Création de divisions de texte pour le traitement des encadrés


### 2.6 [`hierarchize`]

Date(s) : 09/02/2021 (première version alpha)

**Objectif** : construire une structure arborescente à partir de la hiérarchie des niveaux de titres

- Construction de la hiérarchie (`<div>`)

Référents : Pierre-Yves Buard, Orderic-Vital Pain

### 2.7 [`to TEI`]

Objectifs : définir les modules XSL pour l'ensemble du traitement et leurs modalités d'intégration

lister les modules et leurs types

préciser les modalités d'intégration


#### Module Body

Date(s) :

Objectifs :

Question : organisation ici en sous-modules (paragraphes, listes, citations, notes, entretien) ?

Exemple : 

- structure/div : https://git.unicaen.fr/fnso/i-fair-ir/schema-tei/-/blob/master/structure-div.md

- paragraphe : https://git.unicaen.fr/fnso/i-fair-ir/schema-tei/-/blob/master/paragraphe.md

- liste : https://git.unicaen.fr/fnso/i-fair-ir/schema-tei/-/blob/master/listes.md

- typo : https://git.unicaen.fr/fnso/i-fair-ir/schema-tei/-/blob/master/typo.md



#### Module typo

Date(s) :

Objectifs : absence de module typo pour l'instant, la pass de `cleanup` permettant le nettoyage et le tri des enrichissements.


#### Module Back

Date(s) : 24/03/2021

Objectifs : ajoute d'un `@` au div de la `<div>` afin de faciliter le déplacement ultérieur de ces éléments dans la `<back>` du fichier TEI

> permis par l'insertion d'un `@outline-level`dans la pass de `cleanup`

- Biblio : https://git.unicaen.fr/fnso/i-fair-ir/schema-tei/-/blob/master/bibliographie.md
- Annexe(s) : https://git.unicaen.fr/fnso/i-fair-ir/schema-tei/-/blob/master/annexe.md

#### Module Front

Date(s) : 30/03/2021

Objectifs :

#### Module Header

Date(s) :

Objectifs :

#### Module Maths

Date(s) :

Objectifs :


### \#2.8 Conversion de la TEI Métopes vers la TEI OpenEdition

## 3. Validation

`xmllint`

<hr/>

## Annexes 
### Deprecated : script

*Script correspondant au pipeline circe*

**Configuration**

```
cd pipeline
cp soffice.conf.dist soffice.conf
```

Modifier le chemin vers soffice en fonction de votre installation dans le fichier `soffice.conf`.

Pour lancer les transformations taper la commande :

`sh pipeline-circe.sh fichier.docx`

Exemple avec le fichier test *Socio_4_07_Mounier.docx*  : `sh pipeline-circe.sh Socio_4_07_Mounier.docx`

```tree
/pipeline/

├── pipeline-circe.sh 
├── saxon9.jar
├── fichier.docx
├── fichier_conversion
│   ├── fichier.xml
│   ├── fichier_01_clean.xml
│   └── fichier_02_hierarchize.xml
```

