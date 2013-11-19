import os
import os.path

import pystache
import pystache.defaults

from th import tools


def get_tmpl_root():
    return os.path.join(
        os.environ["_TH_ROOT"], "share", "note", "tmpl")


def tex_renderer(delimiters=("{*", "*}"), search_dirs=[get_tmpl_root()]):
    pystache.defaults.DELIMITERS = delimiters
    return pystache.Renderer(escape=lambda u: u,
                             search_dirs=search_dirs,
                             file_extension="tex")


def latex(val, ndigits=2, scale=1):
    if val is None:
        return "---"

    if isinstance(val, tuple) or isinstance(val, list):
        value, error = tools.pdg_round((val[0] * scale, val[1] * scale))
        return "%s $\pm$ %s" % (value, error)
    else:
        fmt = "%%.%df" % ndigits
        return fmt % (val * scale)
