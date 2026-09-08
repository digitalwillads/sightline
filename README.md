# Sightline

A competitor ad-intelligence prototype, built as a lead magnet for
Digital Will Ads. Paste a competitor's website; the report shows every ad
they are running, how long each has survived, the persuasion angle behind
each one, and where their spend sits against the corner nobody has claimed.
An account puts a brand on a weekly email of what changed.

**Live:** https://digitalwillads.github.io/sightline/

## What is real

The three demo domains carry genuine data, pulled from the Meta Ad Library
on 8 September 2026:

| Domain | Live ads | Longest run | EU reach |
|---|---|---|---|
| huel.com | 62 | 326 days | 46.5M |
| specsavers.ie | 36 | 181 days | 13.2M |
| layahealthcare.ie | 54 | 63 days | 3.8M |

Real ad copy, real start dates, real variant counts, real platforms, and the
real creatives in `assets/`. Any other domain returns a sample report, badged
as such in the report header.

## The constraint

Meta discloses non-political ads only where they deliver inside the EU, so the
pull is scoped to Ireland. A US-only advertiser returns nothing from the
official API. A production build needs its own scraper and daily snapshots,
because "days running" and the weekly change email both depend on stored history.

## Rebuilding the data

See `tools/README.md`.
