from th.model.ups import UpsModel


def prepare_model(canvas, name, data, interval, nbins, has_splot):
    m1, m2 = interval
    model = UpsModel(canvas=canvas,
                     data=data,
                     interval=interval,
                     nbins=nbins
                     )
    return model
