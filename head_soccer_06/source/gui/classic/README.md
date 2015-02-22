## How to use classic gui stuff? ##


# Moving bar #

To use it first import the library
```
from source.gui.bar import Bar
```
Then create a Bar object
```
my_bar = Bar(width,height,bar_size,x,y,bar_color=(0,0,255),bar_background=(255,255,255),border_color=(0,0,0))
```
what is each thing?
*width, height: the x and y axis dimension of the total bar created
*bar_size: the relative size of the marked bar part, relative to the total bar height, while 1 means the bar height, 0.25 
*x,y: the position of the bar where in the context it is draw
*bar_color, bar_background, border_color, different color configurations of the bar, the have a default

Then you will need to update the bar according to mouse events (that uses pygame mouse functions so you don't need to give it events), and to draw it in some pygame surface in order to visualize it

```
my_bar.LogicUpdate() //update bar according to events, you don't need to give it nothing
my_bar.GraphicUpdate(surface) //update the bar drawn on the given surface that you need to give
```

How to set the bar position as an exception?
Use the function SetBarPosition, using as parameter the position of the bar that is 0 if it is the min position and 1 if it is the max position

```
my_bar.SetBarPosition(position)
```

