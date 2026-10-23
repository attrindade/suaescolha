# Sua escolha muda o cenário

Perguntas de sim ou não, cada uma com fonte, para te ajudar a decidir e para conversar com indecisos no 2º turno de 25/10/2026.

No ar em **https://suaescolha.pages.dev**

## Nada do que você responde é gravado

O app é uma página estática: o servidor só entrega os arquivos, e nenhuma resposta sai do celular.

- **Sem envio de dados.** O código do app (`site/app.js`) não tem `fetch`, `XMLHttpRequest` nem `sendBeacon`. Não existe servidor próprio, banco de dados ou formulário.
- **Sem gravação no celular.** Não usa cookie, `localStorage`, `sessionStorage` nem IndexedDB. As respostas e o perfil ficam só na memória da página (`const perfil = {}` e `resp` em `fonte/app.html`) e somem ao tocar em "Nova pessoa" ou ao fechar a página.
- **Sem medidor de acessos.** Nenhum Google Analytics, pixel ou script de terceiros. A política de segurança (`site/_headers`) só deixa a página carregar código, fontes e imagens do próprio site (`script-src 'self'`, `connect-src 'self'`, `form-action 'none'`).
- **Funciona sem internet.** O `site/sw.js` guarda no celular só os arquivos do site (página, código, fontes e ícones), nunca respostas.
- **Perfil opcional e sem dado sensível.** O perfil (idade, gênero, escolaridade, município, voto) serve só para escolher a ordem das perguntas. Não pergunta religião.

### Como conferir

Baixe o repositório e procure qualquer forma de envio ou gravação:

```
grep -n -i -E "fetch\(|XMLHttpRequest|sendBeacon|localStorage|sessionStorage|indexedDB|document\.cookie" site/app.js site/sw.js
```

Só aparecem os `fetch` do `sw.js`, que baixam os arquivos do próprio site para funcionar sem internet.

## Arquivos

| Pasta | O que tem |
|---|---|
| `fonte/app.html` | O app inteiro: perguntas, fontes, estilo e código |
| `fonte/montar.py` | Gera `site/` a partir de `fonte/app.html` (página, `app.js` e cabeçalhos de segurança) |
| `site/` | O que vai para o ar, sem nenhuma etapa a mais |

Para gerar o site: `python fonte/montar.py fonte/app.html`.

## Responsável

André Trindade · andrettrindade@gmail.com
