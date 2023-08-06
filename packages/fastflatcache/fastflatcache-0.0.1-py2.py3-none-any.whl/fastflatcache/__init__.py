'''fast flat cache framework'''

__version__ = '0.0.1'


class __App:
    from .app import app


Cache = __App.app._Cache
