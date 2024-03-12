import unrealsdk
import random
from typing import Any, Callable
from abc import ABC, abstractmethod
from unrealsdk import UObject, UFunction, FStruct, UClass
from Mods.Structs import Vector, BehaviorKernelInfo
from Mods.ModMenu import Hook
from .classes import BLHelper




# Constant objects.
GEARBOX_GLOBALS: UObject        = unrealsdk.FindObject("GearboxGlobals", "GearboxFramework.Default__GearboxGlobals")

# Constant classes.
ACTOR_CLASS: UClass                             = unrealsdk.FindClass("Actor")
PROJECTILE_CLASS: UClass                        = unrealsdk.FindClass("WillowProjectile")
SERVER_PROJECTILE_CLASS: UClass                 = unrealsdk.FindClass("WillowServerSideProjectile")
CONTROLLER_CLASS: UClass                        = unrealsdk.FindClass("Controller")
ATTRIBUTE_DEFINITION_CLASS: UClass              = unrealsdk.FindClass("AttributeDefinition")




@Hook("WillowGame.Behavior_GetItemPrice.ApplyBehaviorToContext")
def call_instance_main_method(this: UObject, function: UFunction, params: FStruct)-> bool:
    """
    Hijack Behavior_GetItemPrice to create custom BPD behaviors.
    Behavior_GetItemPrice is unused an can be exploited to not make it run it's own code.
    Use the NetIndex's int property as a key.
    Use the Item's object property for running codes, allow you to use the object's fields and functions.
    Use the Markup's float property for usefull stuff, ie: search radius, an enum.
    """
    
    method_key: int = this.NetIndex
    # Behavior must have a context.
    if not params.ContextObject: 
        return True

    INSTANCES_METHOD_CASES_DICT : dict = {
        1:     PyBehavior_GetLocation_Instance.apply_behavior_on_context,
        2:     PyBehavior_GetAttributeValue_Instance.apply_behavior_on_context,
        3:     PyBehavior_GetAttributeContext_Instance.apply_behavior_on_context,
        4:     PyBehavior_AllowProjectileCrit_Instance.apply_behavior_on_context,
    }
    # Call the main instance methods using the key's value.
    main_instance_method: Callable  = INSTANCES_METHOD_CASES_DICT.get(method_key)

    if main_instance_method: main_instance_method(this, function, params) 
    return True 




class PyBehaviorBase(ABC):
    """Class for new behaviors to be inherited."""

    @abstractmethod
    def apply_behavior_on_context(self, this: UObject, function: UFunction, params: FStruct) -> None:
        raise NotImplementedError

    def get_world_body(self, context: UObject) -> UObject: 
        """Return the pawn if the context is a player controller or willowmind. Because their locations don't get updated."""

        return context.Pawn if BLHelper.object_is_class_or_subclass_of(context, CONTROLLER_CLASS) else context
    
    def publish_BPD_variable(self, kernel_info: tuple, variable: Any) -> None:
        """Publish a variable in a BPD. Check the variable type to call the correct publishing function."""

        behavior_kernel: UObject = GEARBOX_GLOBALS.GetBehaviorKernel()
        type_cases_dict: dict = {
            int:        behavior_kernel.PublishIntOutputVariable, 
            bool:       behavior_kernel.PublishBoolOutputVariable, 
            float:      behavior_kernel.PublishFloatOutputVariable, 
            tuple:      behavior_kernel.PublishVectorOutputVariable, 
            UObject:    behavior_kernel.PublishObjectOutputVariable,
            type(None): behavior_kernel.PublishObjectOutputVariable,
        }
        type_cases_dict[type(variable)](kernel_info, variable)




class PyBehavior_GetLocation(PyBehaviorBase):
    """
    Behavior to publish the context's location in a BPD variable.
    Context must be an actor.
    """
    
    def apply_behavior_on_context(self, this: UObject, function: UFunction, params: FStruct) -> None:
        if not BLHelper.object_is_class_or_subclass_of(params.ContextObject, ACTOR_CLASS): 
            return

        context: UObject        = self.get_world_body(params.ContextObject)
        context_location: tuple = tuple(Vector(context.Location))

        self.publish_BPD_variable(BehaviorKernelInfo(params.KernelInfo), context_location)




class PyBehavior_GetAttributeValue(PyBehaviorBase):
    """
    Behavior to publish the value of an attribute definition using the context in a BPD variable.
    Use the Item's object property with an attribute definition.
    """
    
    def get_attribute_value_from_context(self, context: UObject, attribute_definition: UObject)-> UObject:
        resolved_context: UObject = attribute_definition.ResolveContext(context)
        return attribute_definition.GetValueFromContext(resolved_context)

    def apply_behavior_on_context(self, this: UObject, function: UFunction, params: FStruct) -> None:
        context: UObject                = params.ContextObject
        attribute_definition: UObject   = this.Item
        
        if not BLHelper.object_is_class_or_subclass_of(attribute_definition, ATTRIBUTE_DEFINITION_CLASS): 
            return

        context_value: float|int|bool   = self.get_attribute_value_from_context(context, attribute_definition)
        self.publish_BPD_variable(BehaviorKernelInfo(params.KernelInfo), context_value)




class PyBehavior_GetAttributeContext(PyBehaviorBase):
    """
    Behavior to publish the attribute definition's resolved context using the context in a BPD variable, ie: the weapon of the context if using a WeaponAttributeContextResolver.
    Use the Item's object property with an attribute definition.
    Very usefull with ObjectPropertyContextResolvers, we can manually get any context.
    Can use InstanceDataContextResolver to get an instance data object of the context, using Behavior_AddObjectInstanceData / Behavior_AddInstanceDataFromBehaviorContext.
    """

    def get_resolved_context_from_attribute(self, context: UObject, attribute_definition: UObject)-> UObject:
        return attribute_definition.ResolveContext(context)

    def apply_behavior_on_context(self, this: UObject, function: UFunction, params: FStruct) -> None:
        context: UObject                = params.ContextObject
        attribute_definition: UObject   = this.Item
        
        if not BLHelper.object_is_class_or_subclass_of(attribute_definition, ATTRIBUTE_DEFINITION_CLASS): 
            return

        resolved_context: UObject       = self.get_resolved_context_from_attribute(context, attribute_definition)
        self.publish_BPD_variable(BehaviorKernelInfo(params.KernelInfo), resolved_context)




class PyBehavior_AllowProjectileCrit(PyBehaviorBase):
    """Behavior to allow WillowProjectiles to crit using Behavior_CauseDamage without the need to attach."""

    PROJECTILE_CLASSES : list = [PROJECTILE_CLASS, SERVER_PROJECTILE_CLASS]

    def allow_projectile_crit(self, context: UObject):
        context.bTraceIgnoreRigidBodyForPawns = False

    def apply_behavior_on_context(self, this: UObject, function: UFunction, params: FStruct) -> None:
        if not BLHelper.object_class_in_list_of_classes(params.ContextObject, self.PROJECTILE_CLASSES): 
            return
        context: UObject = params.ContextObject
        self.allow_projectile_crit(context)




PyBehavior_GetLocation_Instance                     = PyBehavior_GetLocation()
PyBehavior_GetAttributeValue_Instance               = PyBehavior_GetAttributeValue()
PyBehavior_GetAttributeContext_Instance             = PyBehavior_GetAttributeContext()
PyBehavior_AllowProjectileCrit_Instance             = PyBehavior_AllowProjectileCrit()
...
def register():
    pass
    

if __name__ == "__main__":
    register()