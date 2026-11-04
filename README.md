# 🌹 Rose - Effortless Skin Changer for LoL

<div align="center">

  <img src="./assets/icon.png" alt="Rose Icon" width="128" height="128">

[![Installer](https://img.shields.io/badge/Installer-Windows-32A832)](https://github.com/Alban1911/Rose/releases/latest) [![Ko-Fi](https://img.shields.io/badge/KoFi-Donate-C03030?logo=ko-fi&logoColor=white)](https://ko-fi.com/roseapp) [![Discord](https://img.shields.io/discord/1490473857075642621?color=32A832&logo=discord&logoColor=white&label=Discord)](https://discord.com/invite/roseskins) [![License](https://img.shields.io/badge/License-MIT-C03030)](LICENSE) [![Downloads](https://img.shields.io/github/downloads/Alban1911/Rose/total?color=32A832&label=Downloads&cacheSeconds=86400)](https://github.com/Alban1911/Rose/releases/latest)


</div>

---

> [!IMPORTANT]
> **Branch `rose-1.5.0` do Private-Rose (uso pessoal).** Rose 1.5.0 rodando a partir do código, antes do instalador oficial. Veja [Rose 1.5.0 local](#rose-150-local-private-rose) logo abaixo.

## Rose 1.5.0 local (Private-Rose)

### Por que esta branch existe

- **04/11/2026:** depois do patch do League, o Rose 1.4.9 parou de injetar skins. A DLL do LTK que ele usa (1.29.2) só aceita versões do jogo até 01/11/2026 (`LTK patcher does not support game builds after 2026-11-01 04:00`).
- **A DLL nova do LTK não resolve no 1.4.9.** Desde a 1.32, o LTK Manager baixa a DLL à parte, e o Rose 1.4.9 a recusa ("not a recognized LTK patcher DLL"). Testamos e confirmamos.
- **O Rose 1.5.0 muda o modelo.** Em vez de usar a DLL e o host do LTK, ele controla o próprio LTK Manager pela ponte LeagueToolFlop (LTF). O código saiu em 04/11/2026, antes do instalador.

Esta branch é o código oficial da 1.5.0 (`f645bac`) mais um commit nosso.

### O que mudamos

| Arquivo | Mudança | Motivo |
| --- | --- | --- |
| `config.py` | `INJECTION_THRESHOLD_MAX_S` de 2.0 para 4.0 | Com o limite em 1 s, o patcher começava depois de a partida ser criada (`joined too late`). |
| `Pengu Loader/plugins/ROSE-SettingsPanel/index.js` | `THRESHOLD_MAX_S` de 2.0 para 4.0 | O controle de **Limite de injeção** nas Configurações acompanha o novo máximo. |
| `run_dev.bat` | Arquivo novo | Abre o Rose pelo código, como administrador. |

**Nesta branch não entra:**
- O `ltk_launcher.exe` e o `LeagueToolFlop.dll` compilados.
- O `Pengu Loader.exe`.
- Os arquivos do LTK.

Os dois primeiros itens já são excluídos pelo `.gitignore` do Rose. Por isso a branch não leva nenhum arquivo assinado pelo LTK, e cada PC monta o seu.

### Requisitos

- **Windows com o Rose oficial já instalado e aberto uma vez.** Ele baixa as skins para `%LOCALAPPDATA%\Rose` e fornece o Pengu Loader.
- **LTK Manager 1.33.0 ou mais novo**, instalado pelo [instalador oficial](https://github.com/LeagueToolkit/ltk-manager/releases/latest). Abra uma vez e inicie o patcher, para ele baixar a DLL dele.
- **Python 3.13.**
- **Visual Studio C++ Build Tools** com o compilador x64, para compilar o LTF.

### Como montar num PC

```bat
git clone -b rose-1.5.0 https://github.com/gabrielbonin/Private-Rose.git Rose-1.5.0
cd Rose-1.5.0
python -m venv .venv
findstr /v /i pyinstaller requirements.txt > requirements-run.txt
.venv\Scripts\python -m pip install -r requirements-run.txt
.venv\Scripts\python scripts\build_ltf.py
copy "C:\Program Files\Rose\_internal\Pengu Loader\Pengu Loader.exe" "Pengu Loader\"
copy "C:\Program Files\Rose\_internal\Pengu Loader\Pengu Loader.exe.config" "Pengu Loader\"
```

- O `pyinstaller==6.3.0` fica de fora porque não existe para o Python 3.13 e só serve para gerar o `.exe`.
- O `build_ltf.py` gera o `injection\tools\ltk_launcher.exe` e o `injection\tools\LeagueToolFlop.dll`. Um aviso sobre `vswhere.exe` pode aparecer e não atrapalha.

### Como usar

1. Feche o Rose instalado, pelo ícone perto do relógio, e feche o LTK Manager. O launcher da 1.5.0 se recusa a assumir um LTK Manager já aberto.
2. Abra o `run_dev.bat` e aceite o pedido de administrador.
3. Em **Configurações**, deixe o **Limite de injeção** em **2 s** e clique em **Salvar**. Se aparecer `joined too late` no log, suba para 2,5 ou 3 s.
4. Escolha a skin antes do fim da contagem. Uma troca feita depois do limite é ignorada.

Na contagem regressiva da seleção, o Rose abre o LTK Manager escondido, importa a skin, desativa as outras skins do perfil do LTK só para aquela partida e inicia o patcher.

### Testado em 04/11/2026

- **Practice Tool:** com limite de 1,11 s, a skin não apareceu, três vezes (`joined too late`, de 1,4 a 1,6 s de atraso). Com 2 s, a primeira tentativa atrasou 0,1 s, e a seguinte funcionou, com a K/DA Firestarter Ignition Akali.
- **Partida normal:** ainda não testada.

### Avisos

- **Verificação do LTK:** a 1.5.0 abre o LTK Manager como se ele tivesse sido iniciado pelo Windows Explorer, para passar pela verificação do patcher do LTK (`VRF00000008`). Isso está em `native/ltf/VENDORED.md`. O LTK pode bloquear isso numa atualização futura, e antivírus podem desconfiar.
- **Licença do patcher do LTK** (`LTK-PATCHER-LICENSE.md`, no repositório do LTK Manager): permite usar o patcher em outros programas. Quem distribuir os arquivos dele fora do instalador oficial precisa remover a assinatura do LTK. Por isso esta branch não leva esses arquivos.
- **Riscos:** projeto não oficial, sem afiliação com a Riot Games. Use por sua conta e risco.

### Quando sair o instalador oficial

Instale o Rose 1.5.0 oficial e volte a usar o atalho normal. Esta branch deixa de ser necessária. Se o limite de 2 s também for curto no oficial, vale sugerir ao Rose aumentar o máximo.

### Atualizar com o Rose oficial

```bat
git remote add upstream https://github.com/Alban1911/Rose
git fetch upstream
git merge upstream/main
.venv\Scripts\python scripts\build_ltf.py
```

---

## Overview

Rose is an open-source automatic skin changer for League of Legends that enables seamless access to all skins in the game. The application runs silently in the system tray and automatically detects skin selections during champion select, injecting the chosen skin when the game loads.

Built on the [Pengu Loader](https://github.com/PenguLoader/PenguLoader) framework, Rose integrates JavaScript extensions into the League Client to enable modular UI interactions. It strictly modifies local rendering variables to display custom models and textures. It is designed purely as an exploration of client-side asset management, providing no manipulation of network data, memory states, or gameplay mechanics, thereby **offering zero competitive advantage**.

## Architecture

Rose consists of three main components:

### Python Backend

- **LCU API Integration**: Communicates with the League Client via the League Client Update (LCU) API
- **Skin Injection**: Handles skin injection compatible with Riot Vanguard
- **WebSocket Bridge**: Operates a WebSocket server for real-time communication with frontend plugins
- **Skin Management**: Downloads and manages skin files from the [LeagueSkins repository](https://github.com/Alban1911/LeagueSkins)
- **Party Mode**: Enables skin sharing between friends in the same lobby via a Cloudflare WebSocket relay
- **Game Monitoring**: Tracks game state, champion select phases, and loadout countdowns
- **Auto-Updater**: Checks GitHub for new releases and prompts users to install updates
- **Analytics**: Sends a startup ping, a 15-minute presence heartbeat, and a best-effort close ping (configurable, runs in a background thread)

### Analytics and privacy

Rose sends a pseudonymous, randomly generated installation ID and the app version
to `https://analytics.rosekeys.site/` when analytics are enabled. The ID is not derived
from the Windows Machine GUID. Analytics can be disabled with
`ANALYTICS_ENABLED = False` in `config.py`.

The analytics API and dashboard are maintained separately from this public
client repository. Only aggregate usage metrics are exposed through the
dashboard; raw activity and server credentials remain private.

### Cloudflare Workers

- **rose-party-relay**: Durable Object-backed WebSocket relay that manages party rooms (max 10 members per room) for real-time skin selection broadcasting between friends. It refuses Rose versions older than 1.4.4

### Pengu Loader Plugins

Rose includes a suite of JavaScript plugins that extend the League Client UI:

- **ROSE-UI**: Unlocks locked skin previews in champion select, enabling hover interactions on all skins
- **ROSE-SkinMonitor**: Monitors currently selected skin's name and sends it to the Python backend via WebSocket. It also hosts the bridge the other plugins use to talk to Rose
- **ROSE-CustomSkinSelector**: Lists the custom skin mods made for the hovered skin and applies the one you pick
- **ROSE-CustomWheel**: Custom mods panel for maps, fonts, announcers and other mods
- **ROSE-ChromaWheel**: Enhanced chroma selection interface for choosing any chroma variant
- **ROSE-FormsWheel**: Custom form selection interface for skins with multiple forms (Elementalist Lux, Sahn Uzal Mordekaiser, Spirit Blossom Morgana, Radiant Sett)
- **ROSE-SettingsPanel**: Settings panel accessible from the League of Legends Client
- **ROSE-RandomSkin**: Random skin selection feature
- **ROSE-HistoricMode**: Access to the last used skin for every champion
- **ROSE-PartyMode**: Party mode UI — displays a panel in lobby and champion select to enable skin sharing, view connected peers, and see friends' skin selections in real time
- **ROSE-I18n**: Translates Rose's menus into the language picked in Settings, else the League client's
- **ROSE-Jade**: Client customization — regalia borders, backgrounds, banners, icons, titles, and win/loss stats (shipped disabled)

## How It Works

1. **League Client Integration**: Rose activates **[Pengu Loader](https://github.com/PenguLoader/PenguLoader)** on startup, which injects the JavaScript plugins into the League Client. If the client is already open, Rose restarts it so the plugins load (during champion select, the restart waits for the lobby or the end of the game)
2. **Skin Detection**: When you hover over a skin in champion select, `ROSE-SkinMonitor` detects the selection and sends it to the Python backend
3. **Game Opening Delay**: To give the injection time to happen, Rose suspends the game process until the overlay is ready. If Rose closes during that window, it resumes the game the next time it starts
4. **Game Injection**: Rose injects the selected skin when the game starts
5. **Seamless Experience**: The skin loads as if you owned it, with full chroma support and no gameplay impact (Rose will **never** provide any competitive advantage to its users)

## Features

- **Smart Injection**: Never injects skins you already own
- **Custom Mods**: Custom skins, maps, fonts and announcers (`.fantome`, `.zip` and `.modpkg`)
- **Party Mode**: Friends running Rose 1.4.4 or newer see each other's skins and custom mods in game
- **Loading Screen Name**: The loading screen shows the injected skin's name; the chat and the name over your champion keep the champion's
- **Multi-Language Support**: Works with any client language, with Rose's menus in 22 languages
- **Open Source**: Fully open source and extensible
- **Free**: If you bought this software, you got scammed 💀

## Requirements

- **Windows 10/11**
- **League of Legends** installed
- **LTK Manager** - the app Rose applies skins through; Rose finds it on its own (see below)

### LTK Manager Requirement

Rose applies skins through LTK Manager, which it drives over the bridge it
builds from `native/ltf/` (`ltk_launcher.exe` + `LeagueToolFlop.dll`). Install
LTK Manager once and Rose finds it: a path set as `ltkManagerPath` in
`config.ini` wins, then a running instance, then the known install locations.

If Rose can't find LTK Manager, it says so at startup: install it, or click
**Set up path** and select its `ltk-manager.exe` (Rose saves it as
`ltkManagerPath` and starts). You never have to open LTK Manager yourself:
Rose starts it in the background during champ select and closes it after the
game. A running LTK Manager is left alone: Rose only closes the instance it
started itself. The bridge can only load into an LTK Manager Rose starts, so if
yours is already open when a game starts, Rose skips the injection and asks you
in Troubleshooting to close it (also from the system tray).

For each game Rose turns off the mods you enabled in LTK Manager, so only the
selected skin is patched in, and turns them back on afterwards. LTK Manager's
patcher only applies to a game started after it began scanning, so Rose
installs the skin you select while the champ select countdown runs. The skin
selected at the injection threshold (1 to 2 seconds before the countdown ends,
in Settings) is the one applied: a change after it is ignored, so you keep that
skin instead of getting the default one.

## Installation

1. Download the latest installer from [Releases](https://github.com/Alban1911/Rose/releases/latest)
2. Run the installer as Administrator
3. Launch Rose from the Start Menu or desktop shortcut

## Building from source

Rose builds the Pengu Loader executable from the vendored source in
`vendor/PenguLoader-1.1.6/` as part of the normal Rose build. You do not need
to download or commit a prebuilt `Pengu Loader.exe`.

### Prerequisites

- Windows 10/11
- Python 3.11 or newer
- Visual Studio Build Tools with the .NET desktop build tools, WPF support,
  and the .NET Framework 4.7.2 targeting pack (for Pengu Loader), and the
  MSVC C++ build tools with the C++20 workload (for the LTF bridge in
  `native/ltf/`)
- Inno Setup 6 if you also want to create the installer

Clone the repository and enter its directory:

```powershell
git clone https://github.com/Alban1911/Rose.git
cd Rose
```

Install the Python dependencies first:

```powershell
python -m pip install -r requirements.txt
```

Build the loader by itself, if needed:

```powershell
python scripts/build_pengu_loader.py
```

Build Rose (rebuilds the loader and the LTF bridge):

```powershell
python scripts/build_pyinstaller.py
```

The packaged application is written to `dist/Rose/`. To build both Rose and
the Windows installer in one step:

```powershell
python scripts/build_all.py
```

The installer is written to `installer/Rose_Setup_<version>.exe`. Use
`scripts/build_pyinstaller.py` or `scripts/build_all.py` instead of invoking
`pyinstaller Rose.spec` directly, because the Rose build scripts compile
Pengu Loader first.

To create the update package the auto-updater downloads from a release
(`installer/update_package_<version>.zip`, `hashes.game.txt` excluded):

```powershell
python scripts/create_update_package.py
```

## Credits

Rose uses the [official Pengu Loader](https://github.com/PenguLoader/PenguLoader)
project. Its source is vendored and built as part of Rose, with Rose-specific
lifecycle integration added around the loader. Please see the
[official Pengu Loader license](https://github.com/PenguLoader/PenguLoader/blob/main/LICENSE)
and credit the Pengu Loader contributors.

## Contributing

Contributions are welcome. Report bugs and suggest features through the
[issue forms](https://github.com/Alban1911/Rose/issues/new/choose), and ask
for installation help on [Discord](https://discord.com/invite/roseskins).

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup, the tests and
checks that CI runs on every pull request, and the project structure.

## Legal Disclaimer

This project is not endorsed by or affiliated with Riot Games. Riot Games and all related properties are trademarks or registered trademarks of Riot Games, Inc.

Riot Games does not allow custom skins that reproduce its real skins, which is what Rose does. Use Rose at your own risk: its developers are not responsible for any consequence of using it, including account suspensions or bans.

## Support

If you enjoy Rose and want to support its development:

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/roseapp)

Your support helps keep the project alive and motivates continued development!

---

**Rose** - _League, unlocked._
