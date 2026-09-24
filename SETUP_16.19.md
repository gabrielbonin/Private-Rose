# Rose — patch 16.19 fix / correção do patch 16.19

**[Português](#português)** · **[English](#english)**

Unofficial build of Rose with the fix from [PR #273](https://github.com/Alban1911/Rose/pull/273), to use until the PR is merged and an official release ships.

---

## Português

### Por que isto existe
O patch 16.19 do League quebrou a injeção do Rose em três pontos (detalhes no [PR #273](https://github.com/Alban1911/Rose/pull/273)):
1. a `cslol-dll.dll` antiga trava o jogo na inicialização;
2. a DLL nova recusa as skins do Rose pela verificação anti-skinhack;
3. o jogo recusa as WADs do `mkoverlay` como "instalação corrompida" e manda reparar o cliente.

Este código corrige os três. A correção do item 1 usa o **injetor do LTK Manager** (`ltk_patcher_host.exe` + `ltk_patcher_dll.dll`), que a League Toolkit atualizou para o 16.19.

### Por que o injetor da LTK não vem junto
A licença da LTK (`LTK-PATCHER-LICENSE.md`, no repositório do [LTK Manager](https://github.com/LeagueToolkit/ltk-manager)) não permite redistribuir os binários com a assinatura digital deles. Então **cada pessoa instala o LTK Manager oficial** no próprio PC, e o `INICIAR_ROSE.bat` copia o injetor dessa instalação. Nada é baixado nem redistribuído por este repositório.

### Pré-requisitos (uma vez só)
1. **Rose oficial instalado** em `C:\Program Files\Rose`, já aberto pelo menos uma vez e com a `cslol-dll.dll` configurada.
2. **LTK Manager oficial** (v1.21.0 ou mais novo): https://github.com/LeagueToolkit/ltk-manager/releases — só precisa estar instalado.
3. **Python 3.11 ou mais novo**: https://www.python.org/downloads/ — marque **"Add python.exe to PATH"** na instalação.

### Como usar
1. Baixe este repositório (botão **Code → Download ZIP**) e extraia.
2. Feche o Rose oficial (ícone da rosa na bandeja → Sair). Se ele abre com o Windows, desative isso nas configurações dele.
3. Dê dois cliques em **`INICIAR_ROSE.bat`** e aceite o pedido de administrador. Na primeira vez ele prepara tudo (1–2 minutos).
4. Deixe a janela preta aberta enquanto joga.
5. Se os botões do Rose não aparecerem no cliente, feche e abra o cliente do League.

### Problemas
- Logs: `%LOCALAPPDATA%\Rose\logs` (`rose_*.log` e `rose_runoverlay_*.log`).
- LTK Manager atualizado? Apague `injection\tools\ltk_patcher_host.exe` e rode o `INICIAR_ROSE.bat` de novo.
- Sem o injetor da LTK o Rose volta para a `cslol-dll.dll` antiga, que **não funciona no 16.19** (o jogo trava).

---

## English

### Why this exists
League patch 16.19 broke Rose's injection in three places (details in [PR #273](https://github.com/Alban1911/Rose/pull/273)):
1. the legacy `cslol-dll.dll` hangs the game at startup;
2. the new DLL's anti-skinhack check rejects Rose's skins;
3. the game rejects `mkoverlay` WADs as a "corrupt installation" and triggers a client repair.

This code fixes all three. Fix #1 uses the **LTK Manager patcher** (`ltk_patcher_host.exe` + `ltk_patcher_dll.dll`), which League Toolkit updated for 16.19.

### Why the LTK patcher is not included
The LTK license (`LTK-PATCHER-LICENSE.md` in the [LTK Manager](https://github.com/LeagueToolkit/ltk-manager) repo) does not allow redistributing the binaries with their code signature. So **everyone installs the official LTK Manager** on their own PC, and `INICIAR_ROSE.bat` copies the patcher from that install. This repo downloads and redistributes nothing.

### Requirements (one time)
1. **Official Rose installed** in `C:\Program Files\Rose`, opened at least once, with `cslol-dll.dll` set up.
2. **Official LTK Manager** (v1.21.0 or newer): https://github.com/LeagueToolkit/ltk-manager/releases — it only needs to be installed.
3. **Python 3.11 or newer**: https://www.python.org/downloads/ — tick **"Add python.exe to PATH"** during install.

### Usage
1. Download this repo (**Code → Download ZIP**) and extract it.
2. Quit the official Rose (rose icon in the tray → Quit). If it starts with Windows, turn that off in its settings.
3. Double-click **`INICIAR_ROSE.bat`** and accept the administrator prompt. The first run sets everything up (1–2 minutes).
4. Keep the black console window open while you play.
5. If Rose's buttons don't show in the client, restart the League client.

### Troubleshooting
- Logs: `%LOCALAPPDATA%\Rose\logs` (`rose_*.log` and `rose_runoverlay_*.log`).
- Updated LTK Manager? Delete `injection\tools\ltk_patcher_host.exe` and run `INICIAR_ROSE.bat` again.
- Without the LTK patcher Rose falls back to the legacy `cslol-dll.dll`, which **does not work on 16.19** (the game hangs).
