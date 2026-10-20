import colorsys
import turtle


# Cree la fenetre dans laquelle Turtle va dessiner.
screen = turtle.Screen()
screen.setup(width=1000, height=800)
screen.bgcolor("black")
screen.title("L'escargot disco")
# Autorise les couleurs RGB entre 0 et 1.
turtle.colormode(1.0)

# Cree la tortue qui tient le crayon.
pen = turtle.Turtle()
pen.speed(6)  # 0 signifie : dessiner le plus vite possible.
pen.width(6)  # Epaisseur du trait.

# Repete les instructions 180 fois pour tracer la spirale.
for step in range(100):
	# Fait varier la couleur a chaque tour pour obtenir un arc-en-ciel.
	hue = step / 50
	pen.pencolor(colorsys.hsv_to_rgb(hue, 1, 1))
	# Avance un peu plus loin a chaque etape, puis tourne de 91 degres.
	pen.forward(step*20 * 0.45)
	pen.right(91)

pen.hideturtle()  # Cache la tortue une fois le dessin termine.
screen.exitonclick()  # Ferme la fenetre quand on clique dessus.
