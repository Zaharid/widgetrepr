Widgetrepr
===========

A widget representation of IPython HasTraits objects. It allows to create and
edit such objects with a graphical form from the IPython notebook interface.


Features
--------
* Allows to add a new variable to the IPython notebook namespace from the
object created in the form.

* Lists composed of other HasTraits instances allow to create a new element 
and edit and delete the existing ones.

* Existing objects can also be edited with the graphical interface.

* Any class can implement a WidgetRepresentation class to customize the way 
it will be displayed.

* Interfaces with the [mongotraits](https://github.com/Zaharid/mongotraits) 
package to provide a graphical editor to MongoDB enabled objects. 

Dependencies
------------

* [IPython Notebook](http://ipython.org/)


Install
-------

Download the package and run `python  setup.py install`.
