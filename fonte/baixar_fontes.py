"""Baixa as fontes do Google Fonts para dentro do site (site/fonts/), para não depender de servidor de fora.
As três famílias têm licença OFL, que permite hospedar a cópia."""
import re
import urllib.request
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent / "site"
PASTA = SITE / "fonts"
PASTA.mkdir(exist_ok=True)
URL = ("https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:ital,wght@0,400;0,700;1,400"
       "&family=Barlow+Condensed:wght@600;700;800&family=Share+Tech+Mono&display=swap")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"

css = urllib.request.urlopen(urllib.request.Request(URL, headers={"User-Agent": UA}), timeout=30).read().decode("utf-8")
# Só os blocos latin e latin-ext: português não usa cirílico nem vietnamita
blocos = re.findall(r"/\* ([\w-]+) \*/\s*(@font-face \{.*?\})", css, re.S)
saida = []
for subset, bloco in blocos:
    if subset not in ("latin", "latin-ext"):
        continue
    url = re.search(r"url\((https://fonts\.gstatic\.com/[^)]+\.woff2)\)", bloco).group(1)
    familia = re.search(r"font-family: '([^']+)'", bloco).group(1).replace(" ", "")
    peso = re.search(r"font-weight: (\d+)", bloco).group(1)
    estilo = re.search(r"font-style: (\w+)", bloco).group(1)
    nome = f"{familia}-{peso}{'i' if estilo == 'italic' else ''}-{subset}.woff2"
    dados = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=30).read()
    assert dados[:4] == b"wOF2", f"{nome} não é woff2"
    (PASTA / nome).write_bytes(dados)
    saida.append(f"/* {subset} */\n" + bloco.replace(url, f"/fonts/{nome}"))
    print(nome, len(dados) // 1024, "KB")
(PASTA / "fonts.css").write_text("\n".join(saida) + "\n", encoding="utf-8")
print("fonts.css com", len(saida), "blocos")
