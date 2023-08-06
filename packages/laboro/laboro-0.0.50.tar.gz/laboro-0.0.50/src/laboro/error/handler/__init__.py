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
          Handler.handle_error(kind, value)

      with FakeObj() as obj:
        raise Exception("This Exception will be logged as critical and backtracked.")
  """

  @staticmethod
  def handle_error(name, session, kind, value):
    """Log the given error with its traceback and exit with exit code 1."""
    level = logging.INFO
    exit_msg = "Exited"
    exit_code = 0
    if kind == SystemExit:
      if value.code is not None:
        exit_code = value.code
    elif kind is not None:
      level = logging.CRITICAL
      exit_code = f"{kind.__name__}: {value}"
    exit_msg += f" {name} / {session} with {exit_code}"
    logging.getLogger().log_section("WORKFLOW", exit_msg, level=level)
    if kind is not None and kind != SystemExit:
      if logging.getLogger().getEffectiveLevel() <= logging.DEBUG:
        traceback.print_exc()
