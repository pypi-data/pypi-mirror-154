import os
import logging
from laboro.error import LaboroError
from laboro.validator import Validator


class Module:
  def __init__(self, filepath, args=None):
    self.filepath = filepath
    self.args = args
    self.specification = self._validate_spec()
    self._validate_args()

  @staticmethod
  def laboro_method(func):
    def wrapper(self, *args, **kwargs):
      if len(args) > 1:
        logging.error("Using method with args instead of kwargs !")
        logging.warning("No argument checking will be done.")
        func(*args[1:])
      else:
        try:
          method = func.__name__
          methods = self.specification["methods"]
          method = [meth for meth in methods if meth["name"] == method][0]
          Validator().validate_method_args(method, kwargs)
        except IndexError as err:
          raise LaboroError(f"UnknownMethodError: Unknown method: {method}") from err
        func(self, **kwargs)
    return wrapper

  def _validate_spec(self):
    """Load module specification from its YAML data file."""
    base_spec = os.path.join(os.path.dirname(__file__),
                             "schema",
                             "object.yml")
    spec_file = os.path.join(os.path.dirname(self.filepath),
                             "schema",
                             "specification.yml")
    return Validator().validate_instance(schema=base_spec,
                                         instance=spec_file)

  def _validate_args(self):
    """Validate arguments against a specification.
    """
    spec_file = os.path.join(os.path.dirname(self.filepath),
                             "schema",
                             "specification.yml")
    return Validator().validate_obj_args(specification=spec_file,
                                         args=self.args)

  def get_arg_value(self, arg):
    """Get the value of the specified argument.

    Arguments:
      arg: The argument to get the value from.

    Returns:
      The value of the searched argument. The type of the return value depend of the value of the searched argument.

    Raises:
      ``laboro.error.LaboroError``: When the specified argument is not known to the module.
    """
    if arg in self.args:
      return self.args[arg]
    msg = {"type": "UnknownModuleArgError",
           "message": f"Module argument not found: {arg}"}
    raise LaboroError(f"[{msg['type']}] {msg['message']}")

  def get_arg_value_as_string(self, arg):
    """Get the value of the specified argument as a string.

    Arguments:
      arg: The argument to get the value from.

    Returns:
      ``str``: The string representation of value of the searched argument.

    Raises:
      ``laboro.error.LaboroError``: When the specified argument is not known to the module.
    """
    if arg in self.args:
      return str(self.args[arg])
    msg = {"type": "UnknownModuleArgError",
           "message": f"Module argument not found: {arg}"}
    raise LaboroError(f"[{msg['type']}] {msg['message']}")
