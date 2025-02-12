from .import BiRefNetSessionGeneral


class BiRefNetSessionHRSOD(BiRefNetSessionGeneral):
    @classmethod
    def model_source(cls):
        return "https://github.com/danielgatis/rembg/releases/download/v0.0.0/BiRefNet-HRSOD_DHU-epoch_115.onnx"

    @classmethod
    def name(cls):
        return "birefnet-hrsod"