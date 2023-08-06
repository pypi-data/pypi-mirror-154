import os
import time
import uuid
import logging
from laboro.error.handler import Handler as ErrorHandler
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
      exit_code = kind.__name__
    logging.info(f"[+] Workflow ended with code: {exit_code}")
    ErrorHandler().handle_error(kind, value, traceback)
    self.context.logger.remove_file_handler(self.session)

  def run(self):
    """Run the workflow."""
    logging.info(f"  [+] Running workflow: [{self.name}] {self.session}")
    time.sleep(1)
