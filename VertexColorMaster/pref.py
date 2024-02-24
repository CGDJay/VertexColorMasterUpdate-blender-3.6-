import bpy
import rna_keymap_ui 
from bpy.types import  AddonPreferences
from bpy.props import (
	StringProperty,
	BoolProperty,
	IntProperty,
	FloatProperty,
	FloatVectorProperty,
	EnumProperty,
	PointerProperty,
)

class Panel_Preferences(AddonPreferences):

    bl_idname = __package__


    
    
    def draw (self, context):
        layout = self.layout
     
        box = layout.box()
        col = box.column()
        col.label(text="Keymap List:",icon="KEYINGSET")


        wm = bpy.context.window_manager
        kc = wm.keyconfigs.user
        old_km_name = ""
        get_kmi_l = []
        for km_add, kmi_add in addon_keymaps:
            for km_con in kc.keymaps:
                if km_add.name == km_con.name:
                    km = km_con
                    break

            for kmi_con in km.keymap_items:
                if kmi_add.idname == kmi_con.idname:
                    if kmi_add.name == kmi_con.name:
                        get_kmi_l.append((km,kmi_con))

        get_kmi_l = sorted(set(get_kmi_l), key=get_kmi_l.index)

        for km, kmi in get_kmi_l:
            if not km.name == old_km_name:
                col.label(text=str(km.name),icon="DOT")
            col.context_pointer_set("keymap", km)
            rna_keymap_ui.draw_kmi([], kc, km, kmi, col, 0)
            col.separator()
            old_km_name = km.name

classes = ( 

Panel_Preferences,

)

#-------------------------------------------------------
#KeyMaps
disabled_kmis = []

# Find a keymap item by traits.
# Returns None if the keymap item doesn't exist.


def get_active_kmi(space: str, **kwargs) -> bpy.types.KeyMapItem:
    kc = bpy.context.window_manager.keyconfigs.user
    km = kc.keymaps.get(space)
    if km:
        for kmi in km.keymap_items:
            for key, val in kwargs.items():
                if getattr(kmi, key) != val and val is not None:
                    break
            else:
                return kmi




addon_keymaps = []


def register():
    for cls in classes :
        bpy.utils.register_class(cls)

    #-------------------------------------------------------
#KeyMaps

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = wm.keyconfigs.addon.keymaps.new(name='Vertex Paint')
        # pie menu

        kmi = km.keymap_items.new('wm.call_menu_pie', 'V', 'PRESS')
        kmi.properties.name = "VERTEXCOLORMASTER_MT_PieMain"
        kmi.active = True
        addon_keymaps.append((km, kmi))


        # override 'x' to use VCM flip brush colors
        kmi = km.keymap_items.new('vertexcolormaster.brush_colors_flip', 'X', 'PRESS')
        kmi.active = True
        addon_keymaps.append((km, kmi))
    

def unregister():
    for cls in classes :
        bpy.utils.unregister_class(cls)

    #-------------------------------------------------------
#KeyMaps

    # unregister shortcuts
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    km = kc.keymaps['3D View']
    
    for km, kmi in addon_keymaps:
        try:
            km.keymap_items.remove(kmi)
            wm.keyconfigs.addon.keymaps.remove(km)
        except ReferenceError as e:
            e
            
    addon_keymaps.clear()
