# -*- coding: utf-8 -*-
"""
Created on Fri May 16 18:57:47 2014

@author: zah
"""
from collections import OrderedDict
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



def class_widget(cls, default_values):
    if _e:
        raise e
    cont = widgets.ContainerWidget()
    #Need sorted and dict
    children = []
    wdict = OrderedDict()
    class_traits = cls.class_traits()
    if hasattr(cls, '_widget_fields'):
        items = [(field,class_traits[field]) for field in cls._widget_fields]
    elif hasattr(cls, '_hidden_fields'):
        items = [(k,v) for (k,v) in class_traits.items() 
                if k not in cls._hidden_fields]
    else:
        items = class_traits.items()
       
    if hasattr(cls, "_member_names"):
        def order(item):
            name, trait = item
            if 'order' in trait._metadata:
                return trait._metadata['order']
            try:
                return cls._member_names.index(name)
            except ValueError:
                return float('inf')
        items = sorted(items, key = order)
    
    for name,trait in items:
        w = get_widget(name, trait)
        if w is None: continue
        if name in default_values:
            w.value = default_values[name]
        children += [w]
        wdict[name] = w
    cont.children = children
    return (cont, wdict)


class CreateManager(object):
    
    def __init__(self, varname, cls, default_values = None):
        self.varname = varname
        self.cls = cls
        if default_values is None:
            self.default_values = {}
        else:
            self.default_values = default_values
    
    def make_class_widget(self):
        if hasattr(self.cls, 'class_widget'):
            self.cont,self.wdict = self.cls.class_widget(self.default_values)
        else:
            self.cont,self.wdict = class_widget(self.cls, self.default_values)
        #TODO: Do this right.
        if 'name' in self.wdict and self.varname:
            self.wdict['name'].value = self.varname
    
    def read_form(self):
        values = {}
        for name, w in self.wdict.items():
            trait = w.traits()['value']
            try:
                value  = trait.eval_value(w.value)
            except AttributeError:
                value = w.value
            values[name] = value
        return values
    
    def new_object(self, button):
        values = self.read_form()
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
    
    

def create_object(varname, cls, default_values = None):
    if _e:
        raise _e
    if hasattr(cls, "CreateManager"):
        cm = cls.CreateManager(varname, cls, default_values)
    else:
        cm = CreateManager(varname, cls, default_values)
    cm.create_object()
    