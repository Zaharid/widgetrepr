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
    Unicode,Bool,Int,Float, Enum, List, HasTraits
)

from . import widgetrepr
from labcore.widgets.traits import ExecutableTrait

class EvaluableWidget(widgets.TextWidget):
    
    value = ExecutableTrait(help="Evaluable Python ", sync=True)

class ListWidget(widgets.ContainerWidget):
    value = List(help = 'value', sync = True)
    add_representation = None
    
    def __init__(self, klass, *args, **kwargs):
        
        self.klass = klass
            
        if 'add_representation' in kwargs:
            self.add_representation = kwargs.pop('add_representation')
        elif hasattr(self.klass, 'WidgetRepresentation'):
            self.add_representation = self.klass.WidgetRepresentation
        elif issubclass(self.klass, HasTraits):
            self.add_representation = widgetrepr.WidgetRepresentation
            
        super(ListWidget, self).__init__(*args, **kwargs)
    
    def _value_changed(self, value):
        title = widgets.LatexWidget(self.description)
        children = [title]
        for elem in value:
            wcont = widgets.ContainerWidget(description = str(elem))
            wtitle = widgets.LatexWidget(value = str(elem))
            
            edit_button = widgets.ButtonWidget(description = "Edit")
            delete_button = widgets.ButtonWidget(description = "Delete")
            wcont.children = [wtitle, edit_button, delete_button]
            
            children.append(wcont)
            
        add_button = widgets.ButtonWidget(description = "Add Command")

        def add_f(button):
            if self.add_representation:
                wr =  self.add_representation(self.klass, 
                      container_widget = widgets.PopupWidget)
            else:
                raise NotImplementedError() 
            wr.create_object()
             
        add_button.on_click(add_f)
        children.append(add_button)
        self.children = children


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



