#!/bin/bash
export PYTHONPATH=.
python projects/Mnist/train_net.py --exp_root /workspace/user_code/workspace/VFoundation/experiment/ --config config_mnist_new.yaml --nnodes 1 --nproc_per_node 2 --node_rank 0 --master_addr 127.0.0.1 --master_port 23450
