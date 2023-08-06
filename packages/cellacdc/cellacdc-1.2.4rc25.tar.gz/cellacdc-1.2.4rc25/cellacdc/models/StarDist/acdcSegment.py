from stardist.models import StarDist2D
from csbdeep.utils import normalize
import numpy as np
import os

from cellacdc import models

class Model:
    def __init__(self, model_name='T_cell'):
        stardist_default_models = models.STARDIST_MODELS
        stardist_path = os.path.dirname(os.path.abspath(__file__))
        T_cell_path = os.path.join(stardist_path, 'model', 'T_cell')
        if not os.path.exists(T_cell_path):
            model_name = stardist_default_models[0]
        # Initialize model
        if model_name in stardist_default_models:
            self.model = StarDist2D.from_pretrained(model_name)
        else:
            script_path = os.path.abspath(__file__)
            stardist_path = os.path.dirname(script_path)
            model_path = os.path.join(stardist_path, 'model')
            self.model = StarDist2D(None, name=model_name, basedir=model_path)

    def segment(self, image, prob_thresh=0.0, nms_thresh=0.0):
        # Preprocess image
        prob_thresh = prob_thresh if prob_thresh > 0 else None
        nms_thresh = nms_thresh if nms_thresh > 0 else None
        lab, _ = self.model.predict_instances(
            normalize(image),
            prob_thresh=prob_thresh,
            nms_thresh=nms_thresh
        )
        return lab.astype(np.uint16)
