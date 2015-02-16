#Beercave Gamews Beerware license v1.0
       #This code is free to use for anything you want.
       #If you find it useful, I'd appreciate it if you buy me a beer :)
      #See http://www.beercave.co.uk/content/beerware for details
        import pygame 
        from pygame.locals import * 
 
       #wrapper class for all input methods
       #maps controllers to named controls, eg 'FIRE', 'JUMP' etc
     #keeps all that nasty control handling code out of the game classes
        #call GetControl(CONTROL_NAME) to check the control state in game
 
      #clamp value to a min/max range
        def clamp(sourceval, minval, maxval):
     return max(min(sourceval, maxval), minval)
 
     class Input():
      def __init__(self, **kwargs):
       #mappings for keydowns, key states and axis positions
      #format is controlname : [list of [source, (arguments...)\]\] 
     #multiple inputs can all map to the same control
 
       #key/button press events (1,0)
     #identifies if a key/button was pressed this frame
     #['keyevent'], (KEY_ID,)] where KEY_ID is the pygame key id
        #['buttonevent', (STICK_ID, BUTTON_ID)]
        #['mouseevent', (BUTTON_ID)]
       #stickevent tracks whether the joystick was moved in a given 
      #direction this frame. Threshold parameter allows for
      #filtering out of small movements
      #['stickevent', (STICK_ID,AXIS_ID,DIRECTION,THRESHOLD)]
 
        #key/button states (1,0)
       #identifies if a key/button is currently pressed
       #['keystate'], (KEY_ID,)]
      #['buttonstate', (STICK_ID, BUTTON_ID)]
 
        #axis mappings
     #track a joystick axis
     #can also map keyboard controls to a virtual axis so
       #the game code doesn't need to know whether it's
       #dealing with keys or a controller
     #['keyaxis'], (+KEY_ID, -KEY_ID)] 
     #+KEY_ID is mapped to the positive axis direction
      #-KEY_ID is mapped to the negative axis direction
      #['stickaxis', (STICK_ID, AXIS_ID,)]
       #use '-stickaxis' to invert axis values
 
        self.controlMap = {
       'QUIT' : \[\['keyevent', (K_ESCAPE,)\]\],
        'PAUSE' : \[\['keyevent', (K_p,)\]\],
        'START' : [
      ['keyevent', (K_SPACE,)],
       ['keyevent', (K_RETURN,)],
      ['buttonevent', (0,0)]
      ],
     'TEST' : \[\['keyevent', (K_SPACE,)\]\],
     'OPTIONS' : \[\['keyevent', (K_o,)\]\],
      'SCREENSHOT' : \[\['keyevent', (K_RCTRL,)\]\],
       'THRUST' : [
     ['keyaxis', (K_RIGHT, K_LEFT)],
       ['stickaxis', (0,0)]
        ],
     'FIRE' : \[\['keyevent', (K_LCTRL,)],
      ['keyevent', (K_z,)],
       ['mouseevent', (1,)],
      ['mouseevent', (2,)],
      ['mouseevent', (3,)],
      ['buttonevent', (0,0)]
      ],
     'FIRE2' : [
      ['keyevent', (K_LSHIFT,)],
      ['keyevent', (K_c,)],
       ['buttonevent', (0,1)]
      ],
     'TURN' : [
       ['keyevent', (K_x,)],
       ['buttonevent', (0,2)]
      ],
     'CLIMB' : [
      ['keyaxis', (K_UP, K_DOWN)],
      ['-stickaxis', (0,1,)]
      ],
     'STICK1' : [
     ['-stickaxis', (0,0,)]
      ],
     'STICK2' : [
     ['-stickaxis', (0,1,)]
      ],
     'UP' : [
     ['keyevent', (K_UP, )],
      ['stickevent', (0,1,-1,.5)]
     ],
     'DOWN' : [
       ['keyevent', (K_DOWN, )],
        ['stickevent', (0,1,1,.5)]
     ],
     'RIGHT' : [
      ['keyevent', (K_RIGHT, )],
       ['stickevent', (0,0,1,.5)]
     ],
     'LEFT' : [
       ['keyevent', (K_LEFT, )],
        ['stickevent', (0,0,-1,.5)]
     ],
     'FLINGX' : \[\['mousedir', (0,)\]\],
        'FLINGY' : \[\['mousedir', (1,)\]\]
     }
      self.Mouse = [0,0]
      #state for all keys
        self.keys = pygame.key.get_pressed()
       #did event happen this frame for all keys
      self.keyevents = [0] *323
       #all key events this frame
     self.keyspressed = []
     #all mouse events this frame
       self.mouseevents = [0] * 4
      #button press events this frame
        self.buttonevents = \[\[0]*20]
        #state of all joysticks in the system
      self.stickStates = []
 

       self.InitSticks()
        self.gesturetime = 0
     self.gesturex = 0
        self.gesturey = 0
 
        #update the input states
       #your game engine should call this every frame
     #for mouse control to work pass time elapsed this frame as dt
      def Poll(self, dt=0):
       keyevents = pygame.event.get(pygame.KEYDOWN)
      mouseevents = pygame.event.get(pygame.MOUSEBUTTONDOWN)
        stickevents = pygame.event.get(pygame.JOYAXISMOTION)
      buttonevents = pygame.event.get(pygame.JOYBUTTONDOWN)
 
     #clear the events list from the previous frame
     self.keyevents = [0] *323
       self.mouseevents = [0] * 4
      sticks = self.stickCount
      for i in range(0,sticks):
       state = self.stickStates[i]
      axes = state['numaxes'] 
        buttons = state['numbuttons'] 
      state['axisevents'] = [0] * axes
       state['buttonevents'] = [0] * buttons
      state['axes'] = [0.] * axes
 
        #move all pressed keys to an array - will save 
        #iterating over the list every time we check
       #for a keypress
        for event in keyevents:
       self.keyevents[event.key] = True
 
      #all keyevents this frame
      #exposing this is useful for situations where we want to know
      #all the keys that were pressed - ie for handling text input
       self.keyspressed = keyevents
 
      self.keys = pygame.key.get_pressed()
 
       for event in mouseevents:
     self.mouseevents[event.button] = True
 
     for event in stickevents:
     self.stickStates[event.joy]['axisevents'][event.axis] = event.value
 
        for event in buttonevents:
        self.stickStates[event.joy]['buttonevents'][event.button] = True
 
        self.CheckMouse(dt)
 
        self.CheckSticks()
       pygame.event.clear()
 
        #check the system for attached joysticks and initialise
        def InitSticks(self):
        sticks = pygame.joystick.get_count()
      self.stickCount = sticks
      self.stickStates = []
     for i in range(0,sticks):
       state = {}
       state['stick'] = stick =pygame.joystick.Joystick(i)
      stick.init()
      state['name'] = stick.get_name()
       state['numbuttons'] = buttons = stick.get_numbuttons()
       state['numaxes'] = axes  = stick.get_numaxes()
       state['buttonstates'] = [0] * buttons
      state['axes'] = [0.] * axes
        state['axisevents'] = [0] * axes
       state['buttonevents'] = [0] * buttons
      self.stickStates.append(state)
 
       #poll all joysticks for state
      def CheckSticks(self):
       sticks = self.stickCount
      for i in range(0,sticks):
       state = self.stickStates[i]
      stick = state['stick']
      buttons = state['numbuttons']
       axes = state['numaxes']
 
     for k in range(0, axes):
        state['axes'][k] = stick.get_axis(k)
 
       #poll mouse for state
      def CheckMouse(self,dt):
       #basic mouse gestures
      relx,rely = pygame.mouse.get_rel()
 
      #clear the axes so we don't report a movement every frame
      self.Mouse = [0,0]
      #check we've moved a decent amount
     if relx*relx+rely*rely > 10:
     self.gesturetime += dt
        self.gesturex += relx
     self.gesturey += rely
 
     elif self.gesturetime > 0:
      #a gesture just ended
      #change the velocity
       self.Mouse = [self.gesturex, -self.gesturey]
     self.gesturetime = 0
     self.gesturex = 0
        self.gesturey = 0
        return
 
     #call this to get the state of a defined control
       def GetControl(self, name):
        mappings = self.controlMap.get(name, None)
      result = 0.
     for map in mappings:
     source, args = map
        if source == 'keyevent':
       key, = args
       result += self.GetKeyEvent(key)
      if source == 'buttonevent':
        stick,button = args
        result += self.GetButtonEvent(stick, button)
       if source == 'mouseevent':
     button, = args
        result += self.GetMouseEvent(button)
     if (source == 'keystate'):
      key, = args
       result += self.GetKeyState(key)
      if (source == 'keyaxis'):
       key1,key2 = args
       result += self.GetKeyAxis(key1, key2)
      if (source == 'stickaxis'):
     stick, axis = args
     val = self.GetStickAxis(stick, axis)
       result += val
        if (source == '-stickaxis'):
        stick, axis = args
     val = -self.GetStickAxis(stick, axis)
       result += val
        if (source == 'stickevent'):
        stick, axis, direction, threshold = args
       result += self.GetStickEvent(stick, axis, direction, threshold)
        if (source == 'mousedir'):
      axis, = args
      #mouse axis overrules alternatives if in use
       return self.GetMouseAxis(axis)
      return clamp(result, -1, 1)
 
       #functions to handle different control mappings
        def GetKeyEvent(self, key):
        return self.keyevents[key]
 
      def GetButtonEvent(self, stick, button):
     if self.stickCount <= stick: return False 
        return self.stickStates[stick]['buttonevents'][button]
 
      def GetStickEvent(self, stick, axis, direction, threshold):
      if self.stickCount <= stick: return False 
        value = self.stickStates[stick]['axisevents'][axis]
      return value * direction > threshold
 
     def GetMouseEvent(self, button):
       return self.mouseevents[button]
 
     def GetKeyState(self, key):
        return self.keys[key]
 
       def GetKeyAxis(self, key1, key2):
        keys = self.keys
      val1 = 1. if self.keys[key1] else 0.
       val2 = -1. if self.keys[key2] else 0.
       return val1 + val2
 
        def GetStickAxis(self, stick, axis):
     if self.stickCount <= stick: return 0. 
       state = self.stickStates[stick]
      pos = state['axes'][axis]
     return pos
 
      def GetMouseAxis(self, axis):
      return self.Mouse[axis]/1000.
