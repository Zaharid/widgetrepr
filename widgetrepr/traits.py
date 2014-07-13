# -*- coding: utf-8 -*-
"""
Created on Wed May 14 23:43:46 2014

@author: zah
"""

from IPython.utils import traitlets
from IPython.core.interactiveshell import InteractiveShell

class ExecutableTrait(traitlets.CUnicode):
    allow_none = True
    default_value = None
    
    def __init__(self, local_ns=None, global_ns=None, default_value=None, **metadata):
        if local_ns is None and global_ns is None:
            try:
                #Avoid creating a new interactiveshell instance
                __IPYTHON__
            except NameError:
                local_ns = globals()
                global_ns = globals()
            else:
                shell = InteractiveShell.instance()
                local_ns = shell.user_ns
                global_ns = shell.user_global_ns
        self.locals = local_ns
        self.globals = global_ns
        super(ExecutableTrait,self).__init__(default_value, **metadata)

    def eval_value(self, value):
        """Print the local variables in the caller's frame."""
        if value == "" or value is None:
            return None            
        try:
            pyvalue = eval(value, self.globals, self.locals)
        except:
            self.error(None, value)

        return pyvalue
            
            
    def info(self):
        return "Evaluable string in the excution context."