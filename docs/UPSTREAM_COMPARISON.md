# Comparison with upstream PicoMeshCore

Compared against [Vigoleis912/PicoMeshCore](https://github.com/Vigoleis912/PicoMeshCore) at `1849967` (2026-03-28, the latest commit on 2026-11-08). Upstream has no open issues. Nothing has been submitted upstream.

| Area | Upstream | PicoMesh Pro |
| --- | --- | --- |
| UART receive buffer | `Open "COM2:115200"` (default 256 bytes) | 2048 bytes, not yet tested on hardware |
| Longest frame | `MAX_FRAME_LEN = 1024`, above MMBasic's 255-character string limit | 252 |
| Send confirmation | `WaitForSendConfirmation(2000)`: fixed 2 s, no ACK code | Matches the ACK code; wait follows the radio's estimate, 2–15 s |

## Suggested contribution

Send one small change: lower `MAX_FRAME_LEN` so a frame fits in an MMBasic string. It's the narrowest of the three and doesn't change the UI.

Before submitting:

1. Confirm the fix on real hardware.
2. Recheck upstream, since it may have changed.
3. Get the owner's approval. PicoMesh Pro never opens a PR upstream without it.
