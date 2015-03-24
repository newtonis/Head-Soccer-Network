__author__ = 'newtonis'

def gPingText(value):
    value = float(int(value*10))
    value /= 10.0
    if value < 10:
        return "   " + str(value) + " ms"
    elif value < 100:
        return "  " + str(value) + " ms"
    elif value < 1000:
        return " " +str(value) + " ms"
    elif value < 10000:
        return str(value) + " ms "
    else:
        return "       "
def gPingColor(value):
    if value < 100:
        return 0,100,0
    elif value < 150:
        return 0,150,0
    elif value < 200:
        return 50,100,0
    elif value < 250:
        return 255,128,0
    elif value < 300:
        return 255,100,0
    elif value < 400:
        return 255,50,0
    elif value < 500:
        return 255,0,0
    else:
        return 200,0,0