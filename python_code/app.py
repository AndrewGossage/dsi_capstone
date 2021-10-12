# importing button widget from kivy framework
from kivy.core import text
from kivy.uix.button import Button
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from functools import partial
# importing labelbase which which 
# register our custom font for application
from kivy.core.text import LabelBase
from kivy.lang import Builder
import pandas as pd

emp_survey = {name: 0  for name in pd.read_csv('../data/attrition-formated.csv').columns}
emp_survey_key = pd.read_csv('../data/attrition-keys.csv')




# this is the main class which will
# render the whole application




class uiApp(App):
  
    # method which will render our application
    def build(self):
        


        self.fresh = True

        self.window = GridLayout()
        self.window.cols = 1
        self.land = FloatLayout()
        self.b1 = Button(pos_hint={'right': .5, 'center_y': .5}, size_hint=(.2, .2), text='HR Dashboard', font_name='Lemonada')
        self.b2 = Button(pos_hint={'right': .7, 'center_y': .5}, size_hint=(.2, .2), text='Employee Survey', font_name='Lemonada')
        self.b2.bind(on_press=self.load_survey)
        self.land.add_widget(self.b1)
        self.land.add_widget(self.b2)

        self.survey = FloatLayout()
        qs = []
        i = .02
        h = .3
        
        for name in emp_survey.keys(): #terribly hacky code that dynamically creates all needed buttons and labels
            i+=.05
            t = "{'right': h, 'center_y': i}"
            t2 = "{'right':  h +.05, 'center_y': i}"
            c = f"""
self.b_{name} = Button(pos_hint={t}, size_hint=(.25, .05), text=name, font_name='Lemonada')

self.i_{name} = TextInput(pos_hint={t2}, size_hint=(.05, .047), text='', font_name='Lemonada')
self.b_{name}.bind(on_press=partial((lambda self, x: self.help('{name}')), self))
self.survey.add_widget(self.i_{name})
self.survey.add_widget(self.b_{name})             
"""
            
            if name != 'Attrition':
                exec(c,globals(), locals())
            else: i-=.05 
            if i > 0.8: 
                h += .3
                i = .02

        
        

        self.b_back_to_land = Button(pos_hint={'right': .3, 'center_y': i+.9}, size_hint=(.25, .05), text='<- Back to Landing', font_name='Lemonada')
        self.b_back_to_land.bind(on_press=self.load_land)
        self.survey.add_widget(self.b_back_to_land)
        self.b_submit = Button(pos_hint={'right': .6, 'center_y': i+.9}, size_hint=(.25, .05), text='Submit Answers', font_name='Lemonada')
        self.b_submit.bind(on_press=self.sub)
        self.survey.add_widget(self.b_submit)

        self.window.add_widget(self.land)

        return self.window

    def load_survey(self, instance):
       
        self.window.remove_widget(self.land)
        self.window.add_widget(self.survey)
        if self.fresh == True:
            self.fresh = False
            popup = Popup(title='Instructions',
            content=Label(text='Click on the buttons for information about each question.'),
            size_hint=(None, None), size=((450), 200))
            popup.open()

    def set_ans(self, name, text):
        emp_survey[name] = text
        

    def sub(self, instance):
        for name in emp_survey.keys():
            if name != 'Attrition':
                c = f"self.set_ans('{name}',self.i_{name}.text)"
                exec(c)
            

    def help(self, name):
        popup = Popup(title=name,
        content=Label(text=str(emp_survey_key[name][0])),
        size_hint=(None, None), size=((self.window.size[1] * 0.1) + (7 * max(len(name),len(str(emp_survey_key[name][0])))), 100))
        popup.open()
    def load_land(self, instance):
        
        self.window.remove_widget(self.survey)
        self.window.add_widget(self.land)
    
    
        
       
    
    
  
# registering our new custom fontstyle
LabelBase.register(name='Lemonada', 
                  fn_regular='NunitoRegular.ttf')
  
# running the application
uiApp().run()