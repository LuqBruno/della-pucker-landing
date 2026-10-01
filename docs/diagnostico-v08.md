# Diagnóstico e plano — v0.8.0 (01/10/2026)

Pedido: aplicar a base `Landing_Premium_Base` à landing Della & Pucker, com as fases 1–11 do briefing do usuário. Branch de trabalho: `della-pucker-v08-premium` (ponto de partida: commit `c82a2f2`).

## Ponto de partida

- Stack: HTML + CSS + JavaScript ESM, esbuild 0.28.2 gera `assets/site.js` e `assets/house-scene.js`. GSAP 3.15.0, Lenis 1.3.26, Embla 8.6.0, Three 0.186.1. Sem lint nem testes; `npm run check` (sintaxe) e `npm run build`.
- Estado encontrado: revisão 0.7 inacabada da conversa anterior (posters `house-v07-*`, GLB `residencia-rincao-v07.glb`, nome monumental no HTML). O `index.html` ainda apontava para o poster 0.5 (`house-dark.webp`, com piso escuro esverdeado em placa retangular).
- Baseline Lighthouse (0.6.0, medido antes desta rodada; `output/playwright/baseline-metricas.md`): mobile LCP 18,5 s, TBT 8,3 s, 2,64 MB, Performance 28; desktop LCP 1,5 s, TBT 2,1 s, 2,18 MB, Performance 60. Causa principal no mobile: GLB + Three carregados na navegação inicial.

## Identidade

- Logo oficial disponível apenas como JPG 150×150 px (avatar do Instagram). Não há vetor oficial local.
- Ação desta rodada: `assets/logo-della-pucker.svg`. Letras redesenhadas por medição pixel a pixel do JPG (traço geométrico uniforme, alinhamento à direita das duas linhas preservado); "&" cinza vetorizado por traçado (potrace) da camada cinza isolada. A linha "ENG. CIVIL - ARQUITETURA" tem cerca de 7 px de altura no original e não pôde ser vetorizada com fidelidade: no cabeçalho foi omitida; no rodapé aparece como texto vivo. **Não substitui o original da marca**; pedir o arquivo vetorial ao cliente.

## Referências

- Hotle: palavra monumental atrás da arquitetura, câmera baixa, luz interior âmbar.
- Kontra: painel escuro com cantos muito arredondados, imagem principal grande com cards laterais menores, títulos com variação tonal.
- Terceira imagem: painéis grafite em degraus tonais, rótulos mono nos cantos, círculos e linhas de 1 px, malhas wireframe.
- Vídeo enviado (`digioven_pindown.io_1790855815.mp4`) é idêntico byte a byte (SHA-256 `cbf34424…`) a `references/motion-inspiration.mp4`, já decomposto em quadros em `docs/qa/motion-frames-v07/`. Observado: objeto central que se transforma continuamente, sem cortes abruptos; títulos trocam por seção e o objeto vai para a lateral; aceleração/desaceleração moderadas, sem bounce. Não dá para medir curva, duração exata ou se o movimento é ligado ao scroll (é filmagem de tela).

## Problemas por seção

- Cabeçalho: logo cortada embaixo pela máscara, subtítulo ilegível, ativo por seção ok, menu mobile ok.
- Hero: "Do traço à obra." colide com o telhado; casa perto demais e cortada na base; piso verde-escuro em placa; casa toda off-white sem contraste; coluna direita solta; legenda pesada; corte seco para a seção seguinte.
- Intenção: faixa solta, sem ligação com o hero.
- Atuação: quatro cards iguais em 2×2; boa base tonal, falta ritmo e elemento de arquitetura.
- Projetos: carrossel Embla funcional; imagem com `object-fit: contain` deixa faixas; sem srcset; dots sem miniaturas.
- Como começar: só título, parágrafo e planta; sem etapas.
- Contato/rodapé: painel ok; links do rodapé com área de toque pequena (achado do Lighthouse).

## Plano

1. Sistema de design em tokens (cor, tipo, raio, espaço, movimento) em `style.css`.
2. Cabeçalho com logo vetorial e área de respiro.
3. Hero em camadas, posters v08 transparentes (shadow catcher no Blender), casa recuada com base inteira, título fora da colisão, ligação por cotas, construção 3D só no desktop e sob demanda.
4. Seções reorganizadas com o mesmo conteúdo; Embla com miniaturas, progresso e srcset.
5. Verificação: check/build, Playwright em 360/390/430/768/1024/1440/1920, movimento reduzido, fallback, Lighthouse.

React: não migrar. Benefício concreto inexistente para uma página única sem estado complexo; custo de reescrita total, risco de regressão em SEO (HTML hoje é indexável sem JS) e em peso de JS. A base é usada como referência de bibliotecas, versões e padrões de cleanup.
