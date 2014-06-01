# -*- coding: utf-8 -*-
"""
Created on Mon Apr  7 22:24:47 2014

@author: zah
"""
from collections import defaultdict
from collections import Mapping
import inspect

from IPython.html import widgets
from IPython.utils.traitlets import (
    Unicode,Bool,Int,Float, Enum
)

from labcore.widgets.traits import ExecutableTrait

class EvaluableWidget(widgets.TextWidget):
    
    value = ExecutableTrait(help="Evaluable Python ", sync=True)

def get_widget(name, trait):
    name = name.title().replace("_" ," " ).title()
    kw = dict(description = name, value = trait.get_default_value())
    if hasattr(trait, 'values'):
        values = trait.values
        if not isinstance(values, Mapping):
            values = {str(val): val for val in values}
        if trait.allow_none:
            values[""] = None
        kw['values'] = values
    if 'widget' in trait._metadata:
        widget = trait._metadata['widget']
        if inspect.isclass(widget):
            widget = widget(**kw)
    elif 'choices' in trait._metadata:
        choices = {str(item): item for item in trait._metadata['choices']}
        kw['values'] = choices
        widget = widgets.DropdownWidget(**kw)
    elif 'choose_from' in trait._metadata:
        choices = trait._metadata['choose_from']()
        if trait.allow_none:
            choices[""] = None
        kw['values'] = choices
        widget = widgets.DropdownWidget(**kw)
    else:
        widget = widget_mapping[type(trait)](**kw)
    return widget

widget_mapping = defaultdict(lambda: EvaluableWidget, {
     Unicode: widgets.TextWidget,
     Bool: widgets.CheckboxWidget,
     Int: widgets.IntTextWidget,
     Float: widgets.FloatTextWidget,
     Enum: widgets.DropdownWidget
})



