import math
import random
import sys
from dataclasses import InitVar, dataclass, field

import pygame

# ----------------------------------------------------
# Ce fichier crée un petit jeu de feu d'artifice en Python.
# Pour un débutant, voici l'idée générale :
# - on crée des objets "feux d'artifice" qui montent puis explosent
# - chaque explosion est faite de particules colorées
# - pygame dessine tout à l'écran et met à jour les positions
# ----------------------------------------------------

# Taille de la fenêtre du jeu
WIDTH, HEIGHT = 1000, 700

# Couleur de fond (bleu très foncé)
BACKGROUND = (8, 12, 24)


# ----------------------------------------------------
# Cette fonction choisit une couleur aléatoire pour une explosion.
# pygame.Color(0) crée une couleur vide, puis on modifie sa teinte.
# ----------------------------------------------------
def make_color():
    # hue = teinte de la couleur entre 0 et 1
    hue = random.random()
    color = pygame.Color(0)

    # hsva = (teinte, saturation, luminosité, alpha)
    # Ici on garde une saturation et luminosité élevées pour avoir
    # des couleurs vives.
    color.hsva = (hue * 360, 85, 100, 100)

    # On retourne les composantes rouge, vert, bleu
    return color.r, color.g, color.b


# ----------------------------------------------------
# Une particule est un petit point lumineux qui devient de plus en plus
# faible au fil du temps avant de disparaître.
# ----------------------------------------------------
@dataclass
class Particle:
    x: float
    y: float
    velocity: InitVar[tuple]
    color: tuple
    radius: int = 2

    # Durée de vie de la particule (entre 0.8 et 1.5 seconde)
    life: float = field(default_factory=lambda: random.uniform(0.8, 1.5), init=False)
    max_life: float = field(init=False)

    # Gravité, pour faire descendre les particules après l'explosion
    gravity: int = field(default=105, init=False)

    # Parfois, une particule scintille (clignote) avant de disparaître
    twinkle: bool = field(default_factory=lambda: random.random() < 0.18, init=False)

    # Vitesse horizontale et verticale
    vx: float = field(init=False)
    vy: float = field(init=False)

    def __post_init__(self, velocity):
        # On reçoit la vitesse sous forme de tuple (vx, vy)
        self.vx, self.vy = velocity
        self.max_life = self.life

    def update(self, dt):
        # dt = temps écoulé depuis le dernier tour de boucle
        self.life -= dt
        self.vy += self.gravity * dt
        self.x += self.vx * dt
        self.y += self.vy * dt

    def draw(self, surface):
        # Si la particule n'a plus de vie, on ne la dessine pas
        if self.life <= 0:
            return

        # fade = 0 à 1 ; plus la particule est vieille, plus elle est faible
        fade = max(0, self.life / self.max_life)

        # Certains petits points disparaissent au hasard pour un effet scintillant
        if self.twinkle and random.random() < 0.35:
            return

        # On diminue progressivement la couleur selon la vie restante
        color = tuple(int(channel * fade) for channel in self.color)

        # On dessine un cercle à la position actuelle
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), max(1, int(self.radius * fade)))


# ----------------------------------------------------
# Un feu d'artifice est un objet qui monte dans le ciel puis explose.
# ----------------------------------------------------
@dataclass
class Firework:
    # x = position horizontale du feu, si on ne donne pas de valeur elle est choisie au hasard
    x: int | None = None

    # y = hauteur actuelle du feu d'artifice
    y: int = field(default=HEIGHT + 5, init=False)

    # target_y = hauteur où il va exploser
    target_y: int = field(default_factory=lambda: random.randint(130, 330), init=False)

    # Vitesse de montée du feu avant l'explosion
    speed: float = field(default_factory=lambda: random.uniform(350, 500), init=False)

    # Couleur du feu et des particules
    color: tuple = field(default_factory=make_color, init=False)

    # Liste des particules créées après l'explosion
    particles: list = field(default_factory=list, init=False)

    # exploded = True quand la fusée a déjà explosé
    exploded: bool = field(default=False, init=False)

    def __post_init__(self):
        # Si x n'a pas été donné, on le choisit au hasard
        if self.x is None:
            self.x = random.randint(100, WIDTH - 100)

    def update(self, dt):
        # Si le feu n'a pas encore explosé, il monte
        if not self.exploded:
            self.y -= self.speed * dt

            # Dès qu'il atteint sa hauteur cible, on déclenche l'explosion
            if self.y <= self.target_y:
                self.explode()
        else:
            # Après l'explosion, on met à jour toutes les particules
            for particle in self.particles:
                particle.update(dt)

            # On enlève les particules qui sont mortes
            self.particles = [particle for particle in self.particles if particle.life > 0]

    def explode(self):
        # Le feu est désormais explosé
        self.exploded = True

        # Nombre de particules de base dans l'explosion
        count = random.randint(65, 105)
        for _ in range(count):
            angle = random.uniform(0, math.tau)
            speed = random.uniform(45, 230)
            velocity = (math.cos(angle) * speed, math.sin(angle) * speed)
            self.particles.append(Particle(self.x, self.y, velocity, self.color, random.choice((1, 2, 3))))

        # Quelques particules très lumineuses pour donner un effet de brillance
        for _ in range(18):
            angle = random.uniform(0, math.tau)
            speed = random.uniform(90, 280)
            velocity = (math.cos(angle) * speed, math.sin(angle) * speed)
            spark_color = random.choice(((255, 245, 190), (255, 255, 255), self.color))
            self.particles.append(Particle(self.x, self.y, velocity, spark_color, 2))

    def draw(self, surface):
        # Avant l'explosion, on dessine une petite fusée lumineuse
        if not self.exploded:
            pygame.draw.circle(surface, (255, 245, 190), (int(self.x), int(self.y)), 3)
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y + 8)), 2)
        else:
            # Après l'explosion, on dessine toutes les particules
            for particle in self.particles:
                particle.draw(surface)


# ----------------------------------------------------
# Fonction principale du jeu.
# C'est là que tout démarre.
# ----------------------------------------------------
def main():
    # Initialisation de pygame
    pygame.init()

    # Création de la fenêtre du jeu
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Feu d'artifice")

    # Horloge qui limite le nombre d'images par seconde
    clock = pygame.time.Clock()

    # Police d'écriture pour le texte en bas de l'écran
    font = pygame.font.Font(None, 24)

    # Liste qui contient tous les feux d'artifice de l'écran
    fireworks = []

    # auto_launch = True si les feux sont lancés automatiquement
    auto_launch = True
    launch_timer = 0
    running = True

    # Boucle principale du jeu
    while running:
        # dt = temps écoulé entre deux frames, en secondes
        dt = min(clock.tick(60) / 1000, 0.04)

        # Gestion des événements clavier/souris/fermeture de fenêtre
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    auto_launch = not auto_launch
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                fireworks.append(Firework(event.pos[0]))

        # Gestion du lancement automatique de feux d'artifice
        launch_timer -= dt
        if auto_launch and launch_timer <= 0:
            fireworks.append(Firework())
            if random.random() < 0.28:
                fireworks.append(Firework())
            launch_timer = random.uniform(0.35, 0.85)

        # On remplit l'écran avec la couleur de fond
        screen.fill(BACKGROUND)

        # Ajout de petites étoiles sur le fond noir
        for _ in range(45):
            x = random.randrange(WIDTH)
            y = random.randrange(HEIGHT)
            pygame.draw.circle(screen, (35, 43, 61), (x, y), 1)

        # Mise à jour et dessin de chaque feu d'artifice
        for firework in fireworks:
            firework.update(dt)
            firework.draw(screen)

        # On enlève les feux qui ont fini et qui n'ont plus de particules
        fireworks = [firework for firework in fireworks if not firework.exploded or firework.particles]

        # Texte d'aide affiché en bas
        hint = "Clic : lancer  |  Espace : pause/reprise  |  Echap : quitter"
        label = font.render(hint, True, (160, 172, 195))
        screen.blit(label, (18, HEIGHT - 32))

        # On met à jour l'affichage à l'écran
        pygame.display.flip()

    # Quand on sort de la boucle, on ferme pygame proprement
    pygame.quit()
    sys.exit()


# Si ce fichier est exécuté directement, la fonction main démarre
if __name__ == "__main__":
    main()
