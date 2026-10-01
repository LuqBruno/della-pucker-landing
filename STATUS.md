# STATUS — Della & Pucker

## Revisão vigente de 01/10/2026 — versão local 0.8.0

Pedido: aplicar a base `Landing_Premium_Base` com as fases 1–11 do briefing (diagnóstico, sistema de design, cabeçalho/logo, hero em camadas com construção 3D, seções, carrossel, animação, responsivo, acessibilidade/SEO, desempenho, verificação). Durante a rodada o usuário pediu a construção otimizada para celular: implementada com sequência de quadros do Blender. O vídeo reenviado é idêntico ao `references/motion-inspiration.mp4` (mesmo SHA-256). Lidos AGENTS da raiz/área/projetos e da base, README/STATUS/package. React não adotado (justificativa em `docs/relatorio-v08.md`).

Verificações efetivas desta rodada: check/build aprovados; Playwright/Chrome em 360, 390, 430, 768, 1024, 1440, 1920 com overflow 0; zoom 200% sem overflow; construção desktop e mobile em 6 momentos; menu (foco, Esc, inert, trava de scroll, fechar no link), carrossel (toque, arraste, teclado, limites, miniaturas, rótulos), âncoras com offset, movimento reduzido e `?renderer=static`, contatos (mesmo destino wa.me, nada enviado), console sem erros. Lighthouse 13 mobile/desktop 2× cada; FPS do 3D medido em RTX 3050 Laptop (média 64–67 fps, p95 36 ms). Capturas `docs/qa/qa-v08-*.jpg`; relatórios em `output/qa-v08/`.

Publicação da prévia (pedido do usuário, 01/10/2026): repositório público https://github.com/LuqBruno/della-pucker-landing, Pages em https://luqbruno.github.io/della-pucker-landing/. Workflow concluído com sucesso; conferidos no ar: HTTP 200 da página e dos recursos, construção mobile (sequência) e desktop (3D), sem overflow, `noindex` ativo; vídeo/quadros de inspiração e `dev-scene.html` não publicados (404). Nenhuma mensagem enviada ao cliente.

Pendências reais: arquivo original da logo; aprovação dos textos alterados e do visual; autorização de logo/imagens; confirmação de contato/endereço; domínio para canonical/sitemap/robots; teste em aparelho físico e INP. Próxima ação: enviar o link ao cliente (pelo usuário) e colher aprovação; remover `noindex` só na publicação definitiva.

## Histórico — revisão de 01/10/2026, versão local 0.6.0


Pedido: integrar recursos da base premium sem copiar identidade, corrigir logo/avatar e manter preto/grafite em toda a landing. Foram lidos mapa, AGENTS de raiz/área/projetos e da base, README/package/estado do cliente e base. Perfil oficial reconsultado no navegador; mesma logo de 150×150 px, bio/contato/serviços e projetos preservados. A circularidade observada anteriormente pertence ao avatar do Instagram, não à composição original da marca.

Implementado: marca direta no cabeçalho/rodapé, sem moldura, arredondamento, sombra ou brilho. Máscara CSS usa a luminância do JPG oficial para eliminar preto na composição e preservar contornos/cinzas; margens negras recortadas opticamente, sem deformação. Não há PNG transparente novo nem redesenho. Tentativa de edição por IA rejeitada por alterar letras; não integrada. Pendente: vetor/transparente oficial com definição superior. Ampliação da imagem pequena evidencia limites do original; não alegar nitidez vetorial.

Base aplicada na stack JavaScript: GSAP 3.15.0/ScrollTrigger para entrada e construção, Lenis 1.3.26 no desktop compatível somente, Embla 8.6.0 para carrossel manual; Three 0.186.1 preservado. Bundle assets/site.js gerado no dev/build. Carrossel: projeto principal e próximo parcial, setas/posição/dots, teclado/arraste, limites e ausência de autoplay. Scroll nativo mobile. Limpeza de eventos/observadores/ticker/GSAP e retomada via bfcache; cada engine controla propriedades diferentes. Hierarquia do hero ajustada com assinatura menor e casa mais próxima do texto mobile. Interface continua neutra em todas as seções; plantas/renders originais não recoloridos.

Blender desta rodada: arquivos da 0.5 preservados (blender/residencia-rincao-dark.blend e assets/models/residencia-rincao.glb); não foi criado novo modelo/render nesta revisão de logo/base. Construção GSAP continua sete etapas e câmera fixa. Referência é render oficial; aproximações históricas continuam válidas.

Verificações efetivas novas:

- Check e build passam; novas dependências instaladas localmente, auditoria npm retornou zero vulnerabilidades no momento da instalação.
- Desktop 1440×900 e mobile 360×800, 390×844, 430×932 inspecionados. Zero overflow horizontal; logo sem raio/sombra, recorte e contraste observados no cabeçalho e rodapé. Máscara de luminância confirmada no navegador. Bordas preservam raster, não são vetorizadas.
- Menu mobile abre/fecha; Escape retorna foco. Todos os seis contatos apontam para wa.me/554834127737 com mensagem coerente única; não enviada.
- Galeria Embla: avanço pelo botão no celular, Home/End e limites 01/03–03/03 no desktop, arraste de mouse confirmado 01/03→02/03. Gesto de toque real não executado em aparelho físico.
- Construção observada da estrutura à cobertura/esquadrias/conclusão e atalho de pular. Idle em repouso e paused fora do hero confirmados. ?motion=reduce mostra poster e nenhum canvas. Preferência do sistema atendida pelo código; não alterada no computador. Falha física de GPU não provocada.
- Imagens carregadas, console sem erros/avisos relevantes na inspeção. Capturas finais qa-v06-desktop-1440.jpg, qa-v06-mobile-390.jpg, qa-v06-mobile-static-430.jpg e qa-v06-footer-desktop.jpg em docs/qa. Capturas qa-v05 são históricas, não prova desta revisão.

Limites: fonte da logo pequena; solicitar original oficial para acabamento de alta definição. Dispositivo físico, auditoria integral de acessibilidade e Core Web Vitals não medidos. Autorização comercial de imagens/logo, aprovação do cliente e validação final de dados ainda pendentes. Próxima ação: apresentar a versão local 0.6.0; não publicar automaticamente. Nenhum push/deploy ou mensagem ao cliente.

## Revisão escura de 01/10/2026 — versão local 0.5.0

Decisão vigente: último pedido do usuário substitui os fundos claros e qualquer verde de interface por preto/grafite, textos brancos e contraste neutro. Perfil oficial reconsultado no navegador: logo circular preta/branca e destaques monocromáticos sustentam a direção. Fontes, proporções, superfícies e luz são interpretações editoriais propostas, não um manual oficial de marca. Hotle, Kontra e vídeo enviado foram examinados como referências de composição/movimento, sem copiar identidade ou dados.

Implementado: dark.css em todo o site/build; navegação com vidro preto, hero escuro, serviços grafite, galeria preta e encerramento escuro. CTAs brancos, controles discretos, curvas consistentes e profundidade moderada. Casa clara integrada por luz frontal/de recorte, ambiente neutro e suavização de bordas; verde restrito à vegetação, sem recolorir projetos oficiais. Câmera adaptada ao aspecto mobile/tablet. Segunda passagem corrigiu fachada cortada em tablet, recorte/integração do fallback e detalhes da cobertura revelados antes do apoio: cada etapa agora compartilha um plano de corte mundial.

Blender: novo editável blender/residencia-rincao-dark.blend, script dark_presentation.py, renders Cycles 2000×1100 e 1100×1100; assets/house-dark.webp (132.808 bytes) e house-dark-mobile.webp (61.114 bytes). Modelo GLB anterior preservado (867.196 bytes); shader/luz web adaptados no código, não um render idêntico ao Cycles. Originais de referência e versão anterior preservados. Comparação lado a lado em blender/comparacao-dark-referencia.png; composição de referência/prévia em docs/qa/comparacao-direcao-v05.png.

Verificações novas desta rodada:

- npm run check e npm run build passaram; dark.css, posters e recursos 3D incluídos na saída. Sem nova dependência, push, deploy ou mensagem ao cliente.
- Hero inspecionado em 375×812, 430×932, 768×1024, 1024×900 e 1440×900; overflow horizontal zero. Capturas qa-v05-* distinguem esta versão do histórico.
- Construção observada em desktop: base/estrutura, fechamentos, cobertura, esquadrias e casa completa. Revelação corrigida e câmera fixa. Cena pausada fora do hero e idle em repouso; CTA continua disponível.
- Carrossel: setas no celular, Home/End no desktop; posição 01/03 e 03/03 confirmada e limites desabilitados. Arraste/toque preservados do código existente; gesto físico em aparelho real não foi repetido nesta rodada.
- Menu mobile/Escape/foco conferidos. Imagens da marca/projetos/planta/posters carregadas. Todos os seis destinos de contato iguais a wa.me/554834127737, com mensagem única sobre projeto/orçamento; não enviada.
- ?motion=reduce e ?renderer=static inspecionados em desktop/mobile: zero canvas, poster carregado e controles de construção ocultos. Preferência do sistema não foi alterada; falha real de GPU não foi provocada.
- Cores calculadas dos principais fundos/textos/CTAs são neutras, sem verde na interface. Console sem erros/avisos na inspeção. Contraste e foco revistos visualmente; não equivale a auditoria integral WCAG ou medição formal de Core Web Vitals.

Avaliação visual: a nova versão aproxima o contraste, a escala arquitetônica e a continuidade editorial das referências, mantendo a marca real. O estudo não reproduz o paisagismo, a luz solar nem a precisão do render oficial; esses limites não foram ocultados. Referência é render, não foto; medidas e partes ocultas continuam aproximadas. Pendentes: autorização comercial de logo/imagens, original vetorial, confirmação de contato/endereço/escopo e aprovação do cliente. Próxima ação: apresentar a prévia local 0.5.0 e colher retorno; não publicar automaticamente.

## Rodada concluída em 01/10/2026 — versão local 0.4.0

Decisão vigente: referências Hotle, Kontra, NeoVision e vídeo do usuário; acabamento de hierarquia, curvas e profundidade solicitado posteriormente. Marca continua monocromática, com logotipo oficial e materiais reais do perfil. Figma não conectado: refinamento feito no código e navegador. Nenhum push/deploy ou mensagem ao cliente.

Implementação final: casa maior, câmera fixa à altura da fachada, terreno contínuo sem placa, remoção da frase decorativa repetida e dos modos 3D extras. Piso contínuo corrige a sobreposição preta da varanda. Modelo editável salvo em blender/residencia-rincao.blend; GLB otimizado 867.196 bytes. Render Cycles desktop e render próprio para mobile; comparação atual em blender/comparacao-referencia-modelo.png. Scripts editorial_pass.py e mobile_poster.py registram as últimas decisões. Gramado web com grão sutil, sem bandas repetitivas.

Acabamento: imagens/carrossel/superfícies com raios de 20/26 px; botões em cápsula; transparência e desfoque no cabeçalho/legendas; profundidade discreta, microinterações e entradas curtas. Texto/contato permanecem disponíveis durante o scroll. Carrossel manual com imagem principal, continuidade, contador, limites, setas, dots, arraste de mouse e teclado. Toque utiliza scroll nativo e não captura rolagem vertical.

Verificações efetivas da revisão final:

- npm run check e npm run build passaram. Modelo exportado e recursos locais presentes no build; referências privadas de inspiração e ferramentas locais não entram em dist.
- Primeira dobra inspecionada em 375×812, 430×932, 768×1024, 1024×900 e 1440×900, sem overflow horizontal. Segunda passagem corrigiu enquadramento, piso, textura e recorte do fallback. Capturas qa-v04-* identificam esta versão, não a 0.2.
- Construção observada em desktop/celular: base, estrutura, fechamentos, cobertura, esquadrias e conclusão; câmera fixa, crescimento por planos de corte e acesso ao CTA preservado. Pular para a casa pronta funciona. Cena pausada fora do hero e idle em repouso.
- Menu mobile abre/fecha; Escape devolve foco ao botão. Carrossel testado com próximo, arraste desktop, Home/End e limites; posição 01/03 a 03/03. Gesto físico de toque não foi testado em aparelho real.
- Imagens reais, planta e logotipo carregados; destinos dos CTAs inspecionados: wa.me/554834127737 com mensagem única sobre projeto/orçamento. Nenhuma mensagem enviada.
- ?motion=reduce e ?renderer=static inspecionados: sem canvas, poster carregado, controles de construção ocultos e conteúdo disponível. Preferência real do sistema atendida no código; não foi alterada configuração do computador. Não houve simulação forçada de perda de contexto WebGL.
- Console sem erros relevantes na inspeção. Checks não equivalem a auditoria completa WCAG ou benchmark em celular físico; Core Web Vitals não foram medidos formalmente.

Limites: referência oficial é render, não foto; proporções inferidas de vistas e planta sem cotas. Partes ocultas, fundação, estrutura, interiores e paisagem são aproximações de estudo, não projeto executivo. Confirmação comercial de contato/endereço/escopo, autorização de imagens/logo e arquivo vetorial da marca continuam pendentes. Próxima ação: apresentar a prévia local e obter retorno, sem publicar automaticamente.

## Histórico intermediário de 01/10/2026 — superado pela revisão acima

Pedido vigente: hero impactante, residência do material oficial modelada no Blender, construção somente no hero, identidade monocromática, movimentos discretos e carrossel editorial. Não há autorização de publicação nesta rodada.

Direção implementada: casa pronta na abertura; transição curta para implantação e construção controlada pelo scroll; cena integrada ao fundo, sem painel retangular e sem modos extras. Título e CTA imediatos, indicação de fase/progresso reduzida. Projetos em seção escura, imagens generosas sem remover marcas d'água; arraste de mouse, toque nativo, setas, dots, contador, limites, Arrow/Home/End e movimento reduzido. Planta real substitui ilustração genérica no primeiro contato.

Identidade reconsultada no Instagram oficial em 01/10: logo circular preto/branco, destaques monocromáticos, visualizações arquitetônicas e modelos estruturais. Tons neutros orientam a página; cinzas esverdeados mínimos são interpretação da iluminação/entorno, não cor oficial confirmada. Sem terracota de marca. Logo oficial preservado, disponível apenas em avatar 150 px: solicitar original vetorial antes de publicação comercial.

Referências Pinterest consultadas no navegador: 2674081025095575 (Solar System UI UX, parcialmente limitado por modal de login), 852728510714316067 (Museum of Ancient Art: objeto principal iluminado, tipografia integrada), 655133077031523766 (Explore the Space: composição monocromática com elemento principal grande). As duas imagens enviadas pelo usuário também orientam escala e contraste. Não foram copiadas imagens, marcas, contadores ou estruturas dessas referências.

### Verificações desta rodada até aqui

- Sintaxe de script, gallery, cena, materiais e scripts locais: npm run check passou.
- Build estático passou, antes do último refinamento do Blender; repetir na integração final.
- Contato da bio reconsultado: wa.me/554834127737. Todos os botões recebem o mesmo número e mensagem sobre projeto/orçamento; nenhuma mensagem foi enviada.
- Código do carrossel passou simulações de posições/limites, teclado, arraste, cancelamento vertical, bloqueio de clique após arraste e movimento reduzido. Isso não substitui teste visual em navegador/aparelho.
- Servidor local respondeu HTTP 200 no computador. A aba fornecida pelo navegador está na tela ERR_CONNECTION_REFUSED e sua representação data: é bloqueada pela política do navegador; revisão visual integrada está pendente de recuperar o acesso normal à prévia. Não foram contornadas permissões nem alteradas proteções de rede.
- Capturas abaixo são históricas da versão 0.2.0, não prova da nova composição. Ainda não declarar validadas as cinco larguras nesta rodada.

### Arquivos e aproximações

blender/residencia-rincao.blend editável; scripts de criação/refinamento/exportação em blender/. GLB local em assets/models/residencia-rincao.glb, fases 0–6. Referência é renderização, não fotografia de obra: publicações DXfLBPXj5nQ e DXfA76_DjFo. Planta sem escala, vistas incompletas: medidas, interiores, fundações e estrutura são aproximações ilustrativas. Sem validade técnica/executiva ou simulação certificada de construção.

### Próxima ação

Concluir comparação/render final do Blender e integração do poster; repetir build; recuperar a aba local para segunda inspeção, cinco larguras, sequência completa, menu, galeria, teclado, imagens, console e fallback. Autorização comercial de logo/imagens, contato/endereço/região e aprovação do cliente continuam pendentes. Nenhum push/deploy realizado.

Registro histórico de 30/09/2026, versão **0.2.0**, superado pela revisão 0.4.0 acima. Nenhuma contratação, aprovação ou publicação confirmada.

## Histórico — construção 3D e acabamento de 30/09

Pedido do usuário de 30/09/2026: substituir o diagrama SVG por construção tridimensional real, mantendo a identidade mineral/monocromática. Antes das alterações foram inspecionados código, materiais, README e página completa em desktop/celular. Diagnóstico: hero inicialmente pouco expressivo, desenho e render final de casas diferentes, serviços pouco diferenciados e preenchimento preto indevido no SVG auxiliar.

Implementado: residência original em Three.js/WebGL, implantação, sapatas/vigas, estrutura, alvenaria com aberturas, cobertura/parapeitos, esquadrias, vidro, madeira, interiores e paisagismo. Materiais procedurais, iluminação, reflexos e sombras direcionais/de contato. Elementos crescem nos apoios, sem peças voando. Estudo conceitual explicitamente identificado, não atribuído à empresa e não equivalente a projeto executivo.

Segunda passagem: iluminação com melhor contraste, abertura lateral real, sombra de contato e proporções refinadas. Hero com CTA imediato e atalho para projetos; seis controles acessíveis e residência pronta. Mobile com enquadramento próprio. Importação dinâmica, limites de resolução/sombras, modo compacto e pausa fora da tela/repouso. Fallback estático WebP para movimento reduzido, economia de dados, dispositivos muito limitados e falha de WebGL. Serviços e galeria refinados, renders diferenciados de modelo estrutural. Todos os CTAs usam o mesmo destino público e mensagem sobre projeto/orçamento.

### Verificações novas — 0.2.0

- `npm run check` e `npm run build`: sucesso após última alteração de código.
- 375×812, 430×932, 768×1024, 1024×900 e 1440×900: inspeção visual e overflow horizontal medido em zero. Capturas `docs/qa/qa-hero-*.jpg`.
- Seis fases conferidas visualmente, incluindo fundação, estrutura, paredes/cobertura e acabamento/final. Engine Three.js r186 confirmado no canvas.
- Primeira dobra, serviços, galeria, primeiro contato e rodapé revisados em desktop/celular. Quatro imagens locais carregadas corretamente e sem distorção.
- Menu abre/fecha; Escape devolve foco ao botão; âncora fecha o menu. Galeria avança por botão e ArrowRight; foco visível de 2 px conferido. Destinos WhatsApp e Instagram inspecionados; nenhuma mensagem enviada.
- Cena fora do hero: `paused` confirmado; em repouso: `idle`. Aproximadamente 6.000 triângulos e 292 chamadas incluindo sombras. CPU de render observada em torno de 1–3 ms no navegador de teste; não é benchmark em celular físico nem medição de GPU.
- `?motion=reduce`: zero canvas, poster carregado, controles ocultos e scroll normal em desktop e 375 px. Regra real do sistema inspecionada no código; configuração do sistema operacional não foi alterada.
- Console da prévia normal sem erros/avisos capturados. Áreas e dimensões das imagens reservadas, sem instabilidade visível nas inspeções; Core Web Vitals não foram formalmente medidos.
- PNG da primeira passagem preservado em `docs/qa/house-first-pass.png`, fora do payload. Poster final WebP com 92.932 bytes; módulo local da cena com aproximadamente 564 KB antes da compressão HTTP.

### Pendências vigentes

Fontes oficiais em 30/09/2026: perfil público @dellapucker, bio e materiais publicados; detalhes no README. Galeria aponta ao perfil, pois não há permalinks individuais preservados. Não há fotografia de obra verificada entre os três materiais selecionados; nenhum render é tratado como fotografia.

Confirmar contato/endereço/CEP, região atendida, escopo dos serviços e fluxo de orçamento. Obter autorização de logo/imagens e originais melhores. Sem preços, horários, avaliações, profissionais ou credenciais inventados. Próxima ação: apresentar prévia local e colher validação; testar aparelho físico intermediário antes da publicação comercial. Nenhum push, deploy ou contato externo nesta rodada.

## Histórico — versão anterior em SVG

## Feito

- Leitura das instruções operacionais da raiz, área de trabalhos reais e projetos ativos.
- Perfil público @dellapucker consultado no Instagram pelo navegador. Bio, link de WhatsApp, endereço e serviços anotados no README com fonte e pendências.
- Pasta exclusiva criada. A direção visual interpreta o logo circular monocromático e materiais arquitetônicos publicados: papel mineral, grafite, terracota de marcação e grade técnica.
- Hero com animação progressiva de uma casa durante a rolagem; o diagrama original em SVG revela implantação, base, estrutura, cobertura e aberturas, enquanto a renderização real de projeto é revelada na etapa final.
- Galeria horizontal com navegação por botões e gesto de toque; menu móvel e CTAs para o link público de WhatsApp.
- Imagens locais de três publicações do próprio perfil, mantendo marcas d'água e anotadas como visualizações/projetos.

## Verificações desta etapa

- `npm run check` e `npm run build` executados com sucesso; prévia estática gerada em `dist/`.
- Página aberta em `http://localhost:3012/`; primeira dobra revisada em desktop (1270 × 720) e celulares (390 × 844 e 360 × 800).
- Sequência do hero conferida durante a rolagem: diagrama técnico progride até estrutura e a visualização do projeto é revelada no trecho final. O estado inicial agora já mostra a implantação do terreno.
- Navegação, títulos, contatos e links do WhatsApp presentes na árvore de acessibilidade; galeria contém três imagens reais do perfil e controles anterior/próximo.
- Imagens locais WebP verificadas: 84.684, 191.400 e 257.448 bytes. No celular menor, as cinco legendas de etapa foram compactadas para caber no hero.
- Movimento reduzido tem alternativa estática prevista em CSS; a animação usa SVG e atualização por `requestAnimationFrame`, sem dependências de renderização 3D.

## Pendências e próxima ação

Validar endereço, serviços, fluxo de orçamento e autorização comercial das imagens com a empresa. Nenhuma publicação em repositório foi solicitada ou realizada. Não enviar mensagem à empresa.
