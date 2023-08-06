from . import api
from . import config
from . import request
from . import stubgen
from .app import app
from .app import auto_route
from .protocol import CriticalError
from .protocol import WeakError
from .request import setup as setup_client
from .stubgen import enable_stubgen
from .stubgen import generate_stub_files
from .stubgen import watch_directory

# defer init
from . import _safe_exit

__version__ = '0.3.1'
