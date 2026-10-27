"""Иконка сайта: синий скруглённый квадрат с белой молнией (как в эмблеме на главной).
Запуск: python3 _build/og/favicon.py — пишет favicon.ico, favicon-32.png, favicon-512.png, apple-touch-icon.png, favicon.svg."""
import os
from PIL import Image, ImageDraw

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
BLUE, WHITE = (0, 119, 182, 255), (255, 255, 255, 255)
BOLT = [(0.585, 0.12), (0.255, 0.555), (0.475, 0.555), (0.405, 0.88), (0.745, 0.43), (0.52, 0.43)]


def draw(size, radius=0.22, bg=True):
    s = 1024
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if bg:
        d.rounded_rectangle((0, 0, s - 1, s - 1), radius=int(s * radius), fill=BLUE)
    d.polygon([(x * s, y * s) for x, y in BOLT], fill=WHITE)
    return im.resize((size, size), Image.LANCZOS)


big = draw(512)
big.save(os.path.join(ROOT, "favicon-512.png"))
draw(32).save(os.path.join(ROOT, "favicon-32.png"))
draw(180, radius=0).convert("RGB").save(os.path.join(ROOT, "apple-touch-icon.png"))
draw(64).save(os.path.join(ROOT, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
pts = " ".join(f"{x * 64:.1f},{y * 64:.1f}" for x, y in BOLT)
open(os.path.join(ROOT, "favicon.svg"), "w").write(
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#0077B6"/>'
    f'<polygon points="{pts}" fill="#fff"/></svg>\n')
