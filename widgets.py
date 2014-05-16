# -*- coding: utf-8 -*-
"""
Created on Mon Apr  7 22:24:47 2014

@author: zah
"""
from collections import defaultdict

from IPython.html import widgets
from IPython.utils.traitlets import List,Unicode,Bool,Int,Float,Instance,Any,Type,
from IPython.utils import traitlets


widget_mapping = defaultdict(lambda: widgets.TextWidget, {
     Unicode: widgets.TextWidget,
     Bool: widgets.CheckboxWidget,
     Int: widgets.IntTextWidget,
     Float: widgets.FloatTextWidget,

})

class ListWidget(widgets.ContainerWidget):

    value = List(sync=True)
    description = Unicode(help="Description of the value this widget represents", sync=True)
    title = Unicode(value = 'List', sync=True)
    def __init__(self, *args, **kwargs):
        super(ListWidget, self).__init__(*args, **kwargs)
        self._title_label = widgets.LatexWidget(value = self.title)
        self._item_container = widgets.ContainerWidget()

    def _value_changed(self, name, old, new):
        self.add_items()

    def add_items(self):
        for i,item in enumerate(self.value):
            pass

class ElementWidget(widgets.ContainerWidget):
    lst = List(sync = True)
    index = Any(sync = True)
    value = Any(sync = True)

    _elem_control = Type(widgets.Widget)

    def __init__(self, *args, **kwargs):
        super(ListWidget,self).__init__(*args, **kwargs)
        self._callbacks = widgets.CallbackDispatcher()
        self._elem_widget = self._elem_control(description = self.index)
        traitlets.link((self,'value'),(self._elem_widget,'value'))
        self._del_but = widgets.ButtonWidget()


        children = [
            self._elem_widget()

        ]
