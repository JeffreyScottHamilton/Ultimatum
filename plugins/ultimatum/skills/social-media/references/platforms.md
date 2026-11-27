# Platforms

Read when a post depends on a size, a length or a caption limit, or before posting through an API or scheduler.

`ult posts specs [channel]` prints the sizes, video length, caption limit and safe zones the checks use, with the month they were last looked at. They are working numbers, not guarantees: platforms change them without notice. Before a post depends on one, open the platform's own help page and say what you checked.

## What we found on 2026-11-27, and how sure it is

Read from search results and third-party guides, not every platform's own page:

- **Instagram:** captions 2,200 characters, about 125 shown before "more". Several sources report hashtags cut to 5 per post and Reel in December 2025; some older pages still say 30. Our check flags more than 5 as a fix, not a blocker.
- **TikTok:** the app allows about 4,000 caption characters; sources quoting the Content Posting API give 2,200. A scheduler that posts through the API may stop at 2,200, so the check warns above that.
- **Pinterest:** Pinterest's own help page and API schema give 800 characters for a description, 100 for a title and 500 for alt text; several tool sites still say 500.
- **Reels length, Shorts length and title, LinkedIn, X and Facebook:** not re-confirmed this time; the numbers in `ult posts specs` are older. Check before relying.

## Posting through an API

From earlier search previews, not the platforms' own pages; check before planning around them:

- TikTok: an app that has not passed TikTok's review may post only privately through the API.
- Instagram: API posts have a daily cap per account; sources disagree on the number.
- YouTube: one API upload uses a large share of the default daily quota.

## Safe zones

Vertical video and stories put buttons and captions over the edges. Keep words and faces inside the safe area `ult posts specs` prints (pixels from the top, bottom and right), and look at the file in the app's preview before approval.
