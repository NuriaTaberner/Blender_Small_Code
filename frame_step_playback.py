bl_info = {
    "name": "Frame Step Playback",
    "description": "Play and step through frames at custom intervals",
    "author": "Nuria Taberner",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "category": "Animation"
    "doc_url": "https://github.com/NuriaTaberner/Blender_Small_Code"
}

import bpy

# ⏱️ Custom properties
class FrameStepSettings(bpy.types.PropertyGroup):
    interval: bpy.props.IntProperty(
        name="Frame Interval",
        description="Number of frames to skip",
        default=10,
        min=1
    )
    is_playing: bpy.props.BoolProperty(
        name="Play Mode",
        description="Whether interval playback is active",
        default=False
    )

# ▶️ Step Forward
class FRAMESTEP_OT_Forward(bpy.types.Operator):
    bl_idname = "framestep.forward"
    bl_label = "Step Forward"

    def execute(self, context):
        settings = context.scene.frame_step_settings
        context.scene.frame_current += settings.interval
        return {'FINISHED'}

# ◀️ Step Backward
class FRAMESTEP_OT_Backward(bpy.types.Operator):
    bl_idname = "framestep.backward"
    bl_label = "Step Backward"

    def execute(self, context):
        settings = context.scene.frame_step_settings
        context.scene.frame_current -= settings.interval
        return {'FINISHED'}

# 🏃 Playback Timer
def playback_timer():
    settings = bpy.context.scene.frame_step_settings
    if not settings.is_playing:
        return None
    bpy.context.scene.frame_current += settings.interval
    return 0.1  # Seconds per frame step

# 🎬 Play
class FRAMESTEP_OT_Play(bpy.types.Operator):
    bl_idname = "framestep.play"
    bl_label = "Play with Interval"

    def execute(self, context):
        context.scene.frame_step_settings.is_playing = True
        bpy.app.timers.register(playback_timer)
        return {'FINISHED'}

# ⏸️ Stop
class FRAMESTEP_OT_Stop(bpy.types.Operator):
    bl_idname = "framestep.stop"
    bl_label = "Stop Playback"

    def execute(self, context):
        context.scene.frame_step_settings.is_playing = False
        return {'FINISHED'}

# 📐 UI Panel
class FRAMESTEP_PT_Panel(bpy.types.Panel):
    bl_label = "Frame Step Playback"
    bl_idname = "FRAMESTEP_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Animation'

    def draw(self, context):
        layout = self.layout
        settings = context.scene.frame_step_settings
        layout.prop(settings, "interval")
        row = layout.row()
        row.operator("framestep.backward", icon='TRIA_LEFT')
        row.operator("framestep.forward", icon='TRIA_RIGHT')
        layout.operator("framestep.play", icon='PLAY')
        layout.operator("framestep.stop", icon='PAUSE')

# 🔧 Register
classes = [
    FrameStepSettings,
    FRAMESTEP_OT_Forward,
    FRAMESTEP_OT_Backward,
    FRAMESTEP_OT_Play,
    FRAMESTEP_OT_Stop,
    FRAMESTEP_PT_Panel
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.frame_step_settings = bpy.props.PointerProperty(type=FrameStepSettings)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.frame_step_settings

if __name__ == "__main__":
    register()
