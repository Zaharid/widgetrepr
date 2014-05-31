# -*- coding: utf-8 -*-
"""
Created on Fri May 16 18:57:47 2014

@author: zah
"""
#Delay errors so that this module can be imported without IPython.
_e = False
try:
    from IPython.display import display
    from IPython.html import widgets
    from IPython.core.interactiveshell import InteractiveShell
except ImportError as e:
    _e = Exception("You need the module %s to produce widgets." % e.name)
else:
    shell = InteractiveShell.instance()
    
from labcore.widgets.widgets import get_widget



def class_widget(cls):
    if _e:
        raise e
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
    
    def make_class_widget(self):
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
        return obj
        
    @property
    def create_description(self):
        return "Create %s" % self.cls.__name__
    
    def create_button(self):
        button = widgets.ButtonWidget(description = self.create_description)
        button.on_click(self.new_object)
        return button        
        
    def create_object(self):
        self.make_class_widget()
        button = self.create_button()
        self.cont.children = self.cont.children + (button,)
        display(self.cont)
    
    

def create_object(varname, cls):
    if _e:
        raise _e
    if hasattr(cls, "CreateManager"):
        print("has cm")
        cm = cls.CreateManager(varname, cls)
    else:
        cm = CreateManager(varname,cls)
    cm.create_object()
    