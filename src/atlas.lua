local manifest = require("assets.love_sprites.manifest")

local Atlas = {}
Atlas.__index = Atlas

function Atlas.new()
  local self = setmetatable({
    sheets = {},
    quads = {},
  }, Atlas)

  for key, data in pairs(manifest.sheets) do
    local image = love.graphics.newImage(data.file)
    image:setFilter("nearest", "nearest")
    self.sheets[key] = {
      image = image,
      data = data,
    }
    self.quads[key] = {}
    for frame = 1, data.frames do
      self.quads[key][frame] = love.graphics.newQuad(
        (frame - 1) * data.frameWidth,
        0,
        data.frameWidth,
        data.frameHeight,
        image:getDimensions()
      )
    end
  end

  return self
end

function Atlas:frame(key, t)
  local sheet = self.sheets[key]
  if not sheet then
    return nil
  end
  local data = sheet.data
  local frame = math.floor((t or 0) / data.duration) % data.frames + 1
  return sheet.image, self.quads[key][frame], data
end

function Atlas:draw(key, t, x, y, sx, sy, ox, oy)
  local image, quad, data = self:frame(key, t)
  if not image then
    return false
  end
  love.graphics.draw(image, quad, math.floor(x), math.floor(y), 0, sx or 1, sy or sx or 1, ox or 0, oy or 0)
  return true, data
end

return Atlas
