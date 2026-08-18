Petit éditeur de pdf  avec 2 onglet , le premier pour ajouter des images  via import

 importer toutes les images sur une page puis les placer et ensuite les fixer avant de travailler sur une seconde page

second onglet : réorganiser les pages de pdfs en ouvrant plusieurs documents , onréorganise les pages en glisser / déposer.
On peut également supprimer des pages puis enregistrer les "colones" en un nouveau pdf.


requis : pip install pymupdf pillow PyQt5 PyPDF2

Si vous avez des erreurs avec PyQt5, essayez :
pip install PyQt5 PyQt5-sip

pour les html la seconde version est la plus aboutie a prioriser , ne contient que l'import d'image pour le moment.....


L'outil charge au démarrage deux bibliothèques PDF.js depuis le serveur externe cdnjs.cloudflare.com.

 Une fois ces bibliothèques téléchargées, tous les traitements sont réalisés localement dans le navigateur de l'utilisateur.

 Le PDF est lu directement depuis le poste de travail et n'est pas envoyé vers Internet.

 Les images ajoutées au document sont également traitées localement.

 Aucun appel fetch, API REST, WebSocket ou mécanisme d'upload n'a été identifié dans le code.


 Le principal risque réside dans la dépendance à un CDN externe pour récupérer PDF.js.
 Cloudflare peut voir qu'un poste accède à sa bibliothèque, mais ne reçoit pas le contenu des PDF traités.
 Le fait que les scripts soient chargés sans blocage indique que votre environnement de sécurité les autorise actuellement.
 Le risque de fuite de données via ce code est donc très faible.
 Le risque le plus crédible serait une compromission future de la bibliothèque ou du CDN utilisé.
 Pour une entreprise classique, l'utilisation paraît acceptable avec un niveau de risque faible.
 Pour un environnement très sécurisé ou industriel, 
il serait préférable d'héberger les bibliothèques PDF.js sur un serveur interne plutôt que de les télécharger depuis Internet.


Conclusion

À ce jour, je ne vois aucun comportement d'exfiltration de données ni de communication réseau suspecte dans ce code. Le seul flux externe observé est le téléchargement de PDF.js depuis Cloudflare. Pour un usage bureautique standard en entreprise, le risque est faible (environ 2 à 3/10). Le point d'attention principal reste la dépendance à un fournisseur externe pour charger les bibliothèques JavaScript.


Les seuls téléchargements externes concernent les bibliothèques PDF.js hébergées sur le CDN Cloudflare (cdnjs.cloudflare.com). Le reste du traitement est effectué localement sur le poste de travail.

Concernant le fait que ces scripts ne soient pas bloqués par la sécurité de votre poste, c'est un indicateur plutôt positif :

Le domaine cdnjs.cloudflare.com est largement utilisé dans le monde professionnel.
Votre proxy, filtrage web ou EDR (Defender, CrowdStrike, SentinelOne, etc.) ne semble pas le considérer comme une source à bloquer.
Si le script était considéré comme dangereux ou non conforme à la politique de l'entreprise, le téléchargement aurait probablement été bloqué ou remonté dans les journaux de sécurité.

Cela ne signifie cependant pas un risque nul :

Confiance à un fournisseur externe (Cloudflare).
Une modification malveillante de la bibliothèque, bien que peu probable, aurait un impact potentiel sur les utilisateurs.
Certaines entreprises imposent que toutes les bibliothèques JavaScript soient hébergées en interne afin d'éliminer cette dépendance.

