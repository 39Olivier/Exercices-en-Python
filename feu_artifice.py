import math
import random
import sys
from dataclasses import InitVar, dataclass, field

import pygame


WIDTH, HEIGHT = 1000, 700
BACKGROUND = (8, 12, 24)


def make_color():
    hue = random.random()
    color = pygame.Color(0)
    color.hsva = (hue * 360, 85, 100, 100)
    return color.r, color.g, color.b


@dataclass
class Particle:
    x: float
    y: float
    velocity: InitVar[tuple]
    color: tuple
    radius: int = 2
    life: float = field(default_factory=lambda: random.uniform(0.8, 1.5), init=False)
    max_life: float = field(init=False)
    gravity: int = field(default=105, init=False)
    twinkle: bool = field(default_factory=lambda: random.random() < 0.18, init=False)
    vx: float = field(init=False)
    vy: float = field(init=False)

    def __post_init__(self, velocity):
        self.vx, self.vy = velocity
        self.max_life = self.life

    def update(self, dt):
        self.life -= dt
        self.vy += self.gravity * dt
        self.x += self.vx * dt
        self.y += self.vy * dt

    def draw(self, surface):
        if self.life <= 0:
            return
        fade = max(0, self.life / self.max_life)
        if self.twinkle and random.random() < 0.35:
            return
        color = tuple(int(channel * fade) for channel in self.color)
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), max(1, int(self.radius * fade)))


@dataclass
class Firework:
    x: int | None = None
    y: int = field(default=HEIGHT + 5, init=False)
    target_y: int = field(default_factory=lambda: random.randint(130, 330), init=False)
    speed: float = field(default_factory=lambda: random.uniform(350, 500), init=False)
    color: tuple = field(default_factory=make_color, init=False)
    particles: list = field(default_factory=list, init=False)
    exploded: bool = field(default=False, init=False)

    def __post_init__(self):
        if self.x is None:
            self.x = random.randint(100, WIDTH - 100)

    def update(self, dt):
        if not self.exploded:
            self.y -= self.speed * dt
            if self.y <= self.target_y:
                self.explode()
        else:
            for particle in self.particles:
                particle.update(dt)
            self.particles = [particle for particle in self.particles if particle.life > 0]

    def explode(self):
        self.exploded = True
        count = random.randint(65, 105)
        for _ in range(count):
            angle = random.uniform(0, math.tau)
            speed = random.uniform(45, 230)
            velocity = (math.cos(angle) * speed, math.sin(angle) * speed)
            self.particles.append(Particle(self.x, self.y, velocity, self.color, random.choice((1, 2, 3))))

        # A few bright sparks make the burst feel layered.
        for _ in range(18):
            angle = random.uniform(0, math.tau)
            speed = random.uniform(90, 280)
            velocity = (math.cos(angle) * speed, math.sin(angle) * speed)
            spark_color = random.choice(((255, 245, 190), (255, 255, 255), self.color))
            self.particles.append(Particle(self.x, self.y, velocity, spark_color, 2))

    def draw(self, surface):
        if not self.exploded:
            pygame.draw.circle(surface, (255, 245, 190), (int(self.x), int(self.y)), 3)
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y + 8)), 2)
        else:
            for particle in self.particles:
                particle.draw(surface)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Feu d'artifice")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 24)
    fireworks = []
    auto_launch = True
    launch_timer = 0
    running = True

    while running:
        dt = min(clock.tick(60) / 1000, 0.04)
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

        launch_timer -= dt
        if auto_launch and launch_timer <= 0:
            fireworks.append(Firework())
            if random.random() < 0.28:
                fireworks.append(Firework())
            launch_timer = random.uniform(0.35, 0.85)

        screen.fill(BACKGROUND)
        for _ in range(45):
            x = random.randrange(WIDTH)
            y = random.randrange(HEIGHT)
            pygame.draw.circle(screen, (35, 43, 61), (x, y), 1)

        for firework in fireworks:
            firework.update(dt)
            firework.draw(screen)
        fireworks = [firework for firework in fireworks if not firework.exploded or firework.particles]

        hint = "Clic : lancer  |  Espace : pause/reprise  |  Echap : quitter"
        label = font.render(hint, True, (160, 172, 195))
        screen.blit(label, (18, HEIGHT - 32))
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
