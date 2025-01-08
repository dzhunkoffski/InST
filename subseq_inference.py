import subprocess

if __name__ == '__main__':
    base_command = [
        "python", "inference.py",
        "--content", "data/content_images",
        "--device", "1",
        "--embedding", "logs/train_styles2025-01-08T01-07-50_allstyles/checkpoints/embeddings.pt"
    ]
    style_images = [
        "data/sty/31.png", "data/sty/anime.jpg", "data/sty/chineseart.jpg",
        "data/sty/lines.jpg", "data/sty/mosaic.jpg", "data/sty/picasso.jpg",
        "data/sty/plastilin.jpg", "data/sty/reimbrandt.jpg", "data/sty/tomnjerry.jpg",
        "data/sty/village.jpg"
    ]
    out_names = [
        '31', 'anime', 'chineseart', 'lines', 'mosaic', 'picasso', 'plastilin',
        'reimbrandt', 'tomnjerry', 'village'
    ]

    for i in range(len(style_images)):
        command = base_command + ["--style", style_images[i]] + ["--run_name", 'all_'+out_names[i]]
        print(f"********************************** Executing: {' '.join(command)}")
        subprocess.run(command)
