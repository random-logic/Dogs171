from keras.models import Sequential
from keras.layers import Flatten
from keras.applications import VGG16
from sklearn.decomposition import PCA
from PIL import Image

import numpy as np
import pickle

class MLModel:
    def __init__(self):
        with open('pca.pkl', 'rb') as f:
            self.pca = pickle.load(f)

        with open('FFNN_model.pkl', 'rb') as f:
            self.loaded_model = pickle.load(f)

        # Load VGG16 model without top layers
        vgg16 = VGG16(weights='imagenet', include_top=True, classifier_activation=None)

        # Freeze the convolutional base
        vgg16.trainable = False

        # Create a new model to extract features
        self.feature_extraction_model = Sequential([
            vgg16,
            Flatten()
        ])

    def get_features(self, img: Image.Image) -> np.array:
        return self.feature_extraction_model.predict(np.expand_dims(img, axis = 0))[0]

    def predict(self, img: Image.Image) -> str:
        features = self.get_features(img)
        features = self.pca.transform(features)
        predictions = self.loaded_model.predict(features)

        raise "not done implementing predict"