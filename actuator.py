from collections import defaultdict
import inspect
import six
import warnings
from importlib import import_module
from importlib import reload
from pkgutil import iter_modules

def walk_modules(path):
    mods = []
    mod = import_module(path)
    reload(mod)
    mods.append(mod)
    if hasattr(mod, '__path__'):
        for _, subpath, ispkg in iter_modules(mod.__path__):
            fullpath = path + '.' + subpath
            if ispkg:
                mods += walk_modules(fullpath)
            else:
                submod = import_module(fullpath)
                reload(submod)
                mods.append(submod)
    return mods

def iter_spider_classes(module):
    from asyncio_config.manager import Manager
    for obj in six.itervalues(vars(module)):
        if inspect.isclass(obj) and issubclass(obj, Manager) and obj.__module__ == module.__name__ and  getattr(obj, 'name', None):
            yield obj

class LoadSpiders():
    def __init__(self):
        self._spiders = {}
        self._found = defaultdict(list)
        self.spider_modules = ['spider']
        self. _load_all_spiders()

    def _check_name_duplicates(self):
        dupes = ["\n".join("  {cls} named {name!r} (in {module})".format(
                                module=mod, cls=cls, name=name)
                           for (mod, cls) in locations)
                 for name, locations in self._found.items()
                 if len(locations)>1]
        if dupes:
            msg = ("There are several spiders with the same name:\n\n"
                   "{}\n\n  This can cause unexpected behavior.".format(
                        "\n\n".join(dupes)))
            warnings.warn(msg, UserWarning)

    def _load_spiders(self, module):
        for spcls in iter_spider_classes(module):
            self._found[spcls.name].append((module.__name__, spcls.__name__))
            self._spiders[spcls.name] = spcls

    def _load_all_spiders(self):
        for name in self.spider_modules:
            try:
                for module in walk_modules(name):
                    self._load_spiders(module)
            except ImportError as e:
                    raise
        self._check_name_duplicates()

