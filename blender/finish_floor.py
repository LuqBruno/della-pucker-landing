"""Remove overlapping coplanar porch slabs; one continuous opaque deck."""
import bpy,os
from mathutils import Vector
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bpy.ops.wm.open_mainfile(filepath=os.path.join(ROOT,'blender','residencia-rincao.blend'))
scene=bpy.context.scene
names={'Laje ala dormitorios','Laje social','Varanda lateral','Varanda frontal'}
for o in list(scene.objects):
    if o.name in names or o.name.startswith('Embasamento '):bpy.data.objects.remove(o,do_unlink=True)
def slab(name,loc,dims,material,stage):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.dimensions=dims
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    o.name=name;o['buildStage']=stage;o.data.materials.append(bpy.data.materials[material])
    for c in list(o.users_collection):c.objects.unlink(o)
    c=bpy.data.collections['%02d_%s'%(stage,'Fundacao' if stage==1 else 'Acabamento')];c.objects.link(o)
    mod=o.modifiers.new('Aresta laje','BEVEL');mod.width=.005;mod.segments=2;bpy.ops.object.modifier_apply(modifier=mod.name)
    layer=o.data.uv_layers.new(name='Surface metres')
    for p in o.data.polygons:
        axis=max(range(3),key=lambda k:abs(p.normal[k]))
        for li in p.loop_indices:
            v=o.matrix_world@o.data.vertices[o.data.loops[li].vertex_index].co
            pair=(v.y,v.z) if axis==0 else ((v.x,v.z) if axis==1 else (v.x,v.y))
            layer.data[li].uv=(pair[0]/1.3,pair[1]/1.3)
    return o
# The unscaled plan has a rectangular platform perimeter including the wraparound porch.
slab('Laje continua residencial e varanda',(-.685,0,.42),(8.17,10.5,.20),'Concreto aparente',1)
slab('Embasamento continuo',(-.685,0,.255),(8.184,10.514,.51),'Piso cimenticio',6)
slab('Piso continuo opaco varanda',(-.685,0,.532),(8.176,10.506,.014),'Piso cimenticio',6)
scene['floor_correction']='2026-10-01: continuous opaque slab; no duplicated coplanar porch faces.'
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'blender','residencia-rincao.blend'))
scene.render.filepath=os.path.join(ROOT,'blender','residencia-rincao-final.png');bpy.ops.render.render(write_still=True)
cam=scene.camera;cam.location=(-6.0,24.5,5.3);cam.rotation_euler=(Vector((-.45,1,2.0))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=49
scene.render.filepath=os.path.join(ROOT,'blender','residencia-rincao-frontal.png');bpy.ops.render.render(write_still=True)
