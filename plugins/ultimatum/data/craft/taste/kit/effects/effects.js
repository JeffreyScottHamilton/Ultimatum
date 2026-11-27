// Taste kit: three WebGL effects on one small runtime (tech pages only).
//
//   <div class="fx" data-fx="orb-sphere" data-seed="3"></div>
//   <script defer src="effects.js"></script>   (a plain script, so the page also works from disk)
//
// The element's CSS poster shows first and stays when motion is reduced, on
// phones (under 700px), without WebGL2, or when a shader fails to build. A
// canvas mounts only near the screen (IntersectionObserver) and is released
// when it leaves; the drawing loop also stops while the tab is hidden.
// Budget (performance.md § WebGL): at most 4 live contexts, device pixel ratio
// capped at 1.5, about 1.5 MP across all canvases, noise at half resolution,
// 30 frames a second. Each effect runs for RUN seconds, then holds its last
// frame, so it needs no pause control; a fine pointer entering restarts it.
// Colours come from the page tokens --bg, --ink and --accent.
// window.tasteEffects.start(root) mounts frames added later.

(() => {

const RUN = 8;
const MAX_LIVE = 4;
const MAX_PIXELS = 1.5e6;
const FRAME_MS = 1000 / 30;
const STILL = '(prefers-reduced-motion: reduce), (max-width: 699px)';

const HEAD = `#version 300 es
precision highp float;
uniform vec2 u_res; uniform float u_time; uniform float u_seed;
uniform vec3 u_bg; uniform vec3 u_ink; uniform vec3 u_accent; uniform vec2 u_point;
out vec4 o;
float hash(vec2 p) {
  ivec2 cell = ivec2(floor(p)) + 8192;
  uint h = (uint(cell.x) * 1597334677u) ^ (uint(cell.y) * 3812015801u);
  h = h * 747796405u + 2891336453u; h ^= h >> 16u; h *= 2246822519u; h ^= h >> 13u;
  return float(h) / 4294967295.0;
}
float vnoise(vec2 p) {
  vec2 cell = floor(p), f = fract(p);
  vec2 s = (3.0 - 2.0 * f) * f * f;
  float top = mix(hash(cell + vec2(0, 1)), hash(cell + vec2(1, 1)), s.x);
  float low = mix(hash(cell), hash(cell + vec2(1, 0)), s.x);
  return mix(low, top, s.y);
}
`;

const EFFECTS = {
  // Quiet: soft shapes in the accent family drifting under a still grain.
  'grain-gradient': { scale: 0.5, src: `
void main() {
  vec2 p = gl_FragCoord.xy / u_res.y;
  float aspect = u_res.x / u_res.y;
  float t = u_time * 0.045 + u_seed * 1.7;
  p += 0.18 * vec2(vnoise(p * 1.6 + t), vnoise(p * 1.6 - t + 4.0)) - 0.09;
  float field = 0.0;
  for (int k = 0; k < 3; k++) {
    float fk = float(k) + u_seed;
    vec2 c = vec2(aspect * (0.2 + 0.6 * hash(vec2(fk, 3.0))) + 0.12 * sin(t * 2.0 + fk),
                  0.2 + 0.6 * hash(vec2(7.0, fk)) + 0.1 * cos(t * 1.6 + fk * 2.0));
    field += exp(-dot(p - c, p - c) * 5.5);
  }
  vec3 soft = mix(u_bg, u_accent, 0.42);
  vec3 col = mix(u_bg, soft, clamp(field, 0.0, 1.0));
  col += (hash(gl_FragCoord.xy * 1.37) - 0.5) * 0.045;
  o = vec4(col, 1.0);
}` },

  // Focal: one lit sphere with a rim; the light leans toward the pointer.
  'orb-sphere': { scale: 0.75, src: `
void main() {
  vec2 p = (2.0 * gl_FragCoord.xy - u_res) / u_res.y;
  float r = 0.62;
  float swing = 0.55 * sin(u_time * 0.5 + u_seed);
  vec3 light = normalize(vec3(-0.55 + swing + 0.5 * u_point.x, 0.6 + 0.3 * u_point.y, 0.85));
  vec3 col = mix(u_bg, u_ink, 0.06 * smoothstep(1.4, 0.0, length(p - vec2(0.12, -0.7)) * 1.6));
  float d = length(p);
  if (d < r) {
    vec3 n = vec3(p / r, sqrt(1.0 - d * d / (r * r)));
    float lit = max(dot(n, light), 0.0);
    float rim = pow(1.0 - n.z, 3.0);
    float shine = pow(max(dot(reflect(-light, n), vec3(0, 0, 1)), 0.0), 40.0);
    vec3 body = mix(mix(u_ink, u_accent, 0.35), u_accent, lit);
    col = body + rim * mix(u_accent, u_bg, 0.5) * 0.9 + shine * 0.55;
  }
  float edge = smoothstep(r + 0.006, r - 0.006, d);
  o = vec4(mix(mix(u_bg, u_ink, 0.04), col, max(edge, d < r ? 1.0 : 0.0)), 1.0);
}` },

  // Pattern: signals running along a hairline grid; never behind UI.
  'grid-pulse': { scale: 0.75, src: `
uniform float u_cell;
void main() {
  vec2 g = gl_FragCoord.xy / u_cell;
  vec2 dist = abs(fract(g + 0.5) - 0.5) * u_cell;
  float hair = max(smoothstep(1.0, 0.0, dist.x), smoothstep(1.0, 0.0, dist.y));
  vec3 col = mix(u_bg, u_ink, 0.1 * hair);
  float fade = 1.0 - smoothstep(${(RUN - 1.5).toFixed(1)}, ${RUN.toFixed(1)}, u_time);
  vec2 line = floor(g + 0.5);
  float rowPick = hash(vec2(line.y, u_seed)), colPick = hash(vec2(u_seed, line.x + 50.0));
  float along = 0.0;
  if (rowPick > 0.72) {
    float head = fract(u_time * (0.05 + 0.05 * rowPick) + rowPick * 9.0) * (u_res.x / u_cell + 6.0) - 3.0;
    float behind = head - g.x;
    along = max(along, smoothstep(2.2, 0.0, dist.y) * step(0.0, behind) * exp(-behind * 0.45));
  }
  if (colPick > 0.78) {
    float head = fract(u_time * (0.04 + 0.05 * colPick) + colPick * 5.0) * (u_res.y / u_cell + 6.0) - 3.0;
    float behind = head - g.y;
    along = max(along, smoothstep(2.2, 0.0, dist.x) * step(0.0, behind) * exp(-behind * 0.45));
  }
  o = vec4(mix(col, u_accent, along * fade), 1.0);
}` },
};

// Read a CSS colour token as 0..1 RGB, whatever colour syntax it uses.
const swatch = new OffscreenCanvas(2, 2).getContext('2d', { willReadFrequently: true });
function rgb(el, name, fallback) {
  const raw = getComputedStyle(el).getPropertyValue(name).trim() || fallback;
  swatch.globalCompositeOperation = 'copy';
  swatch.fillStyle = fallback; // kept if the token does not parse
  swatch.fillStyle = raw;
  swatch.fillRect(0, 0, 2, 2);
  const px = swatch.getImageData(0, 0, 2, 2).data;
  return [px[0], px[1], px[2]].map((v) => v / 255);
}

function build(gl, src) {
  const program = gl.createProgram();
  const parts = [[gl.VERTEX_SHADER, '#version 300 es\nin vec2 a;\nvoid main() { gl_Position = vec4(a, 0.0, 1.0); }'],
                 [gl.FRAGMENT_SHADER, HEAD + src]];
  for (const [kind, text] of parts) {
    const stage = gl.createShader(kind);
    gl.shaderSource(stage, text);
    gl.compileShader(stage);
    const built = gl.getShaderParameter(stage, gl.COMPILE_STATUS);
    if (!built) throw new Error(`compile: ${gl.getShaderInfoLog(stage)}`);
    gl.attachShader(program, stage);
  }
  gl.linkProgram(program);
  const linked = gl.getProgramParameter(program, gl.LINK_STATUS);
  if (!linked) throw new Error(`link: ${gl.getProgramInfoLog(program)}`);
  return program;
}

const live = new Map(); // element -> state

function pixelsInUse(except) {
  let sum = 0;
  for (const [el, s] of live) if (el !== except) sum += s.canvas.width * s.canvas.height;
  return sum;
}

function mount(el) {
  const effect = EFFECTS[el.dataset.fx];
  if (!effect || live.has(el) || live.size >= MAX_LIVE) return;
  const canvas = document.createElement('canvas');
  canvas.setAttribute('aria-hidden', 'true');
  const gl = canvas.getContext('webgl2', { antialias: false, alpha: false, powerPreference: 'low-power' });
  if (!gl) { el.dataset.fxState = 'poster: no webgl2'; return; }
  let program;
  try { program = build(gl, effect.src); } catch (err) {
    el.dataset.fxState = 'poster: shader failed';
    el.dataset.fxError = String(err.message).slice(0, 200);
    gl.getExtension('WEBGL_lose_context')?.loseContext();
    return;
  }
  const box = el.getBoundingClientRect();
  const over = 24; // oversize by 24 css px, clipped by the frame
  const dpr = Math.min(window.devicePixelRatio || 1, 1.5);
  let k = dpr * effect.scale;
  const want = (box.width + over) * (box.height + over) * k * k;
  const room = MAX_PIXELS - pixelsInUse(el);
  if (want > room) k *= Math.sqrt(Math.max(room, 0) / want);
  if (k < 0.2) { el.dataset.fxState = 'poster: pixel budget spent'; gl.getExtension('WEBGL_lose_context')?.loseContext(); return; }
  const w = Math.round((box.width + over) * k), h = Math.round((box.height + over) * k);
  Object.assign(canvas, { width: w, height: h });
  gl.useProgram(program);
  gl.viewport(0, 0, w, h);
  gl.bindBuffer(gl.ARRAY_BUFFER, gl.createBuffer());
  const cover = new Float32Array([-1, 3, -1, -1, 3, -1]); // one triangle over the whole frame
  gl.bufferData(gl.ARRAY_BUFFER, cover, gl.STATIC_DRAW);
  const at = gl.getAttribLocation(program, 'a');
  gl.enableVertexAttribArray(at);
  gl.vertexAttribPointer(at, 2, gl.FLOAT, false, 0, 0);
  const u = (name) => gl.getUniformLocation(program, name);
  gl.uniform2f(u('u_res'), w, h);
  gl.uniform1f(u('u_seed'), Number(el.dataset.seed || 1));
  gl.uniform3fv(u('u_bg'), rgb(el, '--bg', '#f3f4f5'));
  gl.uniform3fv(u('u_ink'), rgb(el, '--ink', '#15181c'));
  gl.uniform3fv(u('u_accent'), rgb(el, '--accent', '#0a5c63'));
  gl.uniform1f(u('u_cell'), 40 * k);
  gl.uniform2f(u('u_point'), 0, 0);
  el.append(canvas);
  const state = { canvas, gl, program, u, start: 0, last: 0, raf: 0, done: false, point: [0, 0] };
  live.set(el, state);
  el.dataset.fxState = 'running';
  play(el, state);
}

function draw(state, seconds) {
  const { gl, u } = state;
  gl.uniform1f(u('u_time'), seconds);
  gl.uniform2f(u('u_point'), state.point[0], state.point[1]);
  gl.drawArrays(gl.TRIANGLES, 0, 3);
}

function play(el, state) {
  cancelAnimationFrame(state.raf);
  state.done = false;
  state.start = 0;
  const tick = (now) => {
    if (document.hidden || !live.has(el)) { state.raf = 0; return; }
    if (!state.start) state.start = now;
    if (now - state.last >= FRAME_MS - 1) {
      state.last = now;
      const seconds = Math.min((now - state.start) / 1000, RUN);
      draw(state, seconds);
      if (!el.classList.contains('fx--on')) el.classList.add('fx--on');
      if (seconds >= RUN) { state.done = true; state.raf = 0; el.dataset.fxState = 'settled'; return; }
    }
    state.raf = requestAnimationFrame(tick);
  };
  state.raf = requestAnimationFrame(tick);
}

function unmount(el) {
  const state = live.get(el);
  if (!state) return;
  cancelAnimationFrame(state.raf);
  live.delete(el);
  state.gl.getExtension('WEBGL_lose_context')?.loseContext();
  state.canvas.remove();
  el.classList.remove('fx--on');
  el.dataset.fxState = 'unmounted';
}

function start(root = document) {
  const frames = [...root.querySelectorAll('.fx[data-fx]')];
  const still = matchMedia(STILL);
  if (still.matches) { frames.forEach((el) => { el.dataset.fxState = 'poster: still'; }); return; }
  const near = new IntersectionObserver((entries) => {
    for (const e of entries) (e.isIntersecting ? mount : unmount)(e.target);
  }, { rootMargin: '200px 0px' });
  frames.forEach((el) => {
    near.observe(el);
    if (!matchMedia('(pointer: fine)').matches) return;
    if (el.dataset.fx === 'orb-sphere') {
      el.addEventListener('pointermove', (ev) => {
        const s = live.get(el);
        if (!s) return;
        const b = el.getBoundingClientRect();
        s.point = [((ev.clientX - b.left) / b.width) * 2 - 1, 1 - ((ev.clientY - b.top) / b.height) * 2];
        if (s.done) draw(s, RUN);
      });
    }
    el.addEventListener('pointerenter', () => { const s = live.get(el); if (s && s.done) play(el, s); });
  });
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) return;
    for (const [el, s] of live) if (!s.done && !s.raf) play(el, s);
  });
  still.addEventListener('change', () => { if (still.matches) [...live.keys()].forEach(unmount); });
}

window.tasteEffects = { start };
start();
})();
