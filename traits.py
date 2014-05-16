# -*- coding: utf-8 -*-
"""
Created on Wed May 14 23:43:46 2014

@author: zah
"""
import inspect

from IPython.utils import traitlets

class ExecutableTrait(traitlets.TraitType):
    allow_none = True
    default_value = None
    
    def __init__(self, default_value=None, **metadata):
        super(ExecutableTrait,self).__init__(default_value, **metadata)
        
    
    def validate(self, obj, value):
        """Print the local variables in the caller's frame."""
        if value == "":
            return None
            
        #__set__->_validate->validate
        frame = inspect.currentframe().f_back.f_back.f_back
        try:
            pyvalue = eval(value, frame.f_globals, frame.f_locals)
        except:
            self.error(obj, value)

        return pyvalue
            
            
    def info(self):
        return "Evaluable string in the excution context."

class TTest(traitlets.HasTraits):
    x = ExecutableTrait()

x = TTest()
y = 5
x.x= 'y'