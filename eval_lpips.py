import os
import argparse
import glob
from pathlib import Path
from tqdm import tqdm

import numpy as np
from PIL import Image

import lpips

import torch
import torch.nn.functional as F
import torchvision
from torchvision.io import ImageReadMode
from torch.utils.data import Dataset, DataLoader

class LpipsImgDataset(Dataset):
    def __init__(self, output_root: str, content_root: str, style_root: str):
        self.content = content_root
        self.style = style_root

        self.output_imgs = glob.glob(os.path.join(output_root, '**', '*.png'), recursive=True)
        print(f'-----> Found {len(self.output_imgs)} images')
    
    def __len__(self):
        return len(self.output_imgs)
    
    def _get_style_path(self, output_img_path: str):
        style_no = os.path.basename(os.path.dirname(output_img_path)).split('-')[-1]
        style_type = os.path.basename(os.path.dirname(output_img_path)).split('-')[:-1]
        style_type = '-'.join(style_type)

        style_img_path = os.path.join(self.style, style_type, f'{style_no}.jpg')
        if not os.path.isfile(style_img_path):
            raise FileNotFoundError(style_img_path)
        return style_img_path
    
    def _get_content_path(self, output_img_path: str):
        content_name = Path(output_img_path).stem.split('*')[0][:-1]
        content_img_path = os.path.join(self.content, f'{content_name}.png')
        if not os.path.isfile(content_img_path):
            raise FileNotFoundError(content_img_path)
        return content_img_path
    
    def _read_lpips_img(self, path: str):
        img = torchvision.io.read_image(
            path=path, mode=ImageReadMode.RGB
        )
        # Normalize to [-1;1]
        img = img / 255.0
        img -= 0.5
        img /= 0.5
        return img

    def __getitem__(self, index):
        output_img_path = self.output_imgs[index]
        content_img_path = self._get_content_path(output_img_path)

        output_img = self._read_lpips_img(output_img_path)
        content_img = self._read_lpips_img(content_img_path)

        return output_img, content_img

def main(opt):
    device = torch.device(opt.device)
    print(f'------> Will run on device {device}')

    dataset = LpipsImgDataset(
        output_root=opt.output, content_root=opt.content, style_root=opt.style
    )
    dataloader = DataLoader(
        dataset=dataset, batch_size=opt.batch_size,
        shuffle=False, num_workers=4, drop_last=False
    )
    loss_fn = lpips.LPIPS(net=opt.lpips_backbone)
    loss_fn = loss_fn.to(device)

    lpips_score = 0.0
    total_seen = 0

    print('-----> START BENCHMARKING')
    with torch.no_grad():
        for output, content in tqdm(dataloader):
            output = output.to(device)
            content = content.to(device)

            curr_batch_size = output.size(0)
            total_seen += curr_batch_size

            score = loss_fn.forward(output, content).sum().item()
            lpips_score += score
    
    print(f'-----> LPIPS: {lpips_score / total_seen}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=str)
    parser.add_argument('--content', type=str)
    parser.add_argument('--style', type=str)
    parser.add_argument('--batch_size', type=int, default=16)
    parser.add_argument('--lpips_backbone', type=str, default='vgg')
    parser.add_argument('--device', type=str, default='cuda:0')
    opt = parser.parse_args()
    main(opt)