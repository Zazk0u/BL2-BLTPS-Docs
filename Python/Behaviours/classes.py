import unrealsdk
from unrealsdk import UObject, UFunction, FStruct, UClass
from math import sqrt




class BLHelper:
    """Class helper for my global functions."""
    
    def object_is_class_or_subclass_of(object: UObject, class_type: UClass) -> bool:
        """
        Return True if the object is class or subclass of the class given. 
        Return False if no object is given.
        """ 

        if not object: 
            return False

        if object.Class is class_type: 
            return True
    
        while object.ObjectArchetype is not None:
            object = object.ObjectArchetype

            if object.Class is class_type:
                return True    
        return False
    
    def object_class_in_list_of_classes(object: UObject, class_list: list) -> bool:
        """
        Return True if the object's class is in the list of classes. 
        """ 

        if not object: 
            return False
        
        if object.Class in class_list: 
            return True
        return False
    
    def get_actor_distance_from_actor_context(context: UObject, actor: UObject) -> float:
        """Return the distance between two actors.""" 

        x, y = context.Location.X, context.Location.Y
        _x, _y = actor.Location.X, actor.Location.Y
        return sqrt((_x - x)**2 + (_y - y)**2)

    def in_range_of_actor_context(context: UObject, actor: UObject, search_radius: float) -> bool:
        """Evaluate the distance between a context actor and another actor."""

        return search_radius >= BLHelper.get_actor_distance_from_actor_context(context, actor)
    
    def __init__(self) -> None:
        if type(self) == BLHelper: 
            raise TypeError(f"{type(self)} cannot be instantiated.")




...
def register():
    pass
    

if __name__ == "__main__":
    register()