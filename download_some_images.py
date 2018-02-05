import random
import os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.request import urlretrieve

IMG_URL = "https://picsum.photos/{w}/{h}/"
PATH = Path(__file__).parent / "archive_manager" / "dummy_data"
os.makedirs(PATH, exist_ok=True)


def download_image(i, w, h, prefix="image"):
    name = PATH / f"{prefix}_{i + 1:04d}.jpeg"
    url = IMG_URL.format(w=w, h=h)
    print(i, url, name)
    urlretrieve(url, name)
    print(i, "OK")


with ThreadPoolExecutor(max_workers=20) as e:
    # download logos
    futs = [e.submit(download_image, i, 160, 100, "logo") for i in range(3)]
    
    # download sample images
    for i in range(400):
        e.submit(download_image, i, random.randint(500, 600),
                 random.randint(400, 500))

for fut in futs:
    fut.result()
print("done")
