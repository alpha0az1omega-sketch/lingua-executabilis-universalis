# TECHNICAL DEBT AND FIXES
- **Heredoc Issues:** Avoid triple backticks in terminal heredocs. Use Python scripts to write files.
- **Astro Build:** Ensure `collection.astro` points to `primitives_3d/*.html` and not the obsolete flat SVGs.
- **GPG Key Expiration:** Check the expiration date of key `4ED4A15B...` and extend it if necessary.
- **OTS Upgrades:** Run `ots upgrade` on all `.ots` files annually to ensure Bitcoin anchoring remains complete.
- **Web Performance:** `mathesis_nova.html` uses Three.js. Ensure fallbacks for mobile devices (lower particle count).
