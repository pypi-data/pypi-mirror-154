import os
import logging
from jsonpath import JSONPath
from laboro.error import LaboroError
from laboro.validator import Validator


class Manager:
  """The ``laboro.config.manager.Manager`` object loads all configuration files needed by ``Laboro`` to operate.
  It first loads and checks the main configuration file then loads the workflow configuration file and checks that all parameters comply to each module definition.
  It is used by the ``workflow.manager`` to retrieve any configuration parameter needed by any module used in the workflow.

  Arguments:
    main_config: A string representing the main Laboro configuration filename.

  Returns:
    ``laboro.config.manager.Manager``: The configuration manager.

  Raises:
    ``laboro.error.LaboroError``: When one of the configuration files are not found.
  """

  @property
  def main_config(self):
    """Get the main_config as a dict."""
    return self._main_config

  @property
  def workflow_config(self):
    """Get the workflow_config as a dict."""
    return self._workflow_config

  @main_config.setter
  def main_config(self, filename):
    """Set the main_config from a YAML file.

    Arguments:
      filename: A string specifying the YAML file to load the configuration from."""
    schema = os.path.join(os.path.dirname(__file__),
                          "schema",
                          "main.yml")
    self._main_config = Validator().validate_instance(schema=schema,
                                                      instance=filename)

  @workflow_config.setter
  def workflow_config(self, filename):
    """Set the workflow_config from a YAML file.

    Arguments:
      filename: A string specifying the YAML file to load the configuration from."""
    schema = os.path.join(os.path.dirname(__file__),
                          "schema",
                          "workflow.yml")
    self._workflow_config = Validator().validate_instance(schema=schema,
                                                          instance=filename)

  def __init__(self, main_config):
    self.main_config = main_config
    self._workflow_config = dict()

  def get_parameter(self, level, param):
    """Returns the configuration parameter specified by ``param`` from the configuration ``level``.
    ``level`` is a string defining the configuration parameter level. It must be one of ``main`` or ``workflow``.

    Arguments:
      level: A string that specify the level from which retrieve the parameter.
             ``level`` Must be one of ``main`` or ``workflow``.
      param: A string that specify the parameter name as described by the JSONPath spec.

    Returns:
      Any type, depending on YAML file from which the configuration is generated.

    Raises:
      laboro.error.LaboroError: When the specified parameter is unknown or ``level`` value is not valid.

    ..  code-block:: python

        manager = Manager(main_conf, workflow_conf)
        manager.get_parameter("workflow", "$.laboro.workflow.steps[0].actions[0].input.value")
    """
    levels = {"main": self.main_config,
              "workflow": self.workflow_config}
    try:
      config = levels[level]
      try:
        return JSONPath(param).parse(config)[0]
      except IndexError as err:
        logging.critical(f"UnknownParameter: [{level}]: {param}")
        raise LaboroError(f"UnknownParameter: [{level}]: {param}") from err
    except KeyError as err:
      logging.critical(f"BadConfLevel: Bad configuration level: {level}")
      raise LaboroError(f"BadConfLevel: Bad configuration level: {level}") from err
