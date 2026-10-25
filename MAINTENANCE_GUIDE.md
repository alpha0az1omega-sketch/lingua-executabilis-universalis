# L.E.U. MAINTENANCE & UPGRADE GUIDE

## 1. Routine Maintenance (Monthly)
- **OTF Upgrade:** Run `ots upgrade V9_FINAL.sha256.ots` to integrate the latest Bitcoin block confirmations.
- **Dependency Update:** Run `pip install --upgrade -r requirements.txt` to patch security vulnerabilities.
- **Log Audit:** Review `DAILY_GENESIS_LOG.md` to ensure no anomalies (e.g., hash collisions) have occurred.

## 2. Server Infrastructure
- **Cloudflare Workers:** The Genesis Engine is deployed on Cloudflare for 99.99% uptime. Renewal is automatic.
- **Domain Name:** `alpha0az1omega.com` is set to auto-renew for the next 10 years.
- **IPFS Pinning:** All visual artifacts are pinned on Pinata to ensure they remain accessible even if the main server goes down.

## 3. Technical Debt Management
- **Heredoc Bugs:** Avoid using triple backticks in shell scripts; use Python scripts for file generation.
- **Astro Build:** Ensure `collection.astro` always points to `primitives_3d/*.html` and not the obsolete flat SVGs.
- **OpenCV / Video Generation:** The `venv` must be activated before running `generate_video.py`. Never install globally with `--break-system-packages`.

## 4. Upgrading the Protocol
- **Version Control:** Every new version must be tagged (e.g., `v10.0.0`) and the `VERSION.md` file updated.
- **Backward Compatibility:** Do not break the SHA-256 mapping of the 20 primitives. New entities must inherit from the old ones.
