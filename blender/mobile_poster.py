"""Square Cycles fallback: same fixed façade, framing reserved for mobile."""
import bpy,os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bpy.ops.wm.open_mainfile(filepath=os.path.join(ROOT,'blender','residencia-rincao.blend'))
s=bpy.context.scene;s.render.resolution_x=1100;s.render.resolution_y=1100
s.cycles.samples=32;s.render.filepath=os.path.join(ROOT,'blender','residencia-rincao-mobile.png')
bpy.ops.render.render(write_still=True)
