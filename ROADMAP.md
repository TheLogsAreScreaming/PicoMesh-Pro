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

## Still required for a final v0.1.0

`v0.1.0-rc.1` was published on 2026-11-08 as a prerelease that has not been tested on hardware.

- [x] Review current `main` and verify all intended fixes are merged (2026-11-07, `082e756`)
- [x] Resolve the High findings (R1, R2) in the [reliability audit](docs/RELIABILITY_AUDIT.md), fixed in source; confirm on hardware below
- [x] Verify CI status on the prerelease commit (`6882ae0`, run 42485276888); repeat for the final commit
- [ ] Run PicoMite/PicoCalc + MeshCore companion hardware tests, recording firmware and wiring
- [ ] Confirm startup, contacts, messages, channel send, backup/restore and reconnect behavior
- [ ] Add real, privacy-safe screenshots (documentation synced with source on 2026-11-07)
- [x] Channel export writes a temp file first (#95); a power cut in the short replace step is a recorded limitation
- [ ] Fix what hardware testing finds, and publish another release candidate if the fixes are significant
- [ ] Confirm wiring and installation instructions for the target firmware
- [ ] Publish the final release only after the release gates are met and the owner approves

See [release-readiness checklist](docs/RC_READINESS_CHECKLIST.md).

## Later enhancements (not release promises)

- [x] Private-channel key command, confirmed against MeshCore firmware source (#98); needs a hardware test
- [x] Path hash size command, confirmed against MeshCore firmware source (#98); needs a hardware test
- [ ] Improve persistent preferences, where safe and supported (startup hint for a saved channel list added in #95; automatic loading waits for hardware testing)
- [x] Run pure MMBasic helpers under MMB4L in CI (#99)
- [ ] Add executable protocol tests or hardware-backed fixtures; the UART code still can't run under MMB4L without a radio
- [x] Compare with [upstream PicoMeshCore](https://github.com/Vigoleis912/PicoMeshCore) and choose a narrow contribution ([comparison](docs/UPSTREAM_COMPARISON.md))
- [ ] Submit that contribution after hardware confirmation and owner approval
- [x] Audit follow-ups: forward-clock prompt and band warning (#96), several pending confirmations (#97)

**Policy:** Mark a source feature implemented when merged, but mark hardware validation complete only after actual device testing. Do not publish an RC as hardware-validated without evidence.
