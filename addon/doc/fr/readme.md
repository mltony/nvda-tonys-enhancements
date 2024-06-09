# Tony's enhancements #

Cette extension contient un certain nombre de petites améliorations
apportées au lecteur d'écran NVDA, chacune d'entre elles étant trop petite
pour mériter une extension séparée.

Cette extension est compatible avec les versions NVDA 2022.4 et 2024.1.

## Téléchargements

Veuillez installer la dernière version depuis l'add-on store de NVDA.

## Commandes de navigation améliorées dans les tableaux
* NVDA+Contrôle+chiffre - aller à la 1ère/2ème/3ème/... 10ème colonne du
  tableau.
* NVDA+Alt+chiffre - aller à la 1ère/2ème/3ème/... 10ème ligne du tableau.

## Copier des tableaux dans le presse-papiers

Avec les raccourcis suivants, vous pouvez copier le tableau entier ou la
ligne actuelle ou la colonne actuelle de manière formatée, afin que vous
puissiez le coller comme un tableau dans un éditeurs de texte riches, tels
que Microsoft Word ou WordPad.

* NVDA+Alt+T - Affiche le menu contextuel avec des options pour copier le
  tableau ou une partie de celui-ci.

Il existe également des scripts distincts pour la copie des tableaux, des
lignes, des colonnes et des cellules, mais aucun raccourci clavier n'est
assigné par défaut, des raccourcis clavier personnalisés peuvent leur être
assignés dans le dialogue  Gestes de commandes de NVDA.

## Commutation automatique de la langue
Permet de changer automatiquement la langue de votre synthétiseur par le jeu
de caractères. lexpression régulière pour chaque langue peut être configurée
dans la fenêtre Préférences pour cette extension. Veuillez vous assurer que
votre synthétiseur prend en charge toutes les langues qui vous
intéressent. La commutation entre deux langues latin ou deux langues dont
les jeux de caractères sont similaires n'est pas pris en charge pour le
moment.

## Commandes de recherche rapide

À partir de la version v1.18, les commandes QuickSearch ont été déplacées
vers [l'extension IndentNav](https://github.com/mltony/nvda-indent-nav).

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

À partir de la version v1.18, afficher/masquer les commandes ont été
déplacées vers [l'extension Task
Switcher](https://github.com/mltony/nvda-task-switcher).

## Bip lorsque NVDA est occupé

Cochez cette option pour que NVDA fournisse un retour audio lorsque NVDA est
occupé. Le fait que NVDA soit occupé n'indique pas nécessairement un
problème avec NVDA, mais c'est plutôt un signal à l'utilisateur que les
commandes NVDA ne seront pas traitées immédiatement.

## Réglage du volume de l'application

Cette fonctionnalité a été fusionnée dans le noyau NVDA et est disponible
dans NVDA v2024.3 ou version ultérieure.

## Séparation de l'audio

Cette fonctionnalité a été fusionnée dans le noyau NVDA et est disponible
dans NVDA v2024.2 ou version ultérieure.

## Fonctions améliorées de la souris

* Alt+pavNumDivisé : Le curseur  du pointeur de la souris  à l'objet actuel
  et cliquer avec lui.
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

## Priorité du processus de NVDA dans le système

Cela permet d'augmenter la priorité du processus de NVDA dans le système, ce
qui pourrait améliorer la réactivité de NVDA, en particulier lorsque la
charge du processeur est élevée.

## Correction d'un bogue lorsque le focus est coincée dans la barre des tâches lorsque vous appuyez sur Windows+numéros

Cette fonctionnalité a été supprimée à partir de la version v1.18. Si vous
avez besoin d'une fonctionnalité de changement de tâche plus fiable,
envisagez d'utiliser [l'extension Task
Switcher](https://github.com/mltony/nvda-task-switcher).

[[!tag dev stable]]

[1]: https://www.nvaccess.org/addonStore/legacy?file=tonysEnhancements
