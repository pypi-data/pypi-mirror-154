import os
import logging
from laboro.error import LaboroError
from laboro.history import History
from laboro.workspace import Workspace
from laboro.context.store import Store
from laboro.config.manager import Manager as ConfigMgr
from laboro.module.manager import Manager as ModuleMgr
from laboro.error.handler import Handler as ErrorHandler


class Context:
  def __init__(self, logger):
    self.logger = logger
    self.store = Store()
    self.history = None
    self.modulemgr = ModuleMgr()
    self.configmgr = ConfigMgr("/etc/laboro/laboro.yml")
    self.workspacedir = self.configmgr.get_parameter("main",
                                                     "$.laboro.workspacedir")
    self.histdir = self.configmgr.get_parameter("main",
                                                "$.laboro.histdir")
    self.workflowdir = self.configmgr.get_parameter("main",
                                                    "$.laboro.workflowdir")
    self.logdir = self.configmgr.get_parameter("main",
                                               "$.laboro.log.dir")
    self.loglevel = self.configmgr.get_parameter("main",
                                                 "$.laboro.log.level")
    self.workspace = None
    logging.getLogger().vault.clear()

  def reset(self, workflow_name, session):
    try:
      logging.getLogger().log_section("WORKFLOW",
                                      f"Started {workflow_name} / {session}")
      logging.getLogger().vault.clear()
      self._configure_logger(workflow_name, session)
      self.set_workflow_config(workflow_name)
      self.workspace = Workspace(workspacedir=self.workspacedir,
                                 workflow=workflow_name,
                                 session=session)
      history_path = os.path.join(self.histdir, f"{workflow_name}.db")
      self.history = History(filename=history_path,
                             workflow=workflow_name,
                             session=session,
                             params=self.configmgr.workflow_config)
      self.history.enter()
      self.install_packages()
      return self
    except Exception as err:
      ErrorHandler().handle_error(workflow_name,
                                  session,
                                  err.__class__,
                                  str(err))

  def exit(self, name, session, kind, value):
    self.workspace.delete()
    self.history.exit(kind, value)
    ErrorHandler().handle_error(name, session, kind, value)
    self.logger.remove_file_handler(session)

  def _configure_logger(self, workflow_name, session):
    self.logger.add_file_handler(self.logdir, workflow_name, session)
    self.logger.set_log_level(self.loglevel)

  def set_workflow_config(self, workflow_name):
    config_file_name = os.path.join(self.workflowdir, f"{workflow_name}.yml")
    logging.info(f"[+] Loading workflow_config: {config_file_name}")
    self.configmgr.workflow_config = config_file_name

  def install_packages(self):
    """Install all packages listed in the workflow configuration file.
    """
    packages = self.configmgr.get_parameter("workflow", "$.packages")
    for pkg in packages:
      self.modulemgr.install_package(pkg)

  def put(self, prop, value):
    self.store.put(prop, value)

  def get(self, prop):
    return self.store.get(prop)

  def _register_class(self, module, cls):
    self.modulemgr.register_class_from_module(cls, module)

  def _register_instance_secrets(self, instance, args):
    if args is not None:
      class_args = instance.specification["args"]
      secret_keys = [arg["name"] for arg in class_args if arg["secret"]]
      secrets = [args[key] for key in args.keys() if key in secret_keys]
      list(map(logging.getLogger().vault.add, secrets))

  def _instantiate(self, module, cls, args):
    logging.info(f"[+] Object instantiation: {module}.{cls}")
    mod = self.modulemgr.get_class_from_module(cls=cls, module=module)
    instance = mod(context=self, args=args)
    self._register_instance_secrets(instance, args)
    return mod(context=self, args=args)

  def instantiate(self, module, cls, args):
    self._register_class(module, cls)
    return self._instantiate(module, cls, args)

  def register_method_secrets(self, instance, method, args):
    if args is not None:
      try:
        method_args = [meth for meth in instance.specification["methods"] if meth["name"] == method][0]["args"]
        secret_keys = [arg["name"] for arg in method_args if arg["secret"]]
        secrets = [args[key] for key in args.keys() if key in secret_keys]
        list(map(logging.getLogger().vault.add, secrets))
      except IndexError as err:
        raise LaboroError(f"UnknownMethodError: Unknown method {instance.__class__.__name__}.{method}") from err
