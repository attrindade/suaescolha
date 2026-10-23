"""Monta o site a partir de fonte/app.html: index.html com prévia (Open Graph) e ícones, app.js com todo o
código (o HTML não leva script embutido, para a política de segurança só aceitar código deste site) e _headers."""
import re
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
SITE = AQUI.parent / "site"
artefato = Path(sys.argv[1]).read_text(encoding="utf-8").splitlines()

# Depois da meta do claude.ai até o último </script>: fontes, estilo, corpo e script (sem o esqueleto e o <title>)
ini = next(i for i, l in enumerate(artefato) if l.startswith('<meta name="claude:')) + 1
fim = max(i for i, l in enumerate(artefato) if l.strip() == "</script>")
miolo = "\n".join(artefato[ini:fim + 1])

URL = "https://suaescolha.pages.dev/"
DESC = "Perguntas de sim ou não, cada uma com fonte, para te ajudar a decidir e para conversar com indecisos no 2º turno."

head = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Sua Escolha Muda o Cenário</title>
<meta name="description" content="{DESC}">
<link rel="canonical" href="{URL}">
<meta name="theme-color" content="#009C3B">
<meta property="og:type" content="website">
<meta property="og:locale" content="pt_BR">
<meta property="og:site_name" content="Sua Escolha">
<meta property="og:title" content="Sua escolha muda o cenário">
<meta property="og:description" content="{DESC}">
<meta property="og:url" content="{URL}">
<meta property="og:image" content="{URL}og.jpg?v=3">
<meta property="og:image:secure_url" content="{URL}og.jpg?v=3">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Sua escolha muda o cenário: perguntas de sim ou não, com fonte, para o 2º turno de 25 de outubro">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Sua escolha muda o cenário">
<meta name="twitter:description" content="{DESC}">
<meta name="twitter:image" content="{URL}og.jpg?v=3">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/icon-192.png" sizes="192x192" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/manifest.webmanifest">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Sua Escolha">
<style>:root{{color-scheme:light;box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}html{{scroll-padding-top:env(safe-area-inset-top,0px)}}body{{margin:0;padding:0;font:14px -apple-system,BlinkMacSystemFont,sans-serif;background:#fff;color:#000}}img{{max-width:100%}}[hidden]{{display:none!important}}</style>
</head>
<body>
"""

rodape = """
<style>
.rodape{max-width:560px;margin:0 auto;padding:0 max(16px,env(safe-area-inset-right,0px)) 32px max(16px,env(safe-area-inset-left,0px));display:flex;flex-direction:column;gap:10px;align-items:center;text-align:center;font-size:14px;color:var(--muted)}
.rodape p{margin:0}
.rodape a{color:var(--link);font-weight:700}
.compartilhar{font:700 16px/1 var(--f-body);padding:13px 18px;border-radius:10px;border:2px solid var(--verde);background:transparent;color:var(--fg);cursor:pointer}
.compartilhar:focus-visible{outline:3px solid var(--amarelo);outline-offset:2px}
</style>
<footer class="rodape">
  <button class="compartilhar" id="btnCompartilhar" type="button">Mandar a ferramenta para alguém</button>
  <p id="avisoCompartilhar" aria-live="polite"></p>
  <p>Para abrir como app, até sem internet: no menu do navegador, toque em <b>Adicionar à tela inicial</b>.</p>
  <p>Responsável: <span class="resp-nome">André Trindade</span> · andrettrindade@gmail.com</p>
  <p>Nada do que você responde é gravado. <a href="https://github.com/attrindade/suaescolha">Veja o código aberto no GitHub</a>.</p>
</footer>
<script>
$("btnCompartilhar").addEventListener("click", async () => {
  const dados = {title:"Sua escolha muda o cenário", text:"24 perguntas de sim ou não, cada uma com fonte, para te ajudar a decidir e para conversar com indecisos no 2º turno:", url:"https://suaescolha.pages.dev/?v=3"};
  if (navigator.share) { try { await navigator.share(dados); } catch(e){} return; }
  try { await navigator.clipboard.writeText(dados.url); $("avisoCompartilhar").textContent = "Link copiado."; }
  catch(e){ $("avisoCompartilhar").textContent = dados.url; }
});
if ("serviceWorker" in navigator) navigator.serviceWorker.register("/sw.js").catch(()=>{});
</script>
</body>
</html>
"""

pagina = head + miolo + "\n" + rodape

# Todo <script> embutido vai, na mesma ordem, para app.js, carregado no fim do <body>
scripts = re.findall(r"<script>(.*?)</script>", pagina, re.S)
pagina = re.sub(r"<script>.*?</script>\n?", "", pagina, flags=re.S)
pagina = pagina.replace("</body>", '<script src="/app.js"></script>\n</body>')
assert "<script>" not in pagina and " on" + "click=" not in pagina
(SITE / "app.js").write_text("\n;\n".join(scripts), encoding="utf-8")
(SITE / "index.html").write_text(pagina, encoding="utf-8")

# Cabeçalhos de segurança: só código, fontes e imagens deste site; nada de moldura em outro site
CSP = ("default-src 'none'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; "
       "font-src 'self'; connect-src 'self'; manifest-src 'self'; worker-src 'self'; base-uri 'none'; "
       "form-action 'none'; frame-ancestors 'none'; object-src 'none'; upgrade-insecure-requests")
(SITE / "_headers").write_text(f"""/*
  Content-Security-Policy: {CSP}
  X-Content-Type-Options: nosniff
  X-Frame-Options: DENY
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=(), usb=(), bluetooth=(), serial=(), hid=()
  Strict-Transport-Security: max-age=31536000; includeSubDomains
  Cross-Origin-Opener-Policy: same-origin

/sw.js
  Cache-Control: no-cache

/app.js
  Cache-Control: no-cache

/
  Cache-Control: public, max-age=0, must-revalidate

/og.jpg
  Cache-Control: public, max-age=86400
""", encoding="utf-8")
print("index.html", (SITE / "index.html").stat().st_size // 1024, "KB | app.js", (SITE / "app.js").stat().st_size // 1024, "KB |", len(scripts), "scripts")
