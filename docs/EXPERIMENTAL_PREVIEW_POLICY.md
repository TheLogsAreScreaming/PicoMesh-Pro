# Experimental preview policy (planning only)

**No experimental preview has been published or approved.** This document describes how to decide whether a source-only preview is appropriate when hardware validation is unavailable.

## Labels and claims

- Label any proposed preview **UNVERIFIED EXPERIMENTAL SOURCE — NO HARDWARE VALIDATION**.
- Do not call it a stable, release candidate, or hardware-compatible build without evidence.
- Describe the Python protocol simulator as a reference model only. It does not run `meshcore.bas`, implement MeshCore firmware, or exercise physical UART.
- Explain that unverified firmware/wiring combinations may not work, and data/configuration could be affected.

## Minimum pre-preview review

- [ ] Choose a specific source SHA and verify GitHub Actions on that exact SHA.
- [ ] Review source changes, attribution/license and installation instructions.
- [ ] Confirm no private keys, test contacts, credentials or personal data in examples.
- [ ] Confirm a safe opt-in testing plan and issue reporting process.
- [ ] Decide whether source-only distribution is appropriate without hardware results.
- [ ] Obtain explicit maintainer approval for the exact publication scope and wording.

## Distribution choices

1. **Preferred while untested:** Keep source on `main` and invite volunteers to test a pinned commit; no tag or GitHub release required.
2. **Optional later:** Publish a clearly marked experimental source snapshot, only after explicit owner approval.
3. **RC:** `v0.1.0-rc.1` was published on 2026-11-08 at the owner's direction as an untested prerelease. Keep any final release on HOLD until required hardware evidence is recorded.

See [RC evidence log](RC_EVIDENCE_LOG.md) and [readiness checklist](RC_READINESS_CHECKLIST.md). Nothing here authorizes automatic publication or an upstream contribution.
