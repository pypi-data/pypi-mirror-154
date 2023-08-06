import os
import shutil
import logging
from laboro.error import LaboroError


class Workspace:
  """The ``laboro.workspace.Workspace`` object manages the workflow and instances workspaces.

  The workflow workspace is a directory named after the workflow name within the Laboro global temp directory.

  Instances workspaces are a workflow workspace sub-directory named after the workflow session.

  A ``Workspace`` instance is used to store files and data within the workflow execution.

  Arguments:
    workspacedir: A string defining the directory where all workspaces are stored.
    workflow: A string defining the workflow name.
    session: A unique string defining the workflow execution session.

  Returns:
    ``laboro.workspace.Workspace``: The workspace for the workflow session.

  Raises:
    ``laboro.error.LaboroError``: When any error such as *OSError* while creating the workspace occurs.
  """
  def __init__(self, workspacedir, workflow, session):
    try:
      self.workspacepath = os.path.join(workspacedir, workflow, session)
      logging.info(f"  [+] Creating workspace: {self.workspacepath}")
      os.makedirs(self.workspacepath)
    except Exception as err:
      raise LaboroError(f"[{err.__class__.__name__}] {str(err)}") from err

  def delete(self):
    """Deletes the instance workspace and all its content.
    This will **not** delete the workflow workspace.

    Raises:
      ``laboro.error.LaboroError``: When any error such as *OSError* while creating the workspace occurs.
    """
    logging.info(f"  [+] Deleting workspace: {self.workspacepath}")
    try:
      shutil.rmtree(self.workspacepath)
    except Exception as err:
      raise LaboroError(f"[{err.__class__.__name__}] {str(err)}") from err
