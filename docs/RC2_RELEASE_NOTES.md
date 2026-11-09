# PicoMesh Pro v0.1.0-rc.2 — release notes

**Prerelease, not tested on hardware.** No version of PicoMesh Pro has been run on a PicoMite, PicoCalc or MeshCore radio. Only automated checks have passed.

## New since rc.1

- Channel backup writes a temporary file first, so the old backup stays until the new one is complete.
- Startup mentions when a saved channel list exists.
- The radio clock asks for a typed `SYNC` before jumping forward by more than a day.
- Radio settings warn about frequencies outside the usual LoRa bands.
- Late delivery confirmations are tracked for the nine most recent unconfirmed direct messages.
- New commands set a private channel key on slots 1–7 and the path hash size. Both need a typed `APPLY`.

## Known limitations

- A power cut during the short replace step of an export can leave only `CHANNELS.TMP`. The restore screen points this out.
- Channel keys are visible on screen while you type them. They are never stored or printed.
- Radios without a battery clock can show the `SYNC` prompt after a radio restart.
- Band warnings don't know your region. Check what's legal where you are.
- Everything listed in the [rc.1 notes](RC1_RELEASE_NOTES_DRAFT.md) still applies, except the items changed above.

See the [hardware test plan](UART_COMMAND_RESPONSE_HARDWARE_TEST_PLAN.md) and [evidence log](RC_EVIDENCE_LOG.md).
