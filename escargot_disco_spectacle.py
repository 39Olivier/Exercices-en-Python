import colorsys
import math
import random
import turtle


WIDTH = 1000
HEIGHT = 800
FRAME_DELAY = 20

screen = turtle.Screen()
screen.setup(width=WIDTH, height=HEIGHT)
screen.bgcolor("black")
screen.title("L'escargot disco - final feu d'artifice")
turtle.colormode(1.0)
screen.tracer(0)

background = turtle.Turtle(visible=False)
background.penup()
for _ in range(90):
    background.goto(
        random.randint(-WIDTH // 2 + 10, WIDTH // 2 - 10),
        random.randint(-HEIGHT // 2 + 10, HEIGHT // 2 - 10),
    )
    background.dot(random.choice((2, 2, 3)), random.choice(("white", "light blue", "light yellow")))

pen = turtle.Turtle()
pen.speed(0)
pen.width(5)
pen.penup()
pen.goto(0, 0)
pen.pendown()


class Spark:
    def __init__(self, x, y, hue):
        angle = random.uniform(0, math.tau)
        speed = random.uniform(2.0, 6.0)
        self.dx = math.cos(angle) * speed
        self.dy = math.sin(angle) * speed
        self.gravity = 0.075
        self.life = random.randint(45, 75)
        self.max_life = self.life
        self.hue = (hue + random.uniform(-0.08, 0.08)) % 1
        self.turtle = turtle.Turtle()
        self.turtle.shape("circle")
        self.turtle.shapesize(0.35)
        self.turtle.color(colorsys.hsv_to_rgb(self.hue, 1, 1))
        self.turtle.penup()
        self.turtle.goto(x, y)

    def update(self):
        self.dy -= self.gravity
        self.turtle.goto(self.turtle.xcor() + self.dx, self.turtle.ycor() + self.dy)
        self.life -= 1
        remaining = self.life / self.max_life
        self.turtle.color(colorsys.hsv_to_rgb(self.hue, 1, max(0.05, remaining)))
        self.turtle.shapesize(max(0.06, 0.35 * remaining))
        if self.life <= 0:
            self.turtle.hideturtle()
            return False
        return True


step = 0
frame = 0
sparks = []
burst_positions = []
next_burst_frame = 0


def explode(x, y, hue):
    for _ in range(48):
        sparks.append(Spark(x, y, hue))


def animate():
    global step, frame, next_burst_frame

    if step < 100:
        hue = step / 50
        pen.pencolor(colorsys.hsv_to_rgb(hue % 1, 1, 1))
        pen.forward(step * 20 * 0.18)
        pen.right(91)
        step += 1
    else:
        pen.hideturtle()
        if burst_positions:
            if frame >= next_burst_frame:
                x, y, hue = burst_positions.pop(0)
                explode(x, y, hue)
                next_burst_frame = frame + 28

        sparks[:] = [spark for spark in sparks if spark.update()]

    screen.update()
    frame += 1
    screen.ontimer(animate, FRAME_DELAY)


def start_fireworks():
    x = max(-350, min(350, pen.xcor()))
    y = max(-250, min(250, pen.ycor()))
    burst_positions.extend(
        (
            (x, y, 0.12),
            (-240, 130, 0.52),
            (240, 190, 0.82),
        )
    )
    animate()


screen.ontimer(start_fireworks, FRAME_DELAY)
screen.exitonclick()
