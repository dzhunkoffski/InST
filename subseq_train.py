import os
from pathlib import Path
import subprocess
import argparse
import glob

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--style', type=str)
    cfg = parser.parse_args()

    base_command = [
        "python", "main.py",
        "--base", "configs/stable-diffusion/v1-finetune.yaml",
        "-t",
        "--actual_resume", "models/sd/sd-v1-4.ckpt",
        "--gpus", "1,3",
        "--no-test"
    ]
    dirs = [d for d in os.listdir(cfg.style) if os.path.isdir(os.path.join(cfg.style, d))]
    print(f'FOUND {len(dirs)} styles')
    for i in range(len(dirs)):
        command = base_command + ['-n', dirs[i], '--data_root', os.path.join(cfg.style, dirs[i])]
        print(f"********************************** Executing: {' '.join(command)}")
        subprocess.run(command)
