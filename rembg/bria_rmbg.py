from typing import List
import numpy as np
from PIL import Image
from PIL.Image import Image as PILImage
from .base import BaseSession


class BriaRmBgSession(BaseSession):
    def predict(self, img: PILImage) -> List[PILImage]:
        ort_outs = self.inner_session.run(
            None,
            self.normalize(
                img, (0.485, 0.456, 0.406), (0.229, 0.224, 0.225), (1024, 1024)
            ),
        )

        pred = ort_outs[0][:, 0, :, :]

        ma = np.max(pred)
        mi = np.min(pred)

        pred = (pred - mi) / (ma - mi)
        pred = np.squeeze(pred)

        mask = Image.fromarray((pred * 255).astype("uint8"), mode="L")
        mask = mask.resize(img.size, Image.Resampling.LANCZOS)

        return [mask]

    @classmethod
    def model_source(cls):
        return "https://github.com/danielgatis/rembg/releases/download/v0.0.0/bria-rmbg-2.0.onnx"

    @classmethod
    def name(cls):
        return "bria-rmbg"
