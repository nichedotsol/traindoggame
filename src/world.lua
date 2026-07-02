return {
  stops = {
    { name = "forest", label = "FOREST", next = "MOUNTAINS", passenger = "conductor", hazard = "pine_rock" },
    { name = "mountains", label = "MOUNTAINS", next = "CITY", passenger = "sheep_hiker", hazard = "snow_boulder" },
    { name = "city", label = "CITY", next = "DESERT", passenger = "cool_cat", hazard = "lantern" },
    { name = "desert", label = "DESERT", next = "OCEAN", passenger = "bear_tourist", hazard = "cactus" },
    { name = "ocean", label = "OCEAN", next = "ARCTIC", passenger = "fox_passenger", hazard = "wave_crate" },
    { name = "arctic", label = "ARCTIC", next = "SPACE", passenger = "rabbit_passenger", hazard = "ice_spike" },
    { name = "space", label = "SPACE", next = "MOON", passenger = "astronaut", hazard = "meteor" },
    { name = "moon", label = "MOON", next = "HOME", passenger = "frog_friend", hazard = "crater" },
  },
}
