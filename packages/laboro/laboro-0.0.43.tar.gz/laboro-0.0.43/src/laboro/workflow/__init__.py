import uuid
import logging


class Workflow:
  """The ``laboro.workflow.Workflow`` object is the main class for the workflow representation.
  It load all configuration needed, set alk objects such History, Vault and workspace and run according to its configuration.

  The Workflow object provides a runtime context that will handle log, history, vault, and workspace, etc.

  Arguments:
    name: A string representing the workflow name.
    context: A ``laboro.context.Context`` instance.

  Returns:
    ``laboro.workflow.Workflow``: A Workflow object.

  ..  code-block:: python

      from laboro.vault import Vault()
      from laboro.log.manager import Manager as LogMgr
      from laboro.context import Context
      from laboro.workflow import Workflow

      logmgr = LogMgr(vault=Vault())
      context = Context(logger=logmgr)
      with Workflow(name="my_workflow", context=context) as wkf:
        wkf.run()
        ...
  """
  def __init__(self, name, context):
    self.name = name
    self.memory = dict()
    self.session = str(uuid.uuid4())
    self.context = context.reset(self.name, self.session)

  def __enter__(self):
    return self

  def __exit__(self, kind, value, traceback):
    exit_msg = "Exiting"
    if value is not None:
      exit_msg += f" with {value}"
    logging.getLogger().log_section("WORKFLOW", exit_msg)
    exit_code = 0
    if kind == SystemExit:
      if value.code is not None:
        exit_code = value.code
    elif kind is not None:
      exit_code = f"{kind.__name__}: {value}"
    self.context.exit(self.session, kind, value, traceback, exit_code)

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
