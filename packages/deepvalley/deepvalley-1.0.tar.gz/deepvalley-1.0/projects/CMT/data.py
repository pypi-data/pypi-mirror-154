# -*- coding : utf-8 -*-
# @Time   : 2021/10/7 23:19
# @Author : goodli
# @File   : aiac.py
# @Project: Valley 山谷

import os
import zipfile
import numpy as np
import pickle
from io import BytesIO
import glob
import random
import pandas as pd

from transformers import AutoTokenizer
from yacs.config import CfgNode
from torch.utils.data import Dataset

from valley.config import configurable
from valley.utils.plugin import  PluginType, reg_plugin


@reg_plugin(PluginType.DATASET, "AIAC_TRAIN")
class AIAC(Dataset):
    @configurable
    def __init__(self, cfg: CfgNode):
        self.cfg = cfg
        self.data_root = cfg.DATA.DATASET.data_root
        self.bert_path = cfg.DATA.DATASET.bert_path

        self.max_video_len = cfg.DATA.DATASET.max_video_len
        self.max_title_len = cfg.DATA.DATASET.max_title_len
        self.max_asr_len = cfg.DATA.DATASET.max_asr_len

        #f = open(os.path.join(self.data_root) + 'pairwise.tsv')
        self.data = []

        label_f = pd.read_csv(os.path.join(self.data_root, "pairwise.tsv"), sep='\t', header=None, dtype={0:str, 1:str})

        label = label_f.values

        for i in range(len(label)):
            self.data.append((label[i][0], label[i][1], label[i][2]))

        self.tokenizer = AutoTokenizer.from_pretrained(self.bert_path)
        tag_cat_map = pickle.load(open(os.path.join(self.data_root, 'tag_cat_map.pkl', 'rb')))
        self.tag_map = tag_cat_map['tag']
        self.cat_map = tag_cat_map['cat']
        self.tag_num = len(self.tag_map)
        self.cat_num = len(self.cat_map)

        self.handle = zipfile.ZipFile(os.path.join(self.data_root, 'pairwise.zip'))

    def __len__(self):
        return len(self.data)

    def read_npy(self, id):
        # npy = np.load('data/pairwise/%s.npy'%id, allow_pickle=True).item()
        npy = np.load(BytesIO(self.handle.read(id + '.npy')), allow_pickle=True).item()

        _frame_feature = npy['frame_feature']
        _frame_feature = np.stack(_frame_feature).astype(np.float32)  # len dim

        _frame_len, _frame_dim = _frame_feature.shape

        _title = npy['title']
        _asr = npy['asr_text']

        ### pad feature ###
        ### dataset max len = 32
        frame_feature = np.zeros((self.max_video_len, _frame_feature.shape[1]), dtype=np.float32)
        frame_mask = np.zeros((self.max_video_len), dtype=np.int32)
        frame_feature[:_frame_len] = _frame_feature
        frame_mask[:_frame_len] = 1
        ###

        ### pad title
        _title = self.tokenizer.encode(_title)
        title = np.zeros((self.max_title_len,), dtype=np.int32)
        title_mask = np.zeros((self.max_title_len,), dtype=np.int32)
        title_tot = len(_title)
        if title_tot >= self.max_title_len:
            title[:] = _title[:self.max_title_len]
            title_mask[:] = 1
        else:
            title[:title_tot] = _title[:]
            title_mask[:title_tot] = 1
        ###

        ### pad asr
        _asr = self.tokenizer.encode(_asr)
        asr = np.zeros((self.max_asr_len,), dtype=np.int32)
        asr_mask = np.zeros((self.max_asr_len,), dtype=np.int32)
        asr_tot = len(_asr)
        if asr_tot >= self.max_asr_len:
            asr[:] = _asr[:self.max_asr_len]
            asr_mask[:] = 1
        else:
            asr[:asr_tot] = _asr[:]
            asr_mask[:asr_tot] = 1
        ###

        tag = np.zeros((self.tag_num,), dtype=np.float32)
        cat = self.cat_map[npy['category_id'][0]]
        for t in npy['tag_id']:
            tag[self.tag_map[t]] = 1
        return frame_feature, frame_mask, title, title_mask, asr, asr_mask, tag, cat

    def __getitem__(self, idx):
        id1, id2, score = self.data[idx]

        data1 = self.read_npy(id1)
        data2 = self.read_npy(id2)

        return data1 + data2 + (score,)


@reg_plugin(PluginType.DATASET, "AIAC_VALID")
class AIAC_valid(Dataset):
    def __init__(self, cfg, bert_path):
        self.cfg = cfg
        self.data_root = cfg.DATA.DATASET.valid.data_root
        self.bert_path = cfg.DATA.DATASET.valid.bert_path

        self.max_video_len = cfg.DATA.DATASET.valid.max_video_len
        self.max_title_len = cfg.DATA.DATASET.valid.max_title_len
        self.max_asr_len = cfg.DATA.DATASET.valid.max_asr_len

        # names = glob.glob("data/test_a/*.npy")
        self.handle = zipfile.ZipFile(os.path.join(self.data_root, 'test_a.zip'))
        names = self.handle.namelist()
        self.data = []
        for n in names:
            if n.endswith('.npy'):
                id = n.split('/')[-1].replace('.npy', '')
                self.data.append(id)
        self.tokenizer = AutoTokenizer.from_pretrained(bert_path)

    def __len__(self):
        return len(self.data)

    def read_npy(self, id):
        # npy = np.load('data/test_a/%s.npy'%id, allow_pickle=True).item()
        npy = np.load(BytesIO(self.handle.read(id + '.npy')), allow_pickle=True).item()

        _frame_feature = npy['frame_feature']
        _frame_feature = np.stack(_frame_feature)
        _title = npy['title']
        _asr = npy['asr_text']

        ### pad feature ###
        ### dataset max len = 32
        frame_feature = np.zeros((self.max_video_len, _frame_feature.shape[1]), dtype=np.float32)
        frame_mask = np.zeros((self.max_video_len), dtype=np.int32)
        frame_tot = _frame_feature.shape[0]
        frame_feature[:frame_tot] = _frame_feature
        frame_mask[:frame_tot] = 1
        ###

        ### pad title
        # _title = self.tokenizer.encode(_title)
        _title = self.tokenizer.encode(_title)
        title = np.zeros((self.max_title_len,), dtype=np.int32)
        title_mask = np.zeros((self.max_title_len,), dtype=np.int32)
        title_tot = len(_title)
        if title_tot >= self.max_title_len:
            title[:] = _title[:self.max_title_len]
            title_mask[:] = 1
        else:
            title[:title_tot] = _title[:]
            title_mask[:title_tot] = 1
        ###

        ### pad asr
        _asr = self.tokenizer.encode(_asr)
        asr = np.zeros((self.max_asr_len,), dtype=np.int32)
        asr_mask = np.zeros((self.max_asr_len,), dtype=np.int32)
        asr_tot = len(_asr)
        if asr_tot >= self.max_asr_len:
            asr[:] = _asr[:self.max_asr_len]
            asr_mask[:] = 1
        else:
            asr[:asr_tot] = _asr[:]
            asr_mask[:asr_tot] = 1
        ###
        return frame_feature, frame_mask, title, title_mask, asr, asr_mask

    def __getitem__(self, idx):
        id = self.data[idx]
        data = self.read_npy(id)
        return (int(id),) + data


@reg_plugin(PluginType.DATASET, "AIAC_PRETRAIN")
class AIAC_pretrain(Dataset):

    def __init__(self, cfg):
        self.cfg = cfg
        self.data_root = cfg.DATASET.TRAIN.DATA_ROOT
        self.bert_path = cfg.MODEL.BERT_PATH

        self.max_video_len = cfg.DATASET.TRAIN.MAX_VIDEO_LEN  # max_video_len
        self.max_title_len = cfg.DATASET.TRAIN.MAX_TITLE_LEN  # max_title_len
        self.max_asr_len   = cfg.DATASET.TRAIN.MAX_ASR_LEN    # max_asr_len

        self.data = []
        names = glob.glob(self.data_root + "/pretrain_*.zip")
   
        self.handles = {}
        for zipname in names:
            handle = zipfile.ZipFile(zipname, 'r')
            self.handles[zipname] = handle
            namelist = handle.namelist()
            for n in namelist:
                self.data.append((zipname, n))

        tag_cat_map = pickle.load(open(os.path.join(self.data_root, 'tag_cat_map.pkl'), 'rb'))
        self.tag_map = tag_cat_map['tag']
        self.cat_map = tag_cat_map['cat']
        self.tag_num = len(self.tag_map)
        self.cat_num = len(self.cat_map)

        self.tokenizer = AutoTokenizer.from_pretrained(self.bert_path)

    def __len__(self):
        return len(self.data)

    def read_npy(self, zipname, id):

        npy = np.load(BytesIO(self.handles[zipname].read(id)), allow_pickle=True).item()

        _frame_feature = npy['frame_feature']
        _frame_feature = np.stack(_frame_feature).astype(np.float32)  # len dim

        # random flip
        if random.randint(0, 1) == 1:
            _frame_feature = _frame_feature[::-1, :]
        ###

        _title = npy['title']
        _asr = npy['asr_text']

        ### pad feature ###
        ### dataset max len = 32
        frame_feature = np.zeros((self.max_video_len, _frame_feature.shape[1]), dtype=np.float32)
        frame_mask = np.zeros(self.max_video_len, dtype=np.int32)
        frame_tot = _frame_feature.shape[0]
        frame_feature[:frame_tot] = _frame_feature
        frame_mask[:frame_tot] = 1

        ###

        ### pad title
        _title = self.tokenizer.encode(_title)
        title = np.zeros((self.max_title_len,), dtype=np.int32)
        title_mask = np.zeros((self.max_title_len,), dtype=np.int32)
        title_tot = len(_title)
        if title_tot >= self.max_title_len:
            title[:] = _title[:self.max_title_len]
            title_mask[:] = 1
        else:
            title[:title_tot] = _title[:]
            title_mask[:title_tot] = 1
        ###

        ### pad asr
        _asr = self.tokenizer.encode(_asr)
        asr = np.zeros((self.max_asr_len,), dtype=np.int32)
        asr_mask = np.zeros((self.max_asr_len,), dtype=np.int32)
        asr_tot = len(_asr)
        if asr_tot >= self.max_asr_len:
            asr[:] = _asr[:self.max_asr_len]
            asr_mask[:] = 1
        else:
            asr[:asr_tot] = _asr[:]
            asr_mask[:asr_tot] = 1
        ###

        tag = np.zeros((self.tag_num,), dtype=np.float32)
        cat = self.cat_map[npy['category_id'][0]] if npy['category_id'][0] in self.cat_map else self.cat_num - 1
        for t in npy['tag_id']:
            if t in self.tag_map:
                tag[self.tag_map[t]] = 1

        return (frame_feature, frame_mask, title, title_mask, asr, asr_mask, tag, cat)

        """
        return {
                    "frame_feature": frame_feature, 
                    "frame_mask": frame_mask, 
                    "title": title, 
                    "title_mask": title_mask, 
                    "asr": asr, 
                    "asr_mask": asr_mask, 
                    "tag": tag, 
                    "cat": cat
                }
        """

    def __getitem__(self, idx):
        zipname, id = self.data[idx]

        frame_feat, frame_mask, title, title_mask, asr, asr_mask, tag, cat = self.read_npy(zipname, id)

        return {
                    "frame_feat": frame_feat, 
                    "frame_mask": frame_mask, 
                    "title": title, 
                    "title_mask": title_mask, 
                    "asr": asr, 
                    "asr_mask": asr_mask, 
                    "tag": tag, 
                    "cat": cat
                }

        