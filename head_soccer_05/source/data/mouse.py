## cursors from windows for use with pygame
"""Set of cursors familiar to windows users
arrow is the standard windows cursor
hand is the link mouseover cursor, used in IE
diagResize1 is the bottom-right/top-left hand corner resizing cursor
text is the text editing cursor
"""

import pygame
import pygame.cursors
import pygame.mouse

arrow_strings = ( #sized 24x24
  "X                       ",
  "XX                      ",
  "X.X                     ",
  "X..X                    ",
  "X...X                   ",
  "X....X                  ",
  "X.....X                 ",
  "X......X                ",
  "X.......X               ",
  "X........X              ",
  "X.........X             ",
  "X..........X            ",
  "X......XXXXXX           ",
  "X...X..X                ",
  "X..XX..X                ",
  "X.X  X..X               ",
  "XX   X..X               ",
  "X     X..X              ",
  "      X..X              ",
  "       X..X             ",
  "       X..X             ",
  "        XX              ",
  "                        ",
  "                        ",
)
arrow=((24,24),(0,0))+pygame.cursors.compile(arrow_strings,".","X")


hand_strings = ( #sized 24x24
  "     XX                 ",
  "    X..X                ",
  "    X..X                ",
  "    X..X                ",
  "    X..X                ",
  "    X..XXX              ",
  "    X..X..XXX           ",
  "    X..X..X..XX         ",
  "    X..X..X..X.X        ",
  "XXX X..X..X..X..X       ",
  "X..XX........X..X       ",
  "X...X...........X       ",
  " X..X...........X       ",
  "  X.X...........X       ",
  "  X.............X       ",
  "   X............X       ",
  "   X...........X        ",
  "    X..........X        ",
  "    X..........X        ",
  "     X........X         ",
  "     X........X         ",
  "     XXXXXXXXXX         ",
  "                        ",
  "                        ",
)
hand=((24,24),(5,0))+pygame.cursors.compile(hand_strings,".","X")

text_strings = ( #sized 24x24
  "XXX XXX                 ",
  "   X                    ",
  "   X                    ",
  "   X                    ",
  "   X                    ",
  "   X                    ",
  "   X                    ",
  "   X                    ",
  "   X                    ",
  "   X                    ",
  "   X                    ",
  "   X                    ",
  "   X                    ",
  "   X                    ",
  "   X                    ",
  "XXX XXX                 ",
  "                        ",
  "                        ",
  "                        ",
  "                        ",
  "                        ",
  "                        ",
  "                        ",
  "                        ",
)
text=((24,24),(3,7))+pygame.cursors.compile(text_strings,".","X")

diagResize1_strings = ( #sized 24x24
  "XXXXXXX                 ",
  "X.....X                 ",
  "X....X                  ",
  "X...X                   ",
  "X..X.X                  ",
  "X.X X.X                 ",
  "XX   X.X                ",
  "      X.X               ",
  "       X.X   XX         ",
  "        X.X X.X         ",
  "         X.X..X         ",
  "          X...X         ",
  "         X....X         ",
  "        X.....X         ",
  "        XXXXXXX         ",
  "                        ",
  "                        ",
  "                        ",
  "                        ",
  "                        ",
  "                        ",
  "                        ",
  "                        ",
  "                        ",
)
diagResize1=((24,24),(8,8))+pygame.cursors.compile(diagResize1_strings,"X",".") #inverted

def set_cursor(array):
    pygame.mouse.set_cursor(*array)