from .import BiRefNetSessionGeneral


class BiRefNetSessionGeneralLite(BiRefNetSessionGeneral):
    @classmethod
    def model_source(cls):
        return "https://github.com/danielgatis/rembg/releases/download/v0.0.0/BiRefNet-general-bb_swin_v1_tiny-epoch_232.onnx"

    @classmethod
    def name(cls):
        return "birefnet-general-lite"
