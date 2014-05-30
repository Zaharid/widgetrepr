# -*- coding: utf-8 -*-
"""
Created on Mon Apr  7 22:24:47 2014

@author: zah
"""
from collections import defaultdict
import inspect

from IPython.html import widgets
from IPython.utils.traitlets import (
    List,Unicode,Bool,Int,Float,Instance,Any,Type,
)
from IPython.utils import traitlets
from IPython.core.interactiveshell import InteractiveShell

from labcore.widgets.traits import ExecutableTrait

shell = InteractiveShell.instance()
class EvaluableWidget(widgets.TextWidget):
    
    value = ExecutableTrait(shell.user_ns, shell.user_global_ns,
                            help="Evaluable Python ", sync=True)

def get_widget(name, trait):
    name = name.title().replace("_" ," " ).title()
    if 'widget' in trait._metadata:
        widget = trait._metadata['widget']
        if inspect.isclass(widget):
            widget = widget(description = name, value = trait.default_value)
    elif 'choices' in trait._metadata:
        choices = trait._metadata['choices']
        widget = widgets.DropdownWidget(values = choices,description = name, 
            value = trait.default_value )
    elif 'choose_from' in trait._metadata:
        choices = trait._metadata['choose_from']()
        widget = widgets.DropdownWidget(values = choices,description = name, 
            value = trait.default_value )
    else:
        widget = widget_mapping[type(trait)](description = name, 
            value = trait.default_value)
    return widget

widget_mapping = defaultdict(lambda: EvaluableWidget, {
     Unicode: widgets.TextWidget,
     Bool: widgets.CheckboxWidget,
     Int: widgets.IntTextWidget,
     Float: widgets.FloatTextWidget,
})



