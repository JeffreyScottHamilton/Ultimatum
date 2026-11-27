# Brand assets: folders, names, records and clean-up

Read at step 2 of `brand-flow.md` when a brand has more than a handful of files (logos, photos, campaign pieces), or when someone cannot find "the latest logo". Keep it as light as the team: a solo owner needs the folder and naming rules, not the manifest.

## One home with three zones

Keep every brand file under one root, split by how often it changes:

```
brand/
  core/            # changes rarely; only the brand owner edits
    logo/          #   svg/, pdf/, png/  (see brand-visual.md § Logo use)
    colour/        #   swatch files, the exported token file
    type/          #   licence files and links; never font binaries without licence
    guide/         #   the guidelines file and its PDF export
  library/         # reusable, approved pieces
    photo/  illustration/  icon/  pattern/  template/
  work/            # campaign and one-off pieces, by year
    2026/
      spring-open-day/
        draft/  final/  source/
  archive/         # retired versions; read-only
```

Rules: `core/` is the only place a logo is taken from; copies elsewhere are a bug. `work/` folders are created per campaign and moved whole to `archive/` when the campaign ends. Source files (layered design files, raw photos) sit beside their exports in `source/`, never mixed into `final/`.

In a website repo, only the exports the site serves belong in the repo (`public/brand/` or similar). Masters and raw photos live in shared storage; the repo links to them in the guide.

## Names that sort and explain

Build every file name from the same parts, lower case, words joined by hyphens, parts joined by underscores:

```
<kind>_<subject>_<variant>_<size-or-format>_<yyyymmdd>_v<n>.<ext>
```

| Part | Examples | Notes |
|---|---|---|
| kind | `logo`, `photo`, `banner`, `social`, `doc` | from a fixed list |
| subject | `lockup`, `symbol`, `team-kitchen`, `open-day` | what it shows or is for |
| variant | `colour`, `mono`, `reversed`, `dark-ground` | omit when there is only one |
| size or format | `1200x630`, `a4`, `512` | pixels for screen, paper size for print |
| date | `20260314` | when the version was approved |
| version | `v1`, `v2` | bump on any visible change |

Examples:

```
logo_lockup_reversed_svg_20260301_v2.svg
photo_team-kitchen_wide_2400_20260210_v1.jpg
social_open-day_story_1080x1920_20260320_v3.png
```

The date makes a folder sort by age; the version stops "final-final-2". Never put "final" or "new" in a name.

## A record per asset (when the library grows)

Past about a hundred files, keep a manifest next to the library: one JSON or CSV record per asset. The minimum useful fields:

| Field | Holds |
|---|---|
| `id` | a stable short id, unchanged across versions |
| `path` | current file path |
| `kind`, `subject` | as in the file name |
| `status` | `draft`, `in-review`, `approved`, `retired` |
| `version`, `approved_on`, `approved_by` | who said yes, and when |
| `rights` | owned, licensed (with licence and expiry), or credit needed (with the credit line) |
| `alt` | the default alt text, for images |
| `tags` | a few words from the tag list |
| `replaces` | the id of the asset this one supersedes |

Keep old versions as separate records with `status: retired`, so a page that still uses one can be found. A short JSON example:

```json
{
  "id": "ph-0042",
  "path": "brand/library/photo/photo_team-kitchen_wide_2400_20260210_v1.jpg",
  "kind": "photo",
  "subject": "team-kitchen",
  "status": "approved",
  "version": 1,
  "approved_on": "2026-02-10",
  "approved_by": "owner",
  "rights": "owned",
  "alt": "Two cooks plating lunch at the pass",
  "tags": ["people", "kitchen", "warm"]
}
```

## Tags from a fixed list

Free-form tags decay into synonyms within weeks. Keep a short controlled list in the guide, in groups: subject (people, product, place, food), mood (still, busy, warm), use (hero, social, print), season or campaign. A new tag is added to the list first, then used.

## Finding things

With names built as above, plain search does most of the work:

- all reversed logos: files matching `logo_*_reversed_*`;
- everything for one campaign: the campaign folder, or `*_open-day_*`;
- everything awaiting review: manifest records with `status` `in-review`.

## Clean-up, every quarter

1. Move finished campaign folders from `work/` to `archive/`.
2. Find files outside the naming pattern and rename or remove them.
3. Check `rights`: licences near expiry are renewed or the asset is retired and its pages are updated.
4. Find duplicate exports of the same master and keep one.
5. Make sure every logo in use on the site matches the current `core/logo/` version (a quick checksum or visual diff).
6. Record what moved in the guide's change log.
