# Baseline Lighthouse — Della & Pucker 0.6.0

Executado em 01/10/2026 antes da edição desta rodada, em http://localhost:3012/. Lighthouse 13.0.0 via npx, Chrome headless 154, Node 22.20.0. Dependências da landing não alteradas pela auditoria.

| Medida | Mobile | Desktop |
| --- | ---: | ---: |
| LCP | 18.482 ms | 1.471 ms |
| CLS | 0,000156 | 0,000884 |
| TBT | 8.308 ms | 2.120 ms |
| Bytes transferidos na navegação | 2.639.148 | 2.176.723 |
| Performance | 28 | 60 |
| Acessibilidade automática | 96 | 100 |
| SEO | 100 | 100 |

Mobile: emulação 412×823, CPU 4×, RTT 150 ms, throughput simulado 1.638,4 Kbps. Desktop: preset desktop padrão. Uma execução por configuração, sem tratamento estatístico. Relatórios completos adjacentes baseline-mobile.report.json/html e baseline-desktop.report.json/html.

## Achados

- O mobile carregou house-scene.js, GLB e Draco na navegação inicial. GLB local 867.196 B; bundle 3D 628.718 B; interface 159.506 B. Poster desktop 132.808 B; mobile 61.114 B.
- LCP mobile identificado como img.house-poster. CLS baixo, mas execução do 3D bloqueia a thread principal na auditoria. Tempo observado de scripting de house-scene.js: 6.701 ms.
- Console registrou apenas favicon.ico 404. Corrigir icon explícito ou resposta equivalente sem redesenhar marca.
- Links WhatsApp/Instagram do rodapé possuem caixas de 65×15 / 61×15 px e pouca separação. Ampliar a área de toque.
- Auditoria automática de contraste não registrou falhas. Não equivale a certificação integral WCAG.

## Limitações

O Chrome foi iniciado com --headless=new --disable-gpu --no-sandbox. O custo do WebGL pode diferir fortemente de um dispositivo físico com GPU; a medição é um baseline de laboratório repetível, não desempenho de campo. O servidor local não reproduz compressão/cache/CDN da hospedagem comercial. INP não é medido por auditoria navigation e não foi estimado a partir do TBT. FPS do 3D não medido neste teste.
