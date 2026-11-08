# PicoMesh Pro — volunteer hardware validation

**Status: recruitment plan only. No public beta, release, or hardware certification has been issued.**

We need volunteers with a PicoMite/PicoCalc and a compatible MeshCore UART companion radio. The maintainer has not yet run this project on physical hardware. Volunteers should understand this is experimental source code, not a verified product.

## Before volunteering

- Confirm exact board and firmware versions, MeshCore companion model and UART firmware.
- Read the original board-specific wiring documentation. Verify power, voltage levels, TX/RX and common ground. Do not guess pin assignments.
- Use test nodes and non-sensitive data. Do not transmit emergency or safety-critical messages for validation.
- Review [UART test plan](UART_COMMAND_RESPONSE_HARDWARE_TEST_PLAN.md), [channel restore test plan](CHANNEL_RESTORE_HARDWARE_TEST_PLAN.md) and [troubleshooting](UART_TROUBLESHOOTING.md).
- Back up existing configuration first; test channel restore with disposable local metadata only.

## Suggested staged test session

1. Record source commit SHA, the PicoMesh Pro version shown at startup, board/firmware versions and wiring (without secrets).
2. Load program; verify menu appears and does not crash.
3. Read-only device query, time sync and startup responses.
4. Contact sync with quiet and active traffic.
5. Direct send and channel send using consenting test peers; distinguish queued, delivered and unknown outcomes.
6. Export/restore channel name/index metadata, including malformed input; verify reserved #public behavior.
7. Partial-frame, timeout and reconnect tests, only if safely reproducible.
8. Note stability and any unexpected output during an extended smoke test.
9. If time allows, run scenarios 8–16 in the UART test plan, which cover the reliability-audit fixes.

## How to report

Open a [**Hardware test report** issue](https://github.com/TheLogsAreScreaming/PicoMesh-Pro/issues/new?template=hardware-test.yml). The form uses the title `Hardware test: <board> / <companion> / <short outcome>` and asks for:
- Source commit SHA and exact firmware versions
- PASS / FAIL / NOT TESTED per scenario
- Steps to reproduce and expected vs observed behavior
- Redacted serial logs or screenshots, if available
- Whether the tester consents to attribution in release notes

Never post private channel keys, contact public keys, personal messages, precise coordinates or identifying node traffic. Maintainers should request consent before quoting testers.

## Acceptance and publication

A successful Python CI run is not hardware acceptance. Record observed outcomes in [RC evidence log](RC_EVIDENCE_LOG.md), review blockers, and keep release on HOLD until the maintainer explicitly approves publication. Do not auto-create tags, releases or upstream PRs.
