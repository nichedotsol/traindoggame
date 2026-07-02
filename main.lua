local Atlas = require("src.atlas")
local world = require("src.world")

local atlas
local game
local W, H = 1280, 720
local baseW, baseH = 320, 180
local scale = 4

local function key(category, subject, action)
  return category .. "_" .. subject .. "_" .. action
end

local function resetLeg()
  local stop = world.stops[game.stopIndex]
  game.distance = 0
  game.items = {}
  for x = 330, game.levelLength - 230, 245 do
    table.insert(game.items, { type = "collectible", subject = "gold_whistle", action = "spin", x = x, y = 92, taken = false })
  end
  for x = 540, game.levelLength - 300, 420 do
    table.insert(game.items, { type = "hazard", subject = stop.hazard, action = "active", x = x, y = 123 })
  end
  for x = 770, game.levelLength - 420, 620 do
    table.insert(game.items, { type = "passenger", subject = stop.passenger, action = "wave", x = x, y = 101, greeted = false })
  end
  table.insert(game.items, { type = "portal", subject = stop.name, action = "open", x = game.levelLength - 120, y = 72 })
end

local function newGame()
  game = {
    stopIndex = 1,
    distance = 0,
    levelLength = 1500,
    speed = 92,
    whistles = 0,
    hearts = 3,
    status = "ready",
    message = "PRESS SPACE TO CHOO CHOO CHOO",
    messageTime = 4,
    t = 0,
    player = { x = 62, y = 125, vy = 0, grounded = true, duck = false, hurt = 0, action = "idle" },
    particles = {},
    items = {},
    flash = 0,
  }
  resetLeg()
end

local function choo()
  if game.status == "won" or game.status == "lost" then
    return
  end
  game.status = "playing"
  game.message = "CHOO CHOO CHOO!"
  game.messageTime = 0.9
  game.speed = math.min(160, game.speed + 22)
  if game.player.grounded then
    game.player.vy = -205
    game.player.grounded = false
  end
  for i = 1, 8 do
    table.insert(game.particles, {
      subject = "smoke",
      action = i % 3 == 0 and "burst" or "puff",
      x = game.player.x + 42 - i * 3,
      y = game.player.y - 54 + i % 2 * 4,
      vx = -28 - i * 6,
      vy = -18 - i,
      life = 0.7,
    })
  end
end

local function rects(a, b)
  return a.x < b.x + b.w and a.x + a.w > b.x and a.y < b.y + b.h and a.y + a.h > b.y
end

local function hurt()
  if game.player.hurt > 0 then return end
  game.hearts = game.hearts - 1
  game.player.hurt = 1.2
  game.flash = 0.35
  game.message = "TRACK TROUBLE!"
  game.messageTime = 1.3
  for i = 1, 8 do
    table.insert(game.particles, {
      subject = "heart",
      action = "lose",
      x = game.player.x + 24 + i * 2,
      y = game.player.y - 35,
      vx = -35 + i * 8,
      vy = -65,
      life = 0.5,
    })
  end
  if game.hearts <= 0 then
    game.status = "lost"
    game.message = "LINE DELAYED - PRESS R"
    game.messageTime = 99
  end
end

local function nextStop()
  if game.stopIndex == #world.stops then
    game.status = "won"
    game.message = "MOON REACHED!"
    game.messageTime = 99
    return
  end
  game.stopIndex = game.stopIndex + 1
  game.flash = 0.5
  game.message = world.stops[game.stopIndex].label .. " STATION"
  game.messageTime = 2
  resetLeg()
end

function love.load()
  love.graphics.setDefaultFilter("nearest", "nearest")
  atlas = Atlas.new()
  newGame()
end

function love.resize(w, h)
  W, H = w, h
  scale = math.max(1, math.floor(math.min(W / baseW, H / baseH)))
end

function love.keypressed(k)
  if k == "space" then
    choo()
  elseif k == "r" then
    newGame()
  elseif k == "escape" then
    love.event.quit()
  end
end

function love.update(dt)
  game.t = game.t + dt
  game.messageTime = math.max(0, game.messageTime - dt)
  game.flash = math.max(0, game.flash - dt)
  game.player.hurt = math.max(0, game.player.hurt - dt)
  game.player.duck = love.keyboard.isDown("down") or love.keyboard.isDown("s")

  if game.status == "playing" then
    game.speed = math.max(86, game.speed - dt * 8)
    game.distance = game.distance + game.speed * dt
  end

  game.player.vy = game.player.vy + 530 * dt
  game.player.y = game.player.y + game.player.vy * dt
  if game.player.y >= 125 then
    game.player.y = 125
    game.player.vy = 0
    game.player.grounded = true
  end

  if not game.player.grounded then
    game.player.action = game.player.vy > 95 and "land" or "jump"
  elseif game.player.duck then
    game.player.action = "duck"
  elseif game.player.hurt > 0 then
    game.player.action = "hurt"
  elseif game.message == "CHOO CHOO CHOO!" and game.messageTime > 0 then
    game.player.action = "cheer"
  elseif game.status == "playing" then
    game.player.action = "move"
  else
    game.player.action = "idle"
  end

  for i = #game.particles, 1, -1 do
    local p = game.particles[i]
    p.x = p.x + p.vx * dt
    p.y = p.y + p.vy * dt
    p.vy = p.vy + 55 * dt
    p.life = p.life - dt
    if p.life <= 0 then
      table.remove(game.particles, i)
    end
  end

  local playerBox = game.player.duck
    and { x = game.player.x + 13, y = game.player.y - 27, w = 55, h = 24 }
    or { x = game.player.x + 8, y = game.player.y - 50, w = 76, h = 45 }

  for _, item in ipairs(game.items) do
    local sx = item.x - game.distance + game.player.x
    if sx > -90 and sx < baseW + 90 then
      if item.type == "collectible" and not item.taken then
        if rects(playerBox, { x = sx, y = item.y, w = 30, h = 28 }) then
          item.taken = true
          game.whistles = game.whistles + 1
          table.insert(game.particles, { subject = "star_coin", action = "sparkle", x = sx, y = item.y, vx = 5, vy = -55, life = 0.45 })
        end
      elseif item.type == "hazard" then
        if rects(playerBox, { x = sx + 8, y = item.y + 8, w = 24, h = 28 }) then
          hurt()
        end
      elseif item.type == "passenger" and not item.greeted then
        if math.abs(sx - game.player.x) < 44 then
          item.greeted = true
          item.action = "cheer"
          game.whistles = game.whistles + 1
          game.message = "PASSENGER CHEERED!"
          game.messageTime = 1.2
        end
      elseif item.type == "portal" then
        if sx < game.player.x + 55 and game.status == "playing" then
          nextStop()
        end
      end
    end
  end
end

local function drawText(text, x, y, s)
  love.graphics.push()
  love.graphics.translate(math.floor(x), math.floor(y))
  love.graphics.scale(s or 1)
  love.graphics.print(text, 0, 0)
  love.graphics.pop()
end

local function drawHud()
  love.graphics.setColor(0.08, 0.07, 0.12)
  love.graphics.rectangle("fill", 0, 0, baseW, 22)
  love.graphics.setColor(1, 0.82, 0.28)
  drawText("TRAINDOG: MOON LINE", 8, 6, 0.55)
  love.graphics.setColor(0.48, 0.86, 1)
  drawText(world.stops[game.stopIndex].label, 126, 6, 0.55)
  love.graphics.setColor(1, 1, 1)
  drawText("WHISTLES " .. string.format("%02d", game.whistles), 184, 6, 0.55)
  for i = 1, 3 do
    local action = i <= game.hearts and "full" or "empty"
    atlas:draw(key("hud", "heart", action), game.t, 276 + i * 11, 5, 0.35)
  end
end

local function drawRoute()
  local y = 160
  love.graphics.setColor(0.08, 0.07, 0.12)
  love.graphics.rectangle("fill", 96, y - 7, 218, 19)
  for i, stop in ipairs(world.stops) do
    local action = i < game.stopIndex and "complete" or (i == game.stopIndex and "selected" or "idle")
    atlas:draw(key("route_icon", stop.name, action), game.t, 102 + (i - 1) * 26, y - 4, 0.45)
  end
end

function love.draw()
  love.graphics.clear(0.05, 0.04, 0.08)
  local ox = math.floor((W - baseW * scale) / 2)
  local oy = math.floor((H - baseH * scale) / 2)
  love.graphics.push()
  love.graphics.translate(ox, oy)
  love.graphics.scale(scale)

  local stop = world.stops[game.stopIndex]
  local envAction = game.flash > 0 and "arrival_flash" or "full_scroll"
  atlas:draw(key("environment", stop.name, envAction), game.t, 0, 0, 1)
  drawHud()

  for _, item in ipairs(game.items) do
    local sx = item.x - game.distance + game.player.x
    if sx > -90 and sx < baseW + 90 then
      if item.type == "collectible" and not item.taken then
        atlas:draw(key("collectible", item.subject, item.action), game.t, sx, item.y, 1)
      elseif item.type == "hazard" then
        local action = math.sin(game.t * 8 + item.x) > 0.5 and "warning" or "active"
        atlas:draw(key("hazard", item.subject, action), game.t, sx, item.y, 1)
      elseif item.type == "passenger" then
        atlas:draw(key("character", item.subject, item.action), game.t, sx, item.y, 1)
      elseif item.type == "portal" then
        atlas:draw(key("portal", item.subject, "open"), game.t, sx, item.y, 1)
      end
    end
  end

  for _, p in ipairs(game.particles) do
    local category = p.subject == "smoke" and "fx" or (p.subject == "heart" and "hud" or "collectible")
    atlas:draw(key(category, p.subject, p.action), game.t, p.x, p.y, p.subject == "smoke" and 0.55 or 0.6)
  end

  atlas:draw(key("character", "train_dog", game.player.action), game.t, game.player.x, game.player.y - 55, 1)

  if game.messageTime > 0 then
    love.graphics.setColor(0.08, 0.07, 0.12, 0.9)
    love.graphics.rectangle("fill", 101, 138, 122, 16)
    love.graphics.setColor(1, 0.82, 0.28)
    drawText(game.message, 111, 143, 0.55)
  end
  drawRoute()

  if game.status == "won" then
    love.graphics.setColor(1, 1, 1, 0.9)
    drawText("FINAL STOP: THE MOON", 96, 86, 0.7)
  end

  love.graphics.pop()
end
