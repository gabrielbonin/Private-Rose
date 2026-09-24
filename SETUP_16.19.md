# Rose — patch 16.19 fix / correção do patch 16.19 (private)

**[Português](#português)** · **[English](#english)**

Private, personal copy of Rose with the fix from [PR #273](https://github.com/Alban1911/Rose/pull/273) and the LTK patcher bundled. For anyone else, use the public branch [`rose-16.19`](https://github.com/gabrielbonin/Rose/tree/rose-16.19).

---

## Português

### Por que isto existe
O patch 16.19 do League quebrou a injeção do Rose em três pontos (detalhes no [PR #273](https://github.com/Alban1911/Rose/pull/273)):
1. a `cslol-dll.dll` antiga trava o jogo na inicialização;
2. a DLL nova recusa as skins do Rose pela verificação anti-skinhack;
3. o jogo recusa as WADs do `mkoverlay` como "instalação corrompida" e manda reparar o cliente.

Este código corrige os três. A correção do item 1 usa o **injetor do LTK Manager** (`ltk_patcher_host.exe` + `ltk_patcher_dll.dll`), que a League Toolkit atualizou para o 16.19.

### Injetor da LTK incluído (uso pessoal)
Esta cópia privada já traz em `injection\tools` o injetor oficial do LTK Manager **v1.21.0**, sem modificações e com a assinatura original da League Toolkit, junto com a licença (`injection\tools\LTK-PATCHER-LICENSE.md`). A licença não permite redistribuir os binários com a assinatura deles, então **não publique nem compartilhe esta cópia**. Para outras pessoas, use a branch pública [`rose-16.19`](https://github.com/gabrielbonin/Rose/tree/rose-16.19), em que cada um instala o LTK Manager.

### Pré-requisitos (uma vez só)
1. **Rose oficial instalado** em `C:\Program Files\Rose`, já aberto pelo menos uma vez e com a `cslol-dll.dll` configurada.
2. **Python 3.11 ou mais novo**: https://www.python.org/downloads/ — marque **"Add python.exe to PATH"** na instalação.

### Como usar
1. Baixe este repositório: logado no GitHub, **Code → Download ZIP** e extraia; ou com Git: `git clone https://github.com/gabrielbonin/Private-Rose "%USERPROFILE%\Desktop\Rose"` (na primeira vez abre o navegador para login).
2. Feche o Rose oficial (ícone da rosa na bandeja → Sair). Se ele abre com o Windows, desative isso nas configurações dele.
3. Dê dois cliques em **`INICIAR_ROSE.bat`** e aceite o pedido de administrador. Na primeira vez ele prepara tudo (1–2 minutos).
4. Deixe a janela preta aberta enquanto joga.
5. Se os botões do Rose não aparecerem no cliente, feche e abra o cliente do League.

### Atualizar
- Com Git: `git -C "%USERPROFILE%\Desktop\Rose" pull`
- Com ZIP: baixe de novo (pode copiar a pasta `.venv` da cópia antiga para não reinstalar).

### Manutenção
- Logs: `%LOCALAPPDATA%\Rose\logs` (`rose_*.log` e `rose_runoverlay_*.log`).
- Nova versão do injetor da LTK: substitua `ltk_patcher_host.exe` e `ltk_patcher_dll.dll` em `injection\tools` pelos da instalação nova do LTK Manager (ficam na pasta de instalação dele, normalmente `%LOCALAPPDATA%\LTK Manager`).
- Sem o injetor da LTK o Rose volta para a `cslol-dll.dll` antiga, que **não funciona no 16.19** (o jogo trava).

---

## English

### Why this exists
League patch 16.19 broke Rose's injection in three places (details in [PR #273](https://github.com/Alban1911/Rose/pull/273)):
1. the legacy `cslol-dll.dll` hangs the game at startup;
2. the new DLL's anti-skinhack check rejects Rose's skins;
3. the game rejects `mkoverlay` WADs as a "corrupt installation" and triggers a client repair.

This code fixes all three. Fix #1 uses the **LTK Manager patcher** (`ltk_patcher_host.exe` + `ltk_patcher_dll.dll`), which League Toolkit updated for 16.19.

### LTK patcher bundled (personal use)
This private copy ships the official LTK Manager **v1.21.0** patcher in `injection\tools`, unmodified and carrying League Toolkit's original signature, plus its license (`injection\tools\LTK-PATCHER-LICENSE.md`). The license does not allow redistributing the binaries with their signature, so **do not publish or share this copy**. For anyone else, use the public [`rose-16.19`](https://github.com/gabrielbonin/Rose/tree/rose-16.19) branch, where each person installs LTK Manager.

### Requirements (one time)
1. **Official Rose installed** in `C:\Program Files\Rose`, opened at least once, with `cslol-dll.dll` set up.
2. **Python 3.11 or newer**: https://www.python.org/downloads/ — tick **"Add python.exe to PATH"** during install.

### Usage
1. Get this repo: signed in to GitHub, **Code → Download ZIP** and extract it; or with Git: `git clone https://github.com/gabrielbonin/Private-Rose "%USERPROFILE%\Desktop\Rose"` (the first time it opens the browser to sign in).
2. Quit the official Rose (rose icon in the tray → Quit). If it starts with Windows, turn that off in its settings.
3. Double-click **`INICIAR_ROSE.bat`** and accept the administrator prompt. The first run sets everything up (1–2 minutes).
4. Keep the black console window open while you play.
5. If Rose's buttons don't show in the client, restart the League client.

### Updating
- With Git: `git -C "%USERPROFILE%\Desktop\Rose" pull`
- With the ZIP: download it again (you can copy the old `.venv` folder over to skip reinstalling).

### Maintenance
- Logs: `%LOCALAPPDATA%\Rose\logs` (`rose_*.log` and `rose_runoverlay_*.log`).
- New LTK patcher version: replace `ltk_patcher_host.exe` and `ltk_patcher_dll.dll` in `injection\tools` with the ones from the new LTK Manager install (its install folder, usually `%LOCALAPPDATA%\LTK Manager`).
- Without the LTK patcher Rose falls back to the legacy `cslol-dll.dll`, which **does not work on 16.19** (the game hangs).
