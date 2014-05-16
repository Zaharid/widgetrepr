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

