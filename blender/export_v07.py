"""Final web-only export with Draco and embedded WebP; editable remains intact."""
import bpy,os,time,json
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bpy.ops.wm.open_mainfile(filepath=os.path.join(ROOT,'blender','residencia-rincao-v07.blend'))
s=bpy.context.scene;objects=[o for o in s.objects if o.type=='MESH' and 'buildStage' in o]
for im in bpy.data.images:
 if im.size[0]>128 and any(w in im.name for w in ['mineral-paint','foundation-concrete','cement-paving','charcoal-roof','coastal-lawn']):im.scale(128,128)
bpy.ops.object.select_all(action='DESELECT');export=[]
for stage in range(7):
 mats=set(o.data.materials[0] for o in objects if int(o['buildStage'])==stage)
 for m in mats:
  copies=[]
  for o in objects:
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
path=os.path.join(ROOT,'assets','models','residencia-rincao-v07.glb')
bpy.ops.export_scene.gltf(filepath=path,export_format='GLB',use_selection=True,export_extras=True,export_cameras=False,export_lights=False,export_image_format='WEBP',export_image_quality=95,export_draco_mesh_compression_enable=True,export_draco_mesh_compression_level=6)
mp=os.path.join(ROOT,'blender','metrics-v07.json')
with open(mp,encoding='utf-8') as f:data=json.load(f)
data['glb_final_webp_bytes']=os.path.getsize(path);data['export_webp_seconds']=round(time.perf_counter()-t,2)
data['mobile_second_pass']='900x900; camera(-8,24.5,4.8), target(-.7,1.2,1.7), lens46. Corrected small initial mobile proof.'
data['mobile_second_pass_timing_notice']='Blender log saved at46.891s including2.282s scene load; exact perf_counter result overwritten by concurrent packaging, not used as performance claim.'
with open(mp,'w',encoding='utf-8') as f:json.dump(data,f,indent=2)
print('FINAL_WEBP_EXPORT',data['glb_final_webp_bytes'])
