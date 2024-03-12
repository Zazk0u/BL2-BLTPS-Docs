import unrealsdk
import random
from unrealsdk import UObject, UFunction, FStruct
from Mods.ModMenu import Hook 

# Just a random message on log, of games or mods i like.
def log_startup_message():
    game_names_tuple = (
        "Also try Version Zeta!",       "Also try Oselands!",               "Also try Snowbound!",              "Also try Exodus!", 
        "Also try Wonderlands!",        "Also try Bloodborne!",             "Also try Pseudoregalia!",          "Also try Dragon Dogma!", 
        "Also try Terraria!",           "Also try Yakuza!",                 "Also try Fallout New Vegas!",      "Also try Path of Exile!", 
        "Also try OneShot!",            "Also try Metal Gear!",             "Also try Dark Souls!",             "Also try Morrowind!", 
        "Also try Hades!",              "Also try Night In The Woods!",     "Also try Borderlands Legends????", "Also try Devil May Cry!",  
        "Also try Doom!",               "Also try Animal Crossing!",        "Also try Kingdom Hearts!",         "Also try Rayman!", 
        "Also try Hollow Knight!",      "Also try Undertale!",              "Also try Deltarune!",              "Also try Nier!",
        "Also try Gunfire Reborn!",     "Also try Robotquest!",             "Also try Brotato!",                "Also try Lego Star Wars: The Complete Saga!",
        "Also try Lethal Company!",     "Also try Celeste!",                "Also try Magicka!",                "Also try Undertale Yellow!",
        "Also try Don't Starve!",
    )
    unrealsdk.Log(random.choice(game_names_tuple))

# This block the boost that ADS give to spread, so that i can edit it to be the same in ADS and outside it.
@Hook("WillowGame.WillowWeapon.GetZoomEffect")
def GetZoomEffect(this: UObject, function: UFunction, params: FStruct)-> bool:
    return False

def register():
    log_startup_message()
    
if __name__ == "__main__":
    register()