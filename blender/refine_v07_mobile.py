"""Second visual pass: mobile camera closer and more frontal, whole house retained."""
import bpy,os,time,json
from mathutils import Vector
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bpy.ops.wm.open_mainfile(filepath=os.path.join(ROOT,'blender','residencia-rincao-v07.blend'))
s=bpy.context.scene;cam=s.camera;cam.location=(-8.0,24.5,4.8)
cam.rotation_euler=(Vector((-.7,1.2,1.7))-cam.location).to_track_quat('-Z','Y').to_euler()
s.render.resolution_x=900;s.render.resolution_y=900;s.cycles.samples=24
s.render.filepath=os.path.join(ROOT,'blender','residencia-rincao-v07-mobile.png')
t=time.perf_counter();bpy.ops.render.render(write_still=True)
path=os.path.join(ROOT,'blender','metrics-v07.json')
with open(path,encoding='utf-8') as f:data=json.load(f)
data['mobile_second_pass_render_seconds']=round(time.perf_counter()-t,2)
data['mobile_second_pass']='900x900; camera (-8,24.5,4.8), target(-.7,1.2,1.7), lens46. Corrected small initial mobile proof.'
with open(path,'w',encoding='utf-8') as f:json.dump(data,f,indent=2)
print('V07_MOBILE_REFINED')
