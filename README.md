# PicoMesh Pro

**A terminal-based MeshCore companion client for Raspberry Pi Pico / PicoMite, written in MMBasic.**

PicoMesh Pro builds on [Vigoleis912's PicoMeshCore](https://github.com/Vigoleis912/PicoMeshCore), adding safer channel workflows, local channel backup and restore, and more defensive UART communication. It is designed for a PicoMite connected by serial UART to a compatible MeshCore companion radio—not as a macOS or mobile application.

> **Pre-release software:** source-level regression checks exist, but the current enhancements have **not yet completed physical PicoMite/PicoCalc hardware validation**. No validated release candidate is available.

## What it does

| Area | Current capabilities |
| --- | --- |
| Messaging | Direct and channel messages. "Delivered" is shown only when the radio's confirmation matches the message you sent, and a confirmation that arrives late is still reported. Text is limited to what the radio accepts (160 characters direct; 160 minus your `"<node name>: "` prefix on channels) |
| Channels | Local channel listing and selection; validation of channel names and indexes; protection of reserved #public mapping |
| Backup and restore | Export and staged restore of local channel names/index mappings; malformed data is rejected before applying changes |
| Device controls | Contact synchronization (once per session, retried if incomplete), device information, time synchronization that is skipped when the Pico clock looks unset, radio settings and TX power checked and confirmed with `APPLY`, and diagnostics |
| UART reliability | 2048-byte receive buffer, resynchronisation on bad or cut-off frames (good frames that follow are kept), bounded waits, and a hint to re-initialize when the radio stops answering |
| Tests | Python source-level regression checks and reference models, a [reliability audit](docs/RELIABILITY_AUDIT.md), and documented hardware test scenarios |

**Important limitations:** backup files do **not** contain private channel keys; private-key configuration and path-hash-size switching are not confirmed implemented. Source-level tests are not a substitute for hardware validation.

## Screenshots

Real screenshots will be added after capturing the application on PicoMite/PicoCalc hardware. **No simulated screens are presented as actual device output.**

| Planned capture | What it will show |
| --- | --- |
| Main menu | Terminal interface and available actions |
| Channel list | Channel names, selection and #public protection |
| Messaging | Channel send and receive workflow |
| Device diagnostics | Radio/device information and UART status |

If you have hardware captures, open a PR adding the images under `docs/screenshots/`, then replace this table with embedded images. Avoid exposing private keys, personal messages, node identifiers or precise locations.

## Hardware

- Raspberry Pi Pico running compatible PicoMite firmware (PicoCalc use requires verifying your specific setup)
- MeshCore companion radio supporting UART (the upstream instructions describe Heltec V4)
- Appropriate UART wiring and power arrangement for your hardware

See [original wiring and firmware setup instructions](docs/UPSTREAM_README.md) before connecting devices. Check voltage, pin assignments and firmware compatibility for your exact boards; do not assume Heltec V4 wiring applies to other radios.

## Getting started

1. Set up the PicoMite and MeshCore companion radio according to the [upstream hardware guide](docs/UPSTREAM_README.md).
2. Obtain [`meshcore.bas`](meshcore.bas) from this repository and transfer it to your PicoMite using your usual MMBasic file-transfer workflow.
3. Confirm the radio is configured for UART companion operation and that the program's `COM2:115200,2048` setting matches your wiring and the radio's baud rate. The second field is the receive buffer size in bytes. If your PicoMite firmware rejects it, change it to `1024`.
4. Set the Pico clock before starting (`DATE$` and `TIME$`). With an unset clock the program skips radio time sync and warns that message timestamps will be wrong.
5. Run the BASIC program on the PicoMite. The first line shows the PicoMesh Pro version; include it, together with the commit SHA, in any report. Start with read-only device queries before attempting sends or channel changes.
6. For validation, follow the [UART command-response hardware test plan](docs/UART_COMMAND_RESPONSE_HARDWARE_TEST_PLAN.md) and [release-readiness checklist](docs/RC_READINESS_CHECKLIST.md).

This is not yet a verified step-by-step installation procedure for every PicoCalc/PicoMite configuration.

## Development and testing

The `tests/` directory contains static Python checks for source-level guards. GitHub Actions runs the repository's configured static checks; check the specific commit's workflow status before relying on a build. **MMBasic runtime behavior must still be tested on hardware.**

- [Release candidate readiness checklist](docs/RC_READINESS_CHECKLIST.md)
- [UART hardware test plan](docs/UART_COMMAND_RESPONSE_HARDWARE_TEST_PLAN.md)
- [Roadmap](ROADMAP.md)

## Upstream and contributions

PicoMesh Pro is independently maintained and derived from [Vigoleis912/PicoMeshCore](https://github.com/Vigoleis912/PicoMeshCore). We intend to propose focused, compatible improvements upstream where appropriate; this repository remains a separate project. Bug reports, reproducible hardware test results and focused pull requests are welcome.

## License and safety

Distributed under the **GNU GPL v3**; see [LICENSE](LICENSE). Original attribution and upstream documentation are retained.

Never commit private channel keys, credentials or sensitive radio traffic. Use a controlled test environment when validating transmission behavior.
