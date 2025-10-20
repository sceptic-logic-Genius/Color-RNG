import random
import json
import os
import time
from datetime import datetime
from collections import defaultdict
from colorama import init, Fore, Style

init()  # Initialize colorama for terminal colors

# Greatly expanded color definitions (unchanged from your original)
COLORS = {
    "red": {"base_prob": 0.08, "shades": ["crimson", "scarlet", "ruby", "maroon", "vermilion", "carmine", "burgundy", "cherry", "garnet", "wine"]},
    "blue": {"base_prob": 0.07, "shades": ["navy", "cyan", "teal", "azure", "cobalt", "sapphire", "ultramarine", "cerulean", "indigo", "periwinkle"]},
    "green": {"base_prob": 0.06, "shades": ["lime", "emerald", "olive", "forest", "jade", "mint", "sage", "chartreuse", "malachite", "pine"]},
    "yellow": {"base_prob": 0.06, "shades": ["gold", "amber", "lemon", "mustard", "saffron", "ochre", "canary", "topaz", "butter", "honey"]},
    "purple": {"base_prob": 0.05, "shades": ["violet", "lavender", "plum", "indigo", "amethyst", "mauve", "lilac", "eggplant", "orchid", "grape"]},
    "orange": {"base_prob": 0.05, "shades": ["tangerine", "peach", "coral", "apricot", "terracotta", "sienna", "pumpkin", "carrot", "copper", "mandarin"]},
    "pink": {"base_prob": 0.05, "shades": ["rose", "blush", "fuchsia", "magenta", "salmon", "flamingo", "bubblegum", "coral", "peony", "carnation"]},
    "brown": {"base_prob": 0.04, "shades": ["chocolate", "tan", "sienna", "umber", "sepia", "coffee", "walnut", "mocha", "taupe", "cocoa"]},
    "black": {"base_prob": 0.04, "shades": ["ebony", "onyx", "jet", "charcoal", "raven", "sable", "coal", "midnight", "ink", "obsidian"]},
    "white": {"base_prob": 0.04, "shades": ["ivory", "pearl", "snow", "cream", "alabaster", "chalk", "linen", "bone", "eggshell", "vanilla"]},
    "gray": {"base_prob": 0.04, "shades": ["silver", "slate", "ash", "steel", "gunmetal", "charcoal", "pewter", "smoke", "fog", "stone"]},
    "neon green": {"base_prob": 0.03, "shades": ["lime neon", "acid green", "electric lime", "toxic green", "volt"]},
    "neon pink": {"base_prob": 0.03, "shades": ["hot pink", "electric pink", "neon rose", "shock pink", "radiant pink"]},
    "turquoise": {"base_prob": 0.03, "shades": ["aqua", "cerulean", "teal", "sky blue", "aquamarine", "tiffany"]},
    "gold": {"base_prob": 0.03, "shades": ["bronze", "brass", "metallic", "goldenrod", "champagne", "nugget"]},
    "silver": {"base_prob": 0.03, "shades": ["platinum", "sterling", "pewter", "nickel", "mercury", "chrome"]},
    "beige": {"base_prob": 0.03, "shades": ["sand", "khaki", "ecru", "fawn", "buff", "oatmeal"]},
    "cyan": {"base_prob": 0.03, "shades": ["sky", "robin egg", "capri", "ice blue", "arctic", "celeste"]},
    "magenta": {"base_prob": 0.03, "shades": ["berry", "raspberry", "cerise", "mulberry", "boysenberry", "claret"]},
    "teal": {"base_prob": 0.03, "shades": ["peacock", "petrol", "viridian", "blue-green", "seafoam", "cyan-teal"]},
    "lavender": {"base_prob": 0.03, "shades": ["lilac", "wisteria", "periwinkle", "mauve", "thistle", "heather"]},
    "maroon": {"base_prob": 0.03, "shades": ["wine", "burgundy", "merlot", "oxblood", "cordovan", "claret"]},
    "olive": {"base_prob": 0.03, "shades": ["khaki", "moss", "drab", "sage", "avocado", "pistachio"]}
}

# Seasonal colors (Idea 6)
SEASONAL_COLORS = {
    "frost white": {"base_prob": 0.03, "shades": ["ice", "snowflake", "glacier"], "active": lambda: 12 <= datetime.now().month <= 2},
    "spooky orange": {"base_prob": 0.03, "shades": ["pumpkin", "ghost", "jack-o-lantern"], "active": lambda: datetime.now().month == 10 and dateti000me.now().day >= 25}
}

MUTATIONS = {
    "albino": 0.05,
    "shiny": 0.02,
    "dark": 0.20,
    "vibrant": 0.05,
    "neon": 0.05,
    "other": 0.005,
    
    "crayon": 0.03
}

OTHER_MUTATIONS = [
    "skin color crayon", "im blue blue", "phlox", "puke", 
    "rainbow", "zebra", "vibrate", "back in black", 
    "druged", "bling", "glitter", "matte", "iridescent", 
    "holographic", "pastel", "metallic"
]

# New constants for enhancements
ACHIEVEMENTS = {
    "First Roll": {"condition": lambda p: p["xp"] > 0, "xp": 50},
    "Shade Collector": {"condition": lambda p: sum(1 for k in p["bestiary"] if "(" in k) >= 10, "xp": 200},
    "Mutation Master": {"condition": lambda p: sum(1 for k in p["bestiary"] if "[" in k) >= 5, "xp": 300}
}


ACHIEVEMENTS = {
    "First Roll": {"condition": lambda p: p["xp"] > 0, "xp": 50},
    "Shade Collector": {"condition": lambda p: sum(1 for k in p["bestiary"] if "(" in k) >= 10, "xp": 200},
    "Mutation Master": {"condition": lambda p: sum(1 for k in p["bestiary"] if "[" in k) >= 5, "xp": 300}
}

DAILY_CHALLENGE = {"task": "3 shades", "goal": 3, "xp": 100, "reset": datetime.now().day}
SHOP_ITEMS = {"Luck Boost (1h)": 50, "Reroll": 20, "Title: Chroma Lord": 100}
LEVEL_PERKS = {50: "5% 2x XP", 200: "Shade (1/10)"}
RARITY_TIERS = {"Common": 0.05, "Uncommon": 0.02, "Rare": 0.01, "Epic": 0.005, "Legendary": 0.001}

DATA_FILE = "color_rng_data.json"
BANNED_PLAYERS = set()
ADMIN_PASSWORD = "ratmatA1"
MAX_LEVEL = 1000
BASE_LUCK = 1.0
LUCK_PER_LEVEL = 0.02

# Color mapping for terminal display
COLOR_MAP = {
    "red": Fore.RED, "blue": Fore.BLUE, "green": Fore.GREEN, "yellow": Fore.YELLOW,
    "purple": Fore.MAGENTA, "orange": Fore.YELLOW, "pink": Fore.MAGENTA, "brown": Fore.RED,
    "black": Fore.WHITE, "white": Fore.WHITE, "gray": Fore.WHITE, "neon green": Fore.GREEN,
    "neon pink": Fore.MAGENTA, "turquoise": Fore.CYAN, "gold": Fore.YELLOW, "silver": Fore.WHITE,
    "beige": Fore.YELLOW, "cyan": Fore.CYAN, "magenta": Fore.MAGENTA, "teal": Fore.CYAN,
    "lavender": Fore.MAGENTA, "maroon": Fore.RED, "olive": Fore.GREEN, "frost white": Fore.CYAN,
    "spooky orange": Fore.YELLOW
}

class ColorRNG:
    def __init__(self):
        self.data = self.load_data()
        self.player_name = None
        self.is_admin = False
        self.last_roll_time = 0
        self.streak = 0
        self.shop_active = False
        self.trade_offer = None
        self.weekly_rarest = {"rarity": 1.0, "player": None, "color": None, "timestamp": datetime.now().strftime("%Y-%m-%d")}

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        return {"players": {}, "leaderboard": {}}

    def save_data(self):
        with open(DATA_FILE, 'w') as f:
            json.dump(self.data, f, indent=2)

    def calculate_xp_needed(self, level):
        return int(100 * (1.1 ** level))

    def get_luck_multiplier(self):
        if not self.player_name or self.player_name not in self.data["players"]:
            return BASE_LUCK
        p = self.data["players"][self.player_name]
        luck = BASE_LUCK + (p["level"] * LUCK_PER_LEVEL) + (p.get("prestige", 0) * 0.5)
        if "luck_boost" in p and time.time() < p["luck_boost"]:
            luck += 0.1
        return min(luck, 5.0)

    def get_active_colors(self):
        active = COLORS.copy()
        for color, info in SEASONAL_COLORS.items():
            if info["active"]():
                active[color] = info
        return active

    def calculate_rarity(self, result):
        active = self.get_active_colors()
        base_prob = active[result["base_color"]]["base_prob"] if result["base_color"] in active else 0.03
        rarity = base_prob * (0.7 if result["shade"] else 1) * (MUTATIONS.get(result["mutation"], 0.005) if result["mutation"] else 1)
        for tier, thresh in RARITY_TIERS.items():
            if rarity <= thresh:
                return tier
        return "Common"

    def roll_color(self):
        current_time = time.time()
        cooldown = max(1, 5 - (self.data["players"].get(self.player_name, {"level": 1})["level"] // 100) * 0.1)
        # if current_time - self.last_roll_time < cooldown:
        #    return f"Wait {cooldown - (current_time - self.last_roll_time):.1f}s"

        luck = self.get_luck_multiplier() + (self.streak // 5) * 0.01
        active_colors = self.get_active_colors()
        
        if random.random() < 0.05 * luck:
            c1, c2 = random.sample(list(active_colors.keys()), 2)
            color = f"{c1}-{c2}"
            shade = None
        else:
            weights = [min(c["base_prob"] * (1 + (luck - 1) * (1 - c["base_prob"])), 0.15) for c in active_colors.values()]
            color = random.choices(list(active_colors.keys()), weights=weights, k=1)[0]
            shade_prob = min(0.7 * luck, 0.95)
            shade = random.choice(active_colors[color]["shades"]) if random.random() < shade_prob and color in active_colors else None

        mutation_roll = random.random()
        mutation = None
        custom_muts = self.data["players"][self.player_name]["custom_mutations"] if self.player_name and "custom_mutations" in self.data["players"][self.player_name] else []
        for mut, prob in MUTATIONS.items():
            if mutation_roll <= min(prob * luck, 0.9):
                mutation = random.choice(OTHER_MUTATIONS + custom_muts) if mut == "other" else mut
                break

        if random.random() < 0.0001:
            result = {"base_color": "Golden Egg", "shade": None, "mutation": None, "xp": 1000, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            self.update_player_data(result)
            return result

        xp = 10 + (20 if shade else 0) + (30 if mutation else 0) + (50 if shade and mutation else 0)
        xp = int(xp * (1 - (active_colors[color]["base_prob"] if color in active_colors else 0.03)))
        if self.player_name and "perks" in self.data["players"][self.player_name] and "5% 2x XP" in self.data["players"][self.player_name]["perks"] and random.random() < 0.05:
            xp *= 2

        result = {"base_color": color, "shade": shade, "mutation": mutation, "xp": xp, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        self.streak += 1
        self.last_roll_time = current_time
        self.update_player_data(result)
        self.check_achievements()
        self.check_daily_challenge(result)
        self.update_weekly_rarest(result)
        
        base_color = color.split("-")[0] if "-" in color else color
        color_code = COLOR_MAP.get(base_color, Fore.WHITE)
        return result

    def update_player_data(self, result):
        if not self.player_name or self.player_name in BANNED_PLAYERS or not result:
            return
        p = self.data["players"].get(self.player_name, {"xp": 0, "level": 1, "bestiary": {}, "coins": 0, "perks": [], "prestige": 0, "custom_mutations": []})

        if "perks" not in p:
            p["perks"] = []

        #full_name = f"{result['base_color']}{f' ({result['shade']})' if result['shade'] else ''}{f' [{result['mutation']}]' if result['mutation'] else ''}"
        full_name = result['base_color']
        if result['shade']:
            full_name += f" ({result['shade']})"
        if result['mutation']:
            full_name += f" [{result['mutation']}]"

        p["bestiary"][full_name] = p["bestiary"].get(full_name, 0) + 1
        p["xp"] += result["xp"]
        p["coins"] = p.get("coins", 0) + random.randint(1, 5)

        while p["xp"] >= self.calculate_xp_needed(p["level"]):
            p["xp"] -= self.calculate_xp_needed(p["level"])
            p["level"] += 1
            for lvl, perk in LEVEL_PERKS.items():
                if p["level"] == lvl and perk not in p["perks"]:
                    p["perks"].append(perk)
                    print(f"{Fore.GREEN}Perk: {perk}{Style.RESET_ALL}")
            if p["level"] >= 500 and "custom_mutations" not in p:
                p["custom_mutations"] = []
                print(f"{Fore.GREEN}Custom mutations unlocked!{Style.RESET_ALL}")
            if p["level"] > MAX_LEVEL:
                p["level"] = MAX_LEVEL
                p["xp"] = 0
                self.is_admin = True
                print(f"{Fore.GREEN}Max level! Prestige available.{Style.RESET_ALL}")

        self.data["players"][self.player_name] = p
        self.data["leaderboard"][self.player_name] = p["level"]
        self.save_data()

    def check_achievements(self):
        if not self.player_name:
            return
        p = self.data["players"][self.player_name]
        achieved = p.get("achievements", {})
        for name, info in ACHIEVEMENTS.items():
            if name not in achieved and info["condition"](p):
                p["xp"] += info["xp"]
                achieved[name] = True
                print(f"{Fore.YELLOW}Achievement: {name} (+{info['xp']} XP){Style.RESET_ALL}")
        p["achievements"] = achieved
        self.save_data()

    def check_daily_challenge(self, result):
        if not self.player_name:
            return
        p = self.data["players"][self.player_name]
        if DAILY_CHALLENGE["reset"] != datetime.now().day:
            p["daily_progress"] = 0
            DAILY_CHALLENGE["reset"] = datetime.now().day
        if result["shade"]:
            p["daily_progress"] = p.get("daily_progress", 0) + 1
            if p["daily_progress"] >= DAILY_CHALLENGE["goal"]:
                p["xp"] += DAILY_CHALLENGE["xp"]
                print(f"{Fore.YELLOW}Daily done! +{DAILY_CHALLENGE['xp']} XP{Style.RESET_ALL}")
                p["daily_progress"] = 0
        self.save_data()

    def update_weekly_rarest(self, result):
        if not self.player_name:
            return
        rarity = self.get_active_colors()[result["base_color"]]["base_prob"] if result["base_color"] in self.get_active_colors() else 0.03
        rarity *= 0.7 if result["shade"] else 1
        rarity *= MUTATIONS.get(result["mutation"], 0.005) if result["mutation"] else 1
        if rarity < self.weekly_rarest["rarity"] or (datetime.now().weekday() == 0 and datetime.now().strftime("%Y-%m-%d") != self.weekly_rarest["timestamp"]):
            #full_name = f"{result['base_color']}{f' ({result['shade']})' if result['shade'] else ''}{f' [{result['mutation']}]' if result['mutation'] else ''}"
            full_name = result['base_color']
            if result['shade']:
                full_name += f" ({result['shade']})"
            if result['mutation']:
                full_name += f" [{result['mutation']}]"

            self.weekly_rarest = {"rarity": rarity, "player": self.player_name, "color": full_name, "timestamp": datetime.now().strftime("%Y-%m-%d")}
            if datetime.now().weekday() == 0 and rarity < 1.0:
                print(f"{Fore.CYAN}Weekly rarest: {self.weekly_rarest['color']} by {self.weekly_rarest['player']}{Style.RESET_ALL}")
                if self.player_name == self.weekly_rarest["player"]:
                    self.data["players"][self.player_name]["xp"] += 100
                    print(f"{Fore.YELLOW}Weekly win! +100 XP{Style.RESET_ALL}")
                self.weekly_rarest["rarity"] = 1.0

    def shop(self):
        if not self.player_name:
            return
        p = self.data["players"][self.player_name]
        print("\nShop:")
        for item, cost in SHOP_ITEMS.items():
            print(f"{item}: {cost}c")
        choice = input("> ").lower()
        if choice in SHOP_ITEMS and p["coins"] >= SHOP_ITEMS[choice]:
            p["coins"] -= SHOP_ITEMS[choice]
            if "Luck Boost" in choice:
                p["luck_boost"] = time.time() + 3600
                print(f"{Fore.GREEN}Luck +0.1x (1h){Style.RESET_ALL}")
            elif "Reroll" in choice:
                print(self.roll_color())
            elif "Title" in choice:
                p["title"] = choice.split(":")[1].strip()
                print(f"{Fore.GREEN}Title: {p['title']}{Style.RESET_ALL}")
            self.save_data()
        elif choice != "exit":
            print("Invalid or too poor!")
        self.shop_active = choice != "exit"

    def prestige(self):
        if not self.player_name:
            return
        p = self.data["players"][self.player_name]
        if p["level"] == MAX_LEVEL:
            p["prestige"] = p.get("prestige", 0) + 1
            p["level"] = 1
            p["xp"] = 0
            p["perks"] = []
            print(f"{Fore.YELLOW}Prestige {p['prestige']}: +{p['prestige'] * 0.5}x luck{Style.RESET_ALL}")
            self.save_data()

    def login(self):
        self.player_name = input("Enter username: ").strip()
        if self.player_name in BANNED_PLAYERS:
            print("You are banned!")
            return False
            
        if self.player_name not in self.data["players"]:
            password = input("New user! Set your password: ").strip()
            self.data["players"][self.player_name] = {"xp": 0, "level": 1, "password": password, "bestiary": {}}
            self.save_data()
        else:
            password = input("Enter password: ").strip()
            if self.data["players"][self.player_name]["password"] != password:
                print("Incorrect password!")
                return False
            if self.data["players"][self.player_name]["level"] >= MAX_LEVEL:
                self.is_admin = True
        return True

        

def main():
    game = ColorRNG()
    print("Welcome to Color RNG!")
    
    if not game.login():
        return
    
    while True:
        player_data = game.data["players"][game.player_name]
        print(f"\nLevel: {player_data['level']} | XP: {player_data['xp']}/{game.calculate_xp_needed(player_data['level'])}")
        print("Press Enter to roll, or type: quit, leaderboard, bestiary, admin <command>")
        choice = input("> ").strip().lower()
        
        if choice == "":
            result = game.roll_color()
            if result:
                output = f"Rolled: {result['base_color']}"
                if result["shade"]:
                    output += f" ({result['shade']})"
                if result["mutation"]:
                    output += f" [{result['mutation']}]"
                print(f"{output} | +{result['xp']} XP")
            
        elif choice == "quit":
            print("Thanks for playing!")
            break
            
        elif choice == "leaderboard":
            print("\nLeaderboard:")
            print("\n".join([f"{k}: Level {v}" for k, v in sorted(game.data["leaderboard"].items(), key=lambda x: x[1], reverse=True)]))
            
        elif choice == "bestiary":
            game.show_bestiary()
            
        elif choice.startswith("admin"):
            print(game.admin_command(choice))
            
        else:
            print("Invalid option!")

if __name__ == "__main__":
    main()
