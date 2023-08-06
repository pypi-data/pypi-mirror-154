#!/usr/bin/env python3

import os

from valley.checkpoint import VCheckpointer
from valley import config
from valley.config import load_default_cfg
from valley.engine import DefaultTrainer, default_argument_parser, dist_launch  #default_setup

#from mnist import add_mnist_config

"""
class Trainer(DefaultTrainer):
    @classmethod
    def build_evaluator(cls, cfg, dataset_name, output_folder=None):
        if output_folder is None:
            output_folder = os.path.join(cfg.OUTPUT_DIR, "inference")
        return COCOEvaluator(dataset_name, output_dir=output_folder)
"""

def setup_cfg(args):
    """
    Create configs and perform basic setups.
    """

    # load default cfg
    cfg = load_default_cfg()

    config_file = os.path.join(args.exp_root, "config", args.config if args.config != "" else "config.yaml")

    #add_mnist_config(cfg)

    # load task specific config
    cfg.merge_from_file(config_file)
    cfg.set_new_allowed(True)

    opts = sum([e.split("=") for e in args.opts], [])
    # override params
    cfg.merge_from_list(opts)
    cfg.set_new_allowed(True)

    dist_url = 'tcp://{}:{}'.format(args.master_addr, args.master_port)
    cfg.merge_from_list(['LAUNCH.HOST_NUM', args.nnodes,
                         'LAUNCH.GPU_PER_HOST', args.nproc_per_node,
                         'LAUNCH.HOST_RANK', args.node_rank,
                         'LAUNCH.DIST_URL', dist_url,
                         'EXPERIMENT.ROOT_DIR', args.exp_root,
                         'EXPERIMENT.EVAL_ONLY', args.eval_only,
                         'EXPERIMENT.RESUME', args.resume,
                         'EXPERIMENT.CFG_FILE', args.config])

    cfg.freeze()
    
    #default_setup(cfg, args)
    
    return cfg


def main(cfg):

    if cfg.EXPERIMENT.EVAL_ONLY:
        model = DefaultTrainer.build_model(cfg)

        checkpoint_dir = os.path.join(cfg.EXPERIMENT.ROOT_DIR, cfg.EXPERIMENT.CHECKPOINT_DIR)
        
        VCheckpointer(model, save_dir=checkpoint_dir).resume_or_load(
            cfg.MODEL.WEIGHTS, resume=cfg.EXPERIMENT.RESUME
        )
        res = DefaultTrainer.test(cfg, model)
        return res

    trainer = DefaultTrainer(cfg)

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
