---
name: social-media
description: "Ultimatum's Social Media workflow. Use it whenever the user asks, in plain chat or with /ultimatum:social-media, for a content plan, a week of posts or a campaign. It picks a channel, drafts posts with one clear next step each, decides what to measure, asks Motion Graphics for a video when one helps, reviews claims, links and tracking, and asks before anything is posted. One single post or tweet is plain writing help instead."
argument-hint: "<the campaign or content plan>"
---

# Ultimatum · Social Media

Task: $ARGUMENTS (if empty, use the user's latest request)

`ult` = `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/ult"` (pass it fully substituted to helpers). Skills: `${CLAUDE_PLUGIN_ROOT}/skills/`.

Read `shared/defaults.md` and `social-media/campaign.md` once. Run `ult social "<task>" --root .`: it prints the steps, whether the launch offer is approved, the video step and the publish gate.

## Steps

1. **Offer.** Run directly from the user's request, or during a launch from the approved offer in the shared brief. If `ult social` says the brief is not approved, draft only from what the Launch Manager shared and say so.
2. **Content planner:** one channel to start, and why (Content Strategy).
3. **Copywriter:** the posts. Each has one clear next step (book, visit, reply) and a tracked link when it points to the site (Social Content, Copywriting).
4. **Analyst:** what to measure (views, site visits, inquiries, bookings) and where the number will come from (Analytics).
5. **Video, only if it helps.** Send Motion Graphics one video brief: goal, length, format, the post it is for, the approved offer. Wait for the checked export it records in the brief (`## Delivered video`). Do not use an export that is not recorded there.
6. **Campaign reviewer:** check every claim against the brief, every link opens, every link is tracked. Report to the Manager; fixes are rechecked.
7. **Approval.** Show the campaign. Post, send, schedule, spend money or change customer records only after the user's yes (`ult gate approve publish "<words>"`). If posts link to the site, check the live link first and record it (`--link`); `ult gate check publish --need-link` must pass. After posting, `ult gate done publish`.
8. **Results.** When numbers are available, record them: `ult social --results "<views, visits, inquiries, bookings, or not available>"`. Bring them to Business and the Launch Manager to decide what to try next.

## Rules

- Use Composio or another connector only if available and the user authorized that account; prefer read-only for research and reporting. Never put credentials in Git, prompts or logs. Without a connector, give the user ready-to-post drafts and say nothing was posted.
- Never invent numbers. If a metric was not available, say so.

## Report

The campaign in a short table (day, channel, post, next step, link), the video status, what was checked, and the one approval you need.
