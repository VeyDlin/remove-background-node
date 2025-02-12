from . import BiRefNetSessionGeneral


class BiRefNetSessionCOD(BiRefNetSessionGeneral):
    @classmethod
    def model_source(cls):
        return "https://github.com/danielgatis/rembg/releases/download/v0.0.0/BiRefNet-COD-epoch_125.onnx-cod"

    @classmethod
    def name(cls):
        return "birefnet-cod"
