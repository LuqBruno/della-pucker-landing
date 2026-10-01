"""Eye-level presentation of the reference study; landscape is illustrative.
Run after quality_residence.py, finish_pass.py and finish_floor.py.
No change to the reference house dimensions or hidden technical assumptions.
"""
import bpy, os, math, random
from mathutils import Vector
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bpy.ops.wm.open_mainfile(filepath=os.path.join(ROOT,'blender','residencia-rincao.blend'))
scene=bpy.context.scene
for o in list(scene.objects):
    if o.name=='Terreno' or o.name.startswith('Gramado') or o.name.startswith('Paisagem editorial'):
        bpy.data.objects.remove(o,do_unlink=True)
# Continuous ground: the plot is not presented as an isolated rectangular plate.
bpy.ops.mesh.primitive_plane_add(size=120,location=(0,0,-.045))
ground=bpy.context.object;ground.name='Paisagem editorial solo';ground['buildStage']=0
ground.data.materials.append(bpy.data.materials['Jardim'])
uv=ground.data.uv_layers.active
for item in uv.data:item.uv*=42
# Small grass silhouettes establish scale in the foreground without a large texture.
random.seed(43);verts=[];faces=[]
for i in range(1900):
    x=random.uniform(-15,15);y=random.uniform(-12,17)
    if -4.85<x<3.5 and -5.5<y<5.5:continue
    z=-.043;h=random.uniform(.035,.095);a=random.random()*math.tau;w=.012
    dx,dy=math.cos(a)*w,math.sin(a)*w;n=len(verts)
    verts.extend([(x-dx,y-dy,z),(x+dx,y+dy,z),(x+.02,y+.015,z+h)])
    faces.append((n,n+1,n+2))
me=bpy.data.meshes.new('Grass scale');me.from_pydata(verts,[],faces);me.update()
o=bpy.data.objects.new('Paisagem editorial relva',me);scene.collection.objects.link(o)
o.data.materials.append(bpy.data.materials['Jardim']);o['buildStage']=6
cam=scene.camera;cam.location=(-10.2,20.6,3.6)
cam.rotation_euler=(Vector((-.2,0,2.0))-cam.location).to_track_quat('-Z','Y').to_euler()
cam.data.lens=44;cam.data.sensor_width=36
for n in scene.world.node_tree.nodes:
    if n.type=='TEX_SKY':n.sun_disc=False
scene.view_settings.exposure=-.2
scene.render.engine='CYCLES';scene.cycles.samples=64;scene.cycles.use_denoising=True
scene.render.resolution_x=2000;scene.render.resolution_y=1100
scene.render.resolution_percentage=100;scene.render.film_transparent=True
scene['editorial_pass']='2026-10-01: fixed eye-level camera, continuous landscape, original roof and porch retained. Landscape is an illustrative presentation, not a surveyed site.'
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'blender','residencia-rincao.blend'))
scene.render.filepath=os.path.join(ROOT,'blender','residencia-rincao-final.png')
bpy.ops.render.render(write_still=True)
print('EDITORIAL_RENDER_COMPLETE')
