import os
import os.path

import pystache
import pystache.defaults


def get_tmpl_root():
    return os.path.join(
        os.environ["_TH_ROOT"], "share", "th", "note", "tmpl")


def tex_renderer(delimiters=("{*", "*}"), search_dirs=[get_tmpl_root()]):
    pystache.defaults.DELIMITERS = delimiters
    return pystache.Renderer(escape=lambda u: u,
                             search_dirs=search_dirs,
                             file_extension="tex")
