import sys
import logging
import traceback


class Handler:
  """The ``laboro.error.handler.Handler`` is a singleton that logs every errors given to its ``handle_error()`` method as critical then exit with code 1.

  This object is useful with object with runtime context.

  ..  code-block:: python

      from laboro.error.handler import Handler

      class FakeObj:
        def __enter__(self):
          pass

        def __exit__(self, kind, value, trace):
          Handler.handle_error(kind, value, trace)

      with FakeObj() as obj:
        raise Exception("This Exception will be logged as critical and backtracked.")
  """

  @staticmethod
  def handle_error(kind, value, trace):
    """Log the given error with its traceback and exit with exit code 1."""
    if kind is not None:
      logging.critical(f"[{kind.__name__}]: {str(value)}")
      if logging.getLogger().getEffectiveLevel() <= logging.DEBUG:
        traceback.print_tb(trace)
      if kind != SystemExit:
        sys.exit(1)
