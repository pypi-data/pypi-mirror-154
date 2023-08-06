import logging


class LaboroLogger(logging.Logger):
  """The ``laboro.logger.LaboroLogger`` overrides the ``logging.Logger`` class.

  It adds a ``laboro.vault.Vault`` instance to the logger object allowing secret management.

  Any secret stored in the vault instance will be redacted before logging.
  """

  def __init__(self, name, level=logging.NOTSET):
    self.vault = None
    super(LaboroLogger, self).__init__(name, level)

  def set_vault(self, vault):
    """Set the ``laboro.vault.Vault`` instance used to prevent secrets to be logged."""
    self.vault = vault

  def makeRecord(self, name, level, fn, lno, msg, args, exc_info, func=None, extra=None, sinfo=None):
    """Override logging.Logger.makeRecord.
    """
    msg = self.vault.protect(msg)
    return super(LaboroLogger, self).makeRecord(name, level, fn, lno, msg, args, exc_info, func, extra, sinfo)
