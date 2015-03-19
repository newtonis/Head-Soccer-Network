__author__ = 'Dylan'

import pygame
from source.gui.window import Window
from source.gui.button import NeutralButton,AcceptButton,RejectButton
from source.gui.text import Text,fonts
from source.gui.input import Input
from source.gui.checkbox import CheckBox
from source.database import session_query
import copy

class SignUp(Window):
    def __init__(self,parent,save):
        Window.__init__(self,"Sign up",(36, 107, 97),(43, 76, 111),0,0,400,210,(255,255,255))
        self.parent = parent
        self.save = save
        font = fonts.BebasNeue.c25
        y_act = 29
        ###  User text  ###
        UserText = Text(font,"Username:",(0,0,0))
        UserText.x = self.width/2 - UserText.surface.get_size()[0] - 5
        UserText.y = y_act
        self.AddElement(UserText,"User Text")
        ###  User input  ###
        UserInput = Input()
        UserInput.AllowAll()
        UserInput.SetParent(self)
        UserInput.SetSize(150,30)
        UserInput.x = self.width/2 + 5
        UserInput.y = UserText.y + (UserText.surface.get_size()[1]/2 - UserInput.size[1]/2)
        self.AddElement(UserInput,"User Input")
        ###  Password text  ###
        y_act += UserText.surface.get_size()[1] + 5
        PassText = Text(font,"Password:",(0,0,0))
        PassText.x = self.width/2 - PassText.surface.get_size()[0] - 5
        PassText.y = y_act
        self.AddElement(PassText,"Pass Text")
        ###  Password input  ###
        PassInput = copy.copy(UserInput)
        PassInput.y = PassText.y + (PassText.surface.get_size()[1]/2 - PassInput.size[1]/2)
        PassInput.password = True
        self.AddElement(PassInput,"Pass Input")
        ###  Pass Confirm text  ###
        y_act += PassText.surface.get_size()[1] + 5
        PassConfText = Text(font,"Confirm password:",(0,0,0))
        PassConfText.x = self.width/2 - PassConfText.surface.get_size()[0] - 5
        PassConfText.y = y_act
        self.AddElement(PassConfText,"Confirm Password Text")
        ###  Pass Confirm input  ###
        PassConfInput = copy.copy(PassInput)
        PassConfInput.y = PassConfText.y + (PassConfText.surface.get_size()[1]/2 - PassConfInput.size[1]/2)
        self.AddElement(PassConfInput,"Confirm Password Input")
        ###  Email text  ###
        y_act += PassConfText.surface.get_size()[1] + 5
        EmailText = Text(font,"Email:",(0,0,0))
        EmailText.x = self.width/2 - EmailText.surface.get_size()[0] - 5
        EmailText.y = y_act
        self.AddElement(EmailText,"Email Text")
        ###  Email input  ###
        EmailInput = copy.copy(PassConfInput)
        EmailInput.password = False
        EmailInput.y = EmailText.y - (EmailText.surface.get_size()[1]/2 - EmailInput.size[1]/2)
        self.AddElement(EmailInput,"Email Input")
        ###  Setting next inputs  ###
        UserInput.next_input = PassInput
        PassInput.next_input = PassConfInput
        PassConfInput.next_input = EmailInput
        EmailInput.next_input = UserInput
        ###  Accept button  ###
        y_act += EmailText.surface.get_size()[1] + 10
        Accept = AcceptButton("Sign up",150,(0,0),font)
        Accept.x = self.width/2+10
        Accept.y = y_act
        self.AddElement(Accept,"Accept")
        ###  Reject button  ###
        Reject = RejectButton("Cancel",150,(0,0),font)
        Reject.x = self.width/2 - 10 - Reject.size[0]
        Reject.y = y_act
        self.AddElement(Reject,"Cancel")
        ###  Extra variables  ###
        self.pressed = False
        self.pressed2 = False
        self.parent.SetRegisterDef(self.RegisterConfirm)
        self.sending_data = False

    def RegisterConfirm(self,data):
        if data["error"] != "":
            self.sending_data = False
            error = Text(fonts.BebasNeue.c20,data["error"],(255,0,0))
            error.x = self.width/2 - error.surface.get_size()[0]/2
            error.y = 29
            if not self.references.has_key("Error"):
                self.AddElement(error,"Error")
                add = error.surface.get_size()[1] + 5
                elements = ["User Text","User Input","Pass Text","Pass Input","Confirm Password Text","Confirm Password Input","Email Text","Email Input","Accept","Cancel"]
                for x in elements:
                    self.references[x].y += add
                self.height += add
                self.GenerateSurface()
            else:
                self.DeleteElement("Error")
                self.AddElement(error,"Error")
        else:
            self.parent.DeleteWindow("SignUp")
            self.parent.AddWindowCenteredOnFront(self.save,None,"Login")
    def LogicUpdate(self):
        Window.LogicUpdate(self)


        if not self.sending_data:
            if (self.references["Accept"].pressed or pygame.key.get_pressed()[pygame.K_RETURN] or pygame.key.get_pressed()[pygame.K_KP_ENTER]) and self.mouseOut:
                self.pressed = True
            else:
                if self.pressed:
                    self.sending_data = True
                    self.pressed = False
                    data = {
                        "action":"register",
                        "username":self.references["User Input"].text,
                        "password":self.references["Pass Input"].text,
                        "confirmation":self.references["Confirm Password Input"].text,
                        "email":self.references["Email Input"].text
                    }
                    self.parent.Send(data)
            if self.references["Cancel"].pressed:
                self.pressed2 = True
            else:
                if self.pressed2:
                    self.pressed2 = False
                    self.parent.DeleteWindow("SignUp")
                    self.parent.AddWindowCenteredOnFront(self.save,None,"Login")

class Login(Window):
    def __init__(self,parent,save):
        self.save = save
        Window.__init__(self,"Login",(36, 107, 97),(43, 76, 111),0,0,400,160,(255,255,255))
        self.parent = parent
        font = fonts.AldoTheApache
        UserText = Text(font.c30,"Username:",(0,0,0))
        UserText.x = self.width/2-UserText.surface.get_size()[0]-5
        UserText.y = self.height/2-UserText.surface.get_size()[1]-2-15
        self.AddElement(UserText,"User Text")
        PassText = Text(font.c30,"Password:",(0,0,0))
        PassText.x = self.width/2-PassText.surface.get_size()[0]-5
        PassText.y = self.height/2 + 7-15
        self.AddElement(PassText,"Pass Text")
        UserInput = Input()
        UserInput.AllowAll()
        UserInput.SetParent(self)
        UserInput.SetSize(150,30)
        UserInput.x = self.width/2 + 5
        UserInput.y = self.height/2 - UserInput.size[1] - 2-15
        self.AddElement(UserInput,"User Input")
        PassInput = copy.copy(UserInput)
        PassInput.y += PassInput.size[1] + 5
        PassInput.password = True
        self.AddElement(PassInput,"Pass Input")
        UserInput.SetNextInput(PassInput)
        Accept = AcceptButton("Login",150,(0,0),font)
        Accept.x = self.width/2+10
        Accept.y = PassInput.y + PassInput.size[1] + 20
        self.AddElement(Accept,"Accept")
        Reject = RejectButton("Cancel",150,(0,0),font)
        Reject.x = self.width/2 - 10 - Reject.size[0]
        Reject.y = Accept.y
        self.AddElement(Reject,"Cancel")

        self.was_pressed1 = False
        self.was_pressed2 = False
        self.parent.SetLoginDef(self.Login)
        self.loging_in = False

        self.username = ""
        self.password = ""
    def Login(self,data): #si el login es correcto
        self.loging_in = False
        if data["pass"] == "DT":
            session_query.SessionDeclareLogin(self.username,self.password)
            self.Kill()
        elif data["pass"] == "error":
            error_msg = Text(fonts.BebasNeue.c20,data["error"],(255,0,0))
            error_msg.x = self.width/2-error_msg.surface.get_size()[0]/2
            error_msg.y = 26
            if not self.references.has_key("Error"):
                self.AddElement(error_msg,"Error")
                extra = error_msg.surface.get_size()[1]
                self.references["User Text"].y += extra
                self.references["Pass Text"].y += extra
                self.references["User Input"].y += extra
                self.references["Pass Input"].y += extra
                self.references["Accept"].y += extra
                self.references["Cancel"].y += extra
                self.references["User Input"].SetBackgroundColor(200,0,0)
                self.references["Pass Input"].SetBackgroundColor(200,0,0)
                self.height += extra
                self.GenerateSurface()
            else:
                self.DeleteElement("Error")
                self.AddElement(error_msg,"Error")
    def LogicUpdate(self):
        Window.LogicUpdate(self)
        if not self.loging_in:
            if self.references["Accept"].pressed or pygame.key.get_pressed()[pygame.K_RETURN] or pygame.key.get_pressed()[pygame.K_KP_ENTER]:
                self.was_pressed2 = True
            else:
                if self.was_pressed2:
                    self.was_pressed2 = False
                    self.loging_in = True
                    self.parent.Send({"action":"check_login","username":self.references["User Input"].text,"password":self.references["Pass Input"].text})
                    self.username = self.references["User Input"].text
                    self.password = self.references["Pass Input"].text
            if self.references["Cancel"].pressed:
                self.was_pressed1 = True
            else:
                if self.was_pressed1:
                    self.parent.DeleteWindow("Login window")
                    self.parent.AddWindowCenteredOnFront(self.save,None,"Login")
                else:
                    self.was_pressed1 = False

class Selector(Window):
    def __init__(self,parent,save):
        self.parent = parent
        Window.__init__(self,"User selector",(36, 107, 97),(43, 76, 111),0,0,400,200,(255,255,255))
        self.save = save
        Login = NeutralButton("Login")
        Login.x = self.width/2-Login.size[0]/2
        Login.y = (self.height)/2+20-(3*Login.size[1]+10)/2
        self.AddElement(Login,"Login")
        SignIn = NeutralButton("Sign Up")
        SignIn.x = Login.x
        SignIn.y = Login.y + Login.size[1] + 5
        self.AddElement(SignIn,"Sign Up")
        Guest = NeutralButton("Enter as guest")
        Guest.x = Login.x
        Guest.y = SignIn.y + SignIn.size[1] + 5
        self.AddElement(Guest,"Guest")
    def LogicUpdate(self):
        Window.LogicUpdate(self)
        if self.references["Login"].pressed:
            self.parent.AddWindowCenteredOnFront(Login(self.parent,self),None,"Login window")
            self.parent.DeleteWindow("Login")
        if self.references["Sign Up"].pressed:
            self.parent.AddWindowCenteredOnFront(SignUp(self.parent,self),None,"SignUp")
            self.parent.DeleteWindow("Login")
        if self.references["Guest"].pressed:
            self.parent.DeleteWindow("Login")
            self.parent.AddWindowCenteredOnFront(self.save,None,"loading")
            self.parent.references["loading"].SetNameInput()