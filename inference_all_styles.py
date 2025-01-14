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
    parser.add_argument('--device', type=int)
    parser.add_argument('--style', type=str)
    cfg = parser.parse_args()

    base_cmd = [
        'python', 'subseq_inference.py',
        '--content', cfg.content,
        '--device', str(cfg.device),
    ]
    styles = [d.name for d in Path(cfg.style).iterdir() if d.is_dir()]
    log.info(f'======= FOUND {len(styles)} styles =======')

    for st in styles:
        emb_ckpt = glob.glob(os.path.join(cfg.embeddings, f'**_{st}'))
        if len(emb_ckpt) == 0 or st == 'Gongbi':
            log.warning('NO EMBEDDIING DIR FOR THIS STYLE')
            continue
        emb_ckpt = emb_ckpt[0]
        log.info('++++++++++ ' + emb_ckpt + ' ++++++++++')
        cmd = base_cmd + [
            '--style', os.path.join(cfg.style, st),
            '--embedding', os.path.join(emb_ckpt, 'checkpoints', 'embeddings.pt')
        ]

        if len(glob.glob(os.path.join('outputs', f'{st}**'))) == 0:
            subprocess.run(cmd)
        else:
            log.warning('SKIP')
