# -*- coding: utf-8 -*-
"""
Created on Wed May 14 23:43:46 2014

@author: zah
"""

from IPython.utils import traitlets

class ExecutableTrait(traitlets.Unicode):
    allow_none = True
    default_value = None
    
    def __init__(self, local_ns, global_ns, default_value=None, **metadata):
        self.locals = local_ns
        self.globals = global_ns
        super(ExecutableTrait,self).__init__(default_value, **metadata)
        
    
    def eval_value(self, value):
        """Print the local variables in the caller's frame."""
        if value == "":
            return None            
        try:
            pyvalue = eval(value, self.globals, self.locals)
        except:
            self.error(None, value)

        return pyvalue
            
            
    def info(self):
        return "Evaluable string in the excution context."