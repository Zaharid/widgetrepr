# -*- coding: utf-8 -*-
"""
Created on Fri May 16 18:57:47 2014

@author: zah
"""
import inspect
from collections import OrderedDict, defaultdict, Mapping
#Delay errors so that this module can be imported without IPython.
from IPython.utils.traitlets import (
    Unicode,Bool,Int,Float, Enum, List, HasTraits, Instance
)
_e = False
try:
    from IPython.display import display
    from IPython.html import widgets
    from IPython.core.interactiveshell import InteractiveShell
except ImportError as e:
    _e = Exception("You need the module %s to produce widgets." % e.name)

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
            self.add_representation = WidgetRepresentation
            
        super(ListWidget, self).__init__(*args, **kwargs)
        self._value_changed(self.value)
    
    def _value_changed(self, value):
        print("tonto")
        title = widgets.LatexWidget(value = self.description)
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


class WidgetRepresentation(object):

    widget_fields = None
    hidden_fields = None
    varname_map = None
    container_widget = widgets.ContainerWidget

    widget_mapping = defaultdict(lambda: EvaluableWidget, {
        Unicode: widgets.TextWidget,
        Bool: widgets.CheckboxWidget,
        Int: widgets.IntTextWidget,
        Float: widgets.FloatTextWidget,
        Enum: widgets.DropdownWidget,
     })


    def __init__(self, cls, varname = None, default_values = None,
                 container_widget = None, widget_fields = None,
                 hidden_fields = None, varname_map = None,
                 create_handler = None):
        self.varname = varname
        self.cls = cls
        if default_values is None:
            self.default_values = {}
        else:
            self.default_values = default_values

        if container_widget is not None:
            self.container_widget = container_widget
        if widget_fields is not None:
            self.widget_fields = widget_fields
        if hidden_fields is not None:
            self.hidden_fields = hidden_fields
        if varname_map is not None:
            self.varname_map = varname_map
        self.create_handler = create_handler

    def get_widget(self, name, trait):
        if name in self.default_values:
            value = self.default_values[name]
        elif name == self.varname_map:
            value = self.varname
        else:
            value = trait.get_default_value()
        description = name.title().replace("_" ," " ).title()
        kw = dict(description = description, value = value)
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
        elif (isinstance(trait, List) and trait._trait):
            if isinstance(trait._trait, Instance):
                trait._trait._resolve_classes()
            if issubclass(trait._trait.klass, HasTraits):
                widget = ListWidget(trait._trait.klass, **kw)
        else:
            widget = self.widget_mapping[type(trait)](**kw)
        return widget

    def class_widget(self, default_values = None):
        if _e:
            raise e
        if default_values is None:
            default_values = self.default_values
        cont = self.container()
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
            w = self.get_widget(name, trait)
            if w is None: continue
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

    def new_object(self):
        values = self.read_form()
        obj = self.cls(**values)
        return obj
    
    def object_to_namespace(self, obj):
        shell = InteractiveShell.instance()
        shell.push({self.varname:obj})
        
    def on_new_object(self):
        obj = self.new_object()
        if self.create_handler:
            self.create_handler(obj)
        else:
            self.object_to_namespace(obj)

    def container(self):
        return self.container_widget()

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
        handler = lambda button: self.on_new_object()
        def handler(button):
            return self.on_new_object()
       
        button.on_click(handler)
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



def create_object(varname, cls, default_values = None, **kwargs):
    if _e:
        raise _e
    if hasattr(cls, "WidgetRepresentation"):
        cm = cls.WidgetRepresentation(cls, varname, default_values, **kwargs)
    else:
        cm = WidgetRepresentation(cls, varname, default_values, **kwargs)
    cm.create_object()

def edit_object(obj, **kwargs):
    if _e:
        raise _e
    cls = obj.__class__
    if hasattr(cls, "WidgetRepresentation"):
        cm = cls.WidgetRepresentation(cls, **kwargs)
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
