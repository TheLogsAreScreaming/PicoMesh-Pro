# UART command-response hardware test plan

These checks require a PicoCalc/PicoMite running `meshcore.bas` and a MeshCore companion radio connected over UART. Python static checks alone cannot verify UART behavior.

## Before testing
- Back up existing local channel mappings and record the firmware versions and wiring.
- Use a test radio and avoid sending repeated messages during uncertain delivery states.
- Record the command, expected result, actual output, and any observed radio disconnect.

## Scenarios
1. **SET_DEVICE_TIME:** Trigger time sync while unsolicited async frames arrive. Confirm an async event is handled and the time-sync acknowledgement is still interpreted correctly.
2. **GET_DEVICE_TIME:** Query device time with an async event arriving first. Confirm the response type is validated and the timestamp displayed is plausible.
3. **DEVICE_QUERY:** Query device info during async activity. Confirm the expected device-info response is parsed rather than the async event.
4. **No radio response:** Disconnect the radio and issue each command. Confirm it exits without hanging and reports a missing response.
5. **Continuous async traffic:** Generate many unsolicited frames during a response wait. Confirm the existing 20-frame cap stops the wait and that the UI remains responsive.
6. **Partial frame:** Interrupt the UART stream mid-header and mid-payload. Confirm the reader returns, and that the next complete frame is read normally (the reader resynchronises instead of discarding the buffer).
7. **Recovery:** Reconnect the radio and repeat the commands; confirm no stale bytes are interpreted as successful responses. After 3 unanswered commands the reconnect hint should appear.

## Scenarios for the reliability-audit fixes

See [reliability audit](RELIABILITY_AUDIT.md) for background on each item.

8. **Startup and buffer (R4):** the program starts without an error on `Open "COM2:115200,2048"`. If it errors, retry with `1024` and record which value worked.
9. **Large contact sync (R4, R10):** with 50 or more contacts, "Contacts loaded" equals "Expected contacts". Repeat three times.
10. **Contacts synced once (R3):** after the first read or send, later reads and sends do not print "Refreshing contacts...".
11. **Message length (R1 and text limit):** a 160-character direct message sends; 161 characters gives "Message too long for the radio". A channel message at the computed limit sends whole and arrives uncut.
12. **Delivery matching (R2, R11):** a direct message to a nearby peer shows "Delivered" with a round-trip time. Send to an out-of-range peer, bring it back, and confirm "Late delivery confirmation" appears once, never "Delivered" for a different message.
13. **Clock (R5):** start with the Pico clock unset and confirm "time sync skipped". Set the clock and confirm sync succeeds.
14. **Radio settings (R6):** re-apply the radio's current settings with `APPLY` and confirm "Radio params saved". Try BW `100` and confirm a local refusal. Answer anything other than `APPLY` and confirm nothing is sent.
15. **Channel import (R7):** run **Import radio channel names** and confirm the summary lists every slot outcome.
16. **File errors (R13):** restore with no `CHANNELS.TXT`, and export to a missing or write-protected drive if possible; the program reports the problem and keeps running.

## Release gate
Do not mark these scenarios passed until observed on physical hardware. Record results and investigate failures before a release candidate.
