# Open Worlds Tutor plugins

| File | What it does | Needs an MFE rebuild? |
|---|---|---|
| `owa_layout.py` | Header links, player Help link, logo alt text, dashboard "Welcome back" heading, Up next + Help sidebar, Resume mission / Course outline buttons, hides Dates and Discussion tabs, Open Worlds footer, turns off the light/dark toggle | Yes, once. After that, link changes are restart-only. |
| favicon (`owa_favicon.py` on the server) | Points every app's favicon at `favicon.ico` in this repo | No (restart lms) |

Paste server commands **one line at a time** (tmux eats pasted blocks).

## Install owa_layout (one MFE rebuild)

1. Take a Hostinger snapshot.
2. `curl -fsSL https://raw.githubusercontent.com/uberearthmann/owa-brand/272d48be7571d6eb96a6f73e3760798345e1b51e/tutor/owa_layout.py -o "$(tutor plugins printroot)/owa_layout.py"`
3. `tutor plugins enable owa_layout`
4. `tutor config save`
5. `grep -c Owa "$(tutor config printroot)/env/plugins/mfe/build/mfe/env.config.jsx"` (expect about 25; 0 means the plugin is not enabled)
6. `docker tag "$(tutor config printvalue MFE_DOCKER_IMAGE)" owa-mfe:before-layout` (instant rollback copy)
7. `docker buildx use singlecpu`
8. `tutor local stop`
9. `tutor images build mfe` (long; leave it running)
10. `tutor local start -d`

## Roll back fast (no rebuild)

1. `docker tag owa-mfe:before-layout "$(tutor config printvalue MFE_DOCKER_IMAGE)"`
2. `tutor plugins disable owa_layout`
3. `tutor config save`
4. `tutor local start -d`

## Change links later (restart only)

- Header links: `tutor config save --set 'OWA_HEADER_LINKS=[{"title": "My courses", "url": "/dashboard"}, {"title": "Catalog", "url": "/courses"}, {"title": "Help", "url": "https://..."}]'`
- Help (player header and dashboard panel): `tutor config save --set OWA_HELP_URL=https://...`
- Footer links: `tutor config save --set 'INDIGO_FOOTER_NAV_LINKS=[{"title": "Help", "url": "..."}, {"title": "Privacy", "url": "..."}, {"title": "Terms", "url": "..."}]'`
- Then `tutor local restart lms`. Relative URLs (`/help`) resolve against the LMS.
