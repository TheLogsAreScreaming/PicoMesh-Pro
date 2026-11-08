# UART troubleshooting for PicoMesh Pro testers

**Safety:** Verify pinout, logic voltage, common ground and power requirements for your exact PicoMite/PicoCalc and MeshCore companion radio. Do not assume one board's wiring applies to another. Never connect incompatible voltage levels.

## Startup reports commands finished but no radio responses

- This message means startup commands were attempted, **not** that radio initialization succeeded.
- Check the radio is powered and running a compatible UART companion firmware.
- Compare the program's `COM2:115200,2048` setting with your board pin mapping and the companion's UART baud rate. The `2048` is the receive buffer size; if the `Open` line errors on your firmware, change it to `1024`.
- Check TX/RX crossover and common ground using the actual board documentation.
- Run a read-only device query and record the exact response or timeout.

## Messages you may see

| Message | Meaning |
| --- | --- |
| `Pico clock looks unset or wrong; time sync skipped` | The Pico date is outside 2024–2099. Set it with `DATE$` and `TIME$`, then use **Device → Sync device time**. The radio never moves its clock backwards, so a wrong future date cannot be undone from here. |
| `Time sync refused: radio clock is already later than the Pico clock` | The radio kept its own (later) time. Check the Pico clock. |
| `Warning: Pico clock not set; message timestamp will be wrong` | The message is still sent, with a wrong timestamp. |
| `The radio has not answered 3 commands in a row.` | Check power, TX/RX wiring and ground, then use **Device → Initialize radio**. |
| `Message too long for the radio` | Direct text is limited to 160 characters by the companion firmware. |
| `Message too long for the radio; it would be cut short` | Channel text plus the `"<node name>: "` prefix the radio adds must fit in 160 characters. |
| `Ignored delivery confirmation for an earlier message` | A confirmation arrived that does not belong to the message just sent. |
| `Late delivery confirmation: your last direct message was delivered` | The confirmation for your last unconfirmed direct message arrived after the wait. |
| `Send OK (delivery not tracked)` | The radio accepted the message but returned no code to track delivery. |
| `Cancelled; radio settings unchanged` | Radio params and TX power are only sent after you type `APPLY`. |

## Contacts stop loading

- The contact synchronization routine can stop after repeated quiet timeouts or sustained asynchronous traffic.
- Treat a partial contact list as incomplete; retry when traffic subsides. An incomplete sync is retried automatically the next time you read or send.
- Contacts added on the radio after a complete sync appear only after **Contacts → Refresh contacts**.
- If "Contacts loaded" is lower than "Expected contacts" on every attempt, note the contact count and report it: the receive buffer may still be overflowing.
- Do not interpret the number of stored contacts as proof that the full list synchronized.

## Direct messages show unknown or unconfirmed status

- **Unknown** means no definitive send response was observed. Do not retry blindly: the radio may have accepted the message.
- **Queued** means the request was accepted for sending, not necessarily delivered. The wait follows the radio's own estimate (2–15 s); flood-routed messages take longer.
- **Delivered** is shown only when the confirmation matches this message.
- A missing delivery confirmation does not prove failure. Verify through the recipient or other independent evidence before retrying.

## Malformed frames or disconnects

- Record the command, frame symptoms, firmware versions and whether the issue is reproducible.
- Test recovery with read-only queries first. Avoid repeated sends while the outcome is unknown.
- For a repeatable failure, include a redacted log and exact source commit SHA in an issue.

## What to include in a bug report

- Exact PicoMesh Pro commit SHA and firmware versions
- Board and radio model, UART port and baud rate
- Expected vs observed behavior and reproduction steps
- Whether a power cycle or reconnect changes the result
- Redacted serial output (remove private keys, contact IDs, message text and precise location)

See [UART hardware test plan](UART_COMMAND_RESPONSE_HARDWARE_TEST_PLAN.md) and [RC evidence log](RC_EVIDENCE_LOG.md). Hardware behavior is not yet certified.
