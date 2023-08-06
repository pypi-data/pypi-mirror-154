#!/usr/bin/env python3

import os
import sys
import torch
from valley.checkpoint import VCheckpointer
from valley import config
from valley.config import setup_cfg
from valley.config import load_default_cfg
from valley.engine import DefaultTrainer, default_argument_parser, dist_launch, default_setup
from valley.solver.build import get_default_optimizer_params, maybe_add_gradient_clipping
import model, data


class Trainer(DefaultTrainer):

    #@classmethod
    #def build_evaluator(cls, cfg, dataset_name, output_folder=None):
    #    if output_folder is None:
    #        output_folder = os.path.join(cfg.OUTPUT_DIR, "inference")
    #    return COCOEvaluator(dataset_name, output_dir=output_folder)


    @classmethod
    def build_optimizer(cls, cfg, model):
        params = get_default_optimizer_params(
            model,
            base_lr=cfg.SOLVER.BASE_LR,
            weight_decay_norm=cfg.SOLVER.WEIGHT_DECAY_NORM,
            #bias_lr_factor=cfg.SOLVER.BIAS_LR_FACTOR,
            #weight_decay_bias=cfg.SOLVER.WEIGHT_DECAY_BIAS,
        )

        optimizer = torch.optim.AdamW(
            params,
            lr = cfg.SOLVER.BASE_LR
        )

        return maybe_add_gradient_clipping(cfg, optimizer)


def main(cfg):

    if cfg.EXPERIMENT.EVAL_ONLY:
        model = Trainer.build_model(cfg)

        checkpoint_dir = os.path.join(cfg.EXPERIMENT.ROOT_DIR, cfg.EXPERIMENT.CHECKPOINT_DIR)
        
        VCheckpointer(model, save_dir=checkpoint_dir).resume_or_load(
            cfg.MODEL.WEIGHTS, resume=cfg.EXPERIMENT.RESUME
        )
        res = Trainer.test(cfg, model)
        return res

    default_setup(cfg)

    trainer = Trainer(cfg)

    trainer.resume_or_load()

    return trainer.train()


if __name__ == "__main__":

    args = default_argument_parser().parse_args()
    print("Command Line Args:", args)

    cfg = setup_cfg(args)

    dist_launch(
        main,
        cfg
    )
