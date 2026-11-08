# PicoMesh Pro v0.1.0-rc.1 — release notes

**Prerelease, not tested on hardware.** This version has never been run on a PicoMite, PicoCalc or MeshCore radio. Only source-level Python checks have passed. Published at the owner's direction on 2026-11-08 so testers can try it.

PicoMesh Pro is an MMBasic terminal client for a PicoMite/PicoCalc connected over UART to a compatible MeshCore companion radio. It builds on Vigoleis912/PicoMeshCore.

## Proposed highlights

- Channel listing and selection, with reserved `#public` mapping protection.
- Channel send workflows and explicit distinction between accepted, queued, delivered and unknown send outcomes.
- Local channel name/index mapping export and staged restore, with malformed-file rejection. Backups do **not** contain private channel keys.
- UART framing length checks, partial-frame timeout handling and bounded asynchronous traffic during selected command-response flows.
- Source-level Python regression tests and GitHub Actions workflow.
- Reliability fixes from the [source audit](RELIABILITY_AUDIT.md), all pending hardware confirmation:
  - Long messages are refused with a clear message instead of stopping the program, and text is limited to what the radio accepts (160 characters direct; channel text minus the node-name prefix the radio adds).
  - "Delivered" is shown only when the confirmation matches the message sent; late confirmations are reported.
  - Contacts sync once per session, and an incomplete sync is retried.
  - Larger UART receive buffer (2048 bytes) and resynchronisation on bad or cut-off frames.
  - Radio time sync is skipped when the Pico clock looks unset; radio settings and TX power are checked and need a typed `APPLY`.
  - Channel scan and import no longer get out of step, and import reports every skipped slot.
  - Legacy direct messages are parsed with the correct layout.
  - Reconnect hint after three unanswered commands; bounded startup and response waits; file errors on channel backup are reported.
- The program shows its version (`0.1.0-rc.1`) at startup and in Device > Show status.

## Known limitations

- Physical PicoMite/PicoCalc and companion radio compatibility is **not yet verified**.
- Python tests inspect source-level invariants; they do not execute MMBasic or validate radio interoperability.
- Private channel key management and path hash size controls are not confirmed features.
- No verified device screenshots are available yet.
- Channel backup export writes `CHANNELS.TMP` first and replaces `CHANNELS.TXT` only when it is complete. A power cut in the brief replace step can leave only `CHANNELS.TMP`, which the restore screen points out.
- Local channel changes are not saved across restarts unless exported.
- Only the most recent unconfirmed direct message is tracked for late confirmation.

## Before publication

- [ ] Choose and record exact candidate commit SHA.
- [x] Change `gAppVersion$` from `0.1.0-dev` to `0.1.0-rc.1` in that commit.
- [ ] Confirm matching GitHub Actions run succeeded; save test artifact URL.
- [ ] Complete and document real hardware smoke tests. **Not done for this prerelease; required before any final release.**
- [ ] Confirm firmware, wiring and installation instructions.
- [ ] Review GPL-3.0 attribution, README, and privacy of included materials.
- [x] Obtain explicit owner approval to publish (2026-11-08, as an untested prerelease).

See [readiness checklist](RC_READINESS_CHECKLIST.md), [evidence log](RC_EVIDENCE_LOG.md) and [hardware test plan](UART_COMMAND_RESPONSE_HARDWARE_TEST_PLAN.md).

**Do not present this prerelease as hardware-validated.**
