import kivy
from logging import getLogger

kivy.require("2.3.0")
from pathlib import Path
from kivy.app import App
from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
import pandas as pd
from kivy_dashboard import login

logger = getLogger()


class Test(TabbedPanel):
    pass


class TabbedPanelApp(App):
    def build(self):
        return Test()


# class to call the popup function
class PopupWindow(Widget):
    def btn(self):
        popFun()


# class to build GUI for a popup window
class P(FloatLayout):
    pass


# function that displays the content
def popFun():
    show = P()
    window = Popup(title="popup", content=show, size_hint=(None, None), size=(300, 300))
    window.open()


# class to accept user info and validate it
class loginWindow(Screen):
    username = ObjectProperty(None)
    pwd = ObjectProperty(None)

    def validate(self):
        logger.info(self.username.text)
        creds = login.Credentials(self.username.text)
        # validating if the email already exists
        if not creds.validate_username():
            popFun()
        else:
            if creds.validate_user(self.pwd.text):
                # switching the current screen to display validation result
                sm.current = "logdata"

                # reset TextInput widget
                self.username.text = ""
                self.pwd.text = ""
            else:
                popFun()


# class to accept sign up info
class signupWindow(Screen):
    name2 = ObjectProperty(None)
    pwd = ObjectProperty(None)

    def signupbtn(self):
        creds = login.Credentials(self.name2.text)
        logger
        if self.name2.text != "":
            if creds.validate_username():
                popFun()
            else:
                creds.create_user(self.pwd.text)
                sm.current = "login"
                self.name2.text = ""
                self.pwd.text = ""
        else:
            # if values are empty or invalid show pop up
            popFun()


# class to display validation result
class logDataWindow(Screen):
    pass


# class for managing screens
class windowManager(ScreenManager):
    pass


# kv file
kv = Builder.load_file("login.kv")
sm = windowManager()

# adding screens
sm.add_widget(loginWindow(name="login"))
sm.add_widget(signupWindow(name="signup"))
sm.add_widget(logDataWindow(name="logdata"))


# class that builds gui
class loginMain(App):
    def build(self):
        return sm


# driver function
if __name__ == "__main__":
    loginMain().run()


# if __name__ == '__main__':
#     TabbedPanelApp().run()
