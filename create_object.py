# -*- coding: utf-8 -*-
"""
Created on Fri May 16 18:57:47 2014

@author: zah
"""
from IPython.display import display
from IPython.html import widgets
from IPython.core.interactiveshell import InteractiveShell

from labcore.widgets.widgets import get_widget

shell = InteractiveShell.instance()

def class_widget(cls):
    cont = widgets.ContainerWidget()
    #Need sorted and dict
    children = []
    wdict = {}
    for name,trait in cls.class_traits().items():
        w = get_widget(name, trait)
        if w is None: continue
        children += [w]
        wdict[name] = w
    cont.children = children
    return (cont, wdict)


class CreateManager(object):
    
    def __init__(self, varname, cls):
        self.varname = varname
        self.cls = cls
    
    def class_widget(self):
        if hasattr(self.cls, 'class_widget'):
            self.cont,self.wdict = self.cls.class_widget()
        else:
            self.cont,self.wdict = class_widget(self.cls)
    
    def new_object(self, button):
        values = {}
        for name, w in self.wdict.items():
            trait = w.traits()['value']
            try:
                value  = trait.eval_value(w.value)
            except AttributeError:
                value = w.value
            values[name] = value
        obj = self.cls(**values)
        shell.push({self.varname:obj})
    
    def create_description(self):
        return "Create %s" % self.cls.__name__
    
    def create_button(self):
        button = widgets.ButtonWidget(description = self.create_description)       
        return button        
        
    def create_object(self):
        cont, __ = self.class_widget()
        button = self.create_button()
        cont.children = cont.children + (button,)
        display(cont)
    
    

def create_object(varname, cls):
    if hasattr(cls, 'class_widget'):
        (cont,wdict) = cls.class_widget()
    else:
        cont,wdict = class_widget(cls)
    description = "Create %s" % cls.__name__
    def _new_obj(b):
        values = {}
        for name, w in wdict.items():
            trait = w.traits()['value']
            try:
                value  = trait.eval_value(w.value)
            except AttributeError:
                value = w.value
            values[name] = value
        obj = cls(**values)
        shell.push({varname:obj})
        
    button = widgets.ButtonWidget(description = description)
    button.on_click(_new_obj)
    cont.children = cont.children + (button,)
    display(cont)
    