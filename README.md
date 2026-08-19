# Petit éditeur de PDF

Petit outil permettant de manipuler des documents PDF directement depuis un navigateur.

L'objectif est de proposer un outil simple pour effectuer rapidement différentes opérations sur des PDF : réorganisation des pages, suppression, duplication, rotation, copie de pages entre documents et ajout d'images.

La version HTML actuelle est la version principale du projet.

---

# 🚀 Version actuelle

La version à privilégier est :

```text
PDF_Image_Editor_MultiPDF.html
```

Cette version fonctionne directement dans un navigateur moderne et utilise **PDF.js** pour l'affichage et la manipulation des documents PDF.

Le projet est toujours en développement et de nouvelles fonctionnalités pourront être ajoutées progressivement.

---

# 📄 Fonctionnalités

## Gestion de plusieurs PDF

L'outil permet d'ouvrir plusieurs documents PDF simultanément et de travailler sur leurs pages.

Il est notamment possible de :

* ouvrir plusieurs PDF ;
* naviguer entre les différents documents ;
* parcourir les pages ;
* déplacer les pages ;
* supprimer des pages ;
* dupliquer des pages ;
* faire pivoter les pages ;
* sélectionner plusieurs pages ;
* copier des pages d'un document vers un autre ;
* réorganiser les pages.

Cette organisation permet notamment de récupérer des pages provenant de plusieurs documents afin de constituer un nouveau document.

---

# 🖼️ Ajout d'images

L'outil permet également d'importer des images dans les pages d'un PDF.

Une image peut être :

* importée depuis le poste de travail ;
* déplacée sur la page ;
* redimensionnée ;
* positionnée à l'endroit souhaité ;
* puis fixée afin de l'intégrer au document.

Cela peut notamment être utilisé pour ajouter :

* une signature sous forme d'image ;
* un logo ;
* un tampon ;
* une annotation graphique ;
* ou tout autre élément visuel.

Le fonctionnement permet d'importer plusieurs images sur une même page, de les positionner correctement, puis de les fixer avant de poursuivre le travail sur une autre page.

---

# 🔄 Travail avec plusieurs documents

L'une des fonctions principales de l'outil est de pouvoir travailler avec plusieurs PDF simultanément.

Exemple :

1. Ouvrir un premier PDF.
2. Ouvrir un second PDF.
3. Sélectionner les pages souhaitées.
4. Copier les pages vers le document cible.
5. Réorganiser les pages.
6. Supprimer les pages inutiles.
7. Ajouter éventuellement des images.
8. Fixer les images sur les pages.
9. Finaliser le document.

---

# 🔐 Confidentialité

Les PDF ouverts avec l'outil sont manipulés dans le navigateur.

Le projet n'utilise pas de service en ligne destiné à recevoir ou stocker les documents de l'utilisateur.

La version actuelle nécessite cependant le téléchargement de PDF.js depuis un CDN externe.

---

# 🌐 PDF.js

La version actuelle utilise :

```text
PDF.js 6.2.108
```

Les bibliothèques sont actuellement chargées depuis `cdnjs.cloudflare.com` :

```javascript
import * as pdfjsLib from "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/6.2.108/pdf.min.mjs";

pdfjsLib.GlobalWorkerOptions.workerSrc =
    "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/6.2.108/pdf.worker.min.mjs";
```

La bibliothèque principale et le worker utilisent volontairement la même version :

```text
6.2.108
```

---

# 🛡️ Mise à jour de sécurité

Le projet a été mis à jour à la suite de la découverte d'une vulnérabilité de sécurité affectant certaines versions de PDF.js.

La version utilisée précédemment a donc été remplacée par :

```text
PDF.js 6.2.108
```

Cette version correspond à la version corrigée indiquée par Mozilla pour la vulnérabilité concernée.

Le projet continuera à suivre les mises à jour de sécurité de PDF.js afin de maintenir une version à jour de la bibliothèque.

> **Important :** l'utilisation d'une version corrigée de PDF.js ne constitue pas une garantie de sécurité absolue. Comme pour toute dépendance externe, les futures vulnérabilités devront être surveillées et les versions mises à jour lorsque cela sera nécessaire.

---

# ☁️ Dépendance au CDN

La version HTML actuelle utilise le CDN :

```text
https://cdnjs.cloudflare.com
```

pour charger :

```text
pdf.min.mjs
pdf.worker.min.mjs
```

Cela signifie que le navigateur doit pouvoir accéder à ce domaine lors du chargement de l'application.

Le CDN est utilisé uniquement pour fournir les bibliothèques nécessaires au fonctionnement de PDF.js.

---

# 🐍 Version Python

Le dépôt contient également une ancienne version basée sur Python, utilisant notamment :

* PyMuPDF ;
* Pillow ;
* PyQt5 ;
* PyPDF2.

Installation :

```bash
pip install pymupdf pillow PyQt5 PyPDF2
```

En cas de problème avec PyQt5 :

```bash
pip install PyQt5 PyQt5-sip
```

Cette version Python n'est actuellement pas la version principale du projet.

---

# 📱 Autres versions

Le dépôt contient également des fichiers correspondant à différentes expérimentations du projet.

La version principale à utiliser actuellement reste :

```text
PDF_Image_Editor_MultiPDF.html
```

---

# 🧭 État du projet

### Version HTML actuelle

* [x] Ouverture de plusieurs PDF
* [x] Navigation entre les documents
* [x] Navigation entre les pages
* [x] Réorganisation des pages
* [x] Suppression de pages
* [x] Duplication de pages
* [x] Rotation des pages
* [x] Sélection de pages
* [x] Copie de pages entre documents
* [x] Import d'images
* [x] Positionnement des images
* [x] Redimensionnement des images
* [x] Fixation des images
* [x] PDF.js 6.2.108

### Évolutions prévues

Version locale

La future version locale fera l'objet d'un **projet ou dossier dédié avec son propre README**, afin de conserver une documentation distincte de la version HTML actuelle.

---

# 📌 En résumé

**Petit éditeur de PDF** est un outil en développement permettant de manipuler simplement des documents PDF depuis un navigateur.

La version actuelle permet notamment :

* d'ouvrir plusieurs PDF ;
* de réorganiser leurs pages ;
* de supprimer, dupliquer ou faire pivoter des pages ;
* de copier des pages entre plusieurs documents ;
* d'ajouter et positionner des images ;
* de fixer les images dans les pages.

La version actuelle utilise **PDF.js 6.2.108**, mise en place à la suite de la vulnérabilité de sécurité découverte dans les versions précédentes.

La version HTML dépend actuellement du CDN `cdnjs.cloudflare.com` pour charger PDF.js.

Une **version locale/autonome** est prévue ultérieurement. Elle sera développée et documentée séparément afin de ne pas mélanger les deux approches dans ce dépôt.
