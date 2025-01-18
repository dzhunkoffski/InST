import os
import subprocess
import argparse
import glob
from pathlib import Path

import logging
log = logging.getLogger(__name__)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--content', type=str)
    parser.add_argument('--embeddings', type=str)
    parser.add_argument('--device', type=int, default=0)
    parser.add_argument('--style', type=str)
    cfg = parser.parse_args()

    base_cmd = [
        'python', '-u', 'subseq_inference.py',
        '--content', cfg.content,
        '--device', str(cfg.device),
    ]
    styles = [d.name for d in Path(cfg.style).iterdir() if d.is_dir()]
    print(f'======= FOUND {len(styles)} styles =======')

    for style in styles:
        if len(glob.glob(os.path.join('outputs', f'{style}*'))):
            print('----->', f'Found {style}, skip')
        else:
            style_path = os.path.join(cfg.style, style)
            emb_path = glob.glob(os.path.join(cfg.embeddings, f'{style}*'))[0]
            emb_path = os.path.join(emb_path, 'checkpoints', 'embeddings.pt')
            cmd = base_cmd + [
                '--style', style_path,
                '--embedding', emb_path
            ]
            subprocess.run(cmd)

    print('+++++++ FINISH +++++++')
