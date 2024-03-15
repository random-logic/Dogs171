from keras.models import Sequential
from keras.layers import Flatten
from keras.applications import VGG16
from sklearn.decomposition import PCA
from PIL import Image

import numpy as np
import pickle

class Model:
    def __init__(self):
        with open('pca.pkl', 'r') as f:
            self.pca = pickle.load(f)
        with open('FFNN_model.pkl', 'r') as f:
            self.nn = pickle.load(f)

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
        predictions = self.nn.predict(features)

        raise "not done implementing predict"