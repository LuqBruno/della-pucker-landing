# Relatório — Della & Pucker v0.8.0 (01/10/2026)

Branch `della-pucker-v08-premium`. Diagnóstico e plano em `docs/diagnostico-v08.md`. Prévia local: `npm run dev` → http://localhost:3012/. Sem publicação, push ou contato com o cliente.

## 1. O que mudou, por seção

- **Sistema**: tokens em `style.css` — preto `#070708`, 6 grafites (`--g1`…`--g6`), branco quente `#f2efe8`, texto secundário AA, um acento âmbar `#d9a35e` (luz das janelas; só no ponto do rótulo e nos vidros do render). Raios 12/24/40, espaços 8→160, grade 12/8/4 colunas, durações 0,2/0,6/1 s, curvas `--ease-out`, `--ease-in`, `--ease-ui`. Máximo 3 famílias (Manrope, DM Sans, DM Mono), com fallbacks métricos medidos (Arial + `size-adjust`) para evitar CLS. `dark.css` (vazio) removido.
- **Cabeçalho**: logo vetorial nova (`assets/logo-della-pucker.svg`, 46 px de altura), fixo e translúcido com borda de 1 px, estado ativo por seção, menu móvel tela cheia (aria-expanded/controls, foco preso, Esc, fecha no link, restaura foco, trava o fundo), ícone ×.
- **Hero**: camadas — fundo com vinheta, grade técnica de 12 colunas, círculos de 1 px, nome monumental "DELLA & PUCKER" cortado nas bordas em grafite, casa (poster Cycles com piso transparente e sombra de contato), piso grafite com reflexo sutil, rótulos mono, marcas de registro, cota "Estudo · sem escala", contador `07 / 07` + nome da etapa, legenda discreta. Título fora da área do telhado, com variação tonal (branco / cinza / cinza claro) e troca "Do traço" ↔ "à obra" durante a construção. Bloco de texto + CTA alinhado à base do título e ligado à casa por uma linha fina. Saída: a casa recua e uma laje grafite de cantos arredondados sobe sobre o hero.
- **Construção**: desktop com GLB + Three (linhas de projeto → fundação → estrutura → fechamentos → cobertura → esquadrias → acabamento), câmera idêntica à do Blender, luz do frio ao âmbar, janelas acendendo no fim, parallax de ponteiro de poucos centímetros, anotações técnicas por etapa. **Celular/tablet** (pedido do usuário durante a rodada): 7 quadros WebP do Blender na câmera do poster mobile, trocados só por opacidade. Pin por `position: sticky` (CSS) com espaço reservado no primeiro paint.
- **Intenção + Atuação**: uma laje grafite contínua; quatro painéis em degraus tonais (g2 → g6) com numeração mono, círculo de 1 px, linha e tag; wireframe do telhado que se desenha com o scroll. Nenhum número inventado.
- **Projetos**: Embla com imagem principal grande e próxima visível, `aspect-ratio` único (16/10 desktop, 4/3 mobile), raio 40, miniaturas como seletor, contador `01 / 03` + barra de progresso, revelação por máscara, srcset 800/1440.
- **Como começar**: o parágrafo virou pergunta + 3 etapas numeradas ligadas por uma linha que se desenha (ver "Textos alterados"); planta publicada mantida.
- **Contato/rodapé**: painel grafite grande com círculos/cotas de 1 px, CTA; rodapé com logo vetorial, subtítulo em texto vivo, links com área de 44 px.

### Textos alterados (avisar o cliente)

- "Construir, regularizar ou visualizar um projeto? Conte o que você tem em mente. Se já houver um terreno, imóvel ou obra, mencione a situação para iniciar a conversa com a equipe." foi dividido em: pergunta + "Conte o que você tem em mente." / "Se já houver um terreno, imóvel ou obra, mencione a situação." / "Inicie a conversa com a equipe."
- Rodapé: acrescentado "Eng. Civil – Arquitetura" (texto da própria logo).
- Rótulos passaram de caixa alta no HTML para caixa alta via CSS (leitura igual).
- Links, número de WhatsApp, mensagem pré-preenchida, Instagram, endereço, title, description e Open Graph preservados. Acrescentados `og:locale`, `og:site_name`, `twitter:card` e JSON-LD `LocalBusiness` com os dados públicos já exibidos no rodapé.

## 2. Bibliotecas

Usadas (versões exatas do package-lock): GSAP 3.15.0 + ScrollTrigger, Lenis 1.3.26 (só desktop com ponteiro fino, ticker único do GSAP), Embla Carousel 8.6.0, Three.js 0.186.1 (GLTFLoader + DRACOLoader), esbuild 0.28.2. Nenhuma dependência nova no projeto.

Descartadas: React/React DOM, Motion, R3F/Drei, Tailwind, Radix/shadcn, Rive, Lottie (da base) — ver seção 3. Swiper, AOS e similares: redundantes com Embla/GSAP. Ferramentas usadas só fora do projeto (scratchpad): potrace/jimp (vetorização da logo) e playwright-core (QA).

## 3. Decisões com números

- **React: não.** A página é única, sem estado complexo; o HTML já é indexável sem JS. Migrar custaria reescrever tudo, somaria ~70 kB gzip de runtime (medida da base) e arriscaria SEO/acessibilidade. Motion não foi usado porque exige React; microinterações ficaram em CSS.
- **GLB vs sequência** — usar os dois, por dispositivo:
  - Desktop GLB: `house-scene.js` 630 kB (161 kB gzip) + GLB Draco 658 kB (593 kB gzip) + decoder Draco 193 kB wasm (63 kB gzip) + 58 kB wrapper (12 kB gzip) ≈ **829 kB transferidos**, abaixo do orçamento de 3 MB. 58.871 triângulos no modelo; 44 draw calls / ~118 mil triângulos com sombras. FPS medido com GPU (RTX 3050 Laptop, ANGLE D3D11) durante o scrub: **média 64–67 fps, p95 36 ms, picos 73–91 ms**. Ganha scrub contínuo, luz que muda e parallax.
  - Celular/tablet sequência: 6 quadros 294 kB + poster 48 kB ≈ **342 kB**, zero JS extra, só composição de opacidade. Sem WebGL em aparelho fraco.
- **Blender vs procedural: Blender** 5.2.2 via linha de comando. Novos: `render_v08.py` (posters com shadow catcher e luz interna), `crop_v08.py`, `render_seq_v08.py` (quadros; quadro 0 em Freestyle). Render: desktop 2400×1500 em 354 s, mobile 1400×1400 em 121 s. Geometria do v07 preservada.
- **Lenis: sim, só desktop** com ponteiro fino e sem movimento reduzido; âncoras usando o `scroll-padding-top` do CSS (offset duplicado corrigido). Celular usa rolagem nativa.
- **Pin**: `position: sticky` em vez de pin do ScrollTrigger — funciona antes do JS, não desloca layout e é mais estável no celular.

## 4. Antes e depois (Lighthouse 13.0.0, Chrome headless sem GPU, localhost)

| Medida | Mobile 0.6 | Mobile 0.8 (2 execuções) | Desktop 0.6 | Desktop 0.8 (2 execuções) |
| --- | ---: | ---: | ---: | ---: |
| Performance | 28 | 92 / 98 | 60 | 84 / 97 |
| LCP | 18.482 ms | 3.035 / 2.110 ms | 1.471 ms | 570 / 632 ms |
| CLS | 0,0002 | 0,0003 / 0,0132 | 0,0009 | 0,0016 / 0,0016 |
| TBT | 8.308 ms | 61 / 60 ms | 2.120 ms | 379 / 145 ms |
| Peso transferido | 2.639.148 B | 645.906 B | 2.176.723 B | 906.870 B |
| Acessibilidade / SEO / Boas práticas | 96 / 100 / – | 100 / 100 / 100 | 100 / 100 / – | 100 / 100 / 100 |

Os números de desktop não incluem o 3D: ele só carrega por intenção (mouse sobre o hero, roda, teclado, toque, scroll), que a auditoria não simula. Numa execução intermediária em que o 3D carregava por ociosidade, o TBT desktop foi 1.760–2.509 ms (Chrome sem GPU). INP não é medido por auditoria de navegação. LCP mobile variou entre execuções (2,1–3,0 s); a meta de 2,5 s foi atingida em uma de duas.

Relatórios: `output/qa-v08/v08-{mobile,desktop}-run{1,2}.report.{html,json}`; baseline em `output/playwright/`.

## 5. Verificação

- `npm run check` e `npm run build` passam (não há lint nem testes no projeto).
- Playwright + Chrome: primeira dobra em 360, 390, 430, 768, 1024, 1440 e 1920 — overflow horizontal 0 em todas; varredura de elementos além da borda em 360 e 1024: nenhum. Zoom 200% (720 px CSS): overflow 0.
- Construção: desktop em 6 momentos (repouso, 10, 30, 50, 70, 90%) e celular 360/390/768 em 6 momentos. Poster em repouso e 3D coincidem na troca.
- Menu: abre, foco no primeiro link, `inert` no conteúdo, scroll travado, Tab preso, Esc fecha e devolve foco, link fecha e rola (topo da seção a 80 px). Carrossel: toque (CDP) 01→02, arraste de mouse 01→02, ArrowRight/End/Home, botões desabilitados nos limites, miniatura → 03 com `aria-current`, slides "1 de 3"… e `aria-roledescription="carousel"`. Ordem de Tab lógica. Âncora "Como começar" com offset do cabeçalho (88 px) e estado ativo.
- Movimento reduzido (390 e 1440) e `?renderer=static`: sem canvas, poster estático, conteúdo completo. Console sem erros; único aviso é o log de compilação de shader do ANGLE/D3D (X4122), do driver.
- Contatos: todos os `[data-contact]` levam a `wa.me/554834127737` com a mesma mensagem; nada foi enviado.
- Capturas: `docs/qa/qa-v08-*.jpg` (dobras, construção desktop/mobile, menu, carrossel, reduzido, estático, logo vetor × original).

## 6. Não determinado com fidelidade na modelagem

A referência é render publicado, não foto; a planta não tem cotas. Medidas, pé-direito, inclinações, profundidade da varanda, escada, partes ocultas (fundos, lateral direita), interiores, fundação e estrutura são aproximações ilustrativas. A luz interna âmbar é escolha de apresentação, não informação do projeto. O telhado da varanda frontal herdou do v07 uma ondulação mais marcada que a do render. O paisagismo (gramado, carro, canteiros) não foi reproduzido.

## 7. Limitações e próximos passos

- Logo: o vetor foi redesenhado/traçado a partir de um JPG de 150 px; o "&" traçado tem pequenas irregularidades em tamanho grande. Pedir o arquivo original (AI/SVG/PDF) e substituir.
- Sem teste em aparelho físico, sem medição de campo (CrUX/RUM) nem INP. FPS medido em notebook com GPU dedicada; faltam aparelhos intermediários.
- Quadro 0 da sequência (linhas) pesa 114 kB; dá para reduzir com qualidade menor ou SVG das linhas.
- Canonical, sitemap e robots dependem do domínio final (ainda não existe).
- O hero não se conecta literalmente ao primeiro card do carrossel, porque a ordem das seções (Atuação antes de Projetos) foi preservada; a transição é o recuo da casa sob a laje grafite.
- Aprovação do cliente para textos alterados, uso da logo/imagens e dados de contato continua pendente.

## 8. Arquivos

Criados: `assets/logo-della-pucker.svg`, `assets/house-v08-{1200,1800}.webp`, `assets/house-v08-mobile-900.webp`, `assets/build-seq/m-{0..5}.webp`, `assets/{loft-arquitetura,projeto-estrutural,residencia-em-construcao}-800.webp`, `blender/render_v08.py`, `blender/crop_v08.py`, `blender/render_seq_v08.py`, `blender/residencia-rincao-v08.blend`, `blender/residencia-rincao-v08-{desktop,mobile}.png`, `blender/sequence-v08/phase-0{0..5}.png`, `blender/metrics-v08.json`, `docs/diagnostico-v08.md`, `docs/relatorio-v08.md`, `docs/qa/qa-v08-*.jpg`, `output/qa-v08/*`.

Alterados: `index.html`, `style.css`, `script.js`, `gallery.js`, `scene/house-scene.js`, `scripts/build.mjs`, `assets/site.js` e `assets/house-scene.js` (gerados), `package.json` (versão 0.8.0), `README.md`, `STATUS.md`.

Removidos: `dark.css` (placeholder vazio). Posters/modelos antigos continuam no repositório, mas não vão para `dist`.
