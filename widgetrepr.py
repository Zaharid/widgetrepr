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


class WidgetRepresentation(object):
    
    widget_fields = None
    hidden_fields = None
    
    def __init__(self, cls, varname = None, default_values = None):
        self.varname = varname
        self.cls = cls
        if default_values is None:
            self.default_values = {}
        else:
            self.default_values = default_values
    
    def class_widget(self, default_values = None):
        if _e:
            raise e
        if default_values is None:
            default_values = self.default_values
        cont = widgets.ContainerWidget()
        #Need sorted and dict
        children = []
        wdict = OrderedDict()
        class_traits = self.cls.class_traits()
        if self.widget_fields:
            items = [(field,class_traits[field]) 
                    for field in self.widget_fields]
        elif self.hidden_fields:
            items = [(k,v) for (k,v) in class_traits.items() 
                    if k not in self.hidden_fields]
        else:
            items = class_traits.items()
           
        if hasattr(self.cls, "_member_names"):
            def order(item):
                name, trait = item
                if 'order' in trait._metadata:
                    return trait._metadata['order']
                try:
                    return self.cls._member_names.index(name)
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
    
    def change_object_f(self, obj):
        def _change_object(button):
            values = self.read_form()
            for key, val in values.items():
                obj[key] = val
        return _change_object
    
    def create_description(self):
        return "Create %s" % self.cls.__name__
    
    def edit_description(self, obj):
        return "Change %s" % obj
    
    def create_button(self):
        button = widgets.ButtonWidget(description = self.create_description())
        button.on_click(self.new_object)
        return button
    
    def edit_button(self, obj):
        button = widgets.ButtonWidget(description = self.edit_description(obj))
        button.on_click(self.chenge_object_f(obj))
        return button 
        
    def create_object(self):
        self.cont, self.wdict = self.class_widget()
        button = self.create_button()
        self.cont.children = self.cont.children + (button,)
        display(self.cont)
    
    def edit_object(self, obj):
        default_values = obj.trait_values()
        self.cont, self.wdict = self.class_widget(default_values)
        button = self.edit_button(obj)
        self.cont.children = self.cont.children + (button,)
        display(self.cont)
    
    

def create_object(varname, cls, default_values = None):
    if _e:
        raise _e
    if hasattr(cls, "WidgetRepresentation"):
        cm = cls.WidgetRepresentation(cls, varname, default_values)
    else:
        cm = WidgetRepresentation(cls, varname, default_values)
    cm.create_object()

def edit_object(obj):
    if _e:
        raise _e
    cls = obj.__class__
    if hasattr(cls, "WidgetRepresentation"):
        cm = cls.WidgetRepresentation(cls)
    else:
        cm = WidgetRepresentation(cls)
    cm.edit_object(obj)

def class_widget(cls, default_values = None):
    if _e:
        raise _e
    if hasattr(cls, "WidgetRepresentation"):
        cm = cls.WidgetRepresentation(cls, default_values)
    else:
        cm = WidgetRepresentation(cls, default_values)
    return cm.class_widget()
    