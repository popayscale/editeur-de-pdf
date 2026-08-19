# Petit éditeur de PDF

Petit outil permettant de manipuler des documents PDF directement depuis un navigateur.

L'objectif est de proposer un outil simple pour effectuer différentes opérations sur les PDF :

* réorganisation des pages ;
* suppression de pages ;
* duplication de pages ;
* rotation ;
* copie de pages entre plusieurs documents ;
* ajout et positionnement d'images.

Le projet existe actuellement sous **deux formes complémentaires** :

* une **version HTML** utilisant PDF.js depuis un CDN ;
* une **version locale Windows**, distribuée sous forme de ZIP et fonctionnant hors ligne.

---

# 🚀 Versions disponibles

## Version HTML

La version HTML principale est :

```text
PDF_Image_Editor_MultiPDF.html
```

Elle fonctionne directement dans un navigateur moderne.

Aucune installation de Python ou de bibliothèque Python n'est nécessaire pour utiliser cette version.

Elle utilise actuellement **PDF.js 6.2.108** pour l'affichage et la manipulation des documents PDF.

### Utilisation

Il suffit d'ouvrir :

```text
PDF_Image_Editor_MultiPDF.html
```

dans un navigateur compatible.

Cette version nécessite cependant un accès à Internet au démarrage afin de télécharger les bibliothèques PDF.js depuis le CDN Cloudflare.

---

# 🖥️ Version locale Windows

Une version locale est également disponible dans le fichier :

```text
editeur-pdf-windows.zip
```

Cette version est destinée aux utilisateurs souhaitant disposer d'une version **hors ligne**, sans dépendance à un CDN externe.

Elle contient notamment les bibliothèques PDF.js directement dans le dossier du programme.

```text
editeur-pdf-windows/
├── lancer-editeur.bat
├── server.py
├── PDF_Image_Editor_MultiPDF.html
├── pdf.min.mjs
└── pdf.worker.min.mjs
```

Le traitement reste sur la machine de l'utilisateur.

La version locale utilise un petit serveur Python fonctionnant uniquement sur :

```text
127.0.0.1
```

Ce serveur permet au navigateur de charger correctement les modules PDF.js locaux.

Il ne s'agit pas d'un serveur distant et il n'est pas destiné à être accessible depuis le réseau.

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

Il est possible d'importer plusieurs images sur une même page, de les positionner, puis de les fixer avant de poursuivre le travail sur une autre page.

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
8. Positionner et fixer les images.
9. Finaliser le document.

---

# 🔐 Confidentialité

L'application est conçue pour manipuler les documents directement sur le poste de l'utilisateur.

Aucun service en ligne n'est utilisé pour recevoir ou stocker les PDF traités.

La différence entre les deux versions concerne principalement le chargement de PDF.js :

| Version        | PDF.js                             | Internet nécessaire      |
| -------------- | ---------------------------------- | ------------------------ |
| HTML           | CDN Cloudflare                     | Oui, pour charger PDF.js |
| Locale Windows | Bibliothèques incluses dans le ZIP | Non                      |

---

# 🌐 PDF.js

La version actuelle utilise :

```text
PDF.js 6.2.108
```

La version HTML charge les bibliothèques depuis `cdnjs.cloudflare.com` :

```javascript
import * as pdfjsLib from "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/6.2.108/pdf.min.mjs";

pdfjsLib.GlobalWorkerOptions.workerSrc =
    "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/6.2.108/pdf.worker.min.mjs";
```

La bibliothèque principale et le worker utilisent volontairement la même version :

```text
6.2.108
```

La version locale Windows utilise ces mêmes bibliothèques, mais les fichiers sont fournis directement dans le ZIP :

```text
pdf.min.mjs
pdf.worker.min.mjs
```

Elle ne dépend donc pas du CDN pour fonctionner.

---

# 🛡️ Mise à jour de sécurité de PDF.js

Le projet a été mis à jour à la suite de la découverte d'une vulnérabilité de sécurité affectant certaines versions de PDF.js.

La version utilisée précédemment a été remplacée par :

```text
PDF.js 6.2.108
```

Cette version correspond à la version corrigée retenue pour le projet.

La mise à jour concerne à la fois la version HTML et la version locale Windows.

Le projet continuera à suivre les mises à jour de sécurité de PDF.js afin de maintenir une version à jour de la bibliothèque.

> **Important :** l'utilisation d'une version corrigée de PDF.js ne constitue pas une garantie de sécurité absolue. Comme pour toute dépendance logicielle, les futures vulnérabilités devront être surveillées et les versions mises à jour lorsque cela sera nécessaire.

---

# ☁️ Dépendance au CDN — version HTML

La version HTML utilise actuellement :

```text
https://cdnjs.cloudflare.com
```

pour charger :

```text
pdf.min.mjs
pdf.worker.min.mjs
```

Elle nécessite donc un accès à Internet au moment du chargement de l'application.

Cette dépendance n'existe pas dans la version locale Windows, puisque les fichiers PDF.js sont directement inclus dans le ZIP.

---

# 📴 Version locale hors ligne

La version :

```text
editeur-pdf-windows.zip
```

est destinée aux utilisateurs qui souhaitent travailler sans connexion Internet.

Elle contient :

```text
lancer-editeur.bat
server.py
PDF_Image_Editor_MultiPDF.html
pdf.min.mjs
pdf.worker.min.mjs
```

## Pré-requis

**Python doit être installé sur Windows.**

Aucune bibliothèque Python supplémentaire n'est nécessaire.

Il suffit d'avoir une installation fonctionnelle de Python permettant d'exécuter :

```bash
python --version
```

## Lancement

1. Décompresser `editeur-pdf-windows.zip`.
2. Vérifier que les fichiers sont présents dans le même dossier.
3. Double-cliquer sur :

```text
lancer-editeur.bat
```

4. Le navigateur s'ouvre automatiquement.
5. Utiliser normalement l'éditeur.

Le serveur utilisé par `server.py` reste limité à la machine locale.

Il n'est donc pas nécessaire de lancer manuellement un serveur ou d'effectuer une configuration particulière.

---

# 🐍 Pourquoi Python dans la version locale ?

Python n'est **pas nécessaire pour la version HTML classique**.

Il est utilisé uniquement dans la version locale Windows afin de lancer un petit serveur HTTP local.

Cette étape est nécessaire car les navigateurs appliquent des restrictions de sécurité lorsque certains modules JavaScript sont chargés directement depuis un fichier `file://`.

Le serveur Python permet donc au navigateur de charger les fichiers PDF.js locaux correctement.

Il ne s'agit pas d'un serveur Internet.

L'adresse utilisée est :

```text
127.0.0.1
```

qui correspond à la machine locale.

---

# 📱 Autres versions

Le dépôt peut également contenir différentes versions ou expérimentations du projet.

La version HTML principale reste :

```text
PDF_Image_Editor_MultiPDF.html
```

La version destinée à une utilisation hors ligne sous Windows est :

```text
editeur-pdf-windows.zip
```

---

# 🧭 État du projet

## Version HTML

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

## Version locale Windows

* [x] Fonctionnement hors ligne
* [x] PDF.js fourni localement
* [x] `pdf.min.mjs` inclus
* [x] `pdf.worker.min.mjs` inclus
* [x] Serveur local intégré
* [x] Lancement simplifié avec `lancer-editeur.bat`

## Évolutions

* [ ] Amélioration des fonctions d'édition PDF
* [ ] Amélioration de l'interface
* [ ] Nouvelles fonctions de manipulation des pages
* [ ] Évolution de la version locale Windows
* [ ] Documentation séparée et complète de la version locale

---

# 📌 En résumé

**Petit éditeur de PDF** est un outil en développement permettant de manipuler simplement des documents PDF depuis un navigateur.

Il existe actuellement en deux déclinaisons :

### 🌐 Version HTML

```text
PDF_Image_Editor_MultiPDF.html
```

* aucune installation Python ;
* utilisation directe dans un navigateur ;
* PDF.js 6.2.108 ;
* PDF.js téléchargé depuis cdnjs.cloudflare.com ;
* connexion Internet nécessaire pour charger la bibliothèque.

### 🖥️ Version locale Windows

```text
editeur-pdf-windows.zip
```

* fonctionnement hors ligne ;
* PDF.js fourni directement avec l'application ;
* aucune dépendance au CDN ;
* petit serveur Python local nécessaire au fonctionnement du navigateur ;
* aucune donnée destinée à être envoyée vers Internet.

La version locale constitue la déclinaison **hors ligne et autonome du projet**. Elle dispose de son propre README et pourra évoluer indépendamment de la version HTML.

Le projet utilise actuellement **PDF.js 6.2.108**, à la suite de la mise à jour de sécurité effectuée sur les versions précédentes.
