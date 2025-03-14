from typing import List
import numpy as np
from PIL import Image
from PIL.Image import Image as PILImage
from scipy.special import log_softmax
from .base import BaseSession

palette1 = [
    0,
    0,
    0,
    255,
    255,
    255,
    0,
    0,
    0,
    0,
    0,
    0,
]

palette2 = [
    0,
    0,
    0,
    0,
    0,
    0,
    255,
    255,
    255,
    0,
    0,
    0,
]

palette3 = [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    255,
    255,
    255,
]


class Unet2ClothSession(BaseSession):
    def predict(self, img: PILImage) -> List[PILImage]:
        ort_outs = self.inner_session.run(
            None,
            self.normalize(
                img, (0.485, 0.456, 0.406), (0.229, 0.224, 0.225), (768, 768)
            ),
        )

        pred = ort_outs
        pred = log_softmax(pred[0], 1)
        pred = np.argmax(pred, axis=1, keepdims=True)
        pred = np.squeeze(pred, 0)
        pred = np.squeeze(pred, 0)

        mask = Image.fromarray(pred.astype("uint8"), mode="L")
        mask = mask.resize(img.size, Image.Resampling.LANCZOS)

        masks = []

        def upper_cloth():
            mask1 = mask.copy()
            mask1.putpalette(palette1)
            mask1 = mask1.convert("RGB").convert("L")
            masks.append(mask1)

        def lower_cloth():
            mask2 = mask.copy()
            mask2.putpalette(palette2)
            mask2 = mask2.convert("RGB").convert("L")
            masks.append(mask2)

        def full_cloth():
            mask3 = mask.copy()
            mask3.putpalette(palette3)
            mask3 = mask3.convert("RGB").convert("L")
            masks.append(mask3)

        upper_cloth()
        lower_cloth()
        full_cloth()

        return masks

    @classmethod
    def model_source(cls):
        return "https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net_cloth_seg.onnx"

    @classmethod
    def name(cls):
        return "u2net_cloth_seg"
