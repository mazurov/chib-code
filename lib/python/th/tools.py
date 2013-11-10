import simplejson
import os.path


def json(file):
    return simplejson.load(open(file, "r"))


def cut_dict2str(fields):
    ret = ""
    prefix = ""
    for field in fields:
        if isinstance(fields[field], tuple) or isinstance(fields[field], list):
            low, high = fields[field]
            if low is not None:
                ret += " %s %s > %.4f" % (prefix, field, low)
                prefix = "&&"
            if high is not None:
                ret += " %s %s < %.4f" % (prefix, field, high)
                prefix = "&&"
        else:
            ret += " %s %s == %.0f" % (prefix, field, fields[field])
            prefix = "&&"
    return ret


def create_path(filename):
    parent = os.path.dirname(filename)
    if not os.path.exists(parent):
        os.makedirs(parent, mode=0644)
