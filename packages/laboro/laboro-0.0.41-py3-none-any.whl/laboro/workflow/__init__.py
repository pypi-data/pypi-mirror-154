import os
import time
import uuid
import logging
from laboro.history import History
from laboro.workspace import Workspace


class Workflow:
  """The ``laboro.workflow.Workflow`` object is the main class for the workflow representation.
  It load all configuration needed, set alk objects such History, Vault and workspace and run according to its configuration.

  The Workflow object provides a runtime context that will handle log, history, vault, and workspace, etc.

  Arguments:
    name: A string representing the workflow name.
    logger: A laboro.logger.manager.Manager instance.

  Returns:
    ``laboro.workflow.Workflow``: A Workflow object.

  ..  code-block:: python

      from laboro.workflow import Workflow
      from laboro.logger.manager import Manager as LogMgr

      logmgr = LogMgr()
      logmgr.set_default()
      with Workflow(name="my_workflow", logger=logmgr) as wkf:
        wkf.run()
        ...
  """
  def __init__(self, name, context):
    self.name = name
    self.context = context
    self.session = str(uuid.uuid4())
    self.context.configure_logger(self.name, self.session)
    self.context.set_workflow_config(self.name)
    self.history = History(filename=os.path.join(self.context.histdir,
                                                 f"{self.name}.db"),
                           workflow=self.name,
                           session=self.session,
                           params=self.context.configmgr.workflow_config)
    self.workspace = Workspace(workspacedir=self.context.workspacedir,
                               workflow=self.name,
                               session=self.session)

  def __enter__(self):
    logging.getLogger().log_section("WORKFLOW",
                                    f"Started {self.name} / {self.session}")
    self.history.__enter__()
    self.context.install_packages()
    return self

  def __exit__(self, kind, value, traceback):
    self.workspace.delete()
    self.history.__exit__(kind, value, traceback)
    exit_code = 0
    if kind == SystemExit:
      if value.code is not None:
        exit_code = value.code
    elif kind is not None:
      exit_code = f"{kind.__name__}: {value}"
    logging.info(f"[+] Workflow ended with code: {exit_code}")
    self.context.handle_error(kind, value, traceback)
    self.context.logger.remove_file_handler(self.session)

  def _instantiate(self, module, cls, args):
    logging.info(f"[+] Object instantiation: {module}.{cls}")
    return self.context.modulemgr.get_class_from_module(cls=cls,
                                                        module=module)(args=args)

  def run(self):
    """Run the workflow."""
    for step in self.context.configmgr.get_parameter("workflow",
                                                     "$.laboro.workflow.steps"):
      logging.getLogger().log_section("STEP", step['name'])
      module = step["module"]["name"]
      cls_args = step["module"]["args"]
      cls = step["module"]["class"]
      self.context.register_class(module, cls)
      instance = self._instantiate(module, cls, cls_args)
      self.context.register_instance_secrets(instance, cls_args)
      for action in step["module"]["actions"]:
        action_args = action["args"]
        self.context.register_method_secrets(instance,
                                             action["method"],
                                             action_args)
        logging.getLogger().log_section("ACTION",
                                        f"{step['name']} / {action['method']}")
        getattr(instance, action["method"])(**action_args)
        time.sleep(2)
    logging.getLogger().log_section("WORKFLOW", "No more steps to run")
