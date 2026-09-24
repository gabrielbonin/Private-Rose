# CLAUDE.md — Private-Rose (manutenção pessoal)

Cópia pessoal do [Rose](https://github.com/Alban1911/Rose) (skin changer de LoL em Python + plugins JS do Pengu Loader) com a correção do patch 16.19 e o injetor do LTK Manager incluído. O objetivo deste arquivo é deixar rápido consertar a injeção quando um patch novo do League quebrar algo. Responda ao usuário em **português (pt-BR)**.

## Repositórios e branches

| Remote | Repo | Uso |
|---|---|---|
| `origin` | `Alban1911/Rose` | upstream oficial. PR #273 (`fix/patch-16.19-injection`) é a correção enviada a eles |
| `fork` | `gabrielbonin/Rose` (público) | `fix/patch-16.19-injection` (branch do PR) e `rose-16.19` (versão pública, **sem** binários da LTK) |
| `private` | `gabrielbonin/Private-Rose` (privado) | `develop` (padrão) e `main`: correção + binários da LTK assinados |

- **Nunca** envie `injection/tools/ltk_patcher_*` para `origin` ou `fork`: a licença da LTK (`injection/tools/LTK-PATCHER-LICENSE.md`) proíbe redistribuir os binários com a assinatura deles. Nas branches públicas eles ficam no `.gitignore`.
- Correções que valem para o Rose oficial: commit em `fix/patch-16.19-injection` (atualiza o PR). Coisas só pessoais: `develop` do privado.
- Não commitar `cslol-dll.dll`, `Pengu Loader.exe`, `hashes.game.txt`, `.venv`, `Pengu Loader/datastore` (arquivo de runtime).

## Como rodar e testar

- `INICIAR_ROSE.bat` → pede admin; na 1ª vez roda `scripts/setup_from_install.ps1` (copia `cslol-dll.dll` e `Pengu Loader.exe` de `C:\Program Files\Rose\_internal`, cria `.venv`, instala deps sem o `pyinstaller`), depois `.venv\Scripts\python.exe main.py`.
- O Rose **precisa** rodar como administrador e o Rose oficial instalado precisa estar fechado.
- `Pengu Loader.exe` não vem no git (é compilado de `vendor/PenguLoader-1.1.6` no build oficial); o setup copia do Rose instalado.
- Teste real = **Practice Tool** (fila 3140) com uma skin que a conta não tem. O Claude não consegue jogar: peça ao usuário e leia os logs depois.
- Checagem rápida de sintaxe: `.venv/Scripts/python.exe -m py_compile <arquivo>`.

## Fluxo da injeção (onde as coisas quebram)

1. Plugins JS (Pengu) detectam a skin no champ select → backend Python (`threads/`, `pengu/`).
2. Rose força a skin base (skin0) na seleção e extrai o `.fantome` da skin de `%LOCALAPPDATA%\Rose\skins\<champ>\<skin>\` (vem do repo [LeagueSkins](https://github.com/Alban1911/LeagueSkins)).
3. `injection/overlay/overlay_manager.py` → `mk_run_overlay`:
   - `mod-tools.exe mkoverlay` monta o overlay em `%LOCALAPPDATA%\Rose\injection\overlay\DATA\FINAL\...wad.client`;
   - `_restore_wad_headers` copia assinatura + checksum da WAD original do jogo para cada WAD do overlay (**obrigatório desde 16.19**);
   - se `injection/tools/ltk_patcher_host.exe` + `ltk_patcher_dll.dll` existem → `_run_ltk_patcher` (protocolo por stdin/stdout: `config loglevel|flags|prefix`, `start scan`, `stop`; eventos `status <ts> <estado> <msg>`, `error`, `dll ...`);
   - senão → legado `mod-tools.exe runoverlay` + `cslol-dll.dll` (**não funciona no 16.19**).
4. O jogo fica suspenso até o injetor começar; depois é liberado (`injection_manager.resume_game()`).

Constantes em `overlay_manager.py`: `LTK_PATCHER_FLAGS = 4` (`CSLOL_HOOK_OPT_OUT_AH_V1`; bits: 1 disable verify, 2 disable file overlay, 4 opt-out anti-skinhack, 8 full WAD scan), `WAD_HEADER_SIZE = 268`.

## Onde olhar quando quebrar

| Log | Caminho | O que mostra |
|---|---|---|
| Rose | `%LOCALAPPDATA%\Rose\logs\rose_*.log` | fluxo completo; filtrar `INJECT`, `LTK patcher`, `Phase transition` |
| Injetor | `%LOCALAPPDATA%\Rose\logs\rose_runoverlay_*.log` | saída do `ltk_patcher_host`/`runoverlay` e da DLL (linhas `dll ...`) |
| Jogo | `C:\Riot Games\League of Legends\Logs\GameLogs\<data>\*_r3dlog.txt` | erro fatal do próprio jogo (últimas linhas) |
| Launcher | `%LOCALAPPDATA%\Rose\logs\log_updater_*.log` | update, hashes, download de skins |

Sinal de crash durante a partida no log do Rose: `Phase transition: InProgress → Reconnect`. `SOFT_REPAIR` em `C:\Riot Games\League of Legends\` = o jogo mandou o cliente reparar a instalação.

## Assinaturas de falha conhecidas (histórico do 16.19)

| Sintoma | Evidência | Causa | Correção |
|---|---|---|---|
| Jogo trava na inicialização (processo "não respondendo", 1 núcleo a 100%) | `rose_runoverlay`: só `[DLL] info: Init in process!`; r3dlog para em `Creating X3D device` | DLL do cslol incompatível com o executável novo | usar o injetor da LTK atualizado |
| Jogo abre sem skin | `dll ... ERROR ... overlay verification failed, disabling overlay ... base-skin check: skin0 is another skin` | anti-skinhack da DLL nova | flag `4` (`OPT_OUT_AH_V1`) |
| Jogo cai ~0,5 s depois de `redirected wad`, cliente "reparando" | r3dlog: `FATAL ERROR - Installation is corrupt. WadFile mount failed ... Problem: Corrupt` | cabeçalho da WAD do mkoverlay (assinatura própria, checksum 0) | `_restore_wad_headers` |
| `runoverlay failed with return code: 1/15` após `Reconnect` | log do Rose | consequência de um dos crashes acima | tratar a causa |

Sucesso no `rose_runoverlay`: `dll attached` → `overlay verified N wad(s)` → `redirected wad: DATA/FINAL/Champions/<Campeão>.wad.client` → no fim, `stop requested` (o tempo nessa linha ≈ duração da partida).

## Checklist quando sair um patch novo

1. Pegar os logs acima da partida que falhou e classificar pela tabela.
2. Conferir a versão do jogo: `(Get-Item "C:\Riot Games\League of Legends\Game\League of Legends.exe").VersionInfo.FileVersion`.
3. **Injetor/DLL:** ver se a LTK publicou DLL nova — commits `chore: refresh dll` em `src-tauri/resources/` de [ltk-manager](https://github.com/LeagueToolkit/ltk-manager) e as [releases](https://github.com/LeagueToolkit/ltk-manager/releases). Atualizar = copiar `ltk_patcher_host.exe` + `ltk_patcher_dll.dll` da instalação nova do LTK Manager (`%LOCALAPPDATA%\LTK Manager`) para `injection/tools` e conferir `Get-AuthenticodeSignature` = `Valid`. O cslol-manager está em modo manutenção (último "refresh cslol dll": abril/2026).
4. **Formato de WAD:** `python scripts/diag/wad_inspect.py <WAD do jogo> <WAD do overlay>` — versão (hoje 3.4), assinatura/checksum iguais, contagem de entradas. Se a versão da WAD mudar, o `mod-tools.exe` (de jul/2026) pode precisar de atualização.
5. **Skins (conteúdo):** o mantenedor regenera o LeagueSkins a cada patch com um commit chamado `26.<patch>` (ex.: `26.18` em 10/09/2026, 10.614 `.fantome`). O launcher do Rose baixa sozinho. No 16.19 as skins antigas funcionaram — só suspeite delas se a WAD estiver íntegra e o crash acontecer ao carregar o campeão.
6. **Mudanças de campos nos `.bin`:** `scripts/diag/propbin.py` lê/escreve PROP bins (roundtrip byte a byte). Ex.: no 16.19 a Riot adicionou em `SkinCharacterDataProperties` o campo `0xa977f4ae` (int32 = id completo da skin); não foi necessário para as skins funcionarem.
7. Sempre que possível, olhar o que a LTK fez: [league-toolkit](https://github.com/LeagueToolkit/league-toolkit) (`crates/ltk_wad`, `rebase.rs` mantém o cabeçalho original) e `ltk-manager` (`crates/ltk-manager-core/src/patcher/`).

## Formatos (referência rápida)

- **WAD v3.4:** `RW` + versão (4 B), assinatura RSA (256 B), checksum (8 B), `u32` n.º de entradas em 268, TOC a partir de 272 com entradas de 32 B (`<QIIIBBHQ>`: path hash xxh64 do caminho minúsculo, offset, tamanho comprimido, tamanho real, tipo|subchunks<<4, duplicado, índice do 1º subchunk, checksum xxh3_64 dos dados). Tipos: 0 raw, 3 zstd, 4 zstd em subchunks (tabela em `<wad>.subchunktoc`).
- **`.fantome`:** zip com `META/info.json` + `WAD/<Campeão>.wad.client`. O carregador de skin é um `skin0.bin` que é o `SkinCharacterDataProperties` + `ResourceResolver` da skin N renomeados para `Skin0`, com link para `DATA/Characters/<Campeão>/Skins/SkinN.bin`.
- **PROP bin:** `PROP`, versão, lista de links, tipos das entradas, entradas (hash FNV-1a minúsculo do nome como chave).

## Outras armadilhas

- `main/__init__.py` exige a `cslol-dll.dll` com hash em `_VALID_DLL_HASHES` para o Rose iniciar, mesmo usando o injetor da LTK.
- O updater (`launcher/update/update_installer.py`) espelha a instalação com `robocopy /MIR`; arquivos fornecidos pelo usuário precisam estar em `PERSISTENT_USER_FILES` e no `/XF`.
- O `.bat` precisa de fim de linha CRLF (`.gitattributes`: `*.bat -text`); o cmd falha nos `goto` com LF.
- Ao rodar o Rose de teste, o Pengu (`rundll32 ... core.dll`) continua preso ao cliente até ele fechar — é normal os botões do Rose continuarem aparecendo.
- A API do GitHub via WebFetch costuma dar 403/rate limit; use `git fetch`/`git ls-remote` ou clones rasos para investigar repositórios externos.
