# Tony's enhancements #

* Auteur : Tony Malykh
* Télécharger [version stable][1]
* Compatibilité NVDA : 2022.4 et 2023.1

Cette extension contient un certain nombre de petites améliorations
apportées au lecteur d'écran NVDA, chacune d'entre elles étant trop petite
pour mériter une extension séparée.

## Commandes de navigation améliorées dans les tableaux

* NVDA+Contrôle+chiffre - aller à la 1ère/2ème/3ème/... 10ème colonne du
  tableau.
* NVDA+Alt+chiffre - aller à la 1ère/2ème/3ème/... 10ème ligne du tableau.

## Commandes de navigation supprimées dans les tableaux

Les suivantes commandes de navigation dans les tableaux ont été supprimées
car elles ont été intégrées dans la dernière version du noyau de NVDA.

* Aller à la première/dernière colonne du tableau.
* Aller à la première/dernière ligne du tableau.
* Lire la colonne actuelle dans le tableau à partir de la cellule actuelle
  vers le bas.
* Lire la ligne actuelle dans le tableau à partir de la cellule actuelle.
* Lire la colonne actuelle dans le tableau à partir du haut.
* Lire la ligne actuelle dans le tableau à partir du début de la ligne.

Remarque : Pour en savoir plus sur les gestes par défaut de NVDA pour ces
fonctionnalités, veuillez vous référer au Guide de l'utilisateur de NVDA.

## Copier des tableaux dans le presse-papiers

Avec les raccourcis suivants, vous pouvez copier le tableau entier ou la
ligne actuelle ou la colonne actuelle de manière formatée, afin que vous
puissiez le coller comme un tableau dans un éditeurs de texte riches, tels
que Microsoft Word ou WordPad.

* NVDA+Alt+T - Affiche le menu contextuel avec des options pour copier le
  tableau ou une partie de celui-ci.

Il existe également des scripts distincts pour la copie des tableaux, des
lignes, des colonnes et des cellules, mais ils n'ont pas de raccourcis
clavier assignés par défaut, les raccourcis clavier personnalisés pour eux
peuvent être assignés dans la boîte de dialogue Gestes de commandes de NVDA.

## Commandes de navigation améliorées dans les mots

À partir de la version 1.8, cette fonctionnalité a été déplacée vers
[l'extension WordNav](https://github.com/mltony/nvda-word-nav/).

## Commutation automatique de la langue

Permet de changer automatiquement la langue de votre synthétiseur par le jeu
de caractères. lexpression régulière pour chaque langue peut être configurée
dans la fenêtre Préférences pour cette extension. Veuillez vous assurer que
votre synthétiseur prend en charge toutes les langues qui vous
intéressent. La commutation entre deux langues latin ou deux langues dont
les jeux de caractères sont similaires n'est pas pris en charge pour le
moment.

## Commandes de recherche rapide

Vous pouvez avoir jusqu'à trois emplacements pour des expressions régulières
configurables que vous recherchez fréquemment pour les rédacteurs. Par
défaut, ils sont affectés aux touches `PrintScreen`, `ScrollLock` et `Pause`
Vous pouvez effectuer une recherche en avant, ou une recherche en arrière en
appuyant sur `Shift` combinée avec ces touches.

## Supprimer l'annonce "non sélectionné" indésirable de NVDA

Supposons que vous ayez un texte sélectionné dans les éditeurs de
texte. Ensuite, vous appuyez sur une touche, comme Début, ou Flèche bas,
qui est censée vous emmener dans une autre partie du document. NVDA
annoncerait «non sélectionné» puis verbaliserait l'ancienne sélection, qui
peut parfois être gênante. Cette fonction empêche NVDA de verbaliser le
texte autrefois sélectionné dans des situations comme celle-ci.

## Frappes dynamiques

Vous pouvez attribuer à certaines frappes des touches dynamiques. Après
avoir exécuté une telle frappe, NVDA vérifiera s'il y a eu une mise à jour
dans la fenêtre ayant actuellement le focus et si la ligne courante est mise
à jour, NVDA la lira automatiquement. Par exemple, certaines frappes dans
les éditeurs de texte doivent être marquées comme dynamiques, telles que
Aller au signet, sauter à une autre ligne ainsi que les frappes de débogage,
telles que pas à pas détaillé (step into)/pas à pas (step over).

Le format du tableau de frappes dynamiques est simple : chaque ligne
contient une règle au format suivant :
```
frappe appName
```
où `appName` est le nom de l'application où cette frappe est marquée comme
dynamique (ou `*` pour être marquée dynamique dans toutes les applications),
et `commande` est une frappe au format NVDA, par exemple,
`control+alt+shift+pagedown`.

Afin de comprendre appName pour votre application, faites ceci :

1. Basculez sur votre application.
2. Ouvrez la console NVDA Python en appuyant sur NVDA+Shift+Z.
3. Tapez `focus.appModule.appName` et appuyez sur Entrée.
4. Appuyez sur F6 pour accéder au volet de sortie et recherchez la valeur
   appName dans la dernière ligne.

## Affichage et masquage des fenêtres

Vous pouvez masquer la fenêtre actuelle et vous pouvez afficher toutes les
fenêtres actuellement masquées. Cela peut être utile si vous utilisez
plusieurs fenêtres dans la même application (disons Chrome) et que vous
souhaitez les réorganiser.

* NVDA+Shift+ tiret (-) : Masquer la fenêtre actuelle.
* NVDA+Shift+= : Afficher toutes les fenêtres actuellement fermées.

Veuillez noter que si vous quittez NVDA pendant qu'une fenêtre est masquée,
il n'y a actuellement aucun moyen de l'afficher après le redémarrage de
NVDA.

## Améliorations de la console

Auparavant, cette extension comprenait un certain nombre de fonctionnalités
liées à la console. À partir de la version 1.8, toutes les fonctionnalités
liées à la console ont été déplacées vers [l'extension Console
Toolkit](https://github.com/mltony/nvda-console-toolkit/). Spécifiquement :

* Sortie console en temps réel
* Mises à jour  du bip sur la console
* Appliquer Contrôle+V dans les consoles

## Bip lorsque NVDA est occupé

Cochez cette option pour que NVDA fournisse un retour audio lorsque NVDA est
occupé. Le fait que NVDA soit occupé n'indique pas nécessairement un
problème avec NVDA, mais c'est plutôt un signal à l'utilisateur que les
commandes NVDA ne seront pas traitées immédiatement.

## Réglage du volume

* NVDA+Contrôle+PagePrec/PageSuiv - ajuste le volume NVDA.
* NVDA+Alt+PagePrec/PageSuiv - ajuste le volume de toutes les applications à
  l'exception de NVDA.

## Séparation de l'audio

En mode Séparation de l'audio, NVDA orientera toute la sortie audio vers le
canal droit, tandis que les applications joueront l'audio dans le canal de
gauche. Les canaux peuvent être basculés dans les paramètres.

* NVDA+Alt+S Bascule le mode séparation de l'audio.

Veuillez noter que dans certaines situations, la sortie audio d'une
application peut être limitée à un canal même lorsque NVDA n'est pas en
cours d'exécution. Par exemple, cela pourrait se produire si NVDA s'est
bloqué pendant que la séparation de l'audio était activée, ou lorsque NVDA
est sorti proprement pendant que l'application en question n'était pas en
cours d'exécution. Dans ces situations, veuillez redémarrer NVDA et
désactiver la séparation de l'audio pendant que l'application en question
est en cours d'exécution.

## Fonctions améliorées de la souris

* Alt+pavNumDivisé : Le curseur  du pointeur de la souris  à l'objet actuel
  et cliquer avec lui
* Alt+pavNumMultiplié : Le curseur  du pointeur de la souris  à l'objet
  actuel et cliquer  avec le bouton droit de la souris.
* Alt+pavNumPlus / pavNumMoins : Le curseur  du pointeur de la souris  à
  l'objet actuel et le défilement haut / bas. Ceci est utile pour le
  défilement des pages Web infinite  et des pages Web qui chargent plus de
  contenu avec le défilement.
* Alt+pavNum effacement : Déplacez le curseur de la souris à l'écart du coin
  supérieur gauche de l'écran. Cela peut être utile pour empêcher le survol
  indésirable sur Windows dans certaines applications.


## Détection du mode insertion dans les éditeurs de texte

Si cette option est activée, NVDA bip lorsqu'il détecte le mode insertion
dans les éditeurs de texte.

## Blocage de la double frappe de la touche Insertion

Dans NVDA, le fait d'appuyer deux fois de suite sur la touche Insertion
bascule le mode d'insertion dans les applications. Cependant, cela arrive
parfois accidentellement et cela déclenche le mode insertion. Comme il
s'agit d'une frappe spéciale, elle ne peut pas être désactivée dans les
paramètres. Cette extension permet de bloquer ce raccourci clavier. Lorsque
la double insertion est bloquée, le mode d'insertion peut toujours être
basculé en appuyant sur NVDA+F2 puis sur Insertion.

Cette option est désactivée par défaut et doit être activée dans les
paramètres.

## Priorité du système du processus de NVDA

Cela permet d'augmenter la priorité du système du processus de NVDA, ce qui
pourrait améliorer la réactivité de NVDA, en particulier lorsque la charge
du processeur est élevée.

## Correction d'un bogue lorsque le focus est coincée dans la barre des tâches lorsque vous appuyez sur Windows+numéros

Il y a un bogue dans Windows 10, et peut-être dans d'autres versions. Lors
de la commutation entre les applications à l'aide du raccourci
Windows+numéro, le focus est parfois coincé dans la zone de la barre des
tâches au lieu de sauter vers la fenêtre existante. Depuis que l'essai de
signaler ce bogue à Microsoft est sans espoir, une solution de contournement
a été implémentée dans cette extension. L'extension détecte cette situation
et joue un bip court à une faible hauteur lorsque cette situation est
détectée, puis l'extension la corrige automatiquement.

[[!tag dev stable]]

[1]: https://www.nvaccess.org/addonStore/legacy?file=tonysEnhancements
