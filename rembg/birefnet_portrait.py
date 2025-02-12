from .import BiRefNetSessionGeneral


class BiRefNetSessionPortrait(BiRefNetSessionGeneral):
    @classmethod
    def model_source(cls):
        return "https://github.com/danielgatis/rembg/releases/download/v0.0.0/BiRefNet-portrait-epoch_150.onnx"

    @classmethod
    def name(cls):
        return "birefnet-portrait"