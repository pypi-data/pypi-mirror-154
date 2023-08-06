import warnings

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

import tensorflow as tf


class EstimatorWrapper(object):
    def __init__(self, model_path: str, tf_version: str = "v1"):
        self.estimator = self.load_model(model_path, tf_version)
        self.model_path = model_path
        self.tf_version = tf_version

    def __getstate__(self):
        return (self.model_path, self.tf_version)

    def __setstate__(self, model_path: str, tf_version: str):
        self.estimator = self.load_model(model_path, tf_version)
        self.model_path = model_path
        self.tf_version = tf_version

    def load_model(self, model_path: str, tf_version: str):
        if tf_version == "v1":
            return tf.contrib.predictor.from_saved_model(model_path)
        else:
            return tf.saved_model.load(model_path)
