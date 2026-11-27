#!/usr/bin/env python3
"""Render pass: open built pages in a headless browser at several widths and
measure what a static lint cannot see (overflow, wrapping, real contrast,
what the first screen shows, covered or hidden text).

Optional: needs the Python `playwright` package and a Chromium it can launch.
Without them it prints a skip line and exits 3, so callers can treat the pass
as unavailable rather than failed. Standard library otherwise.

Usage:
  render_check.py PAGE_OR_DIR_OR_URL [...] [--widths 320,768,1440]
                  [--only RULE,...] [--genre NAME] [--format text|json|github]
                  [--shots DIR] [--allow-remote] [--rules]

Only file paths and http(s) URLs on localhost / 127.0.0.1 / [::1] are opened,
and requests to any other host are blocked, unless --allow-remote is given.
Exit: 0 clean, 1 findings, 2 bad arguments, 3 no browser (skipped).
"""
import argparse
import json
import os
import re
import shutil
import sys
from pathlib import Path
from urllib.parse import urlparse

# rule: (severity, gate or source, what it means)
RULES = {
    "h-scroll": ("high", "gate 34",
                 "the page scrolls sideways at this width; find the element wider than the window"),
    "label-wrap": ("high", "gate 49a",
                   "a button or top-menu link wraps to a second line"),
    "minor-link-wrap": ("medium", "gate 49b",
                        "a footer link, tab or breadcrumb runs past two lines"),
    "low-contrast": ("high", "gate 40",
                     "rendered text against its rendered background is under 4.5:1 (3:1 for large text)"),
    "tiny-text": ("medium", "gate 75",
                  "running text renders under 12px, or other text under 11px"),
    "tight-leading": ("medium", "gate 75",
                      "multi-line prose with line height under 1.3 of its size"),
    "line-length": ("medium", "gate 25",
                    "prose lines average over 88 characters, or under 35 on a long paragraph"),
    "hero-out-of-view": ("high", "gate 44b",
                         "at 1280 x 800 the headline, lede, main action or the visual's centre is below the fold"),
    "dead-band": ("medium", "gate 79",
                  "over 160px of nothing between the hero's last content and the fold at 1440 x 900"),
    "next-section-position": ("low", "gate 44c",
                              "on a 1440 x 900 screen the following block's top edge lands above 760 (cramped hero) or past 900 (no sign there is more)"),
    "no-max-width": ("medium", "gate 44d",
                     "at 1920 prose runs within 120px of the window edge; the container has no cap"),
    "section-gap": ("low", "gate 59",
                    "sections closer than 120px apart at 1440 (64px across a colour change), or every gap identical"),
    "crowded-head": ("medium", "gate 71",
                     "a heading sits closer to what precedes it than to what it introduces"),
    "cramped-box": ("medium", "gate 72",
                    "a tinted panel, or one with a left rule, has its words pressed against the edge"),
    "small-section-heads": ("low", "gate 78",
                            "median section heading under 40px at 1440"),
    "empty-picture": ("medium", "gate 81",
                      "a 300 x 200 or larger block that shows only a fill or gradient"),
    "counting-marks": ("low", "gate 82",
                       "24 or more identical empty marks in a row standing for a number"),
    "photo-wall": ("low", "gate 83",
                   "under the hero, pictures take more than one third of the page area"),
    "stock-close": ("low", "gate 85",
                    "the last block asks only for an email; confirm a newsletter is really what this page is for"),
    "text-covered": ("high", "gate 73",
                     "text is painted under another element (sticky bars excepted)"),
    "accent-flood": ("low", "gate 23",
                     "saturated fills cover over 8% of the first screen (30% atmospheric, 60% playful)"),
    "edge-text": ("medium", "small screens",
                  "text within 12px of the window edge on a phone width"),
    "clipped-text": ("medium", "states",
                     "text cut off by a box that hides its overflow"),
    "hidden-at-rest": ("high", "motion",
                       "a large share of the text is still invisible after scrolling the whole page"),
    "straggler-heading": ("low", "type",
                          "a heading's last line is one word"),
    "script-error": ("high", "states",
                     "the page threw an error while loading"),
    "broken-image": ("high", "assets",
                     "an image failed to load"),
    "waiver-no-reason": ("medium", "linter",
                         "a render-check waiver with no reason or an unknown rule; it waives nothing"),
}

WIDTHS = [320, 375, 414, 768, 1024, 1280, 1440, 1920]
HEIGHT = {1280: 800, 1440: 900, 1920: 1080}
LOCAL_HOSTS = {"localhost", "127.0.0.1", "::1", "[::1]"}
WAIVER = re.compile(r"render-check:\s*allow\s+([\w\-, ]+?)(?::\s*(.*?))?\s*(?:-->|\*/|$)", re.M)

# Every measurement runs inside the page. `opts` says which groups to run at
# this viewport; each finding is [rule, where, detail].
MEASURE_JS = r"""
async (opts) => {
  const out = [];
  const add = (rule, el, detail) => out.push([rule, el ? where(el) : 'page', detail || '']);
  const vw = window.innerWidth, vh = window.innerHeight;
  const cs = (el) => getComputedStyle(el);
  function where(el) {
    if (!el || el.nodeType !== 1) return 'page';
    let s = el.tagName.toLowerCase();
    if (el.id) s += '#' + el.id;
    else if (el.classList.length) s += '.' + [...el.classList].slice(0, 2).join('.');
    const t = (el.innerText || el.getAttribute('aria-label') || el.getAttribute('src') || '').trim().replace(/\s+/g, ' ');
    return t ? s + ' "' + t.slice(0, 40) + '"' : s;
  }
  const cv = document.createElement('canvas'); cv.width = cv.height = 1;
  const cx = cv.getContext('2d', {willReadFrequently: true});
  function rgba(c) {
    if (!c || c === 'transparent') return [0, 0, 0, 0];
    cx.clearRect(0, 0, 1, 1); cx.fillStyle = '#000'; cx.fillStyle = c;
    cx.fillRect(0, 0, 1, 1);
    const d = cx.getImageData(0, 0, 1, 1).data;
    return [d[0], d[1], d[2], d[3] / 255];
  }
  function lum([r, g, b]) {
    const f = (v) => { v /= 255; return v <= 0.04045 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b);
  }
  const ratio = (a, b) => { const x = lum(a), y = lum(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); };
  const over = (top, under) => { const a = top[3]; return [0, 1, 2].map(i => top[i] * a + under[i] * (1 - a)); };
  function background(el) {
    const layers = [];
    for (let n = el; n && n.nodeType === 1; n = n.parentElement) {
      const s = cs(n);
      if (s.backgroundImage && s.backgroundImage !== 'none') return null;
      const c = rgba(s.backgroundColor);
      if (c[3] > 0) { layers.push(c); if (c[3] >= 0.99) break; }
    }
    let base = [255, 255, 255];
    for (let i = layers.length - 1; i >= 0; i--) base = over(layers[i], base);
    return base;
  }
  function shown(el) {
    const r = el.getBoundingClientRect();
    if (r.width < 1 || r.height < 1) return false;
    const s = cs(el);
    if (s.visibility === 'hidden' || s.display === 'none') return false;
    for (let n = el; n && n.nodeType === 1; n = n.parentElement) {
      const q = n.getBoundingClientRect(), t = cs(n);
      if ((q.width <= 2 || q.height <= 2) && /hidden|clip/.test(t.overflow + t.overflowX)) return false;
      if (/inset\(50%|rect\(0/.test(t.clipPath + t.clip)) return false;
    }
    return true;
  }
  function fade(el) {
    let o = 1;
    for (let n = el; n && n.nodeType === 1; n = n.parentElement) {
      const s = cs(n);
      o *= parseFloat(s.opacity);
      if (s.visibility === 'hidden') return 0;
    }
    return o;
  }
  const ownText = (el) => [...el.childNodes].filter(n => n.nodeType === 3).map(n => n.textContent).join('').trim();
  const skipTags = new Set(['SCRIPT', 'STYLE', 'NOSCRIPT', 'TEMPLATE', 'SVG', 'svg', 'OPTION', 'TITLE', 'HEAD']);
  const textEls = [...document.body.querySelectorAll('*')].filter(el => !skipTags.has(el.tagName) && ownText(el).length > 1);
  function lines(el) {
    const rg = document.createRange(); rg.selectNodeContents(el);
    const tops = [];
    for (const r of rg.getClientRects()) {
      if (r.width < 1) continue;
      if (!tops.some(t => Math.abs(t - r.top) < 3)) tops.push(r.top);
    }
    return tops.length;
  }
  function contentBox(el) {
    let t = Infinity, b = -Infinity;
    for (const n of [el, ...el.querySelectorAll('*')]) {
      const media = /^(IMG|SVG|svg|VIDEO|CANVAS|PICTURE|IFRAME|FIGURE)$/.test(n.tagName) || /url\(/.test(cs(n).backgroundImage);
      if (!media && !ownText(n)) continue;
      if (!shown(n)) continue;
      const r = n.getBoundingClientRect();
      t = Math.min(t, r.top + scrollY); b = Math.max(b, r.bottom + scrollY);
    }
    return t === Infinity ? null : {top: t, bottom: b};
  }
  const pinned = (el) => { for (let n = el; n && n.nodeType === 1; n = n.parentElement) { const p = cs(n).position; if (p === 'fixed' || p === 'sticky') return true; } return false; };
  const h1 = document.querySelector('h1');
  let hero = h1 && (h1.closest('section, header') || h1.closest('[class*=hero]'));
  if (!hero && h1 && /^(SECTION|HEADER)$/.test(h1.parentElement.tagName)) hero = h1.parentElement;
  const blocks = () => {
    const root = document.querySelector('main') || document.body;
    const blockish = (k) => /^(SECTION|HEADER|FOOTER|ARTICLE|ASIDE|DIV|FORM|FIGURE)$/.test(k.tagName);
    let kids = [...root.children].filter(k => shown(k) && blockish(k));
    if (kids.length === 1 && kids[0].children.length > 2) kids = [...kids[0].children].filter(k => shown(k) && blockish(k));
    if (root.tagName === 'MAIN') { const f = document.querySelector('body > footer'); if (f && shown(f)) kids.push(f); }
    return kids;
  };

  if (opts.every) {
    const de = document.documentElement;
    if (de.scrollWidth > de.clientWidth + 1) {
      let worst = null;
      for (const el of document.body.querySelectorAll('*')) {
        const r = el.getBoundingClientRect();
        if (r.right > de.clientWidth + 1 && r.width > 0 && !pinned(el)) { worst = el; break; }
      }
      add('h-scroll', worst, de.scrollWidth + 'px wide in a ' + de.clientWidth + 'px window');
    }
    const actions = document.querySelectorAll('button, [role=button], a.btn, a[class*=button], a[class*=btn], input[type=submit], header nav a, nav:not(footer nav) > ul > li > a, nav:not(footer nav) > a');
    for (const el of actions) {
      if (!shown(el) || el.closest('footer')) continue;
      if (lines(el) > 1) add('label-wrap', el, lines(el) + ' lines');
    }
    for (const el of document.querySelectorAll('footer a, [role=tab], nav[aria-label*=readcrumb] a, .breadcrumb a, .breadcrumbs a')) {
      if (shown(el) && lines(el) > 2) add('minor-link-wrap', el, lines(el) + ' lines');
    }
    if (vw <= 414) {
      let first = null, count = 0, gap = Infinity;
      for (const el of textEls) {
        if (!shown(el) || pinned(el)) continue;
        let r = null;
        for (const t of el.childNodes) {
          if (t.nodeType !== 3 || !t.textContent.trim()) continue;
          const rg = document.createRange(); rg.selectNodeContents(t);
          const q = rg.getBoundingClientRect();
          if (q.width > 0) r = r ? {left: Math.min(r.left, q.left), right: Math.max(r.right, q.right), width: 1} : q;
        }
        if (r && r.width > 0 && (r.left < 12 || r.right > vw - 12)) { count++; first = first || el; gap = Math.min(gap, r.left, vw - r.right); }
      }
      if (count) add('edge-text', first, count + ' text block(s), closest ' + Math.round(gap) + 'px from the edge');
    }
    for (const el of textEls) {
      if (!shown(el)) continue;
      const s = cs(el);
      const hidesX = /hidden|clip/.test(s.overflowX), hidesY = /hidden|clip/.test(s.overflowY);
      if (hidesX && el.scrollWidth > el.clientWidth + 1 && !(s.textOverflow === 'ellipsis' && el.title)) add('clipped-text', el, 'cut ' + (el.scrollWidth - el.clientWidth) + 'px sideways');
      else if (hidesY && el.scrollHeight > el.clientHeight + 2 && s.webkitLineClamp === 'none') add('clipped-text', el, 'cut ' + (el.scrollHeight - el.clientHeight) + 'px at the bottom');
    }
    if (opts.cover) {
      const H = document.documentElement.scrollHeight;
      for (let y = 0; y < H; y += Math.max(200, vh - 100)) {
        window.scrollTo(0, y);
        await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
        for (const el of textEls) {
          if (pinned(el) || cs(el).pointerEvents === 'none' || !shown(el) || fade(el) < 0.05) continue;
          const rg = document.createRange(); rg.selectNodeContents(el);
          const r = rg.getClientRects()[0];
          if (!r || r.top < 0 || r.bottom > vh || r.left < 0 || r.right > vw) continue;
          const x = r.left + Math.min(r.width / 2, 20), yy = r.top + r.height / 2;
          const hit = document.elementFromPoint(x, yy);
          if (!hit || hit === el || el.contains(hit) || hit.contains(el)) continue;
          if (pinned(hit)) continue;
          add('text-covered', el, 'under ' + where(hit));
        }
      }
      window.scrollTo(0, 0);
    }
  }

  if (opts.detail) {
    for (const el of textEls) {
      if (!shown(el) || fade(el) < 0.05) continue;
      const s = cs(el), fs = parseFloat(s.fontSize), wt = parseInt(s.fontWeight, 10) || 400;
      const prose = /^(P|LI|TD|DD|BLOCKQUOTE|FIGCAPTION)$/.test(el.tagName);
      if (prose ? fs < 12 : fs < 11) add('tiny-text', el, fs + 'px');
      const bg = background(el);
      if (bg && !el.closest('[disabled], [aria-disabled=true]')) {
        const fg = rgba(s.color);
        const c = ratio(over(fg, bg), bg);
        const need = (fs >= 24 || (fs >= 18.6 && wt >= 700)) ? 3 : 4.5;
        if (c < need - 0.02) add('low-contrast', el, c.toFixed(2) + ':1, needs ' + need + ':1');
      }
      if (/^(P|LI|BLOCKQUOTE|DD)$/.test(el.tagName)) {
        const n = lines(el);
        const lh = s.lineHeight === 'normal' ? 1.2 * fs : parseFloat(s.lineHeight);
        if (n >= 2 && lh / fs < 1.3) add('tight-leading', el, (lh / fs).toFixed(2));
        const chars = (el.innerText || '').length;
        if (el.tagName === 'P' && n >= 3 && chars / n > 88) add('line-length', el, Math.round(chars / n) + ' characters a line');
        if (el.tagName === 'P' && n >= 4 && chars > 200 && chars / n < 35) add('line-length', el, Math.round(chars / n) + ' characters a line');
      }
      if (/^H[1-3]$/.test(el.tagName)) {
        const words = (el.innerText || '').trim().split(/\s+/);
        if (words.length >= 4 && lines(el) >= 2 && !el.querySelector('br')) {
          const rg = document.createRange(); rg.selectNodeContents(el);
          const rs = [...rg.getClientRects()].filter(r => r.width > 1);
          const last = rs[rs.length - 1];
          const probe = document.createElement('span'); probe.textContent = words[words.length - 1];
          probe.style.cssText = 'position:absolute;visibility:hidden;white-space:nowrap;font:inherit;letter-spacing:inherit';
          el.appendChild(probe); const w = probe.getBoundingClientRect().width; probe.remove();
          if (last && last.width <= w + 4) add('straggler-heading', el, '"' + words[words.length - 1] + '" alone');
        }
      }
    }
    for (const h of document.querySelectorAll('h2, h3')) {
      const p = h.previousElementSibling, n = h.nextElementSibling;
      if (!p || !n || !shown(p) || !shown(n) || !shown(h)) continue;
      const above = h.getBoundingClientRect().top - p.getBoundingClientRect().bottom;
      const below = n.getBoundingClientRect().top - h.getBoundingClientRect().bottom;
      if (below > 4 && above < 0.75 * below) add('crowded-head', h, Math.round(above) + 'px above, ' + Math.round(below) + 'px below');
    }
    for (const el of document.body.querySelectorAll('*')) {
      if (!shown(el) || !ownText(el) || /^(BUTTON|INPUT|SELECT|TEXTAREA|A|SPAN|CODE|KBD|MARK|LABEL|EM|STRONG|B|I|TD|TH)$/.test(el.tagName)) continue;
      const s = cs(el);
      if (!/block|flex|grid|list-item/.test(s.display)) continue;
      const parent = el.parentElement ? background(el.parentElement) : null;
      const fill = rgba(s.backgroundColor);
      const filled = fill[3] > 0.2 && parent && ratio(over(fill, parent), parent) > 1.05;
      const sideRule = parseFloat(s.borderLeftWidth) >= 2 && s.borderLeftStyle !== 'none';
      if (!filled && !sideRule) continue;
      const fs = parseFloat(s.fontSize);
      const px = sideRule && !filled ? parseFloat(s.paddingLeft) : Math.min(parseFloat(s.paddingLeft), parseFloat(s.paddingRight));
      const py = Math.min(parseFloat(s.paddingTop), parseFloat(s.paddingBottom));
      if (px < Math.max(8, 0.5 * fs) || (filled && py < Math.max(4, 0.3 * fs))) add('cramped-box', el, 'padding ' + Math.round(py) + 'px / ' + Math.round(px) + 'px');
    }
    const h2s = [...document.querySelectorAll('h2')].filter(shown).map(h => parseFloat(cs(h).fontSize)).sort((a, b) => a - b);
    if (h2s.length >= 2 && h2s[Math.floor(h2s.length / 2)] < 40) add('small-section-heads', null, 'median h2 ' + h2s[Math.floor(h2s.length / 2)] + 'px');
    for (const el of document.body.querySelectorAll('div, section, figure, span, a')) {
      const r = el.getBoundingClientRect();
      if (r.width < 300 || r.height < 200 || !shown(el)) continue;
      if ((el.innerText || '').trim().length > 2) continue;
      if (el.querySelector('img, svg, video, canvas, picture, iframe, object, embed, input, textarea')) continue;
      const s = cs(el);
      if (s.pointerEvents === 'none' && /absolute|fixed/.test(s.position)) continue;
      const painted = (s.backgroundImage !== 'none' && !/url\(/.test(s.backgroundImage)) || rgba(s.backgroundColor)[3] > 0.1;
      if (painted) add('empty-picture', el, Math.round(r.width) + ' x ' + Math.round(r.height));
    }
    for (const el of document.body.querySelectorAll('*')) {
      const kids = [...el.children];
      if (kids.length < 24) continue;
      const key = (k) => k.tagName + '|' + k.className;
      const first = key(kids[0]);
      const same = kids.filter(k => key(k) === first && !(k.innerText || '').trim() && k.getBoundingClientRect().width < 80);
      if (same.length >= 24) add('counting-marks', el, same.length + ' identical marks');
    }
    const heroBottom = hero ? hero.getBoundingClientRect().bottom + scrollY : 0;
    const docH = document.documentElement.scrollHeight;
    let photo = 0;
    for (const im of document.querySelectorAll('img, picture > img, video')) {
      const r = im.getBoundingClientRect();
      if (r.top + scrollY < heroBottom || r.width * r.height < 10000 || /\.svg(\?|$)/.test(im.currentSrc || im.src || '')) continue;
      photo += r.width * r.height;
    }
    const below = (docH - heroBottom) * vw;
    if (below > 0 && photo / below > 1 / 3) add('photo-wall', null, Math.round(100 * photo / below) + '% of the page under the hero');
    const bl = blocks();
    const lastBlock = bl[bl.length - 1];
    const tail = [lastBlock, bl[bl.length - 2]].filter(Boolean);
    for (const b of tail) {
      const f = b.querySelector('form') || b;
      const fields = [...f.querySelectorAll('input, select, textarea')].filter(i => shown(i) && !/^(submit|button|hidden|reset|image)$/.test(i.type));
      if (fields.length === 1 && fields[0].type === 'email') { add('stock-close', b, 'a lone email field in the closing block'); break; }
    }
    const boxes = bl.map(b => ({b, c: contentBox(b), bg: background(b)})).filter(x => x.c);
    const gaps = [];
    for (let i = 0; i + 1 < boxes.length; i++) {
      const g = boxes[i + 1].c.top - boxes[i].c.bottom;
      const change = boxes[i].bg && boxes[i + 1].bg && ratio(boxes[i].bg, boxes[i + 1].bg) > 1.1;
      gaps.push(g);
      if (g < (change ? 64 : 120)) add('section-gap', boxes[i + 1].b, Math.round(g) + 'px after the block above');
    }
    if (gaps.length >= 3 && Math.max(...gaps) - Math.min(...gaps) < 4) add('section-gap', null, 'every gap is ' + Math.round(gaps[0]) + 'px');
    let flood = 0;
    for (const el of document.body.querySelectorAll('*')) {
      if (!shown(el)) continue;
      const c = rgba(cs(el).backgroundColor);
      if (c[3] < 0.5) continue;
      const [r, g, b] = c.map(v => v / 255), mx = Math.max(r, g, b), mn = Math.min(r, g, b), l = (mx + mn) / 2;
      const sat = mx === mn ? 0 : (mx - mn) / (1 - Math.abs(2 * l - 1));
      if (sat < 0.35 || l < 0.2 || l > 0.85) continue;
      const pr = el.parentElement && rgba(cs(el.parentElement).backgroundColor);
      if (pr && pr[3] > 0.5 && pr.slice(0, 3).join() === c.slice(0, 3).join()) continue;
      const q = el.getBoundingClientRect();
      const w = Math.max(0, Math.min(vw, q.right) - Math.max(0, q.left)), h = Math.max(0, Math.min(vh, q.bottom) - Math.max(0, q.top));
      flood += w * h;
    }
    const cap = opts.atmospheric ? 0.30 : opts.loud ? 0.60 : 0.08;
    const declared = /posture:\s*full-palette/i.test(document.documentElement.innerHTML.slice(0, 20000));
    if (!declared && flood / (vw * vh) > cap) add('accent-flood', null, Math.round(100 * flood / (vw * vh)) + '% of the first screen');
    if (hero) {
      const hc = contentBox(hero);
      const idx = bl.indexOf(hero.closest('section, header') || hero);
      const next = bl.find((b, i) => i > idx && b !== hero && !hero.contains(b) && b.tagName !== 'FOOTER') || null;
      if (next) {
        const top = next.getBoundingClientRect().top + scrollY;
        if (top < 760 || top > 900) add('next-section-position', next, 'starts at y ' + Math.round(top));
        const nc = contentBox(next);
        const hb = background(hero), nb = background(next);
        const edge = hb && nb && ratio(hb, nb) > 1.05 ? top : Infinity;
        if (hc && hc.bottom < vh) {
          const empty = Math.min(vh, edge, nc ? nc.top : vh) - hc.bottom;
          if (empty > 160) add('dead-band', hero, Math.round(empty) + 'px empty above the fold');
        }
      }
    }
    for (const im of document.images) {
      if (im.complete && im.naturalWidth === 0 && (im.currentSrc || im.getAttribute('src'))) add('broken-image', im, im.getAttribute('src') || '');
    }
  }

  if (opts.hero && h1) {
    const scope = hero || h1.parentElement;
    const checks = [['headline', h1]];
    const lede = [...scope.querySelectorAll('p')].find(p => shown(p) && (h1.compareDocumentPosition(p) & 4));
    if (lede) checks.push(['lede', lede]);
    const act = [...scope.querySelectorAll('a, button')].find(a => shown(a) && /btn|button|cta|primary/i.test(a.className + ' ' + (a.getAttribute('role') || '') + ' ' + a.tagName));
    if (act) checks.push(['main action', act]);
    const vis = [...scope.querySelectorAll('img, svg, video, picture, canvas')].find(v => { const r = v.getBoundingClientRect(); return r.width * r.height > 40000; });
    for (const [name, el] of checks) if (el.getBoundingClientRect().bottom > vh) add('hero-out-of-view', el, name + ' ends at y ' + Math.round(el.getBoundingClientRect().bottom));
    if (vis) { const r = vis.getBoundingClientRect(); if ((r.top + r.bottom) / 2 > vh) add('hero-out-of-view', vis, 'visual centre at y ' + Math.round((r.top + r.bottom) / 2)); }
  }

  if (opts.wide) {
    for (const p of document.querySelectorAll('p')) {
      if (!shown(p) || (p.innerText || '').length < 100 || p.closest('header, nav, footer')) continue;
      const r = p.getBoundingClientRect();
      if (r.left < 120 || vw - r.right < 120) { add('no-max-width', p, 'gutter ' + Math.round(Math.min(r.left, vw - r.right)) + 'px'); break; }
    }
  }

  if (opts.hidden) {
    const H = document.documentElement.scrollHeight;
    for (let y = 0; y < H; y += Math.max(200, Math.floor(vh * 0.7))) {
      window.scrollTo(0, y);
      await new Promise(r => setTimeout(r, 40));
    }
    window.scrollTo(0, H);
    await new Promise(r => setTimeout(r, 300));
    window.scrollTo(0, 0);
    await new Promise(r => setTimeout(r, 600));
    let total = 0, hid = 0, sample = '';
    for (const el of textEls) {
      const r = el.getBoundingClientRect();
      if (r.width < 1 || r.height < 1) continue;
      const n = ownText(el).length;
      total += n;
      if (fade(el) <= 0.02) { hid += n; if (!sample) sample = ownText(el).slice(0, 40); }
    }
    if (total >= 200 && hid >= 120 && hid / total > 0.25) add('hidden-at-rest', null, Math.round(100 * hid / total) + '% of the text, e.g. "' + sample + '"');
  }

  const waivers = [];
  const walker = document.createTreeWalker(document, NodeFilter.SHOW_COMMENT);
  while (walker.nextNode()) waivers.push(walker.currentNode.textContent);
  for (const st of document.querySelectorAll('style')) waivers.push(st.textContent);
  return {findings: out, waivers};
}
"""


def targets(paths, allow_remote):
    pages, bad = [], []
    for p in paths:
        u = urlparse(p)
        if u.scheme in ("http", "https"):
            if u.hostname not in LOCAL_HOSTS and not allow_remote:
                bad.append(f"{p}: not a local address; pass --allow-remote to open it")
            else:
                pages.append((p, p))
            continue
        path = Path(p)
        if path.is_dir():
            for f in sorted(path.rglob("*.htm*")):
                if "node_modules" not in f.parts and f.suffix in (".html", ".htm"):
                    pages.append((str(f), f.resolve().as_uri()))
        elif path.is_file():
            pages.append((str(path), path.resolve().as_uri()))
        else:
            bad.append(f"{p}: no such file")
    return pages, bad


def parse_waivers(texts):
    allowed, problems = set(), []
    for t in texts:
        for m in WAIVER.finditer(t):
            names = [n.strip() for n in m.group(1).split(",") if n.strip()]
            reason = (m.group(2) or "").strip()
            unknown = [n for n in names if n not in RULES]
            if not reason or unknown:
                problems.append(("waiver-no-reason", "page",
                                 "unknown rule " + ", ".join(unknown) if unknown else "no reason given for " + ", ".join(names)))
                continue
            allowed.update(names)
    return allowed, problems


def check_page(browser, label, url, widths, genre, shots, allow_remote):
    found = {}
    first = {}
    errors = []
    waivers = []

    blocked = set()

    def route(r):
        u = urlparse(r.request.url)
        if u.scheme in ("file", "data", "blob", "about") or u.hostname in LOCAL_HOSTS or allow_remote:
            return r.continue_()
        if r.request.resource_type == "image":
            blocked.add(u.hostname)
        return r.abort()

    for w in widths:
        h = HEIGHT.get(w, 900 if w > 414 else 780)
        page = browser.new_page(viewport={"width": w, "height": h})
        page.route("**/*", route)
        page.on("pageerror", lambda e: errors.append(str(e).splitlines()[0][:160]))
        try:
            page.goto(url, wait_until="load", timeout=30000)
        except Exception as e:  # noqa: BLE001 - report navigation failure as a finding
            found.setdefault(("script-error", "page", f"could not load: {str(e).splitlines()[0][:120]}"), []).append(w)
            page.close()
            continue
        page.wait_for_timeout(150)
        opts = {
            "every": True,
            "cover": w in (375, 1440),
            "detail": w == 1440,
            "hero": w == 1280,
            "wide": w == 1920,
            "hidden": w == 1440,
            "atmospheric": genre == "atmospheric",
            "loud": genre == "playful",
        }
        res = page.evaluate(MEASURE_JS, opts)
        waivers = res["waivers"] or waivers
        for rule, where, detail in res["findings"]:
            per_width = rule in ("h-scroll", "label-wrap", "minor-link-wrap", "edge-text", "clipped-text", "text-covered")
            key = (rule, where, "" if per_width else detail)
            found.setdefault(key, []).append(w)
            if per_width:
                first.setdefault(key, detail)
        if shots:
            Path(shots).mkdir(parents=True, exist_ok=True)
            stem = re.sub(r"[^\w.-]+", "_", label).strip("_")[-80:]
            page.screenshot(path=str(Path(shots) / f"{stem}-{w}.png"), full_page=True)
        page.close()
    for e in dict.fromkeys(errors):
        found.setdefault(("script-error", "page", e), []).append(0)
    allowed, problems = parse_waivers(waivers)
    rows = []
    for (rule, where, detail), ws in found.items():
        if rule in allowed:
            continue
        detail = detail or first.get((rule, where, detail), "")
        if rule == "empty-picture" and blocked:
            detail += "; remote images were blocked (" + ", ".join(sorted(blocked))[:80] + "), try --allow-remote"
        rows.append({"file": label, "rule": rule, "severity": RULES[rule][0], "gate": RULES[rule][1],
                     "where": where, "detail": detail, "widths": sorted(set(x for x in ws if x)),
                     "note": RULES[rule][2]})
    for rule, where, detail in problems:
        rows.append({"file": label, "rule": rule, "severity": RULES[rule][0], "gate": RULES[rule][1],
                     "where": where, "detail": detail, "widths": [], "note": RULES[rule][2]})
    order = {"high": 0, "medium": 1, "low": 2}
    rows.sort(key=lambda r: (order[r["severity"]], r["rule"], r["where"]))
    return rows


def launch():
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return None, None, "the Python playwright package is not installed"
    pw = sync_playwright().start()
    tries = [os.environ.get("RENDER_CHECK_CHROMIUM"), None]
    tries += [shutil.which(n) for n in ("chromium", "chromium-browser", "google-chrome", "chrome")]
    first = ""
    for exe in dict.fromkeys(tries):
        if exe is None and tries.index(None) != tries.index(exe):
            continue
        try:
            opts = {"executable_path": exe, "args": ["--no-sandbox"]} if exe else {}
            return pw, pw.chromium.launch(headless=True, **opts), ""
        except Exception as e:  # noqa: BLE001 - try the next browser
            first = first or str(e).splitlines()[0][:160]
    pw.stop()
    return None, None, "Chromium would not start: " + first


def main(argv=None):
    ap = argparse.ArgumentParser(description="Measure built pages in a headless browser.")
    ap.add_argument("targets", nargs="*")
    ap.add_argument("--widths", default="")
    ap.add_argument("--only", default="")
    ap.add_argument("--genre", default="")
    ap.add_argument("--format", default="text", choices=["text", "json", "github"])
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--shots", default="")
    ap.add_argument("--allow-remote", action="store_true")
    ap.add_argument("--rules", action="store_true")
    a = ap.parse_args(argv)
    if a.rules:
        for k, (sev, gate, note) in RULES.items():
            print(f"{k:24} {sev:7} {gate:14} {note}")
        return 0
    fmt = "json" if a.json else a.format
    only = {x.strip() for x in a.only.split(",") if x.strip()}
    if only - set(RULES):
        print("render-check: unknown rule " + ", ".join(sorted(only - set(RULES))), file=sys.stderr)
        return 2
    try:
        widths = [int(x) for x in a.widths.split(",") if x.strip()] or WIDTHS
    except ValueError:
        print("render-check: --widths takes numbers, e.g. 320,1440", file=sys.stderr)
        return 2
    if not a.targets:
        ap.print_usage(sys.stderr)
        return 2
    pages, bad = targets(a.targets, a.allow_remote)
    for b in bad:
        print("render-check: " + b, file=sys.stderr)
    if bad:
        return 2
    pw, browser, why = launch()
    if not browser:
        print(f"render-check: skipped, no browser ({why})")
        return 3
    rows = []
    try:
        for label, url in pages:
            rows += check_page(browser, label, url, widths, a.genre, a.shots, a.allow_remote)
    finally:
        browser.close()
        pw.stop()
    if only:
        rows = [r for r in rows if r["rule"] in only]
    if fmt == "json":
        print(json.dumps(rows, indent=1))
    elif fmt == "github":
        for r in rows:
            kind = "error" if r["severity"] == "high" else "warning"
            at = f" at {','.join(map(str, r['widths']))}px" if r["widths"] else ""
            print(f"::{kind} file={r['file']},title=render-check {r['rule']}::{r['where']}{at}: {r['detail'] or r['note']}")
    else:
        if not rows:
            print(f"render-check: no findings ({len(pages)} page(s), widths {','.join(map(str, widths))})")
        for r in rows:
            at = f" @{','.join(map(str, r['widths']))}" if r["widths"] else ""
            detail = f" ({r['detail']})" if r["detail"] else ""
            print(f"{r['file']}: {r['severity']:6} {r['rule']}{at}: {r['where']}{detail}; {r['note']} [{r['gate']}]")
    return 1 if rows else 0


if __name__ == "__main__":
    sys.exit(main())
