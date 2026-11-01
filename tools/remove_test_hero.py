with open("payload/war3map.j", "r", encoding="utf-8") as f:
    text = f.read()

# Remove call CreateTestHero()
text = text.replace("    call CreateTestHero()\n", "")

# Remove CreateTestHero function
test_hero_func = """function CreateTestHero takes nothing returns nothing
    local location loc = GetStartLocationLoc(GetPlayerStartLocation(Player(0)))
    local real x = GetLocationX(loc) + 150.0
    local real y = GetLocationY(loc) - 150.0
    local unit hero = CreateUnit(Player(0), 'H002', x, y, 270.0)
    call SetHeroLevel(hero, 10, true)
    call RemoveLocation(loc)
    set loc = null
    set hero = null
endfunction"""

text = text.replace(test_hero_func, "")

with open("payload/war3map.j", "w", encoding="utf-8") as f:
    f.write(text)

print("Removed CreateTestHero. Length:", len(text))
