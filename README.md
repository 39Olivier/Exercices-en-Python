# Exercices en Python

Bienvenue dans ce petit recueil d'exercices Python. Chaque script propose une
activité visuelle pour pratiquer les bases de la programmation tout en créant
des dessins ou des animations.

## Objectifs

En explorant les exercices, tu pourras t'entraîner à :

- utiliser des variables, des boucles et des fonctions ;
- générer des couleurs et des nombres aléatoires ;
- dessiner avec `turtle` et créer des animations ;
- représenter des objets avec des classes ;
- mettre à jour des positions et simuler le mouvement ;
- lire, modifier et améliorer un programme existant.

## Exercices

### 1. Dessiner une spirale colorée

Fichier : [`escargot_disco.py`](./escargot_disco.py)

Le script utilise `turtle` pour dessiner une spirale aux couleurs changeantes.
Essaie de modifier la longueur des segments, l'angle de rotation ou le nombre
d'étapes pour obtenir une nouvelle figure.

```bash
python escargot_disco.py
```

### 2. Animer un escargot disco et un feu d'artifice

Fichier : [`escargot_disco_spectacle.py`](./escargot_disco_spectacle.py)

Cet exercice reprend la spirale et ajoute un ciel étoilé ainsi qu'un final de
gerbes colorées. Les particules se déplacent, ralentissent visuellement et
finissent par disparaître.

```bash
python escargot_disco_spectacle.py
```

### 3. Programmer un feu d'artifice

Fichier : [`feu_artifice.py`](./feu_artifice.py)

Avec Pygame, construis une scène animée où des fusées montent et éclatent en
particules. Le code permet notamment d'étudier les classes, la gravité, le
hasard et la mise à jour d'une animation.

Installe Pygame si nécessaire :

```bash
python -m pip install pygame
```

Puis lance l'exercice :

```bash
python feu_artifice.py
```

## Pour aller plus loin

Choisis un script et apporte-lui une amélioration :

- ajoute une nouvelle couleur ou une nouvelle forme ;
- change la vitesse ou la taille de l'animation ;
- ajoute des étoiles ou des particules ;
- crée une fonction pour éviter de répéter du code ;
- teste plusieurs valeurs et observe leur effet.

## Prérequis

- Python 3 installé ;
- Pygame uniquement pour `feu_artifice.py`.

Les exercices `turtle` utilisent une bibliothèque incluse avec Python.
