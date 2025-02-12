from .import BiRefNetSessionGeneral


class BiRefNetSessionMassive(BiRefNetSessionGeneral):
    @classmethod
    def model_source(cls):
        return "https://github.com/danielgatis/rembg/releases/download/v0.0.0/BiRefNet-massive-TR_DIS5K_TR_TEs-epoch_420.onnx"

    @classmethod
    def name(cls):
        return "birefnet-massive"