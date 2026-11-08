# PicoMesh Pro Roadmap

This document separates **implemented in source** from **validated on hardware**. Source-level regression checks do not prove runtime compatibility with PicoMite or a MeshCore companion radio.

## Implemented in source (hardware verification pending)

- [x] Import upstream MMBasic source and retain GPL-3.0 attribution
- [x] Add local channel listing, selection and radio index mapping
- [x] Guard reserved `#public` channel mapping
- [x] Add channel sending with response/uncertain-delivery feedback
- [x] Add local channel names/indexes export and staged restore (`CHANNELS.TXT`, no keys)
- [x] Validate channel metadata and reject malformed backup files
- [x] Add UART framing, partial-frame timeout recovery and bounded asynchronous response handling
- [x] Add Python source-level regression tests and GitHub Actions workflow
- [x] Document UART command-response and channel restore hardware test scenarios
- [x] Source reliability audit ([RELIABILITY_AUDIT.md](docs/RELIABILITY_AUDIT.md)), with fixes for all 13 findings except atomic export (#83–#92)
- [x] Simulated contact, direct-send, polling, channel and UART-interruption scenarios
- [x] Hardware tester program and issue form
- [x] Version banner at startup (`gAppVersion$`)

## Still required for v0.1.0-rc.1

- [x] Review current `main` and verify all intended fixes are merged (2026-11-07, `082e756`)
- [x] Resolve the High findings (R1, R2) in the [reliability audit](docs/RELIABILITY_AUDIT.md), fixed in source; confirm on hardware below
- [ ] Verify CI status on the exact candidate commit
- [ ] Run PicoMite/PicoCalc + MeshCore companion hardware tests, recording firmware and wiring
- [ ] Confirm startup, contacts, messages, channel send, backup/restore and reconnect behavior
- [ ] Add real, privacy-safe screenshots (documentation synced with source on 2026-11-07)
- [ ] Decide on atomic channel export (audit R13) or record it as a known limitation
- [ ] Record limitations and publish release notes only after the release gates are met

See [release-readiness checklist](docs/RC_READINESS_CHECKLIST.md).

## Later enhancements (not release promises)

- [ ] Confirm firmware support for private-channel key configuration and implement with secret redaction
- [ ] Investigate firmware support for path hash size selection
- [ ] Improve persistent preferences, where safe and supported
- [ ] Add executable MMBasic protocol tests or hardware-backed fixtures beyond static source checks
- [ ] Compare current [upstream PicoMeshCore](https://github.com/Vigoleis912/PicoMeshCore) and prepare a narrow contribution for maintainer review

**Policy:** Mark a source feature implemented when merged, but mark hardware validation complete only after actual device testing. Do not publish an RC as hardware-validated without evidence.
