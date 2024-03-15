from keras.models import Sequential, load_model
from keras.layers import Flatten
from keras.applications import VGG16
from sklearn.decomposition import PCA
from PIL import Image
import numpy as np
import pickle

breed_map = {
    0: 'scottish_deerhound',
    1: 'saluki',
    2: 'yorkshire_terrier',
    3: 'kerry_blue_terrier',
    4: 'borzoi',
    5: 'australian_terrier',
    6: 'sealyham_terrier',
    7: 'labrador_retriever',
    8: 'haired_fox_terrier',
    9: 'bull_mastiff',
    10: 'norwegian_elkhound',
    11: 'komondor',
    12: 'american_staffordshire_terrier',
    13: 'shetland_sheepdog',
    14: 'west_highland_white_terrier',
    15: 'basset',
    16: 'sussex_spaniel',
    17: 'english_setter',
    18: 'standard_poodle',
    19: 'african_hunting_dog',
    20: 'haired_pointer',
    21: 'groenendael',
    22: 'bloodhound',
    23: 'weimaraner',
    24: 'mexican_hairless',
    25: 'boston_bull',
    26: 'cardigan',
    27: 'bluetick',
    28: 'lhasa',
    29: 'basenji',
    30: 'irish_setter',
    31: 'clumber',
    32: 'doberman',
    33: 'malamute',
    34: 'keeshond',
    35: 'eskimo_dog',
    36: 'great_pyrenees',
    37: 'newfoundland',
    38: 'bouvier_des_flandres',
    39: 'toy_poodle',
    40: 'ibizan_hound',
    41: 'rhodesian_ridgeback',
    42: 'irish_wolfhound',
    43: 'dandie_dinmont',
    44: 'scotch_terrier',
    45: 'samoyed',
    46: 'vizsla',
    47: 'pomeranian',
    48: 'appenzeller',
    49: 'coated_retriever',
    50: 'collie',
    51: 'irish_terrier',
    52: 'welsh_springer_spaniel',
    53: 'coated_wheaten_terrier',
    54: 'leonberg',
    55: 'greater_swiss_mountain_dog',
    56: 'norwich_terrier',
    57: 'lakeland_terrier',
    58: 'miniature_schnauzer',
    59: 'entlebucher',
    60: 'bernese_mountain_dog',
    61: 'english_springer',
    62: 'malinois',
    63: 'tzu',
    64: 'afghan_hound',
    65: 'pekinese',
    66: 'staffordshire_bullterrier',
    67: 'blenheim_spaniel',
    68: 'otterhound',
    69: 'toy_terrier',
    70: 'cairn',
    71: 'pug',
    72: 'english_foxhound',
    73: 'affenpinscher',
    74: 'redbone',
    75: 'miniature_pinscher',
    76: 'saint_bernard',
    77: 'french_bulldog',
    78: 'siberian_husky',
    79: 'old_english_sheepdog',
    80: 'gordon_setter',
    81: 'dhole',
    82: 'irish_water_spaniel',
    83: 'rottweiler',
    84: 'giant_schnauzer',
    85: 'border_terrier',
    86: 'border_collie',
    87: 'beagle',
    88: 'cocker_spaniel',
    89: 'tan_coonhound',
    90: 'standard_schnauzer',
    91: 'silky_terrier',
    92: 'brittany_spaniel',
    93: 'boxer',
    94: 'chihuahua',
    95: 'norfolk_terrier',
    96: 'golden_retriever',
    97: 'kelpie',
    98: 'maltese_dog',
    99: 'brabancon_griffon',
    100: 'tibetan_terrier',
    101: 'tibetan_mastiff',
    102: 'japanese_spaniel',
    103: 'walker_hound',
    104: 'great_dane',
    105: 'miniature_poodle',
    106: 'italian_greyhound',
    107: 'airedale',
    108: 'chesapeake_bay_retriever',
    109: 'chow',
    110: 'bedlington_terrier',
    111: 'whippet',
    112: 'briard',
    113: 'pembroke',
    114: 'dingo',
    115: 'papillon',
    116: 'schipperke',
    117: 'german_shepherd',
    118: 'kuvasz',
}

class MLModel:
    def __init__(self):
        with open('pca.pkl', 'rb') as f:
            self.pca = pickle.load(f)

        self.loaded_model = load_model('FFNN_dump.h5')

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
        return self.feature_extraction_model.predict(np.expand_dims(img, axis = 0))

    def predict(self, img: Image.Image) -> str:
        features = self.get_features(img)
        features = self.pca.transform(features)
        
        y_pred_opt = self.loaded_model.predict(features)
        y_pred_classes = np.argmax(y_pred_opt, axis=1)

        return breed_map[y_pred_classes[0]]