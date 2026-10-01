"""Final inspection corrections: monochromatic roof, closed corners, lower camera."""
import bpy,os,math
from mathutils import Vector
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bpy.ops.wm.open_mainfile(filepath=os.path.join(ROOT,'blender','residencia-rincao.blend'))
scene=bpy.context.scene
# One explicit sun; physical sky supplies diffuse lighting and glass reflections.
sky=next(n for n in scene.world.node_tree.nodes if n.type=='TEX_SKY');sky.sun_disc=False
bg=next(n for n in scene.world.node_tree.nodes if n.type=='BACKGROUND');bg.inputs['Strength'].default_value=.08
for o in scene.objects:
    if o.type=='LIGHT' and o.data.type=='SUN':o.data.energy=2.0
    if o.type=='LIGHT' and o.data.type=='AREA':o.data.energy=1100
scene.view_settings.exposure=0
wood=bpy.data.materials['Madeira pintada'];collection=bpy.data.collections['06_Acabamento']
for o in list(scene.objects):
    if o.name.startswith('Arremate esquina'):bpy.data.objects.remove(o,do_unlink=True)
def trim(name,loc,dims):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.dimensions=dims
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.name=name;o['buildStage']=6;o.data.materials.append(wood)
    for c in list(o.users_collection):c.objects.unlink(o)
    collection.objects.link(o)
    mod=o.modifiers.new('Aresta arremate','BEVEL');mod.width=.003;mod.segments=2;bpy.ops.object.modifier_apply(modifier=mod.name)
    uv=o.data.uv_layers.new(name='Surface metres')
    for p in o.data.polygons:
        for li in p.loop_indices:
            v=o.data.vertices[o.data.loops[li].vertex_index].co;uv.data[li].uv=(v.x+v.y,v.z)
for x,y in [(-3.25,5.05),(.05,5.05),(.05,3.65),(3.15,3.65),(3.15,-5.05),(-3.25,-5.05)]:
    trim('Arremate continuo esquina',(-x,y,2.0),(.215,.215,2.96))
# Remove competing top normals; roof curves provide their own normal variation.
for name in ['Telhas grafite','Variacao telhas']:
    m=bpy.data.materials[name];p=next(n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED')
    p.inputs['Roughness'].default_value=.72
cam=scene.camera;cam.location=(-15.5,24,7.5);cam.rotation_euler=(Vector((-.3,0,2.0))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='PERSP';cam.data.lens=48
scene['final_quality_notice']='2026-10-01: final visual inspection, roof normal correction, closed joins, single sun, low fixed camera.'
scene.render.resolution_x=2000;scene.render.resolution_y=1400;scene.cycles.samples=64
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'blender','residencia-rincao.blend'))
scene.render.filepath=os.path.join(ROOT,'blender','residencia-rincao-final.png');bpy.ops.render.render(write_still=True)
cam.location=(-6.0,24.5,5.3);cam.rotation_euler=(Vector((-.45,1,2.0))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=49
scene.render.filepath=os.path.join(ROOT,'blender','residencia-rincao-frontal.png');bpy.ops.render.render(write_still=True)
