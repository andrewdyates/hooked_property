#!/usr/bin/python2.5
# -*- coding: utf-8 -*-
# Copyright © 2010 Andrew D. Yates
# All Rights Reserved.
"""Hooked Property class for Google App Engine Python Datastore.

I intend Hooked Property to be used in db.polymodel.PolyModel model
hierarchies. For a "Table of Properties" style of properties, see "App
Engine Tycoon (aetycoon)" by Αλκης Ευλογημένος and Nick Johnson.

References:
  http://github.com/Arachnid/aetycoon
  http://blog.notdot.net/2009/9/Custom-Datastore-Properties-1-DerivedProperty
"""

from google.appengine.ext import db


class HookedProperty(db.Property):
  """My Datastore property which hooks to its model to set its value.

  HookedProperty adds model instance logic to properties. This is
  useful because a model instance's property value may depend on the
  values of other properties of that model instance and because
  properties inherited from polymodel ancestors may represent
  different abstractions with despite sharing a data type.

  Hooks are model instance functions which return a value and accept at
  least two arguments: `self` and the value passed to set the property.

  Example 1: Hooked Property

  >>> class Label(polymodel.PolyModel):
  ...   name = HookedProperty(set_hook="set_name")
  ...   aliases = db.StringListProperty()
  ...   def set_name(self, value):
  ...     self.aliases = list(set((value, value.lower())))
  ...     return value

  Example 2: Inherit Property, Override Hook

  >>> class SexLabel(Label):
  ...   def set_name(self, property, value, *args, **kwds):
  ...     value = value.upper()[0]
  ...     if value not in ('M', 'F', 'O',):
  ...       raise ValueError("'%s' cannot be a SexLabel" % value)
  ...     return super(SexLabel, self).set_name(value)
  """
  
  def __init__(self, set_hook=None, *argv, **kwds):
    """Initialize Hooked Property with model instance hook name.

    Example:
      >>> name = HookedProperty(set_hook="set_name")

    Args:
      set_hook: str of decorated model instance function hook name
    """
    super(HookedProperty, self).__init__(*argv, **kwds)
    self._set_hook = set_hook
          
  def __set__(self, model_instance, value):
    """Extend property value assignment with it's decorated model instance hook.

    I do not intend for this method to be called explicitly.

    Args:
      model_instance: `db.Model` decorated by this property instance
      value: original value assigned to this property of arbitrary type
    """
    hook = getattr(model_instance, self._set_hook)
    if hook and value is not None:
      value = hook(value)
    super(HookedProperty, self).__set__(model_instance, value)
