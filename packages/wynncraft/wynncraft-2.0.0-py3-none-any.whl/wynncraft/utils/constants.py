# Constants for the wrapper
"""
Your API key. Not required.
"""
API_KEY = ""

"""
The time (in seconds) for which the data is valid in the cache
Default: 300
"""
CACHE_TIME = 300

"""
Enables the rate limiter.
Default: True
"""
RATE_LIMITER = True

"""
Check the syntax of the argument.
Only in Ingredient and Recipe queries.
Raises ValueError if the syntax is wrong.
Default: True
"""
REGEX_CHECK = True

"""
Specifies a timeout in seconds for http request.
Default: 10
"""
TIMEOUT = 10


# Constants for communicating Wynncraft API
URL_V1 = "https://api.wynncraft.com/public_api.php?action="

URL_V2 = "https://api.wynncraft.com/v2/"

URL_V3 = "https://web-api.wynncraft.com/api/v3/"

URL_WYNNTILS = "https://athena.wynntils.com/cache/get/"

URL_CODES = {
    " ": "+",
    "^": "%5E",
    "<": "%3C",
    ">": "%3E"
}

INGREDIENT_QUERIES = [
    "name",
    "tier",
    "level",
    "skills",
    "sprite",
    "identifications",
    "itemOnlyIDs",
    "consumableOnlyIDs"
]

SKILLS = [
    "alchemism",
    "armouring",
    "cooking",
    "jeweling",
    "scribing",
    "tailoring",
    "weaponsmithing",
    "woodworking"
]

SPRITES = [
    "id",
    "damage"
]

IDENTIFICATIONS = [
    "agilitypoints",
    "airdamagebonus",
    "airdefense",
    "attackspeed",
    "damagebonus",
    "damagebonusraw",
    "defensepoints",
    "dexteritypoints",
    "earthdamagebonus",
    "earthdefense",
    "emeraldstealing",
    "exploding",
    "firedamagebonus",
    "firedefense",
    "healthbonus",
    "healthregen",
    "healthregenraw",
    "intelligencepoints",
    "lifesteal",
    "lootbonus",
    "loot_quality",
    "manaregen",
    "manasteal",
    "poison",
    "reflection",
    "soulpoints",
    "speed",
    "spelldamage",
    "spelldamageraw",
    "stamina_regen",
    "strengthpoints",
    "thorns",
    "thunderdamagebonus",
    "thunderdefense",
    "waterdamagebonus",
    "waterdefense",
    "xpbonus"
]

ITEM_ONLY_IDS = [
    "durability",
    "strength",
    "dexterity",
    "intelligence",
    "defence",
    "agility"
]

CONSUMABLE_ONLY_IDS = [
    "duration",
    "charges"
]

ITEM_CATEGORIES = [
    "all",
    "boots",
    "bow",
    "bracelet",
    "chestplate",
    "dagger",
    "helmet",
    "leggings",
    "necklace",
    "ring",
    "spear", 
    "wand"
]

RECIPE_CATEGORIES = [
    "boots",
    "bow",
    "bracelet",
    "chestplate",
    "dagger",
    "food",
    "helmet",
    "leggings",
    "necklace",
    "potion",
    "relik",
    "ring",
    "scroll",
    "spear", 
    "wand"
]

RECIPE_QUERIES = [
    "type",
    "skill",
    "level",
    "durability",
    "healthOrDamage",
    "duration",
    "basicDuration"
]

RECIPE_MIN_MAX = [
    "min",
    "max"
]
