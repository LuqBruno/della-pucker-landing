"""Visual refinement from the two public renders and unscaled published plan.
Only visible architecture is reconstructed; dimensions/hidden structure are estimates.
All source images are preserved. Blender 5.2: editable source, staged GLB, Cycles proof.
"""
import bpy, bmesh, math, os, random
import numpy as np
from mathutils import Vector, Matrix
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bpy.ops.wm.open_mainfile(filepath=os.path.join(ROOT,'blender','residencia-rincao-baseline.blend'))
scene=bpy.context.scene
random.seed(17)
objects=[o for o in scene.objects if o.type=='MESH' and 'buildStage' in o]
groups={i:bpy.data.collections.get('%02d_%s'%(i,n)) for i,n in enumerate(['Implantacao','Fundacao','Estrutura','Fechamentos','Cobertura','Esquadrias','Acabamento'])}
reflection=Matrix.Diagonal((-1,1,1,1))
def reflect_all():
    for o in objects:
        o.data.transform(reflection@o.matrix_world);o.matrix_world=Matrix.Identity(4)
        bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.reverse_faces(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()
if scene.get('orientation_refined'):reflect_all()

def mat(name):return bpy.data.materials.get(name)
white=mat('Pintura mineral clara');frame=mat('Esquadrias brancas');concrete=mat('Concreto aparente');stone=mat('Piso cimenticio')
roof=mat('Telhas grafite');roof2=mat('Variacao telhas');wood=mat('Madeira pintada');glass=mat('Vidro cinza reflexo');grass=mat('Jardim')
def principled(m):return next(n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED')
def srgb(c):return tuple(((v+.055)/1.055)**2.4 if v>.04045 else v/12.92 for v in c)
def color(m,c):m.diffuse_color=(*srgb(c),1);principled(m).inputs['Base Color'].default_value=(*srgb(c),1)
color(white,(.9,.895,.868));color(frame,(.94,.938,.919));color(wood,(.895,.894,.87));color(roof,(.205,.217,.225));color(roof2,(.224,.235,.24))
principled(frame).inputs['Metallic'].default_value=.07
principled(frame).inputs['Roughness'].default_value=.31
principled(wood).inputs['Roughness'].default_value=.55
color(glass,(.67,.77,.80));gp=principled(glass)
gp.inputs['Roughness'].default_value=.12;gp.inputs['Metallic'].default_value=0
gp.inputs['Transmission Weight'].default_value=.72;gp.inputs['IOR'].default_value=1.46;gp.inputs['Coat Weight'].default_value=.15

def assign(o,name,m,stage):
    o.name=name;o.data.materials.clear();o.data.materials.append(m);o['buildStage']=stage
    for c in list(o.users_collection):c.objects.unlink(o)
    groups[stage].objects.link(o);objects.append(o);return o
def box(name,loc,dims,m,stage,bevel=.008):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.dimensions=dims
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);assign(o,name,m,stage)
    if bevel:
        mod=o.modifiers.new('Aresta construtiva','BEVEL');mod.width=bevel;mod.segments=3
        bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=mod.name)
    return o
def beam(name,a,b,w,m,stage,d=None):
    a,b=Vector(a),Vector(b);o=box(name,(a+b)/2,(w,d or w,(b-a).length),m,stage,.004)
    o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler();return o
def mesh(name,verts,faces,m,stage,smooth=False):
    me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update()
    o=bpy.data.objects.new(name,me);groups[stage].objects.link(o);me.materials.append(m);o['buildStage']=stage;objects.append(o)
    if smooth:
        for p in me.polygons:p.use_smooth=True
    return o

# Local baked surface maps. Fine surface noise preserves a believable material scale.
texture_dir=os.path.join(ROOT,'assets','textures');os.makedirs(texture_dir,exist_ok=True)
def surface_map(m,name,base,amplitude,roughness,size=256):
    rng=np.random.default_rng(sum(map(ord,name)))
    fine=rng.normal(0,1,(size,size));yy,xx=np.mgrid[0:size,0:size]
    broad=.45*np.sin(xx*.12+yy*.035)+.3*np.sin(yy*.09-xx*.026)
    field=fine*.3+broad
    rgb=np.array(srgb(base))[None,None,:]*(1+field[:,:,None]*amplitude)
    rgba=np.concatenate((np.clip(rgb,0,1),np.ones((size,size,1))),axis=2).astype(np.float32)
    im=bpy.data.images.new(name,width=size,height=size,alpha=True);im.colorspace_settings.name='Linear Rec.709'
    im.pixels.foreach_set(rgba.ravel());im.filepath_raw=os.path.join(texture_dir,name+'.png');im.file_format='PNG';im.save()
    n=m.node_tree.nodes.new('ShaderNodeTexImage');n.image=im;n.interpolation='Linear';m.node_tree.links.new(n.outputs['Color'],principled(m).inputs['Base Color'])
    principled(m).inputs['Roughness'].default_value=roughness
    # Tangent-space normal perturbation is subtle, not large bumps that change geometry.
    dx=np.gradient(field,axis=1)*amplitude*.20;dy=np.gradient(field,axis=0)*amplitude*.20
    nr=np.stack((.5-dx,.5-dy,np.ones_like(field)),axis=-1);nr=np.concatenate((nr,np.ones((size,size,1))),axis=2).astype(np.float32)
    ni=bpy.data.images.new(name+'-normal',width=size,height=size,alpha=True);ni.colorspace_settings.name='Non-Color';ni.pixels.foreach_set(nr.ravel());ni.filepath_raw=os.path.join(texture_dir,name+'-normal.png');ni.file_format='PNG';ni.save()
    nt=m.node_tree.nodes.new('ShaderNodeTexImage');nt.image=ni;nt.interpolation='Linear';normal=m.node_tree.nodes.new('ShaderNodeNormalMap');normal.inputs['Strength'].default_value=.35
    m.node_tree.links.new(nt.outputs['Color'],normal.inputs['Color']);m.node_tree.links.new(normal.outputs['Normal'],principled(m).inputs['Normal'])
surface_map(white,'mineral-paint',(.90,.895,.868),.045,.82)
surface_map(concrete,'foundation-concrete',(.61,.61,.58),.18,.94)
surface_map(stone,'cement-paving',(.68,.67,.63),.095,.87)
surface_map(roof,'charcoal-roof',(.205,.217,.225),.095,.61)
surface_map(roof2,'charcoal-roof-variation',(.224,.235,.24),.07,.64)
surface_map(grass,'coastal-lawn',(.40,.45,.31),.24,.97)

# Replace the overlapping porch roof by two joined falls and a continuous diagonal hip.
for o in list(objects):
    if o.get('buildStage')==4:
        objects.remove(o);bpy.data.objects.remove(o,do_unlink=True)
def roof_surface(name,x0,x1,y0,y1,height,flow='X'):
    # Corrugated concrete tiles: discrete courses, shallow rounded profiles and lips.
    verts=[];faces=[];nx=max(1,round((x1-x0)/.39));ny=max(1,round((y1-y0)/.265))
    if flow=='X':
        for i in range(nx):
            xa=x0+(x1-x0)*i/nx;xb=x0+(x1-x0)*(i+1)/nx
            for j in range(ny):
                ya=y0+(y1-y0)*j/ny;yb=y0+(y1-y0)*(j+1)/ny;start=len(verts)
                for x,lip in [(xa,.008),(xb,.002)]:
                    for k in range(7):
                        y=ya+(yb-ya)*k/6;verts.append((x,y,height(x,y)+.013+.029*math.sin(math.pi*k/6)+lip))
                for k in range(6):faces.append(tuple(start+n for n in [k,k+7,k+8,k+1]))
    else:
        for j in range(ny):
            ya=y0+(y1-y0)*j/ny;yb=y0+(y1-y0)*(j+1)/ny
            for i in range(nx):
                xa=x0+(x1-x0)*i/nx;xb=x0+(x1-x0)*(i+1)/nx;start=len(verts)
                for y,lip in [(ya,.008),(yb,.002)]:
                    for k in range(7):
                        x=xa+(xb-xa)*k/6;verts.append((x,y,height(x,y)+.013+.029*math.sin(math.pi*k/6)+lip))
                for k in range(6):faces.append(tuple(start+n for n in [k,k+1,k+8,k+7]))
    mesh(name+' telhas',verts,faces,roof,4,True)
    # Substrate/soffit is continuous and gives a credible thickness at every eave.
    vv=[(x0,y0,height(x0,y0)),(x1,y0,height(x1,y0)),(x1,y1,height(x1,y1)),(x0,y1,height(x0,y1))]
    lower=[(x,y,z-.10) for x,y,z in vv];mesh(name+' forro',vv+lower,[(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)],wood,4)
    for a,b in [(vv[0],vv[1]),(vv[1],vv[2]),(vv[2],vv[3]),(vv[3],vv[0])]:
        beam(name+' testeira',(a[0],a[1],a[2]-.065),(b[0],b[1],b[2]-.065),.12,wood,4,.085)
    return vv
left=lambda x,y:3.49+(x+3.68)/3.98*1.43
right=lambda x,y:4.72-(x-.02)/3.55*1.14
roof_surface('Ala dormitorios',-3.68,.30,-5.5,5.48,left)
roof_surface('Ala social',.02,3.57,-5.5,4.0,right)
sx=lambda x:3.63-(x-3.10)/1.98*.42
sy=lambda y:3.63-(y-3.50)/1.98*.42
# Split the L into side, front and triangular corner; preserve the same hip intersection.
roof_surface('Varanda lateral',3.10,5.08,-5.5,3.50,lambda x,y:sx(x))
roof_surface('Varanda frontal',.08,3.10,3.50,5.48,lambda x,y:sy(y),'Y')
vertices=[];faces=[];n=22
for j in range(n+1):
    y=3.50+1.98*j/n
    for i in range(n+1):
        x=3.10+1.98*i/n
        h=min(sx(x),sy(y));profile=.029*math.sin(math.pi*((y if sx(x)<sy(y) else x)/.265)%1)
        vertices.append((x,y,h+.017+profile))
for j in range(n):
    for i in range(n):
        a=j*(n+1)+i;faces.append((a,a+1,a+n+2,a+n+1))
mesh('Encontro diagonal varanda',vertices,faces,roof,4,True)
mesh('Forro encontro varanda',[(3.10,3.50,3.53),(5.08,3.50,3.11),(5.08,5.48,3.11),(3.10,5.48,3.11)],[(0,1,2),(0,2,3)],wood,4)
beam('Espigao varanda',(3.10,3.50,3.66),(5.08,5.48,3.25),.063,roof2,4)
beam('Testeira frontal continua',(3.10,5.48,3.15),(5.08,5.48,3.15),.12,wood,4,.085)
beam('Testeira lateral continua',(5.08,3.50,3.15),(5.08,5.48,3.15),.12,wood,4,.085)
for y in np.arange(-5.25,5.25,.48):
    if y<3.5:beam('Caibro varanda',(3.10,float(y),3.46),(5.04,float(y),3.10),.067,wood,4,.095)
for x in np.arange(.25,4.95,.48):
    if x<3.1:beam('Caibro frontal',(float(x),3.55,3.46),(float(x),5.44,3.10),.067,wood,4,.095)
box('Chamine referencia',(-1.3,-3.75,4.87),(1.05,.8,1.1),stone,4,.009)
box('Capa chamine',(-1.3,-3.75,5.46),(1.16,.91,.09),concrete,4,.012)

# End finish covers the illustrative support structure; no holes beneath a finished house.
box('Embasamento dormitorios',(-1.65,0,.255),(3.514,10.514,.51),stone,6,.009)
box('Embasamento social',(1.7,-.7,.255),(3.214,9.114,.51),stone,6,.009)
box('Embasamento varanda lateral',(4.02,0,.255),(1.514,10.514,.51),stone,6,.009)
box('Embasamento varanda frontal',(2.45,4.52,.255),(4.564,1.464,.51),stone,6,.009)
for x,y in [(-3.35,5.13),(.10,5.13),(.10,3.72),(3.23,3.72),(3.23,-5.13),(-3.35,-5.13)]:
    box('Arremate esquina',(x,y,2.0),(.064,.064,2.96),wood,6,.002)
# Window sill, handles and rails complete the scale of the front openings.
box('Peitoril frontal',(-1.625,5.21,1.53),(1.88,.19,.055),frame,6,.004)
box('Puxador porta',(1.59,3.816,1.49),(.018,.043,.20),frame,6,.005)
box('Trilho porta',(1.575,3.79,.545),(1.66,.07,.025),frame,6,.002)

# Keep the illustrative concrete frame inside the wall thickness at completion.
for o in objects:
    if o.get('buildStage')==2 and o.data.materials[0]==concrete:
        if o.dimensions.x<.25:o.scale.x*=.72
        if o.dimensions.y<.25:o.scale.y*=.72
# Surface normals on the curved tiles are authored geometry; no artificial bump.
for m in [roof,roof2]:
    p=principled(m)
    for link in list(m.node_tree.links):
        if link.to_socket==p.inputs['Normal']:m.node_tree.links.remove(link)

# Generate consistent UVs from world-space dominant face directions (map repeats per metre).
for o in objects:
    if not o.data.uv_layers:o.data.uv_layers.new(name='Surface metres')
    uv=o.data.uv_layers.active.data
    for p in o.data.polygons:
        normal=o.matrix_world.to_3x3()@p.normal;axis=max(range(3),key=lambda k:abs(normal[k]))
        for li in p.loop_indices:
            v=o.matrix_world@o.data.vertices[o.data.loops[li].vertex_index].co
            pair=(v.y,v.z) if axis==0 else ((v.x,v.z) if axis==1 else (v.x,v.y))
            uv[li].uv=(pair[0]/1.3,pair[1]/1.3)

reflect_all();scene['orientation_refined']=True;scene['visual_quality_pass']='2026-10-01 — corrected porch hip, roof courses, glazing, plinth and material maps.'

# Daylight with a broad sky and a low sun produces rich contact shadows/reflections.
scene.world.use_nodes=True;nodes=scene.world.node_tree.nodes;links=scene.world.node_tree.links
nodes.clear();out=nodes.new('ShaderNodeOutputWorld');bg=nodes.new('ShaderNodeBackground');sky=nodes.new('ShaderNodeTexSky');sky.sky_type='SINGLE_SCATTERING'
sky.sun_elevation=math.radians(32);sky.sun_rotation=math.radians(125);sky.sun_disc=True;sky.sun_size=math.radians(.75);sky.sun_intensity=.7
sky.altitude=.1;sky.air_density=1.0
if hasattr(sky,'dust_density'):sky.dust_density=1.5
bg.inputs['Strength'].default_value=.36
links.new(sky.outputs['Color'],bg.inputs['Color']);links.new(bg.outputs['Background'],out.inputs['Surface'])
for o in list(scene.objects):
    if o.type=='LIGHT':bpy.data.objects.remove(o,do_unlink=True)
bpy.ops.object.light_add(type='AREA',location=(-6,8,11));key=bpy.context.object;key.name='Luz natural ampla';key.data.energy=1200;key.data.size=6;key.rotation_euler=(Vector((0,0,1.6))-key.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.light_add(type='SUN');sun=bpy.context.object;sun.name='Sol natural';sun.rotation_euler=(math.radians(38),math.radians(-22),math.radians(-32));sun.data.energy=1.35;sun.data.angle=.075
cam=scene.camera;cam.location=(-17.5,24,12.0);cam.rotation_euler=(Vector((-.5,0,1.65))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='PERSP';cam.data.lens=44;cam.data.sensor_width=36
scene.render.engine='CYCLES';scene.cycles.samples=80;scene.cycles.use_denoising=True;scene.cycles.max_bounces=8;scene.cycles.transmission_bounces=6
scene.render.resolution_x=2000;scene.render.resolution_y=1400;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG';scene.render.film_transparent=True
scene.view_settings.view_transform='AgX';scene.view_settings.look='AgX - Medium High Contrast';scene.view_settings.exposure=.25
scene['study_notice']='Reference reconstruction from public renders and unscaled plan. Estimated dimensions. Concealed foundations/frame illustrative; no executive accuracy.'
# Pack local maps into the editable source as well as keeping their ordinary files.
for im in bpy.data.images:
    if im.filepath and im.source=='FILE':im.pack()
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'blender','residencia-rincao.blend'))

# Merge only copies by phase and material. Editable source retains all parts.
bpy.ops.object.select_all(action='DESELECT');export=[]
for stage in range(7):
    mats=set(o.data.materials[0] for o in objects if o['buildStage']==stage)
    for m in mats:
        copies=[]
        for o in objects:
            if o['buildStage']==stage and o.data.materials[0]==m:
                du=o.copy();du.data=o.data.copy();scene.collection.objects.link(du);du.select_set(True);copies.append(du)
        bpy.context.view_layer.objects.active=copies[0];bpy.ops.object.join();joined=bpy.context.object
        joined.name='stage_%d_%s'%(stage,m.name);joined['buildStage']=stage;bpy.ops.object.transform_apply(location=True,rotation=True,scale=True);export.append(joined);joined.select_set(False)
for o in export:o.select_set(True)
bpy.ops.export_scene.gltf(filepath=os.path.join(ROOT,'assets','models','residencia-rincao.glb'),export_format='GLB',use_selection=True,export_extras=True,export_cameras=False,export_lights=False,export_draco_mesh_compression_enable=True,export_draco_mesh_compression_level=6)
for o in export:bpy.data.objects.remove(o,do_unlink=True)
scene.render.filepath=os.path.join(ROOT,'blender','residencia-rincao-final.png');bpy.ops.render.render(write_still=True)
# Additional frontal camera directly comparable to the official front render.
cam.location=(-7.0,23.5,5.9);cam.rotation_euler=(Vector((-.45,1,2.1))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=49
scene.render.filepath=os.path.join(ROOT,'blender','residencia-rincao-frontal.png');bpy.ops.render.render(write_still=True)
print('QUALITY_COMPLETE',len(objects),'parts;',len(export),'export meshes')
