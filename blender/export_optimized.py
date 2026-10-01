"""Web export only. Full resolution editable source and Cycles proofs are unchanged."""
import bpy,os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bpy.ops.wm.open_mainfile(filepath=os.path.join(ROOT,'blender','residencia-rincao.blend'))
scene=bpy.context.scene
objects=[o for o in scene.objects if o.type=='MESH' and 'buildStage' in o]
for im in bpy.data.images:
    if im.size[0]>128 and any(w in im.name for w in ['mineral-paint','foundation-concrete','cement-paving','charcoal-roof','coastal-lawn']):
        im.scale(128,128)
bpy.ops.object.select_all(action='DESELECT');export=[]
for stage in range(7):
    mats=set(o.data.materials[0] for o in objects if o['buildStage']==stage)
    for m in mats:
        copies=[]
        for o in objects:
            if o['buildStage']==stage and o.data.materials[0]==m:
                du=o.copy();du.data=o.data.copy();scene.collection.objects.link(du);du.select_set(True);copies.append(du)
        bpy.context.view_layer.objects.active=copies[0]
        if len(copies)>1:bpy.ops.object.join()
        joined=bpy.context.object;joined.name='stage_%d_%s'%(stage,m.name);joined['buildStage']=stage
        bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
        # Only the web copies: shallow rounded edges simplify without changing openings.
        dec=joined.modifiers.new('Web geometric budget','DECIMATE');dec.ratio=.56
        bpy.ops.object.modifier_apply(modifier=dec.name)
        export.append(joined);joined.select_set(False)
for o in export:o.select_set(True)
bpy.ops.export_scene.gltf(filepath=os.path.join(ROOT,'assets','models','residencia-rincao.glb'),export_format='GLB',use_selection=True,export_extras=True,export_cameras=False,export_lights=False,export_draco_mesh_compression_enable=True,export_draco_mesh_compression_level=6)
print('OPTIMIZED_WEB_EXPORT',len(export))
