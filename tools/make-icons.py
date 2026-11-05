"""気学アイコン(方位の輪)を作る。使い方: python tools/make-icons.py  (Pillow が必要: pip install pillow)
icons/ の icon-512.png / icon-192.png / icon-maskable-512.png / apple-touch-icon.png を書き出す。
8つの区画: 上下左右(北・東・南・西)が30度、四隅(北東・南東・南西・北西)が60度。
背景は全面を塗る。maskable は、図を縮めて、中央の安全な範囲に収める。"""
import math
from pathlib import Path
from PIL import Image, ImageDraw

BG, GOLD = (0x0b, 0x10, 0x20), (0xd6, 0xb2, 0x6a)
ROOT = Path(__file__).resolve().parent.parent / 'icons'
S = 8                      # 作図は8倍の大きさで行い、縮小してなめらかにする
ANGLES = [15, 75, 105, 165, 195, 255, 285, 345]   # 区画の境目(北を0度、時計回り)
R_OUT, R_HUB, W = 190, 64, 5                      # 外の輪、中央の輪の半径、線の太さ
CENTER_DOT = True                                 # 中央の小さな点。要らなければ False

def render(size, scale=1.0):
    n = 512 * S
    im = Image.new('RGB', (n, n), BG)
    d = ImageDraw.Draw(im)
    c = 256 * S
    def pt(r, deg):
        a = math.radians(deg)
        return c + r * scale * S * math.sin(a), c - r * scale * S * math.cos(a)
    def ring(r, w):
        ro = (r + w / 2) * scale * S
        d.ellipse([c - ro, c - ro, c + ro, c + ro], outline=GOLD, width=max(1, round(w * scale * S)))
    def dot(x, y, w):
        rr = w * scale * S / 2
        d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=GOLD)
    ring(R_OUT, W)
    ring(R_HUB, W)
    for a in ANGLES:
        (x1, y1), (x2, y2) = pt(R_HUB, a), pt(R_OUT, a)
        d.line([x1, y1, x2, y2], fill=GOLD, width=round(W * scale * S))
        dot(x1, y1, W); dot(x2, y2, W)                       # 線の端を丸くする
    if CENTER_DOT:
        r = 12 * scale * S
        d.ellipse([c - r, c - r, c + r, c + r], fill=GOLD)
    return im.resize((size, size), Image.LANCZOS)

if __name__ == '__main__':
    for name, size, scale in (('icon-512.png', 512, 1.0), ('icon-192.png', 192, 1.0),
                              ('icon-maskable-512.png', 512, 0.84), ('apple-touch-icon.png', 180, 1.0)):
        render(size, scale).save(ROOT / name, optimize=True)
        print('wrote', name, size)
