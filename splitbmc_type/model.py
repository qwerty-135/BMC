from torch import nn
from torch.utils.data import Dataset
import torch
import matplotlib.pyplot as plt
from torchvision import datasets, transforms
from torch import nn, optim
from torch.nn import functional as F
from tqdm import tqdm
import os
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import BaggingClassifier,RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
import xgboost as XGB



class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        torch.manual_seed(2)
        self.fc1 = nn.Linear(206, 128)
        self.fc2 = nn.Linear(128, 4)


    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))

        return x


def classifier(model):
    if model == 'LR':
        ML = LogisticRegression
        hypers = {
            'solver': ['newton-cg', 'liblinear','lbfgs', 'saga'],
            'C': [0.0001, 0.001, 0.01],
            'class_weight': [None, 'balanced'],
            'random_state': [42],

        }
    elif model == 'SVM':
        ML = SVC
        hypers = {
            'probability': [True],
            'C': [0.01, 0.1, 1, 10],
            'gamma': [0.001, 0.01, 0.1, 1],
        }
    elif model == 'RF':
        ML = RandomForestClassifier
        hypers = {
            'n_estimators': [10,100,200],
            'max_depth': [None, 10, 50, 100],
            'min_samples_split': [10, 50, 100],
            'random_state': [42],

        }
    elif model == 'XGB':
        ML = XGB
        hypers = {
            'boosting_type': ['gbdt'],
            'n_estimators': [10, 50, 100,200],
            'max_depth': [-1, 10, 50, 100],
            'num_leaves': [2, 5, 10, 50],
            'learning_rate': [0.001, 0.01, 0.1],
            'class_weight': [None, 'balanced'],
            'random_state': [42],

        }
    elif model == 'MLP':
        ML = MLPClassifier
        hypers = {
            'hidden_layer_sizes': [10,50,100,200],
            'solver': ['lbfgs', 'sgd','adam'],
            'learning_rate':['constant', 'adaptive'],
            'random_state': [42],
            'learning_rate_init':[0.01,0.001]
        }
    else:
        raise ValueError('Currently consider LR, SVM, RF, and XGBoost, MLP  only!')
    return ML, hypers

