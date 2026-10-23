"""Gera og.png (1200x630) e os ícones do site a partir dos HTML desta pasta."""
from pathlib import Path
from playwright.sync_api import sync_playwright

AQUI = Path(__file__).resolve().parent
SITE = AQUI.parent / "site"
SITE.mkdir(exist_ok=True)

with sync_playwright() as p:
    nav = p.chromium.launch()
    pg = nav.new_page(viewport={"width": 1200, "height": 630})
    pg.goto((AQUI / "og.html").as_uri())
    pg.evaluate("document.fonts.ready")
    pg.wait_for_timeout(600)
    # JPEG: o WhatsApp descarta prévias acima de ~300 KB
    pg.screenshot(path=str(SITE / "og.jpg"), type="jpeg", quality=88)

    for lado, nome in [(512, "icon-512.png"), (192, "icon-192.png"), (180, "apple-touch-icon.png")]:
        pi = nav.new_page(viewport={"width": 512, "height": 512}, device_scale_factor=lado / 512)
        pi.goto((AQUI / "icone.html").as_uri())
        pi.screenshot(path=str(SITE / nome))
        pi.close()
    nav.close()

for f in sorted([*SITE.glob("*.png"), *SITE.glob("*.jpg")]):
    print(f.name, f.stat().st_size // 1024, "KB")
