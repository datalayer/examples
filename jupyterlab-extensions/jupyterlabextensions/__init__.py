
import json
import os.path as osp

from ._version import __version__
from .app import JlabExtensions
from .kernel_memory import KernelMemoryUsage

HERE = osp.abspath(osp.dirname(__file__))


with open(osp.join(HERE, 'labextension', 'package.json')) as fid:
    data = json.load(fid)


def _jupyter_labextension_paths():
    return [{
        'src': 'labextension',
        'dest': data['name']
    }]

def _jupyter_server_extension_paths():
    return [{
        "module": "jupyterlabextensions.app",
        "app": JlabExtensions
    }]
