# -*- coding : utf-8 -*-
# @Time   : 2021/11/15 0:02
# @Author : goodli
# @File   : cmt.py
# @Project: Valley 山谷

import torch
import torch.nn as nn
import torch.nn.functional as F

from transformers import AutoModel, AutoModelForPreTraining, BertConfig, BertModel

from valley.utils.plugin import reg_plugin, PluginType
from valley.config import configurable


@reg_plugin(PluginType.META_ARCHITECTURE, "CMT")
class CMT(nn.Module):

    def __init__(self, cfg):
        
        super(CMT, self).__init__()

        self.cfg = cfg
        self.frame_proj = nn.Sequential(nn.Linear(self.cfg.MODEL.CNN_DIM, self.cfg.MODEL.BERT_DIM), nn.LayerNorm(self.cfg.MODEL.BERT_DIM))
        self.bert = AutoModel.from_pretrained(self.cfg.MODEL.BERT_PATH)
        self.tag_fc = nn.Linear(self.cfg.MODEL.BERT_DIM, self.cfg.MODEL.TAG_NUM)
        self.cat_fc = nn.Linear(self.cfg.MODEL.BERT_DIM, self.cfg.MODEL.CAT_NUM)
        self.proj = nn.Linear(self.MODEL.BERT_DIM * 3, self.MODEL.PROJ_DIM)

    def forward(self, frame, frame_mask, title, title_mask, asr, asr_mask):

        bs = frame.shape[0]
        frame = self.frame_proj(frame)  # bs 32 768

        emb = self.bert.get_input_embeddings()
        title = emb(title)  # bs 32 768
        asr = emb(asr)

        frame_len = frame.shape[1]
        title_len = title.shape[1]
        asr_len = asr.shape[1]

        inputs_embeds = torch.cat([title, asr, frame], dim=1)  # bs 64 768
        attention_mask = torch.cat([title_mask, asr_mask, frame_mask], dim=1)

        token_type_ids = torch.zeros_like(attention_mask)
        token_type_ids[:, title_len + asr_len:] = 1

        outputs = self.bert(inputs_embeds=inputs_embeds,
                            attention_mask=attention_mask,
                            token_type_ids=token_type_ids)[0]

        frame_mask = frame_mask.unsqueeze(2)
        frame_embeds = (outputs[:, title_len + asr_len:] * frame_mask).sum(dim=1) / frame_mask.sum(dim=1)
        cls_embeds = outputs[:, 0]
        text_mask = torch.cat([title_mask, asr_mask], dim=1).unsqueeze(2)
        text_embeds = (outputs[:, :title_len + asr_len] * text_mask).sum(dim=1) / text_mask.sum(dim=1)
        embeds = torch.cat([frame_embeds, cls_embeds, text_embeds], dim=1)

        if self.training:
            pred_tag = self.tag_fc(cls_embeds)
            pred_cat = self.cat_fc(cls_embeds)
            embeds = self.proj(embeds)
            return embeds, pred_tag, pred_cat
        else:
            if self.with_proj:
                embeds = self.proj(embeds)
            return embeds


def pem_cls_loss(pred, gt):
    pmask = (gt > 0.9).float()
    nmask = (gt <= 0.9).float()
    num_positive = torch.sum(pmask)
    num_entries = num_positive + torch.sum(nmask)
    ratio = num_entries / (num_positive + 1e-10)
    coef_0 = 0.5 * ratio / (ratio - 1 + 1e-10)
    coef_1 = 0.5 * ratio
    eps = 1e-5
    loss_pos = coef_1 * torch.log(pred + eps) * pmask
    loss_neg = coef_0 * torch.log(1. - pred + eps) * nmask
    loss = -1 * torch.sum(loss_pos + loss_neg) / (num_entries + eps)
    return loss


@reg_plugin(PluginType.META_ARCHITECTURE, "CMT_PRETRAIN")
class CMTPretrain(nn.Module):

    def __init__(self, cfg):

        super(CMTPretrain, self).__init__()

        self.cfg = cfg
        self.frame_proj = nn.Sequential(nn.Linear(self.cfg.MODEL.CNN_DIM, self.cfg.MODEL.BERT_DIM), nn.LayerNorm(self.cfg.MODEL.BERT_DIM))
        self.bert = AutoModelForPreTraining.from_pretrained(self.cfg.MODEL.BERT_PATH)
    
        if self.cfg.MODEL.MVM:
            self.mvm_fc = nn.Linear(self.cfg.MODEL.BERT_DIM, self.cfg.MODEL.CNN_DIM)
            self.mvm_mask_embed = nn.Embedding(1, self.cfg.MODEL.BERT_DIM)

        if self.cfg.MODEL.VTM:
            self.vtm_fc = nn.Linear(self.cfg.MODEL.BERT_DIM, 2)

        self.tag_fc = nn.Linear(self.cfg.MODEL.BERT_DIM, self.cfg.MODEL.TAG_NUM)
        self.cat_fc = nn.Linear(self.cfg.MODEL.BERT_DIM, self.cfg.MODEL.CAT_NUM)

    def random_text_mask(self, text, prob=0.15, mask_id=103, mask_token_prob=0.8):

        mask_prob = torch.empty(text.shape[0], text.shape[1]).uniform_(0, 1).to(device=text.device)
        mask = (mask_prob < prob).to(dtype=torch.long)

        token_prob = torch.empty(text.shape[0], text.shape[1]).uniform_(0, 1).to(device=text.device)
        mask_token = (token_prob < mask_token_prob).to(dtype=torch.long)

        text = text * (1 - mask) + \
               mask_id * mask * mask_token + \
               text * mask * (1 - mask_token)

        return text, mask

    def random_frame_mask(self, frame, prob=0.15):

        mask_prob = torch.empty(frame.shape[0], frame.shape[1]).uniform_(0, 1).to(device=frame.device)
        mask = (mask_prob < prob).to(dtype=torch.long)
        _mask = mask.unsqueeze(2)
        frame = frame * (1 - _mask) + self.mvm_mask_embed.weight.unsqueeze(0) * _mask

        return frame, mask

    def _forward(self, frame, frame_mask, title, title_mask, asr, asr_mask):

        # frame # bs 32 1536
        if self.cfg.MODEL.MVM:
            frame_proj = self.frame_proj(frame)  # bs 32 768
            masked_frame, mvm_mask = self.random_frame_mask(frame_proj)
        else:
            frame_proj = self.frame_proj(frame)

        emb = self.bert.get_input_embeddings()
        # title # bs 32

        text = torch.cat([title, asr], dim=1)
        masked_text, mlm_mask = self.random_text_mask(text)
        masked_text = emb(masked_text)

        frame_len = frame.shape[1]
        title_len = title.shape[1]
        asr_len = asr.shape[1]

        inputs_embeds = torch.cat([masked_text, frame_proj], dim=1)  # bs 64 768
        attention_mask = torch.cat([title_mask, asr_mask, frame_mask], dim=1)

        bs = frame_proj.shape[0]

        if self.cfg.MODEL.VTM:
            n_frame_proj = torch.cat([frame_proj[bs // 2:, :], frame_proj[:bs // 2, :]], dim=0)
            n_frame_mask = torch.cat([frame_mask[bs // 2:, :], frame_mask[:bs // 2, :]], dim=0)

            neg_inputs_embeds = torch.cat([masked_text, n_frame_proj], dim=1)
            neg_attention_mask = torch.cat([title_mask, asr_mask, n_frame_mask], dim=1)

            inputs_embeds = torch.cat([inputs_embeds, neg_inputs_embeds], dim=0)
            attention_mask = torch.cat([attention_mask, neg_attention_mask], dim=0)

        token_type_ids = torch.zeros_like(attention_mask)
        token_type_ids[:, title_len + asr_len:] = 1

        outputs = self.bert(inputs_embeds=inputs_embeds, attention_mask=attention_mask, token_type_ids=token_type_ids,
                            output_hidden_states=True)

        mlm_outputs = outputs[0][:bs, :title_len + asr_len]
        _, _, word_num = mlm_outputs.shape
        mlm_mask = mlm_mask * attention_mask[:bs, :title_len + asr_len]
        mlm_outputs = mlm_outputs.reshape(-1, word_num)
        mlm_mask = mlm_mask.view(-1)
        mlm_gt = text.view(-1).long()
        mlm_mask = mlm_mask.bool()
        mlm_outputs = mlm_outputs[mlm_mask]
        mlm_gt = mlm_gt[mlm_mask]

        if self.cfg.MODEL.MVM:
            mvm_outputs = outputs[2][-1][:bs, title_len + asr_len:]
            mvm_outputs = self.mvm_fc(mvm_outputs)
            mvm_mask = mvm_mask * frame_mask
            _, _, dim = mvm_outputs.shape
            mvm_outputs = mvm_outputs.reshape(-1, dim)
            mvm_mask = mvm_mask.view(-1)
            mvm_gt = frame.view(-1, dim)
            # mvm_gt = frame_proj.view(-1, dim)
            mvm_mask = mvm_mask.bool()
            mvm_outputs = mvm_outputs[mvm_mask]
            mvm_gt = mvm_gt[mvm_mask]
            # mvm_neg = mvm_gt[~mvm_mask]
            # mvm_gt = mvm_gt[mvm_mask]
            mvm_neg = None
        else:
            mvm_outputs, mvm_gt, mvm_neg = None, None, None

        if self.cfg.MODEL.VTM:
            vtm_pos_outputs = self.vtm_fc(outputs[2][-1][:bs, 0])
            vtm_neg_outputs = self.vtm_fc(outputs[2][-1][bs:, 0])
            vtm_outputs = torch.cat([vtm_pos_outputs, vtm_neg_outputs], dim=0)
            vtm_gt = torch.zeros((bs * 2,), dtype=torch.long).to(device=vtm_outputs.device)
            vtm_gt[:bs] = 1
        else:
            vtm_outputs, vtm_gt = None, None

        cls_embeds = outputs[2][-1][:bs, 0]
        pred_tag = self.tag_fc(cls_embeds)
        pred_cat = self.cat_fc(cls_embeds)

        return mlm_outputs, mlm_gt, mvm_outputs, mvm_gt, mvm_neg, vtm_outputs, vtm_gt, pred_tag, pred_cat


    def cal_loss(self, mlm_outputs, mlm_gt, mvm_outputs, mvm_gt, mvm_neg, vtm_outputs, vtm_gt, pred_tag, pred_cat, tag, cat):
        if mvm_outputs is not None:
            mvm_gallery = torch.cat([mvm_gt, mvm_neg], dim=0)
            mvm_label = torch.arange(mvm_outputs.shape[0]).to(device=mvm_outputs.device)
            mvm_dot = torch.matmul(mvm_outputs, mvm_gallery.t())
            loss_mvm = F.cross_entropy(mvm_dot, mvm_label)     
        else:
            loss_mvm = 0

        loss_mlm = F.cross_entropy(mlm_outputs, mlm_gt)
        mlm_pred = mlm_outputs.argmax(dim=1)
        tot = mlm_gt.shape[0]
        acc = (mlm_pred == mlm_gt).to(dtype=torch.float32).sum() / tot

        pred_tag = pred_tag.sigmoid()
        loss_tag = pem_cls_loss(pred_tag, tag) * self.cfg.SOLVER.TAG_WEIGHT
        loss_cat = F.cross_entropy(pred_cat, cat) * self.cfg.SOLVER.CAT_WEIGHT

        loss = loss_mlm + loss_mvm + loss_tag + loss_cat

        return loss

    def forward(self, args):

        frame = args["frame_feat"].to("cuda") 
        frame_mask = args["frame_mask"].to("cuda") 

        title = args["title"].to("cuda").to("cuda")
        title_mask = args["title_mask"].to("cuda")

        asr = args["asr"].to("cuda") 
        asr_mask = args["asr_mask"].to("cuda")

        tag = args["tag"].to("cuda") 
        cat = args["cat"].to("cuda")

        predict = self._forward(frame.to("cuda"), frame_mask.to("cuda"), title.to("cuda"), title_mask.to("cuda"), asr.to("cuda"), asr_mask.to("cuda"))

        if self.training:
            return {"loss": self.cal_loss(*predict, tag, cat)}
        else:
            return {"predict": predict}