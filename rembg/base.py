import os
from typing import Dict, List, Tuple
from pathlib import Path
import numpy as np
import onnxruntime as ort
from PIL import Image
from PIL.Image import Image as PILImage


class BaseSession:
    def __init__(
        self,
        model_name: str,
        model_path: Path
    ):
        self.model_name = model_name

        self.providers = []
        _providers = ort.get_available_providers()
        self.providers.extend(_providers)

        self.inner_session = ort.InferenceSession(
            model_path.resolve().as_posix(),
            providers=self.providers,
            sess_options=ort.SessionOptions(),
        )

    def normalize(
        self,
        img: PILImage,
        mean: Tuple[float, float, float],
        std: Tuple[float, float, float],
        size: Tuple[int, int]
    ) -> Dict[str, np.ndarray]:
        im = img.convert("RGB").resize(size, Image.Resampling.LANCZOS)

        im_ary = np.array(im)
        im_ary = im_ary / np.max(im_ary)

        tmpImg = np.zeros((im_ary.shape[0], im_ary.shape[1], 3))
        tmpImg[:, :, 0] = (im_ary[:, :, 0] - mean[0]) / std[0]
        tmpImg[:, :, 1] = (im_ary[:, :, 1] - mean[1]) / std[1]
        tmpImg[:, :, 2] = (im_ary[:, :, 2] - mean[2]) / std[2]

        tmpImg = tmpImg.transpose((2, 0, 1))

        return {
            self.inner_session.get_inputs()[0]
            .name: np.expand_dims(tmpImg, 0)
            .astype(np.float32)
        }

    def predict(self, img: PILImage) -> List[PILImage]:
        raise NotImplementedError

    @classmethod
    def model_source(cls):
        raise NotImplementedError
    
    @classmethod
    def name(cls):
        raise NotImplementedError
