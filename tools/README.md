# Sightline data pipeline

Rebuilds the real Ad Library datasets baked into `../index.html`.

    export TOK=$(keymaster secret get FB_PERSONAL_TOKEN | tail -1)
    python3 pull.py Huel Huel huel.com "meal replacement"
    python3 pull.py "Specsavers" "Specsavers Ireland" specsavers.ie "opticians"
    python3 pull.py "Laya Healthcare" "Laya Healthcare" layahealthcare.ie "health insurance"
    python3 scrape.py          # real creatives -> ../assets/
    python3 scrape_meta.py     # CTA labels, link descriptions, page avatars
    python3 emit.py            # writes library_real.json

`pull.py` fetches, groups ads into creative variants and computes the metrics.
`label.py` holds the hand-read angle labels, positioning coordinates and winner
picks per brand. `emit.py` merges the two into the JSON that replaces the
`const LIBRARY = {...}` block in index.html.

Data is scoped to ads delivering in Ireland, because `ad_type=ALL` only returns
non-political ads inside the EU.

`scrape.py` is the part the API cannot do. `ads_archive` returns no media URL,
only an `ad_snapshot_url` whose page builds the creative in JavaScript. The
script drives a cmux browser surface to render each snapshot, takes the largest
rendered image (or the video plus its poster) and downloads it into `assets/`,
so the mockup ships real files and never carries an access token.

`scrape_meta.py` is a second pass over the same snapshots. It reads the parts
of the ad unit the API withholds — the call-to-action label, the link
description and the advertiser's page avatar — so the card can render a
faithful Meta feed ad rather than a generic tile.
