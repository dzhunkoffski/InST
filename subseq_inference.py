import os
import subprocess
import argparse
import glob
from pathlib import Path

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--content', type=str)
    parser.add_argument('--embedding', type=str)
    parser.add_argument('--device', type=int)
    parser.add_argument('--style', type=str)
    cfg = parser.parse_args()

    base_command = [
        "python", "inference.py",
        "--content", cfg.content,
        "--device", str(cfg.device),
        "--embedding", cfg.embedding
    ]
    style_images = glob.glob(os.path.join(cfg.style, '**.jpg'))

    for i in range(len(style_images)):
        out_name = Path(style_images[i]).stem
        out_prefix = Path(style_images[i]).parts[-2]
        command = base_command + ["--style", style_images[i]] + ["--run_name", f'{out_prefix}-{out_name}']
        print(f"********************************** Executing: {' '.join(command)}")
        subprocess.run(command)
