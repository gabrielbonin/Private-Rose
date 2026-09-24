# Rose com correção para o patch 16.19

Versão não oficial do Rose com a correção do [PR #273](https://github.com/Alban1911/Rose/pull/273), para usar enquanto o PR não é aceito.

## Pré-requisitos (uma vez só)

1. **Rose oficial instalado** (em `C:\Program Files\Rose`) e já aberto pelo menos uma vez, com a `cslol-dll.dll` configurada.
2. **LTK Manager** instalado: baixe o instalador mais recente em https://github.com/LeagueToolkit/ltk-manager/releases. Não precisa usá-lo, só ter instalado — o Rose usa o injetor que vem com ele.
3. **Python 3.11 ou mais novo**: https://www.python.org/downloads/ — na instalação, marque **"Add python.exe to PATH"**.

## Como usar

1. Feche o Rose oficial (ícone da rosa na bandeja → Sair). Se ele abre sozinho com o Windows, desative isso nas configurações dele.
2. Dê dois cliques em **`INICIAR_ROSE.bat`** e aceite o pedido de administrador.
   - Na primeira vez ele prepara tudo (leva 1–2 minutos).
3. Deixe a janela preta aberta enquanto joga.
4. Se os botões do Rose não aparecerem no cliente, feche e abra o cliente do League.

## Problemas

- Os logs ficam em `%LOCALAPPDATA%\Rose\logs` (`rose_*.log` e `rose_runoverlay_*.log`).
- Se o LTK Manager for atualizado, apague `injection\tools\ltk_patcher_host.exe` e rode o `INICIAR_ROSE.bat` de novo para copiar a versão nova.
