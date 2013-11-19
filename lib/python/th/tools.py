import simplejson
import os.path

import locale
locale.setlocale(locale.LC_ALL, 'en_US.utf8')


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
        os.makedirs(parent, mode=0o644)


def pdg_round(ve):  # noqa
    value = ve[0]
    error = ve[1]
    """Given a value and an error, round and format them according to the PDG
    rules for significant digits
    """
    def threeDigits(value):
        "extract the three most significant digits and return them as an int"
        return int(("%.2e" % float(error)).split('e')[0].replace('.', '')
                   .replace('+', '').replace('-', ''))

    def nSignificantDigits(threeDigits):
        assert (threeDigits < 1000,
                "three digits (%d) cannot be larger than 10^3" % threeDigits)
        if threeDigits < 101:
            return 2  # not sure
        elif threeDigits < 356:
            return 2
        elif threeDigits < 950:
            return 1
        else:
            return 2

    def frexp10(value):
        "convert to mantissa+exp representation (same as frex, but in base 10)"
        valueStr = ("%e" % float(value)).split('e')
        return float(valueStr[0]), int(valueStr[1])

    def nDigitsValue(expVal, expErr, nDigitsErr):
        """
        compute the number of digits we want for the value, assuming we
        keep nDigitsErr for the error
        """
        return expVal - expErr + nDigitsErr

    def formatValue(value, exponent, nDigits, extraRound=0):
        """
        Format the value; extraRound is meant for the special case
        of threeDigits>950
        """
        roundAt = nDigits - 1 - exponent - extraRound
        nDec = roundAt if exponent < nDigits else 0
        if nDec < 0:
            nDec = 0
        grouping = value > 9999
        return locale.format('%.' + str(nDec) + 'f', round(value, roundAt),
                             grouping=grouping)

    tD = threeDigits(error)
    nD = nSignificantDigits(tD)
    expVal, expErr = frexp10(value)[1], frexp10(error)[1]
    extraRound = 1 if tD >= 950 else 0
    return (
        formatValue(value, expVal, nDigitsValue(
            expVal, expErr, nD), extraRound),
        formatValue(error, expErr, nD, extraRound))
