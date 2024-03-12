import unrealsdk
from math import sqrt


actor_list: list = []
pp = unrealsdk.GetEngine().GamePlayers[0].Actor.Pawn

ACTOR_CLASS_LIST = unrealsdk.FindAll("PopulationOpportunityDen") # Specifies the actor class to search.
RADIUS_TO_SEARCH = 2000 # Specifies the radius around the player to search.


def get_object_location(object: unrealsdk.UObject):
    return object.Location


def get_object_rotation(object: unrealsdk.UObject):
    return object.Rotation


def get_object_draw_scale(object: unrealsdk.UObject):
    return object.DrawScale


def check_actor_radius_from_player(pp: unrealsdk.UObject, actor: unrealsdk.UObject):
    x, y = pp.Location.X, pp.Location.Y
    _x, _y = actor.Location.X, actor.Location.Y
    return sqrt((_x - x)**2 + (_y - y)**2)


def get_actors_in_radius_of_player():
    if not ACTOR_CLASS_LIST[0].Location: 
        unrealsdk.Log("Class to search must have a location property.")
        return
    
    actor_list.append([actor.PathName(actor) for actor in ACTOR_CLASS_LIST if check_actor_radius_from_player(pp, actor) <= RADIUS_TO_SEARCH])
    return actor_list


unrealsdk.Log(get_actors_in_radius_of_player())
unrealsdk.Log(get_object_location(pp))
unrealsdk.Log(get_object_rotation(pp))

# put the py file in Binaries.
# execute the command bellow while in game.
# pyexec get_actors_in_radius_of_player.py