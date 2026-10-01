"""Second pass: face the same side as the published reference; soften daylight."""
import bpy,os
from mathutils import Matrix,Vector
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bpy.ops.wm.open_mainfile(filepath=os.path.join(ROOT,'blender','residencia-rincao.blend'))
scene=bpy.context.scene
objects=[o for o in scene.objects if o.type=='MESH' and 'buildStage' in o]
if not scene.get('orientation_refined'):
    reflection=Matrix.Diagonal((-1,1,1,1))
    for o in objects:
        o.data.transform(reflection@o.matrix_world);o.matrix_world=Matrix.Identity(4)
        # Reflection changes handedness. Flip winding so exported surfaces stay outward.
        import bmesh
        bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.reverse_faces(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()
    scene['orientation_refined']=True
cam=scene.camera;cam.location=(-17,26,12);cam.rotation_euler=(Vector((-.3,0,1.8))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=19.2
scene.cycles.samples=48
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'blender','residencia-rincao.blend'))
bpy.ops.object.select_all(action='DESELECT');export=[]
for stage in range(7):
    mats=set(o.data.materials[0] for o in objects if o['buildStage']==stage)
    for mat in mats:
        copies=[]
        for o in objects:
            if o['buildStage']==stage and o.data.materials[0]==mat:
                du=o.copy();du.data=o.data.copy();scene.collection.objects.link(du);du.select_set(True);copies.append(du)
        bpy.context.view_layer.objects.active=copies[0];bpy.ops.object.join();o=bpy.context.object;o.name='stage_%d_%s'%(stage,mat.name);o['buildStage']=stage
        bpy.ops.object.transform_apply(location=True,rotation=True,scale=True);export.append(o);o.select_set(False)
for o in export:o.select_set(True)
bpy.ops.export_scene.gltf(filepath=os.path.join(ROOT,'assets','models','residencia-rincao.glb'),export_format='GLB',use_selection=True,export_extras=True,export_cameras=False,export_lights=False,export_draco_mesh_compression_enable=True,export_draco_mesh_compression_level=6)
for o in export:bpy.data.objects.remove(o,do_unlink=True)
scene.render.filepath=os.path.join(ROOT,'blender','residencia-rincao-render.png');bpy.ops.render.render(write_still=True)
