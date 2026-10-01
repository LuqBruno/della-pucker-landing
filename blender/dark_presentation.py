"""Dark architectural presentation. Original reference geometry is unchanged.
Lighting and landscape mood are editorial, not a recorded site condition.
"""
import bpy, os, math
from mathutils import Vector
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bpy.ops.wm.open_mainfile(filepath=os.path.join(ROOT,'blender','residencia-rincao.blend'))
s=bpy.context.scene
for o in list(s.objects):
    if o.type=='LIGHT':bpy.data.objects.remove(o,do_unlink=True)
s.world.use_nodes=True;n=s.world.node_tree.nodes;n.clear()
out=n.new('ShaderNodeOutputWorld');bg=n.new('ShaderNodeBackground')
bg.inputs['Color'].default_value=(.16,.17,.19,1);bg.inputs['Strength'].default_value=.25
s.world.node_tree.links.new(bg.outputs[0],out.inputs[0])
def light(name,pos,energy,size,color):
    bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name=name
    o.data.energy=energy;o.data.shape='DISK';o.data.size=size;o.data.color=color
    o.rotation_euler=(Vector((-.5,0,2))-o.location).to_track_quat('-Z','Y').to_euler()
light('Editorial front softbox',(-6,11,10),2600,8,(1,.95,.88))
light('Editorial edge softbox',(8,-6,8),2200,7,(.88,.93,1))
light('Editorial facade fill',(-10,2,5),900,6,(1,1,1))
grass=bpy.data.materials['Jardim'];nodes=grass.node_tree.nodes;links=grass.node_tree.links
p=next(n for n in nodes if n.type=='BSDF_PRINCIPLED')
for link in list(links):
    if link.to_socket==p.inputs['Base Color']:links.remove(link)
p.inputs['Base Color'].default_value=(.035,.042,.028,1)
cam=s.camera;cam.location=(-10.2,20.6,3.6)
cam.rotation_euler=(Vector((-.7,0,2))-cam.location).to_track_quat('-Z','Y').to_euler()
cam.data.lens=44;s.render.engine='CYCLES';s.cycles.samples=48;s.cycles.use_denoising=True
s.render.resolution_x=2000;s.render.resolution_y=1100;s.render.resolution_percentage=100
s.render.film_transparent=True;s.view_settings.exposure=.15
s['dark_direction']='2026-10-01: monochrome interface; architectural studio lighting, natural ground subdued. Geometry and reference materials retained. Editorial study.'
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'blender','residencia-rincao-dark.blend'))
s.render.filepath=os.path.join(ROOT,'blender','residencia-rincao-dark.png');bpy.ops.render.render(write_still=True)
s.render.resolution_x=1100;s.render.resolution_y=1100;s.cycles.samples=28
s.render.filepath=os.path.join(ROOT,'blender','residencia-rincao-dark-mobile.png');bpy.ops.render.render(write_still=True)
