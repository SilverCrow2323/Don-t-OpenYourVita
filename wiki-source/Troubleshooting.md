# Troubleshooting

Start by checking the application path and the original content folder. This port expects the original game's data to be copied separately.

## Common problems

| Symptom | First check |
|---|---|
| App is not in LiveArea | Confirm the VPK installation completed |
| App opens but content is missing | Check for `ux0:app/RNPYDNOPE/game/` |
| Content folder is in the wrong location | Move `game/` inside `RNPYDNOPE/` |
| Files were copied beside the title-ID folder | Copy the original `game/` directory into the application directory |
| Issue appears only after starting a particular scene | Record the exact scene/action and the error text |

## Report a problem

Include:

- Vita model and firmware, if known.
- Port/VPK version.
- Whether the original game's `game/` folder was copied.
- The exact path used.
- Steps to reproduce and the complete error text.

Do not attach copyrighted game data, account information or unrelated personal files.
