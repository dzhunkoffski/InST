# How to run benchmark

## Preparations
1. Clone this repo:
```bash
https://github.com/dzhunkoffski/InST.git
```
2. Prepare environment:
```bash
conda env create -f environment.yaml
conda activate ldm
```
3. Download [StyleBench](https://drive.google.com/file/d/1Q_jbI25NfqZvuwWv53slmovqyW_L4k2r/view) and unzip it:
```bash
gdown https://drive.google.com/uc?id=1Q_jbI25NfqZvuwWv53slmovqyW_L4k2r
unzip StyleBench.zip -d StyleBench
rm StyleBench.zip
cd StyleBench && mkdir styles
find style -type f \( -iname "*.jpg" \) | while read file; do
    dir=$(basename "$(dirname "$file")")
    base=$(basename "$file")
    cp "$file" "styles/${dir}_$base"
done
cd ..
```
4. Download sd pretrained weights:
```bash
cd models/sd
wget https://huggingface.co/CompVis/stable-diffusion-v-1-4-original/resolve/main/sd-v1-4.ckpt
cd ../..
```
## Finetune model
5. Run training script:
```bash
python main.py --base configs/stable-diffusion/v1-finetune.yaml -t --actual_resume models/sd/sd-v1-4.ckpt -n stylebench --gpus 1,3 --data_root StyleBench/styles --no-test
```
