import unrealsdk
from unrealsdk import UObject, UFunction, FStruct
from Mods.ModMenu import Hook 


def load_constants():
    global ENEMY_SKILLS_TUPLE
    ENEMY_MULTIPLICATIVE_ATTRIBUTES_SKILL = unrealsdk.FindObject("SkillDefinition", "GD_Globals.Skills.Enemies_Multiplicative_Attributes")
    ENEMY_SKILLS_TUPLE = (ENEMY_MULTIPLICATIVE_ATTRIBUTES_SKILL,)


@Hook("WillowGame.WillowAIPawn.PostSpawn")
def on_aipawn_postspawn(aipawn: UObject, function: UFunction, params: FStruct)-> bool:
    if not aipawn.MyWillowMind: return True

    willowmind: UObject         = aipawn.MyWillowMind
    player_controller: UObject  = aipawn.WorldInfo.Game.CachedColiseumStats[0].WPC
    
    activate_skills_for_aipawn(willowmind, True if willowmind.IsEnemy(player_controller) else False)
    return True
    

def activate_skills_for_aipawn(willowmind: UObject, is_enemy: bool) -> None:
    if is_enemy: [willowmind.Behavior_ActivateSkill(skill) for skill in ENEMY_SKILLS_TUPLE]
    


...    
def register():
    load_constants()
    

if __name__ == "__main__":
    register()

