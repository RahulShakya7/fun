from turtle import *

bgcolor('black')
hideturtle()
speed(50)
for i in range(420):
    if i % 2 == 0:
        color('blue')
    elif i % 3 == 0:
        color('violet')
    elif i % 4 == 0:
        color('indigo')
    else:
        color('cyan')
    forward(i * 2)
    left(91)
done()
