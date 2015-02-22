# How to use classic gui stuff? #


## Moving bar ##

### First import the library ###
```python
from source.gui.bar import Bar
```
### Then create a Bar object ###
```python
my_bar = Bar(width,height,bar_size,x,y,bar_color=(0,0,255),bar_background=(255,255,255),border_color=(0,0,0))
```
#### what is each thing? ####
* **width, height**: the x and y axis dimension of the total bar created
* **bar_size**: the relative size of the marked bar part, relative to the total bar height, while 1 means the bar height, 0.25 
* **x,y**: the position of the bar where in the context it is draw
* **bar_color, bar_background, border_color**:, different color configurations of the bar, the have a default


Then you will need to update the bar according to mouse events (that uses pygame mouse functions so you don't need to give it events), and to draw it in some pygame surface in order to visualize it

```python
my_bar.LogicUpdate() //update bar according to events, you don't need to give it nothing
my_bar.GraphicUpdate(surface) //update the bar drawn on the given surface that you need to give
```

### How to get the bar position? ###
Access the bar .position property, that has the position relative to bar size
```python
my_bar.position
```
* **my_bar.position = 0** if it is the min position
* **my_bar.position = 1** if it is the max position
* **my_bar.position = 0.25** if it is the quarter of the range of positions
* **my_bar.position = 0.75** if it is three quarters of the range of positions
* and so on

### How to set the bar position as an exception? ###
Use the function SetBarPosition, using as parameter the position of the bar
```python
my_bar.SetBarPosition(position)
```
the position is the same as the descripted before, relative to bar size


### How to set bar parent ###
Imagine that the bar is not on the main screen, is it on a window ant its x and y are from the 0,0 of that window. You need so to tell the them which is their context to make him know how to update the mouse events correcty, as the x and y of the bar are relative to the bar context.

So in order to do that you need to call

```python
my_bar.SetParent(parent)
```

Parent variable must be the context of the bar, that must have x,y properties because the bar will use them to update the events. If the x,y properties don't exist the program will throw an exception so ensure that. For example if the bar is into a window, and you want to update to bar according to the window 0,0 parent should be that window. It must have x and y properties as a window also has a position.
