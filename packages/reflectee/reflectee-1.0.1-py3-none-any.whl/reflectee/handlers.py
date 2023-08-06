import inspect
import os
import sys
from importlib import import_module
from pathlib import Path

__all__ = ["handlers", "register", "loads"]

handlers = {}

API_PATH = os.environ.get(
    "REFLECTEE_API_PATH", os.environ.get("API_PATH", "api")
)


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def loads(api_path):
    global API_PATH
    API_PATH = api_path
    for path in Path(api_path).rglob("*.py"):
        event = str(path)[len(api_path) + 1 : -3]
        module_name = str(path).replace("/", ".")[0:-3]
        handler = cached_import(module_name, "handle")
        if handler:
            _register(event, handler)


def _register(event: str, handler):

    if event not in handlers:
        handlers[event] = handler
        print(bcolors.OKGREEN + f"[{event}] registered !" + bcolors.ENDC)
    else:
        raise Exception(f"{event} already registered")


def register(event: str | None = None):
    def wrapper(handler):
        if not event:
            frame = inspect.stack()[1]
            module = inspect.getmodule(frame[0])
            filename = module.__file__
            event2 = str(filename).split(API_PATH, 1)[-1][:-3].strip("/")
            _register(event2, handler)
        else:
            _register(event, handler)
        return handler

    return wrapper


def cached_import(module_path, class_name):
    modules = sys.modules
    if module_path not in modules or (
        # Module is not fully initialized.
        getattr(modules[module_path], "__spec__", None) is not None
        and getattr(modules[module_path].__spec__, "_initializing", False)
        is True
    ):
        import_module(module_path)
    return getattr(modules[module_path], class_name, None)
