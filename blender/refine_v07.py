"""V07 editorial presentation of the public-render study; never executive accuracy.
Preserves originals and writes a new editable, staged GLB, and Cycles proofs.
"""
import bpy, os, math, time, json
from mathutils import Vector
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bpy.ops.wm.open_mainfile(filepath=os.path.join(ROOT,'blender','residencia-rincao-dark.blend'))
s=bpy.context.scene
def shader(m):return next(n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED')
def linear(c):return tuple(((v+.055)/1.055)**2.4 if v>.04045 else v/12.92 for v in c)
def set_color(m,c):
 p=shader(m)
 for link in list(m.node_tree.links):
  if link.to_socket==p.inputs['Base Color']:m.node_tree.links.remove(link)
 p.inputs['Base Color'].default_value=(*linear(c),1);m.diffuse_color=(*linear(c),1)

# No green editorial floor: the house reference still has authentic planting.
ground=bpy.data.materials.new('Solo editorial grafite');ground.use_nodes=True
set_color(ground,(.12,.12,.13));p=shader(ground);p.inputs['Roughness'].default_value=.78;p.inputs['Metallic'].default_value=.05
noise=ground.node_tree.nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=58;noise.inputs['Detail'].default_value=2
bump=ground.node_tree.nodes.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.1;bump.inputs['Distance'].default_value=.015
ground.node_tree.links.new(noise.outputs['Fac'],bump.inputs['Height']);ground.node_tree.links.new(bump.outputs['Normal'],p.inputs['Normal'])
for o in list(s.objects):
 if o.name.startswith('Paisagem editorial relva'):
  bpy.data.objects.remove(o,do_unlink=True)
 elif o.name.startswith('Paisagem editorial solo') or o.name.startswith('Gramado'):
  o.data.materials.clear();o.data.materials.append(ground)

# Contrast from materials observed in the reference, not invented dark windows.
glass=bpy.data.materials['Vidro cinza reflexo'];set_color(glass,(.49,.51,.52));p=shader(glass)
p.inputs['Metallic'].default_value=0;p.inputs['Roughness'].default_value=.065
p.inputs['Transmission Weight'].default_value=.82;p.inputs['IOR'].default_value=1.46;p.inputs['Coat Weight'].default_value=.2
for name in ['Telhas grafite','Variacao telhas']:
 p=shader(bpy.data.materials[name]);p.inputs['Roughness'].default_value=.58;p.inputs['Metallic'].default_value=.02
shader(bpy.data.materials['Pintura mineral clara']).inputs['Roughness'].default_value=.85
shader(bpy.data.materials['Madeira pintada']).inputs['Roughness'].default_value=.56
shader(bpy.data.materials['Esquadrias brancas']).inputs['Roughness'].default_value=.31
shader(bpy.data.materials['Piso cimenticio']).inputs['Roughness'].default_value=.88

# Broad softboxes describe the roof courses, eaves, plinth and white-painted wood.
for o in list(s.objects):
 if o.type=='LIGHT':bpy.data.objects.remove(o,do_unlink=True)
s.world.use_nodes=True;n=s.world.node_tree.nodes;n.clear()
out=n.new('ShaderNodeOutputWorld');bg=n.new('ShaderNodeBackground');bg.inputs['Color'].default_value=(.18,.18,.19,1);bg.inputs['Strength'].default_value=.36
s.world.node_tree.links.new(bg.outputs['Background'],out.inputs['Surface'])
def light(name,pos,target,energy,size,color):
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name=name
 o.data.energy=energy;o.data.shape='DISK';o.data.size=size;o.data.color=color
 o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
light('V07 facade daylight',(-7,13,10),(-.5,0,2),2200,8,(1,.96,.90))
light('V07 roof rim',(6,-5,12),(0,0,2.5),2800,6,(.94,.96,1))
light('V07 lateral fill',(-10,-2,6),(-1,0,2),900,6,(1,1,1))
light('V07 interior editorial',(1.1,2.7,2.2),(1.1,4.8,1.2),36,1,(1,.73,.46))
cam=s.camera;cam.data.type='PERSP';cam.data.lens=46;cam.data.sensor_width=36
def camera(pos,target):cam.location=pos;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler()
camera((-12.6,25.8,5.1),(-.7,1.0,1.50))
s.render.engine='CYCLES';s.cycles.samples=32;s.cycles.use_denoising=True;s.cycles.max_bounces=8;s.cycles.transmission_bounces=6
s.render.resolution_x=1800;s.render.resolution_y=1100;s.render.resolution_percentage=100
s.render.image_settings.file_format='PNG';s.render.film_transparent=True
s.view_settings.view_transform='AgX';s.view_settings.look='AgX - Medium High Contrast';s.view_settings.exposure=.12
s['v07_notice']='2026-10-01: public render reconstruction; dimensions/hidden parts approximate. Neutral editorial floor, soft architectural lighting and framing retain stairs. No executive accuracy.'
s['v07_reference']='references/render-perspectiva.webp and references/fachada-frontal.webp; official renders, not photos.'
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'blender','residencia-rincao-v07.blend'))
timings={}
def render(name):
 t=time.perf_counter();s.render.filepath=os.path.join(ROOT,'blender',name);bpy.ops.render.render(write_still=True);timings[name]=round(time.perf_counter()-t,2)
render('residencia-rincao-v07-desktop.png')
s.render.resolution_x=900;s.render.resolution_y=1100;s.cycles.samples=24
camera((-18.0,36.8,6.6),(-.7,1.0,1.55));render('residencia-rincao-v07-mobile.png')

# A small measured prototype, NOT an optimised production sequence.
os.makedirs(os.path.join(ROOT,'blender','sequence-v07'),exist_ok=True)
camera((-12.6,25.8,5.1),(-.7,1.0,1.50));s.render.resolution_x=640;s.render.resolution_y=400;s.cycles.samples=8
meshes=[o for o in s.objects if o.type=='MESH' and 'buildStage' in o]
for stage in range(7):
 for o in meshes:o.hide_render=int(o['buildStage'])>stage
 render(os.path.join('sequence-v07','phase-%02d.png'%stage))
for o in meshes:o.hide_render=False

# Export merged copies by stage/material and decimate only the web copy.
for im in bpy.data.images:
 if im.size[0]>128 and any(w in im.name for w in ['mineral-paint','foundation-concrete','cement-paving','charcoal-roof','coastal-lawn']):im.scale(128,128)
bpy.ops.object.select_all(action='DESELECT');export=[]
for stage in range(7):
 mats=set(o.data.materials[0] for o in meshes if int(o['buildStage'])==stage)
 for m in mats:
  copies=[]
  for o in meshes:
   if int(o['buildStage'])==stage and o.data.materials[0]==m:
    du=o.copy();du.data=o.data.copy();s.collection.objects.link(du);du.select_set(True);copies.append(du)
  bpy.context.view_layer.objects.active=copies[0]
  if len(copies)>1:bpy.ops.object.join()
  joined=bpy.context.object;joined.name='stage_%d_%s'%(stage,m.name);joined['buildStage']=stage
  bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
  if len(joined.data.polygons)>3:
   dec=joined.modifiers.new('Web budget v07','DECIMATE');dec.ratio=.56;bpy.ops.object.modifier_apply(modifier=dec.name)
  export.append(joined);joined.select_set(False)
for o in export:o.select_set(True)
t=time.perf_counter()
bpy.ops.export_scene.gltf(filepath=os.path.join(ROOT,'assets','models','residencia-rincao-v07.glb'),export_format='GLB',use_selection=True,export_extras=True,export_cameras=False,export_lights=False,export_image_format='WEBP',export_image_quality=95,export_draco_mesh_compression_enable=True,export_draco_mesh_compression_level=6)
timings['export_glb_seconds']=round(time.perf_counter()-t,2)
timings['export_meshes']=len(export);timings['glb_bytes']=os.path.getsize(os.path.join(ROOT,'assets','models','residencia-rincao-v07.glb'))
with open(os.path.join(ROOT,'blender','metrics-v07.json'),'w',encoding='utf-8') as f:json.dump(timings,f,indent=2)
print('V07_COMPLETE',json.dumps(timings))
