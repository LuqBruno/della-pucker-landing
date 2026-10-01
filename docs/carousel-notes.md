# Carrossel manual — revisão de 01/10/2026

`gallery.js` expõe `window.initProjectGallery()`. Carregar com `defer` **antes** de `script.js`; no script principal remover os handlers antigos de galeria e chamar a função uma vez. Chamadas repetidas retornam a mesma instância. A instância oferece `go(index)`, `measure()` e `destroy()`.

Contrato: `.projects-section` contém `.project-track`, artigos `.project-item`, setas `[data-project-scroll="-1"]`/`[data-project-scroll="1"]`, um texto `.gallery-position` com `aria-live="polite"` e botões `[data-project-index="0"]`, `1`, `2`. Número de projetos detectado automaticamente. Setas usam atributo nativo `disabled`; dots recebem `aria-current` e rótulos. Não há reprodução automática.

CSS necessário: overflow horizontal nativo, flex, `scroll-snap-type:x mandatory`, `scroll-snap-align:start`, slides sem encolher. Reservar proporções das imagens. Recomenda-se `touch-action:pan-x pan-y`, `.project-track {cursor:grab}` e `.project-track.is-dragging {cursor:grabbing}`; controles de toque com pelo menos 44 px. A distinção de gesto vertical/horizontal no celular é responsabilidade do scroll nativo, sem eventos de toque interceptados.

Arraste por mouse ativa somente após deslocamento horizontal maior que 8 px e 1,2× o vertical; preserva cliques normais nos links. Durante o arraste a captura do ponteiro mantém continuidade, snap e seleção são suspensos temporariamente; no fim são restaurados e a imagem mais próxima é alinhada. Clique originado pelo arraste é bloqueado. Cancelamento, perda da captura e perda de foco restauram o estado. Setas, dots e teclado (←, →, Home, End) avançam manualmente, com movimento reduzido respeitado.

As posições são medidas relativamente ao primeiro artigo e limitadas ao scroll máximo real, incluindo a última imagem. ResizeObserver acompanha mudança de largura e imagens carregadas; indicador e controles refletem o projeto mais próximo. Não exige dependências. Sem JavaScript, artigos e links continuam acessíveis pelo scroll nativo.

Verificação desta subetapa: sintaxe via `node --check gallery.js`; simulação de comportamento em Node com posições de slides reais (0, 1024 e último slide limitado a 1800 px), primeiro/último estado, avanço rápido, Home/End, arraste por mouse, restauração de snap, bloqueio do clique do arraste, gesto vertical preservado e preferência de movimento reduzido. A inspeção no navegador, os recortes e a navegação em celular/desktop pertencem à rodada integrada do agente principal; não são declarados como verificados neste registro.
