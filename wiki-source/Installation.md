# Install on PS Vita

The port is distributed as a VPK. The original game's `game/` data folder must be copied separately after installing the VPK.

## Before you begin

- Have a PS Vita with VitaShell available.
- Download the VPK for this port from the project's published release/source location.
- Obtain the original game from the [creator's page](https://via01.itch.io/dont-open-your-eyes).
- Transfer the original game's `game/` folder to the Vita.

> [!IMPORTANT]
> **MUST KNOW!!** Do not rename the title ID directory. The documented path is `ux0:app/RNPYDNOPE`.

## Install

1. Install the VPK using your normal VitaShell VPK workflow.
2. Open VitaShell and confirm the application directory exists.
3. Copy the original game's `game/` folder into:

```
ux0:app/RNPYDNOPE/
```

4. Confirm that the final layout contains:

```
ux0:app/RNPYDNOPE/game/
```

5. Launch the game from the LiveArea.

## Verify

- The application appears in the Vita LiveArea.
- The `game/` directory is inside the exact title-ID folder.
- The game starts without reporting missing content files.

See [Game files and paths](Game-Files-and-Paths) if the application opens but does not find its content.
