# -*- coding : utf-8 -*-
# @Time   : 2021/10/7 23:19
# @Author : goodli
# @File   : aiac.py
# @Project: Valley 山谷

import torchvision
from torchvision import datasets, transforms

#from transformers import AutoTokenizer
from yacs.config import CfgNode
from torch.utils.data import Dataset
from valley.utils.plugin import  PluginType, reg_plugin
from valley.config.config import configurable
from valley.data import DataType


@reg_plugin(PluginType.DATASET, "MNIST_train")
class MNIST_train(torchvision.datasets.MNIST):
    @configurable
    def __init__(self, out_image, out_target, *args, **kwargs):
        super(MNIST_train, self).__init__(*args, **kwargs)
        self.out_image  = out_image
        self.out_target = out_target

    @classmethod
    def from_config(cls, cfg):
        return {
            "out_image": "image",
            "out_target": "label",
            "root": cfg.DATASET.TRAIN.DATA_ROOT,
            "train": True,
            "download": True,
            "transform": transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))])
        }

    def __getitem__(self, idx):

        data, target = super().__getitem__(idx)
        
        return {self.out_image: data, self.out_target: target, "idx": idx}


@reg_plugin(PluginType.DATASET, "MNIST_valid")
class MNIST_valid(torchvision.datasets.MNIST):
    @configurable
    def __init__(self, out_image, out_target, *args, **kwargs):
        super(MNIST_valid, self).__init__(*args, **kwargs)
        self.out_image = out_image
        self.out_target = out_target

    @classmethod
    def from_config(cls, cfg):
        return {
            "out_image": "image",
            "out_target": "label",
            "root": cfg.DATASET.TEST.DATA_ROOT,
            "train": False,
            "download": True,
            "transform": transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))])
        }

    def __getitem__(self, idx):
        data, target = super().__getitem__(idx)

        return {self.out_image: data, self.out_target: target}
