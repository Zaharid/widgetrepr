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
    