# importing button widget from kivy framework
from kivy.core import text
from kivy.uix.button import Button
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from functools import partial
from kivy.core.text import LabelBase
import pandas as pd
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg #I had to edit line 256 in the source to make this work
from kivy.app import App
import matplotlib.pyplot as plt
import helper
import seaborn as sns

emp_survey = {name: 0  for name in pd.read_csv('../data/attrition-formated.csv').columns}
emp_survey_key = pd.read_csv('../data/attrition-keys.csv')




# this is the main class which will
# render the whole application




class uiApp(App):
  
    # method which will render our application
    def build(self):
        
        
        
        self.fresh = True # this is used to track if someone has already been to the survey page


        #create window and landing page
        self.window = GridLayout()
        self.window.cols = 1
        self.land = FloatLayout()
        self.b1 = Button(pos_hint={'right': .5, 'center_y': .5}, size_hint=(.2, .2), text='HR Dashboard', font_name='nunito')
        self.b2 = Button(pos_hint={'right': .7, 'center_y': .5}, size_hint=(.2, .2), text='Employee Survey', font_name='nunito')
        self.b2.bind(on_press=self.load_survey)
        self.b1.bind(on_press=self.load_hr)
        self.land.add_widget(self.b1)
        self.land.add_widget(self.b2)
        
        
        
        
        
       

        #create survey page
        self.survey = FloatLayout()
        qs = []
        i = .85
        h = .3
        
        for name in emp_survey.keys(): #This code is a little unusual but it dynamically creates all the buttons we need.
            i-=.05
            t = "{'right': h, 'center_y': i}"
            t2 = "{'right':  h +.05, 'center_y': i}"
            c = f"""
self.b_{name} = Button(pos_hint={t}, size_hint=(.25, .05), text=name, font_name='nunito')

self.i_{name} = TextInput(pos_hint={t2}, size_hint=(.05, .047), text='', font_name='nunito')
self.b_{name}.bind(on_press=partial((lambda self, x: self.help('{name}')), self))
self.survey.add_widget(self.i_{name})
self.survey.add_widget(self.b_{name})             
"""
            
            if name != 'Attrition':
                exec(c,globals(), locals())
            else: i+=.05 
            if i < 0.2: 
                h += .3
                i = .85

        


        self.b_back_to_land = Button(pos_hint={'right': .3, 'center_y': 0.9}, size_hint=(.25, .05), text='<- Back to Landing', font_name='nunito')
        self.b_back_to_land.bind(on_press=self.load_land)
        self.survey.add_widget(self.b_back_to_land)
        self.b_submit = Button(pos_hint={'right': .55, 'center_y': .9}, size_hint=(.25, .05), text='Submit Answers', font_name='nunito')
        self.b_submit.bind(on_press=self.sub)
        self.survey.add_widget(self.b_submit)

        self.window.add_widget(self.land)


        #create dashboard page
        self.hr = FloatLayout()
        self.plot_type = 'bar'
        self.b_back_to_land2 = Button(pos_hint={'right': .3, 'center_y': 0.9}, size_hint=(.25, .05), text='<- Back to Landing', font_name='nunito')
        self.b_back_to_land2.bind(on_press=self.load_land2)
        self.hr.add_widget(self.b_back_to_land2)
        self.b_run_model = Button(pos_hint={'right': .55, 'center_y': 0.9}, size_hint=(.25, .05), text='Run Model', font_name='nunito')
        self.b_run_model.bind(on_press=self.run_model)
        self.b_show_plot = Button(pos_hint={'right': .8, 'center_y': 0.9}, size_hint=(.25, .05), text='Show Plot', font_name='nunito')
        self.b_show_plot.bind(on_press=self.show_plot)
        self.b_save_fig = Button(pos_hint={'right': .3, 'center_y': 0.85}, size_hint=(.25, .05), text='Save Plot', font_name='nunito')
        self.b_save_fig.bind(on_press=self.save_fig)
       
        self.b_set_scatter = Button(pos_hint={'right': .55, 'center_y': 0.85}, size_hint=(.25, .05), text='Scatter Plot', font_name='nunito')
        self.b_set_scatter.bind(on_press=partial((lambda self, x: self.set_plot_type('scatter')), self))
        
        self.b_set_hist = Button(pos_hint={'right': .8, 'center_y': 0.85}, size_hint=(.25, .05), text='Histogram', font_name='nunito')
        self.b_set_hist.bind(on_press=partial((lambda self, x: self.set_plot_type('hist')), self))

        self.b_set_kde = Button(pos_hint={'right': .3, 'center_y': 0.8}, size_hint=(.25, .05), text='Density Plot', font_name='nunito')
        self.b_set_kde.bind(on_press=partial((lambda self, x: self.set_plot_type('kde')), self))
        
        self.b_set_bar = Button(pos_hint={'right': .55, 'center_y': 0.8}, size_hint=(.25, .05), text='Bar Plot', font_name='nunito')
        self.b_set_bar.bind(on_press=partial((lambda self, x: self.set_plot_type('bar')), self))

        self.b_load_actuals = Button(pos_hint={'right': .8, 'center_y': 0.8}, size_hint=(.25, .05), text='Load Actuals', font_name='nunito')
        self.b_load_actuals.bind(on_press=self.load_actuals)

        self.hr.add_widget(self.b_load_actuals)
        self.hr.add_widget(self.b_set_bar)
        self.hr.add_widget(self.b_set_scatter)
        self.hr.add_widget(self.b_set_kde)
        self.hr.add_widget(self.b_set_hist)
        self.hr.add_widget(self.b_show_plot)
        self.hr.add_widget(self.b_save_fig)
        self.hr.add_widget(self.b_run_model)
        
        i = .7
        h = .3
        for name in emp_survey.keys(): #This code is a little unusual but it dynamically creates all the buttons we need. 
            i-=.05
            t = "{'right': h, 'center_y': i}"
            t2 = "{'right':  h +.05, 'center_y': i}"
            c2 = f"""
self.o_{name} = Button(pos_hint={t}, size_hint=(.25, .05), text=name, font_name='nunito')
self.o_{name}.bind(on_press=partial((lambda self, x: self.set_x('{name}')), self))
self.hr.add_widget(self.o_{name})             
"""
            
            if name != 'Attrition':
                exec(c2,globals(), locals())
            else: i+=.05 
            if i < 0.1: 
                h += .25
                i = .7
        






        return self.window




#these are the member functions
    
    def set_x(self, name): 
        """Set the x variable for plots"""
        try:
            self.x = self.pred_df[name]
        except:
            t = 'Please insure you have run the model.'
            popup = Popup(title='Failed',
            content=Label(text=str(t)),
            size_hint=(None, None), size=((self.window.size[1] * 0.1) + (7 * len(t)), 100))
            popup.open()
            return

        t = f'X axis of plot set to "{name}".'
        popup = Popup(title='Success',
        content=Label(text=str(t)),
        size_hint=(None, None), size=((self.window.size[1] * 0.1) + (7 * len(t)), 100))
        popup.open()



    def load_survey(self, instance):
        """Loads the survey page"""
        self.window.remove_widget(self.land)
        self.window.add_widget(self.survey)
        if self.fresh == True:
            self.fresh = False
            popup = Popup(title='Instructions',
            content=Label(text='Click on the buttons for information about each question.'),
            size_hint=(None, None), size=((450), 200))
            popup.open()

    def set_ans(self, name, text):
        """sets individual survey answer"""
        emp_survey[name] = text
        

    def sub(self, instance):
        """Submit survey and save answers to csv"""
        s = pd.read_csv('../data/survey-results.csv')
        for name in s.columns:
            if name != 'Attrition':
                c = f"self.set_ans('{name}',self.i_{name}.text)"
                exec(c)
                to_save = {key: emp_survey[key] for key in emp_survey.keys() if key in s.columns}
                        
        save1 = s.append(to_save, ignore_index=True)
        save1.to_csv('../data/survey-results.csv', index=False)
        popup = Popup(title='Submission Accepted',
        content=Label(text=str('Please do not resubmit.')),
        size_hint=(None, None), size=((self.window.size[1] * 0.1) + (7 * max(len(name),len(str(emp_survey_key[name][0])))), 100))
        popup.open()
        
                
    def run_model(self,instance):
        """This fetches the answers from our model"""
        self.pred_df = helper.predict()
        self.default_x = self.pred_df['Age']
        self.x = self.default_x
        
        self.default_y = self.pred_df.proba
        self.y = self.default_y
        t = 'Model has run.'
        popup = Popup(title='Success',
        content=Label(text=str(t)),
        size_hint=(None, None), size=((self.window.size[1] * 0.1) + (7 * len(t)), 100))
        popup.open()




    def load_actuals(self,instance):
        """This fetches the actuals"""
        self.pred_df = helper.la()
        self.x = self.pred_df['Age']
       

        self.default_y = self.pred_df.pred
        self.default_y = self.pred_df.proba
        self.y = self.default_y
        t = 'Actuals Loaded.'
        popup = Popup(title='Success',
        content=Label(text=str(t)),
        size_hint=(None, None), size=((self.window.size[1] * 0.1) + (7 * len(t)), 100))
        popup.open()
    
        
        
    def set_plot_type(self, name):
        """set's the type of plot to be used"""
        try:
            self.plot_type = name
            
        except:
            t = 'Please insure you have run the model.'
            popup = Popup(title='Failed',
            content=Label(text=str(t)),
            size_hint=(None, None), size=((self.window.size[1] * 0.1) + (7 * len(t)), 100))
            popup.open()
            return

        
    def show_plot(self, instance):
        """Generate popup with selected plot"""
        try:
            test_model_run = self.x
        except:
            t = 'Please insure you have run the model.'
            popup = Popup(title='Failed',
            content=Label(text=str(t)),
            size_hint=(None, None), size=((self.window.size[1] * 0.1) + (7 * len(t)), 100))
            popup.open()
            return
        plt.figure()
        print("choosing plot", end='\r')
        try:
            if self.plot_type == 'scatter':
                sns.scatterplot(x = self.x, y=self.pred_df.proba, alpha= max(1/len(self.pred_df.proba),0.2))
                plt.axhline(.5, c='r')
            elif self.plot_type == 'hist':
                for name in self.pred_df.columns:
                    if self.x.name == name:
                        X = name
                temp = self.pred_df.groupby(X).sum()
                plt.hist(temp.pred)
            elif self.plot_type == 'kde':
                sns.kdeplot(x = self.x, y=self.pred_df.proba, fill=True)
                plt.axhline(.5, c='r')
            elif self.plot_type == 'bar':
                for name in self.pred_df.columns:
                    if self.x.name == name:
                        X = name
                temp = self.pred_df.groupby(X).sum()
                plt.bar(temp.index ,temp['proba'])
        except:
            t = 'Error in Generating plot. Ensure Variables are compatible with plot type.'
            popup = Popup(title='Failed',
            content=Label(text=str(t)),
            size_hint=(None, None), size=((self.window.size[1] * 0.1) + (7 * len(t)), 100))
            popup.open()
            return
        
            
        print("readying plot.")
        plt.title(f'Attrition Vs. {self.x.name}')
        plt.ylabel('Attrition')
        plt.xlabel(self.x.name)
        print("readying plot..", end ='\r')
        popup = Popup(title='CoA Vs. Selected Attribute',
        content=FigureCanvasKivyAgg(plt.gcf()),
        size_hint=(.8, .8))
        print("readying plot...", end ='\r')
        print("showing plot     ", end='\n')
        popup.open()
       
            

    def help(self, name):
        """This popup generates prompts for the individual questions."""
        popup = Popup(title=name,
        content=Label(text=str(emp_survey_key[name][0])),
        size_hint=(None, None), size=((self.window.size[1] * 0.1) + (7 * max(len(name),len(str(emp_survey_key[name][0])))), 100))
        popup.open()


    def load_land(self, instance):
        """Loads landing screen"""
        self.window.remove_widget(self.survey)
        self.window.add_widget(self.land)

    def load_land2(self, instance):
        """Loads landing screen"""
        self.window.remove_widget(self.hr)
        self.window.add_widget(self.land)
    def load_hr(self, instance):
        """Loads screen used for data viz"""
        self.window.remove_widget(self.land)
        self.window.add_widget(self.hr)
    
    def save_fig(self, instance):
        """Saves selected plot"""
        try:
            test_model_run = self.x
        except:
            t = 'Please insure you have run the model.'
            popup = Popup(title='Failed',
            content=Label(text=str(t)),
            size_hint=(None, None), size=((self.window.size[1] * 0.1) + (7 * len(t)), 100))
            popup.open()
            return

        
        plt.figure()
        try:
            if self.plot_type == 'scatter':
                sns.scatterplot(x = self.x, y=self.pred_df.proba, alpha= max(1/len(self.pred_df.proba),0.2))
                plt.axhline(.5, c='r')
            elif self.plot_type == 'hist':
                for name in self.pred_df.columns:
                    if self.x.name == name:
                        X = name
                temp = self.pred_df.groupby(X).sum()
                plt.hist(temp.pred)
            elif self.plot_type == 'kde':
                sns.kdeplot(x = self.x, y=self.pred_df.proba, fill=True)
                plt.axhline(.5, c='r')
            elif self.plot_type == 'bar':
                for name in self.pred_df.columns:
                    if self.x.name == name:
                        X = name
                temp = self.pred_df.groupby(X).sum()
                plt.bar(temp.index ,temp['proba'])
        except:
            t = 'Error in Generating plot. Ensure Variables are compatible with plot type.'
            popup = Popup(title='Failed',
            content=Label(text=str(t)),
            size_hint=(None, None), size=((self.window.size[1] * 0.1) + (7 * len(t)), 100))
            popup.open()
            return
        
            
        print("readying plot.")
        plt.title(f'Attrition Vs. {self.x.name}')
        plt.ylabel('Attrition')
        plt.xlabel(self.x.name)

        pop_layout = FloatLayout()
        i_path = TextInput(pos_hint={'right': .8, 'center_y': 0.5}, size_hint=(.7, .6), text='../output/', font_name='nunito')
        b_path = Button(pos_hint={'right': .9, 'center_y': 0.5}, size_hint=(.1, .6), text='Save', font_name='nunito')
        
        b_path.bind(on_press=partial((lambda self, x: plt.savefig(i_path.text)), self))
        pop_layout.add_widget(i_path)
        pop_layout.add_widget(b_path)

        plt.ylabel('Chance of Attrition')
        popup = Popup(title='Input destination filepath',
        content=pop_layout,
        size_hint=(.8, .2))
        
        popup.open()   
        
        
       
    
    
  
# registering our new custom fontstyle
LabelBase.register(name='nunito', 
                  fn_regular='../fonts/nunito/Nunito-Regular.ttf')
  
# running the application
uiApp().run()