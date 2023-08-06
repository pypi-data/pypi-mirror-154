from types import SimpleNamespace


class Store:

  def __init__(self):
    self.storage = SimpleNamespace()

  def put(self, prop, value):
    setattr(self.storage, prop, value)

  def get(self, prop):
    return getattr(self.storage, prop)
