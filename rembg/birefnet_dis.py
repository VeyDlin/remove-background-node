from .import BiRefNetSessionGeneral


class BiRefNetSessionDIS(BiRefNetSessionGeneral):
    @classmethod
    def model_source(cls):
        return "https://github.com/danielgatis/rembg/releases/download/v0.0.0/BiRefNet-DIS-epoch_590.onnx"

    @classmethod
    def name(cls):
        return "birefnet-dis"
