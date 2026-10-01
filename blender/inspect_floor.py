import bpy,os
from mathutils import Vector
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bpy.ops.wm.open_mainfile(filepath=os.path.join(ROOT,'blender','residencia-rincao.blend'))
s=bpy.context.scene;deps=bpy.context.evaluated_depsgraph_get()
for x,y in [(-3,4.7),(-4,4.7),(-3,5.0),(-4,4.2),(-4,0),(-2.4,4.1),(-1.2,4.6)]:
    result,loc,norm,index,obj,_=s.ray_cast(deps,Vector((x,y,2.0)),Vector((0,0,-1)))
    print('FLOOR',x,y,result,tuple(loc),tuple(norm),obj.name if obj else '')
for o in s.objects:
    if any(n in o.name.lower() for n in ['varanda frontal','varanda lateral']):print('OBJECT',o.name,tuple(o.location),tuple(o.dimensions),o.get('buildStage'))
