# Source mirror

The live source is maintained in the existing Sites project declared in .openai/hosting.json. This GitHub directory mirrors the authored code; generated embedded assets and duplicated menu photos are omitted here. For a first local build from this mirror, run `cp ../ordine/menu.js public/menu.js` before `python3 scripts/build.py`. The original embedded photos are retained in the repository at ordine/menu.js. Never copy runtime credentials into source.
