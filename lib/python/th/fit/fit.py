import ROOT
import AnalysisPython.PyRoUts as RU
from th.fit.selector import Selector
from th import tools


class Fit(object):

    def __init__(self, model, tuples, field, cut, nbins,
                 is_unbinned=False, has_splot=False):
        self.model = model
        self.tuples = tuples
        self.cut = cut

        self.is_unbinned = is_unbinned
        self.has_splot = has_splot
        self.nbins = nbins
        self.field = field

        self.data = None

    def process(self):
        self.source()
        self.run()
        return self.model.status

    def run(self):
        if isinstance(self.data, ROOT.TH1D):
            self.model.fitHisto(self.data)
        else:
            self.model.fitTo(self.data)
        return self.model.status

    def dataset(self, selector):
        self.tuples.Process(selector)
        self.data = selector.data

    def histogram(self):
        x1, x2 = self.cut[self.field]
        self.data = RU.h(RU.hID(), RU.hID(), self.nbins, x1, x2)
        self.tuples.Draw('%s >> %s' %
                         (self.field, self.data.GetName()),
                         tools.cut_dict2str(self.cut),
                         "Setw2")

    def source(self):
        print "CUT expr %s" % tools.cut_expr(self.cut)
        if self.is_unbinned:
            if self.has_splot:
                columns = [b.GetName() for b in
                           self.tuples.GetListOfBranches()]
            else:
                columns = [self.field]
            selector = Selector(self.cut, columns=columns)
            self.dataset(selector)
        else:
            self.histogram()

    def __str__(self):
        return str(self.model)
