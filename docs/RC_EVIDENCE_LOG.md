# PicoMesh Pro — release evidence log

Use this form for the exact commit proposed for `v0.1.0-rc.1`. A green source-level test workflow is **not** evidence that the MMBasic program runs on hardware. Leave fields **NOT TESTED** until actual evidence is available. The last six hardware rows cover the [reliability-audit](RELIABILITY_AUDIT.md) fixes; scenarios 8–16 in the [UART test plan](UART_COMMAND_RESPONSE_HARDWARE_TEST_PLAN.md) describe them.

## Candidate identity

- Candidate commit SHA (CI-verified baseline): `082e756c57514b86101cfae50e236b870ae66749` (reverify if candidate changes)
- Date / tester: **NOT RECORDED**
- PicoMite/PicoCalc model and firmware: **NOT RECORDED**
- MeshCore companion model and firmware: **NOT RECORDED**
- UART port, baud rate and wiring: **NOT RECORDED**

## Automated checks

- GitHub Actions run URL: https://github.com/TheLogsAreScreaming/PicoMesh-Pro/actions/runs/42391882087 (`push` on `main`)
- Commit SHA shown in run metadata: `082e756c57514b86101cfae50e236b870ae66749` (`main`, merge of #92; all reliability-audit fixes)
- Job conclusion: **SUCCESS** (`source-regressions`; all reported steps succeeded)
- Test suite: `python -m unittest discover -s tests -v` (source-level checks only)
- Test log artifact: `source-test-results` (artifact ID `13581907070`, downloaded and reviewed 2026-11-07: 167 tests, 0 failures, 0 errors, `OK`)
- Superseded baselines: run 42320456867 at `eccf8d517b6d6470a1d98faa8c2896ee550499e4` (114 tests, `OK`); run 41754015177 at `2065f65c1d3c3aaa02f584f46efc0401e6f4fc2d` (56 tests, `OK`); run 41743741668 at `13dc8221ce0edc47622d0777fb5d51896d69ad86` (49 tests, `OK`)
- Failures and follow-up issues: **NONE REPORTED BY JOB** (hardware issues not assessed)

## Hardware checks

| Scenario | Result | Evidence / notes |
| --- | --- | --- |
| Program loads on PicoMite/PicoCalc | NOT TESTED | |
| UART connection and device query | NOT TESTED | |
| Clock sync and APP_START | NOT TESTED | |
| Contact synchronization with async frames | NOT TESTED | |
| Direct send, accepted/unknown/delivery feedback | NOT TESTED | |
| Channel list, #public mapping and channel send | NOT TESTED | |
| Channel export/restore and malformed backup | NOT TESTED | |
| Partial UART frames, timeout and recovery | NOT TESTED | |
| Disconnect/reconnect and extended smoke test | NOT TESTED | |
| Startup with 2048-byte receive buffer (or 1024 fallback) | NOT TESTED | |
| Sync of 50+ contacts matches expected count | NOT TESTED | |
| Message length limits (direct 160, channel name prefix) | NOT TESTED | |
| Delivery matched to message, late confirmation reported | NOT TESTED | |
| Unset-clock sync skip and radio settings APPLY | NOT TESTED | |
| Channel import summary and file-error handling | NOT TESTED | |

## Release decision

- Release gate owner: repository owner
- Blocking issues: hardware behaviour is unverified (all rows above NOT TESTED)
- Decision: **Published as an untested prerelease at the owner's direction, 2026-11-08.** The exact commit and CI run are on the [release page](https://github.com/TheLogsAreScreaming/PicoMesh-Pro-Releases/releases/tag/v0.1.0-rc.1). A final release stays on **HOLD** until the rows above have real results.

Do not publish a final release or represent the hardware as validated until these fields have been completed with real results. Follow `docs/RC_READINESS_CHECKLIST.md` for the release gates.
