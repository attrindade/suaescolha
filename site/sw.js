// Guarda a página e as fontes no celular para funcionar na rua, com sinal fraco ou sem internet.
// Página: tenta a rede primeiro (pega correções); sem rede, usa a cópia guardada.
const CACHE = "suaescolha-v3";
const BASICO = ["/", "/app.js", "/fonts/fonts.css", "/manifest.webmanifest", "/icon-192.png", "/icon-512.png", "/favicon.svg", "/qr.svg"];

self.addEventListener("install", e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(BASICO)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", e => {
  e.waitUntil(caches.keys()
    .then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});

self.addEventListener("fetch", e => {
  const req = e.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);

  if (req.mode === "navigate") {
    e.respondWith(
      fetch(req).then(r => { const c = r.clone(); caches.open(CACHE).then(k => k.put("/", c)); return r; })
        .catch(() => caches.match("/"))
    );
    return;
  }

  // Só arquivos deste site (as fontes também são locais); código e lista de perguntas vêm da rede primeiro
  if (url.origin !== location.origin) return;
  const atualiza = url.pathname === "/app.js";
  e.respondWith(
    atualiza
      ? fetch(req).then(r => { const c = r.clone(); caches.open(CACHE).then(k => k.put(req, c)); return r; }).catch(() => caches.match(req))
      : caches.match(req).then(hit => hit || fetch(req).then(r => {
          if (r.ok) { const c = r.clone(); caches.open(CACHE).then(k => k.put(req, c)); }
          return r;
        }))
  );
});
