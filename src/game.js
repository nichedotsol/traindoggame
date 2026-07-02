const canvas = document.querySelector("#game");
const ctx = canvas.getContext("2d");
ctx.imageSmoothingEnabled = false;

const ui = {
  stop: document.querySelector("#stop"),
  whistles: document.querySelector("#whistles"),
  hearts: document.querySelector("#hearts"),
  message: document.querySelector("#message"),
  route: document.querySelector("#route"),
};

const W = 320;
const H = 180;
const SCALE = 3;
const GROUND = 140;
const PLAYER_X = 62;
const LEVEL_LENGTH = 1500;

const keys = new Set();
let lastTime = performance.now();
let messageTimer = 4;
let chooTimer = 0;
let shake = 0;

const stops = [
  {
    name: "Forest",
    next: "Alps",
    sky: ["#67b9f0", "#bfeeff"],
    far: "#90cae8",
    mid: "#3e765d",
    near: "#27533f",
    ground: "#5f923f",
    dirt: "#5b3a25",
    rail: "#41313b",
    portal: "#46e96f",
    npc: "ranger",
    hazard: "pineRock",
    landmark: "pines",
  },
  {
    name: "Alps",
    next: "Tokyo",
    sky: ["#75c9ff", "#ecfbff"],
    far: "#d7eef6",
    mid: "#6d92b3",
    near: "#314c67",
    ground: "#d8f3fa",
    dirt: "#7b786f",
    rail: "#363945",
    portal: "#45a7ff",
    npc: "skier",
    hazard: "snowBoulder",
    landmark: "mountains",
  },
  {
    name: "Tokyo",
    next: "Sahara",
    sky: ["#6357be", "#f08aa8"],
    far: "#ffc477",
    mid: "#372f76",
    near: "#1e1941",
    ground: "#4e4364",
    dirt: "#2b263d",
    rail: "#171722",
    portal: "#b65cff",
    npc: "vendor",
    hazard: "lantern",
    landmark: "city",
  },
  {
    name: "Sahara",
    next: "Reef",
    sky: ["#f4a85e", "#ffe7a5"],
    far: "#f7cf78",
    mid: "#c67939",
    near: "#9d5830",
    ground: "#e7b15b",
    dirt: "#8d5732",
    rail: "#4d322f",
    portal: "#ff8b26",
    npc: "guide",
    hazard: "cactus",
    landmark: "dunes",
  },
  {
    name: "Reef",
    next: "Arctic",
    sky: ["#48b7d9", "#d7fff7"],
    far: "#76e0de",
    mid: "#228f9c",
    near: "#156373",
    ground: "#d9ba71",
    dirt: "#6c563e",
    rail: "#33404b",
    portal: "#25e4db",
    npc: "diver",
    hazard: "waveCrate",
    landmark: "lighthouse",
  },
  {
    name: "Arctic",
    next: "Orbit",
    sky: ["#11274e", "#75d8ff"],
    far: "#b8fff4",
    mid: "#59a5c8",
    near: "#1f5f82",
    ground: "#d8f7ff",
    dirt: "#8eb6c4",
    rail: "#3a4d60",
    portal: "#64f7ff",
    npc: "parka",
    hazard: "iceSpike",
    landmark: "aurora",
  },
  {
    name: "Orbit",
    next: "Moon",
    sky: ["#07071b", "#15124c"],
    far: "#45427d",
    mid: "#22235b",
    near: "#121333",
    ground: "#32324f",
    dirt: "#17172c",
    rail: "#54516e",
    portal: "#906cff",
    npc: "astronaut",
    hazard: "meteor",
    landmark: "stars",
  },
  {
    name: "Moon",
    next: "Home",
    sky: ["#050511", "#1b1d35"],
    far: "#777b95",
    mid: "#555a70",
    near: "#33384d",
    ground: "#b9bbc7",
    dirt: "#626676",
    rail: "#494c5b",
    portal: "#f4f5ff",
    npc: "moon",
    hazard: "crater",
    landmark: "earth",
  },
];

const routeNames = stops.map((stop) => stop.name);
ui.route.innerHTML = routeNames.map((name) => `<span class="route-stop" data-stop="${name}">${name}</span>`).join("");

const state = {
  stopIndex: 0,
  distance: 0,
  speed: 86,
  whistles: 0,
  hearts: 3,
  status: "ready",
  won: false,
};

const player = {
  x: PLAYER_X,
  y: GROUND,
  vy: 0,
  grounded: true,
  ducking: false,
  frame: "idle",
  invulnerable: 0,
};

let levelItems = [];
let particles = [];

function canvasSprite(w, h, draw) {
  const c = document.createElement("canvas");
  c.width = w;
  c.height = h;
  const g = c.getContext("2d");
  g.imageSmoothingEnabled = false;
  draw(g, w, h);
  return c;
}

function px(g, x, y, w, h, color) {
  g.fillStyle = color;
  g.fillRect(Math.round(x), Math.round(y), Math.round(w), Math.round(h));
}

function outline(g, x, y, w, h, color = "#111018") {
  px(g, x, y, w, h, color);
}

function dogHead(g, x, y, tongue = true) {
  outline(g, x + 5, y + 2, 24, 23);
  px(g, x + 7, y + 4, 19, 19, "#e0a14a");
  px(g, x + 4, y + 7, 6, 13, "#b77036");
  px(g, x + 24, y + 8, 5, 11, "#b77036");
  px(g, x + 12, y + 3, 10, 5, "#f1bd62");
  px(g, x + 16, y + 13, 4, 3, "#111018");
  px(g, x + 25, y + 14, 7, 6, "#111018");
  px(g, x + 18, y + 20, 10, 2, "#111018");
  if (tongue) {
    px(g, x + 22, y + 22, 7, 10, "#f386a4");
    px(g, x + 25, y + 23, 2, 5, "#ffc0cc");
    px(g, x + 22, y + 31, 6, 2, "#111018");
  }
}

function trainBody(g, wheelShift = 0, tilt = 0) {
  px(g, 4, 22 + tilt, 44, 19, "#111018");
  px(g, 8, 15 + tilt, 26, 13, "#111018");
  px(g, 10, 17 + tilt, 22, 9, "#25232b");
  px(g, 6, 24 + tilt, 39, 14, "#24232a");
  px(g, 14, 10 + tilt, 10, 7, "#111018");
  px(g, 16, 8 + tilt, 12, 3, "#30303a");
  px(g, 37, 8 + tilt, 9, 13, "#111018");
  px(g, 39, 5 + tilt, 11, 4, "#30303a");
  px(g, 43, 20 + tilt, 9, 3, "#bd6841");
  px(g, 2, 35 + tilt, 54, 5, "#111018");
  for (let i = 0; i < 4; i += 1) {
    const x = 9 + i * 11;
    px(g, x, 40 + tilt, 8, 8, "#111018");
    px(g, x + 2 + wheelShift, 42 + tilt, 4, 4, "#555861");
  }
  px(g, 5, 22 + tilt, 4, 14, "#4b2930");
  px(g, 10, 25 + tilt, 3, 8, "#6ea5b3");
}

function trainSprite(kind) {
  return canvasSprite(92, 58, (g) => {
    const tilt = kind === "jump" ? -2 : kind === "duck" ? 4 : 0;
    const wheelShift = kind === "runB" ? 2 : 0;
    trainBody(g, wheelShift, tilt);
    dogHead(g, 49, 10 + tilt, kind !== "duck");
    if (kind !== "duck") {
      px(g, 36, 2 + tilt, 7, 4, "#d9d9df");
      px(g, 28, 0 + tilt, 8, 5, "#e9eef2");
      px(g, 18, 2 + tilt, 7, 4, "#e9eef2");
    }
    if (kind === "jump") {
      px(g, 52, 42, 9, 3, "#f06d46");
      px(g, 39, 43, 7, 2, "#f7b941");
    }
  });
}

function drawSmallFace(g, x, y, coat, hat) {
  px(g, x + 4, y + 5, 14, 14, "#d59a66");
  px(g, x + 6, y + 10, 2, 2, "#111018");
  px(g, x + 14, y + 10, 2, 2, "#111018");
  px(g, x + 9, y + 16, 6, 2, "#111018");
  px(g, x + 2, y + 20, 18, 17, coat);
  px(g, x + 1, y + 37, 7, 6, "#111018");
  px(g, x + 14, y + 37, 7, 6, "#111018");
  px(g, x + 1, y + 1, 20, 6, "#111018");
  px(g, x + 4, y - 1, 14, 6, hat);
}

function npcSprite(kind) {
  return canvasSprite(38, 48, (g) => {
    if (kind === "ranger") drawSmallFace(g, 8, 4, "#2f8250", "#315a36");
    if (kind === "skier") {
      drawSmallFace(g, 8, 4, "#58a8e5", "#f4f5ff");
      px(g, 3, 43, 30, 3, "#111018");
      px(g, 4, 41, 28, 2, "#eafcff");
    }
    if (kind === "vendor") {
      drawSmallFace(g, 8, 4, "#d23b70", "#2d275f");
      px(g, 3, 28, 6, 12, "#ffd45f");
    }
    if (kind === "guide") {
      drawSmallFace(g, 8, 4, "#bf6b36", "#f4d47b");
      px(g, 27, 15, 3, 28, "#111018");
      px(g, 25, 13, 7, 3, "#f4d47b");
    }
    if (kind === "diver") {
      drawSmallFace(g, 8, 4, "#2ea6a2", "#f2cc57");
      px(g, 7, 13, 18, 4, "#76d7ff");
      px(g, 28, 11, 5, 13, "#111018");
    }
    if (kind === "parka") {
      drawSmallFace(g, 8, 4, "#78d3e5", "#eafcff");
      px(g, 10, 7, 14, 15, "#f6f6ff");
    }
    if (kind === "astronaut") {
      px(g, 8, 4, 22, 22, "#111018");
      px(g, 10, 6, 18, 18, "#f4f5ff");
      px(g, 13, 10, 12, 8, "#76d7ff");
      px(g, 9, 26, 20, 17, "#f4f5ff");
      px(g, 15, 29, 8, 5, "#ff6e7d");
      px(g, 7, 43, 9, 4, "#111018");
      px(g, 23, 43, 9, 4, "#111018");
    }
    if (kind === "moon") {
      px(g, 9, 5, 22, 22, "#111018");
      px(g, 11, 7, 18, 18, "#d7d8e1");
      px(g, 15, 12, 3, 3, "#777b95");
      px(g, 23, 16, 4, 4, "#777b95");
      px(g, 12, 28, 18, 14, "#9a9daf");
      px(g, 7, 42, 25, 4, "#111018");
    }
  });
}

function hazardSprite(kind) {
  return canvasSprite(40, 40, (g) => {
    if (kind === "pineRock") {
      px(g, 8, 21, 25, 13, "#111018");
      px(g, 10, 18, 20, 13, "#7b807d");
      px(g, 14, 15, 12, 5, "#aeb5ae");
      px(g, 13, 7, 5, 13, "#35573d");
      px(g, 8, 16, 16, 5, "#2c7542");
    }
    if (kind === "snowBoulder") {
      px(g, 8, 17, 24, 17, "#111018");
      px(g, 10, 14, 20, 17, "#dfeeff");
      px(g, 15, 11, 10, 6, "#ffffff");
      px(g, 14, 25, 5, 3, "#8a9db5");
    }
    if (kind === "lantern") {
      px(g, 17, 5, 5, 28, "#111018");
      px(g, 10, 15, 19, 18, "#111018");
      px(g, 12, 17, 15, 13, "#f05467");
      px(g, 15, 19, 8, 8, "#ffd45f");
    }
    if (kind === "cactus") {
      px(g, 17, 8, 10, 28, "#111018");
      px(g, 19, 6, 6, 28, "#2f9d50");
      px(g, 9, 18, 10, 6, "#111018");
      px(g, 9, 16, 7, 6, "#2f9d50");
      px(g, 25, 22, 9, 6, "#111018");
      px(g, 28, 20, 6, 6, "#2f9d50");
    }
    if (kind === "waveCrate") {
      px(g, 7, 22, 25, 13, "#111018");
      px(g, 9, 19, 21, 13, "#8b5a37");
      px(g, 11, 21, 17, 3, "#d19b57");
      px(g, 4, 13, 30, 8, "#111018");
      px(g, 6, 11, 26, 8, "#58d9e6");
    }
    if (kind === "iceSpike") {
      px(g, 8, 33, 25, 4, "#111018");
      px(g, 12, 10, 7, 23, "#eafcff");
      px(g, 20, 4, 9, 29, "#a7ebff");
      px(g, 27, 17, 5, 16, "#eafcff");
      px(g, 17, 10, 3, 23, "#111018");
    }
    if (kind === "meteor") {
      px(g, 14, 11, 18, 18, "#111018");
      px(g, 16, 9, 15, 17, "#99614d");
      px(g, 20, 13, 4, 4, "#f0ba62");
      px(g, 8, 4, 13, 6, "#ff6e38");
      px(g, 3, 8, 13, 5, "#ffd45f");
    }
    if (kind === "crater") {
      px(g, 5, 24, 30, 11, "#111018");
      px(g, 8, 21, 24, 11, "#777b95");
      px(g, 12, 24, 15, 5, "#484b5d");
      px(g, 17, 18, 7, 5, "#c8cad3");
    }
  });
}

function whistleSprite() {
  return canvasSprite(22, 18, (g) => {
    px(g, 4, 6, 14, 8, "#111018");
    px(g, 5, 4, 12, 8, "#f7b941");
    px(g, 14, 7, 5, 4, "#f7b941");
    px(g, 8, 6, 4, 3, "#fff3b0");
    px(g, 3, 12, 5, 3, "#ff8b26");
  });
}

function portalSprite(color) {
  return canvasSprite(56, 70, (g) => {
    px(g, 5, 13, 46, 52, "#111018");
    px(g, 8, 16, 40, 48, "#6b5d5b");
    px(g, 12, 20, 32, 41, "#312333");
    px(g, 16, 24, 24, 34, color);
    px(g, 19, 27, 18, 28, "#141229");
    px(g, 22, 30, 12, 22, color);
    px(g, 14, 10, 28, 8, "#48414b");
    px(g, 19, 5, 18, 7, "#777b95");
    px(g, 2, 61, 52, 6, "#111018");
    px(g, 0, 52, 8, 10, "#f7b941");
    px(g, 48, 52, 8, 10, "#f7b941");
  });
}

const sprites = {
  train: {
    idle: trainSprite("idle"),
    runA: trainSprite("runA"),
    runB: trainSprite("runB"),
    jump: trainSprite("jump"),
    duck: trainSprite("duck"),
  },
  whistle: whistleSprite(),
  npcs: Object.fromEntries(["ranger", "skier", "vendor", "guide", "diver", "parka", "astronaut", "moon"].map((n) => [n, npcSprite(n)])),
  hazards: Object.fromEntries(["pineRock", "snowBoulder", "lantern", "cactus", "waveCrate", "iceSpike", "meteor", "crater"].map((n) => [n, hazardSprite(n)])),
  portals: Object.fromEntries(stops.map((s) => [s.name, portalSprite(s.portal)])),
};

function buildLevel() {
  const items = [];
  const stop = stops[state.stopIndex];
  for (let x = 310; x < LEVEL_LENGTH - 180; x += 245) {
    items.push({ type: "whistle", x: x + (x % 3) * 21, y: GROUND - 48 - (x % 2) * 16, taken: false });
  }
  for (let x = 520; x < LEVEL_LENGTH - 260; x += 430) {
    items.push({ type: "hazard", kind: stop.hazard, x, y: GROUND, hit: false });
  }
  for (let x = 760; x < LEVEL_LENGTH - 420; x += 620) {
    items.push({ type: "npc", kind: stop.npc, x, y: GROUND, greeted: false });
  }
  items.push({ type: "portal", x: LEVEL_LENGTH - 105, y: GROUND, stop: stop.name });
  levelItems = items;
}

function setMessage(title, body, seconds = 2.1) {
  ui.message.querySelector("strong").textContent = title;
  ui.message.querySelector("span").textContent = body;
  ui.message.classList.remove("is-quiet");
  messageTimer = seconds;
}

function updateRoute() {
  ui.stop.textContent = stops[state.stopIndex].name;
  ui.whistles.textContent = String(state.whistles).padStart(2, "0");
  ui.hearts.textContent = String(state.hearts);
  document.querySelectorAll(".route-stop").forEach((el, index) => {
    el.classList.toggle("is-done", index < state.stopIndex);
    el.classList.toggle("is-current", index === state.stopIndex);
  });
}

function resetGame() {
  state.stopIndex = 0;
  state.distance = 0;
  state.speed = 86;
  state.whistles = 0;
  state.hearts = 3;
  state.status = "ready";
  state.won = false;
  player.y = GROUND;
  player.vy = 0;
  player.grounded = true;
  player.invulnerable = 0;
  particles = [];
  buildLevel();
  updateRoute();
  setMessage("Ready to depart", "Press Space to choo choo choo", 4);
}

function nextStop() {
  if (state.stopIndex === stops.length - 1) {
    state.status = "won";
    state.won = true;
    setMessage("Moon reached!", "TrainDog made the final stop", 99);
    return;
  }
  state.stopIndex += 1;
  state.distance = 0;
  player.y = GROUND;
  player.vy = 0;
  player.grounded = true;
  buildLevel();
  updateRoute();
  const stop = stops[state.stopIndex];
  setMessage(`${stop.name} station`, `Next stop: ${stop.next}`, 2.5);
}

function hurt() {
  if (player.invulnerable > 0 || state.status === "won") return;
  state.hearts -= 1;
  player.invulnerable = 1.2;
  shake = 8;
  updateRoute();
  for (let i = 0; i < 14; i += 1) {
    particles.push({ x: player.x + 32, y: player.y - 24, vx: -40 + Math.random() * 80, vy: -90 + Math.random() * 60, life: 0.55, color: "#ff6e7d" });
  }
  if (state.hearts <= 0) {
    state.status = "lost";
    setMessage("Line delayed", "Press R to restart the moon run", 99);
  } else {
    setMessage("Oof! Track trouble", "Space gets you rolling again", 1.6);
  }
}

function choo() {
  if (state.status === "lost" || state.status === "won") return;
  if (state.status === "ready") state.status = "playing";
  chooTimer = 0.45;
  state.speed = Math.min(state.speed + 18, 150);
  shake = Math.max(shake, 2);
  if (player.grounded) {
    player.vy = -190;
    player.grounded = false;
  }
  for (let i = 0; i < 9; i += 1) {
    particles.push({ x: player.x + 36, y: player.y - 50, vx: -45 - Math.random() * 38, vy: -15 - Math.random() * 34, life: 0.75, color: i % 2 ? "#eef7ff" : "#c6d3dc" });
  }
  setMessage("Choo choo choo!", `${stops[state.stopIndex].name} rails are singing`, 0.9);
}

window.addEventListener("keydown", (event) => {
  if (event.code === "Space") {
    event.preventDefault();
    if (!keys.has(event.code)) choo();
  }
  if (event.code === "KeyR") resetGame();
  keys.add(event.code);
});

window.addEventListener("keyup", (event) => {
  keys.delete(event.code);
});

function drawSky(stop, progress) {
  const grad = ctx.createLinearGradient(0, 0, 0, H);
  grad.addColorStop(0, stop.sky[0]);
  grad.addColorStop(1, stop.sky[1]);
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, W, H);

  if (stop.landmark === "stars" || stop.landmark === "earth") {
    for (let i = 0; i < 44; i += 1) {
      const x = (i * 47 - progress * 0.08) % (W + 20);
      const y = 8 + ((i * 31) % 70);
      px(ctx, x, y, i % 5 === 0 ? 2 : 1, i % 5 === 0 ? 2 : 1, "#f4f5ff");
    }
  } else {
    for (let i = 0; i < 5; i += 1) {
      const x = (i * 88 - progress * 0.08) % 410 - 60;
      const y = 18 + (i % 3) * 14;
      px(ctx, x + 5, y + 8, 34, 7, "#f4f5ff");
      px(ctx, x + 18, y + 3, 26, 12, "#f4f5ff");
      px(ctx, x + 37, y + 9, 23, 6, "#f4f5ff");
    }
  }
}

function drawLandmark(stop, progress) {
  const offset = -progress * 0.16;
  if (stop.landmark === "pines") {
    for (let i = 0; i < 12; i += 1) {
      const x = (i * 42 + offset) % 410 - 45;
      const h = 30 + (i % 3) * 10;
      px(ctx, x + 15, 88 - h / 2, 6, h, "#513a26");
      px(ctx, x + 2, 74 - h / 2, 32, 14, stop.mid);
      px(ctx, x + 6, 62 - h / 2, 24, 14, stop.near);
      px(ctx, x + 10, 51 - h / 2, 16, 13, "#2f704c");
    }
  }
  if (stop.landmark === "mountains") {
    for (let i = 0; i < 6; i += 1) {
      const x = (i * 74 + offset) % 470 - 80;
      px(ctx, x + 10, 94, 58, 28, stop.mid);
      px(ctx, x + 28, 60, 22, 36, "#eafcff");
      px(ctx, x + 36, 76, 30, 24, "#8cadc8");
    }
  }
  if (stop.landmark === "city") {
    for (let i = 0; i < 14; i += 1) {
      const x = (i * 28 + offset) % 390 - 35;
      const h = 25 + (i % 5) * 8;
      px(ctx, x, 113 - h, 20, h, i % 2 ? stop.mid : stop.near);
      px(ctx, x + 5, 101 - h, 4, 4, "#ffd45f");
      px(ctx, x + 13, 111 - h, 4, 4, "#ffd45f");
    }
  }
  if (stop.landmark === "dunes") {
    for (let i = 0; i < 5; i += 1) {
      const x = (i * 92 + offset) % 500 - 90;
      px(ctx, x, 96, 88, 25, stop.far);
      px(ctx, x + 35, 80, 75, 41, stop.mid);
    }
  }
  if (stop.landmark === "lighthouse") {
    const x = 218 + Math.sin(progress * 0.003) * 18;
    px(ctx, x, 53, 20, 66, "#111018");
    px(ctx, x + 4, 57, 12, 58, "#f4f5ff");
    px(ctx, x + 4, 72, 12, 8, "#e0524d");
    px(ctx, x + 1, 46, 18, 9, "#e0524d");
    px(ctx, x - 18, 54, 56, 5, "#ffe483");
  }
  if (stop.landmark === "aurora") {
    px(ctx, 40, 20, 18, 68, "#63e6a8");
    px(ctx, 62, 14, 16, 76, "#78d3ff");
    px(ctx, 82, 22, 20, 60, "#9cffd9");
    px(ctx, 210, 12, 20, 78, "#63e6a8");
  }
  if (stop.landmark === "stars") {
    px(ctx, 220, 38, 15, 26, "#111018");
    px(ctx, 224, 20, 7, 18, "#f4f5ff");
    px(ctx, 218, 48, 27, 13, "#ff6e38");
    px(ctx, 224, 61, 10, 16, "#ffd45f");
  }
  if (stop.landmark === "earth") {
    px(ctx, 220, 22, 38, 38, "#111018");
    px(ctx, 223, 25, 32, 32, "#5eb9ff");
    px(ctx, 228, 32, 10, 7, "#64d56f");
    px(ctx, 241, 42, 11, 7, "#64d56f");
    px(ctx, 232, 50, 6, 4, "#f4f5ff");
  }
}

function drawGround(stop, progress) {
  px(ctx, 0, GROUND + 8, W, H - GROUND, stop.dirt);
  px(ctx, 0, GROUND, W, 13, "#111018");
  px(ctx, 0, GROUND - 5, W, 14, stop.ground);
  for (let x = -40 - (progress % 32); x < W + 40; x += 32) {
    px(ctx, x, GROUND + 1, 20, 4, "#9f7b4d");
    px(ctx, x + 22, GROUND + 1, 16, 4, "#9f7b4d");
    px(ctx, x + 2, GROUND + 8, 5, 17, "#111018");
    px(ctx, x + 3, GROUND + 8, 3, 15, "#6b4b34");
  }
  px(ctx, 0, GROUND + 3, W, 3, stop.rail);
  px(ctx, 0, GROUND + 12, W, 3, stop.rail);
  for (let x = -20 - (progress % 18); x < W + 20; x += 18) {
    px(ctx, x, GROUND + 2, 5, 14, "#2b202a");
  }
}

function drawStationSign(stop) {
  px(ctx, 12, 86, 58, 35, "#111018");
  px(ctx, 15, 89, 52, 29, "#6b4b34");
  px(ctx, 18, 92, 46, 23, "#302333");
  px(ctx, 22, 96, 36, 6, "#f7b941");
  px(ctx, 22, 106, 27, 4, "#f4f5ff");
  px(ctx, 18, 119, 4, 21, "#6b4b34");
  px(ctx, 60, 119, 4, 21, "#6b4b34");
}

function drawChooText() {
  if (chooTimer <= 0) return;
  const alpha = Math.min(1, chooTimer * 2.5);
  ctx.globalAlpha = alpha;
  px(ctx, player.x + 18, player.y - 73, 69, 17, "#111018");
  px(ctx, player.x + 20, player.y - 71, 65, 13, "#fff3cf");
  px(ctx, player.x + 24, player.y - 68, 8, 4, "#312333");
  px(ctx, player.x + 35, player.y - 68, 8, 4, "#312333");
  px(ctx, player.x + 47, player.y - 68, 8, 4, "#312333");
  px(ctx, player.x + 59, player.y - 68, 8, 4, "#312333");
  px(ctx, player.x + 71, player.y - 68, 8, 4, "#312333");
  ctx.globalAlpha = 1;
}

function drawItem(item, screenX, time) {
  if (item.type === "whistle" && !item.taken) {
    const bob = Math.sin(time * 7 + item.x) * 4;
    ctx.drawImage(sprites.whistle, screenX, item.y + bob, 22, 18);
  }
  if (item.type === "hazard") {
    ctx.drawImage(sprites.hazards[item.kind], screenX, item.y - 35, 40, 40);
  }
  if (item.type === "npc") {
    const bob = Math.sin(time * 4 + item.x) * 2;
    ctx.drawImage(sprites.npcs[item.kind], screenX, item.y - 44 + bob, 38, 48);
    if (!item.greeted && Math.abs(screenX - player.x) < 55) {
      px(ctx, screenX + 22, item.y - 61, 12, 12, "#111018");
      px(ctx, screenX + 24, item.y - 59, 8, 7, "#fff3cf");
      px(ctx, screenX + 27, item.y - 57, 2, 3, "#312333");
    }
  }
  if (item.type === "portal") {
    const pulse = Math.sin(time * 6) * 2;
    ctx.drawImage(sprites.portals[item.stop], screenX, item.y - 68 + pulse, 56, 70);
  }
}

function rectsOverlap(a, b) {
  return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

function update(dt) {
  messageTimer -= dt;
  chooTimer -= dt;
  shake = Math.max(0, shake - dt * 18);
  ui.message.classList.toggle("is-quiet", messageTimer < 0 && state.status === "playing");

  player.ducking = keys.has("ArrowDown") || keys.has("KeyS");
  player.invulnerable = Math.max(0, player.invulnerable - dt);

  if (state.status === "playing") {
    state.speed = Math.max(82, state.speed - dt * 9);
    state.distance += state.speed * dt;
  }

  player.vy += 520 * dt;
  player.y += player.vy * dt;
  if (player.y >= GROUND) {
    player.y = GROUND;
    player.vy = 0;
    player.grounded = true;
  }

  particles.forEach((p) => {
    p.x += p.vx * dt;
    p.y += p.vy * dt;
    p.vy += 52 * dt;
    p.life -= dt;
  });
  particles = particles.filter((p) => p.life > 0);

  const playerBox = player.ducking
    ? { x: player.x + 13, y: player.y - 27, w: 55, h: 24 }
    : { x: player.x + 9, y: player.y - 48, w: 68, h: 42 };

  for (const item of levelItems) {
    const sx = item.x - state.distance + PLAYER_X;
    if (sx < -80 || sx > W + 80) continue;
    if (item.type === "whistle" && !item.taken) {
      const bob = Math.sin(performance.now() * 0.007 + item.x) * 4;
      if (rectsOverlap(playerBox, { x: sx, y: item.y + bob, w: 22, h: 18 })) {
        item.taken = true;
        state.whistles += 1;
        updateRoute();
        particles.push({ x: sx + 10, y: item.y, vx: 10, vy: -55, life: 0.45, color: "#f7b941" });
      }
    }
    if (item.type === "hazard") {
      const hazardBox = item.kind === "lantern"
        ? { x: sx + 13, y: item.y - 31, w: 17, h: 32 }
        : { x: sx + 8, y: item.y - 32, w: 24, h: 30 };
      if (rectsOverlap(playerBox, hazardBox)) hurt();
    }
    if (item.type === "npc" && !item.greeted && Math.abs(sx - player.x) < 46) {
      item.greeted = true;
      state.whistles += 1;
      updateRoute();
      setMessage("Passenger cheered!", "+1 whistle for excellent choo", 1.15);
    }
    if (item.type === "portal" && sx < player.x + 56 && state.status === "playing") {
      nextStop();
    }
  }
}

function render(time) {
  ctx.save();
  ctx.setTransform(SCALE, 0, 0, SCALE, 0, 0);
  const stop = stops[state.stopIndex];
  const bumpX = shake > 0 ? (Math.random() - 0.5) * shake : 0;
  const bumpY = shake > 0 ? (Math.random() - 0.5) * shake * 0.5 : 0;
  ctx.translate(bumpX, bumpY);

  drawSky(stop, state.distance);
  drawLandmark(stop, state.distance);
  drawStationSign(stop);
  drawGround(stop, state.distance);

  for (const item of levelItems) {
    const sx = item.x - state.distance + PLAYER_X;
    if (sx > -90 && sx < W + 90) drawItem(item, sx, time);
  }

  particles.forEach((p) => {
    ctx.globalAlpha = Math.max(0, Math.min(1, p.life * 2));
    px(ctx, p.x, p.y, 3, 3, p.color);
    ctx.globalAlpha = 1;
  });

  let trainFrame = "idle";
  if (!player.grounded) trainFrame = "jump";
  else if (player.ducking) trainFrame = "duck";
  else if (state.status === "playing") trainFrame = Math.floor(time * 10) % 2 ? "runA" : "runB";
  if (player.invulnerable > 0 && Math.floor(time * 18) % 2 === 0) ctx.globalAlpha = 0.45;
  ctx.drawImage(sprites.train[trainFrame], player.x, player.y - 55, 92, 58);
  ctx.globalAlpha = 1;
  drawChooText();

  if (state.status === "won") {
    px(ctx, 0, 0, W, H, "rgba(5, 5, 17, 0.34)");
    px(ctx, 84, 45, 152, 56, "#111018");
    px(ctx, 88, 49, 144, 48, "#fff3cf");
    px(ctx, 102, 62, 40, 8, "#312333");
    px(ctx, 150, 62, 66, 8, "#f7b941");
    px(ctx, 108, 78, 104, 6, "#312333");
  }

  ctx.restore();
}

function loop(now) {
  const dt = Math.min(0.033, (now - lastTime) / 1000);
  lastTime = now;
  update(dt);
  render(now / 1000);
  requestAnimationFrame(loop);
}

resetGame();
requestAnimationFrame(loop);
