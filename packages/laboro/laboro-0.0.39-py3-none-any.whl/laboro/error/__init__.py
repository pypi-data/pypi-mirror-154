class LaboroError(Exception):
  """Laboro specific error class.

  Arguments:
    message: A string defining the message to be displayed when error occurs.

  Returns:
    ``laboro.error.LaboroError``: A Laboro Error.

  """
  def __init__(self, message):
    self.message = message
    super().__init__(self.message)
