
from functools import partial
import shelve
import os.path

from th import tmpl


def get_flat_rows(groups):
    rows, flat_groups = [], []
    vspace = 0
    for group in groups:
        vspace += len(group)
        flat_groups.append(vspace)
        rows += group
    return rows, flat_groups


def get_title(field):
    if isinstance(field, str):
        return field
    return field["title"]


def get_scale(field):
    if isinstance(field, str):
        return 1
    return field.get("scale", 1)


def render(
    renderer, is_subtable, is_header, is_footer, scale, bins, first, last,
        pt, label, title, fields, rows, groups, values):
    context = {}
    ncols = len(bins)
    context["header?"] = is_header
    context["footer?"] = is_footer
    context["subtable?"] = is_subtable
    context["scale"] = scale
    context["nallcols"] = ncols * 3
    context["cc"] = "c" * (ncols * 3)
    context["first"] = first
    context["last"] = last
    context["pt"] = pt

    context["label"] = label
    context["title"] = title

    context["bins"] = []
    for bin in bins:
        context["bins"].append({
            "first": bin[0],
            "last": bin[1],
        })

    context["cmidrule"] = []
    for col in range(1, ncols + 1):
        context["cmidrule"].append(
            {
                "first": col * 3,
                "last": col * 3 + 1
            })

    lines = []
    for ikey, key in enumerate(rows):
        field = fields[key]
        line = {
            "field": get_title(field),
            "vspace?": ikey in groups
        }
        str_values = []
        for val in values[key]:
            if val["2011"] == val["2012"]:
                str_values.append({"all": tmpl.latex(
                    val=val["2011"],
                    scale=get_scale(field)
                )})
            else:
                str_values.append(
                    {
                        "2011": tmpl.latex(val=val["2011"],
                                           scale=get_scale(field)),
                        "2012": tmpl.latex(val=val["2012"],
                                           scale=get_scale(field))
                    })
        line["values"] = str_values
        lines.append(line)
    # print context
    context["lines"] = lines

    print(renderer.render_name("fits", context))


def get_db(file_name):
    abs_path = os.path.join(
        os.environ["_TH_ROOT"], "var", "data", file_name)
    return shelve.open(abs_path, "r")


def get_value(db, year, bin, key, ndigits=2):
    bin = tuple(bin)
    if year in db and bin in db[year] and key in db[year][bin]:
        return db[year][bin][key]
    return None


def run(cfg, renderer, name):
    profile = cfg["profiles"][name]
    db = get_db(cfg["dbs"][profile["db"]])
    binning = profile["binning"]
    binspertable = cfg["binspertable"]
    nsubtables = float(len(binning)) / binspertable

    isubtable = -1
    rows, groups = get_flat_rows(profile["groups"])
    render2 = partial(render,
                      renderer=renderer,
                      is_subtable=nsubtables > 1,
                      scale=profile["scale"],
                      label=profile["label"],
                      title=profile["title"],
                      fields=cfg["fields"],
                      rows=rows,
                      groups=groups,
                      pt=profile["pt"]
                      )
    get_value2 = partial(get_value, db=db)

    for ibin, bin in enumerate(binning):
        if ibin % binspertable == 0:
            isubtable += 1

            if isubtable != 0:
                render2(
                    is_header=isubtable == 1,
                    is_footer=False,
                    first=first,   # noqa
                    last=bin[0],   # noqa
                    bins=bins,  # noqa
                    values=values  # noqa

                )

            first = bin[0]   # noqa
            bins = []
            values = {key: [] for key in rows}
        bins.append(bin)
        for key in rows:
            values[key].append(
                {
                    "2011": get_value2(year="2011", bin=bin, key=key),
                    "2012": get_value2(year="2012", bin=bin, key=key)
                }
            )

    render2(
        is_header=isubtable == 0,
        is_footer=True,
        first=first,
        last=bin[1],
        bins=bins,  # noqa
        values=values
    )
