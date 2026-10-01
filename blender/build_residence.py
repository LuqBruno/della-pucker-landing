"""Reference study, not an executive project. Blender 5.2, metres, Z up.
References: DXfLBPXj5nQ (render + plan), DXfA76_DjFo (front render).
Dimensions inferred from unscaled images. Concealed structure is illustrative.
"""
import bpy, math, random, os
from mathutils import Vector
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
random.seed(17)
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
scene=bpy.context.scene
scene.unit_settings.system='METRIC'
groups={}
for i,n in enumerate(['Implantacao','Fundacao','Estrutura','Fechamentos','Cobertura','Esquadrias','Acabamento']):
    c=bpy.data.collections.new('%02d_%s'%(i,n));scene.collection.children.link(c);groups[i]=c

def material(name,hex,rough=.7,metal=0):
    rgb=tuple(int(hex[i:i+2],16)/255 for i in (0,2,4))
    # Convert authored sRGB to linear for glTF/Blender consistency.
    rgb=tuple(((v+.055)/1.055)**2.4 if v>.04045 else v/12.92 for v in rgb)
    m=bpy.data.materials.new(name);m.diffuse_color=(*rgb,1);m.use_nodes=True
    p=next((n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED'),None)
    if p is None:
        p=m.node_tree.nodes.new('ShaderNodeBsdfPrincipled');out=m.node_tree.nodes.new('ShaderNodeOutputMaterial');m.node_tree.links.new(p.outputs['BSDF'],out.inputs['Surface'])
    p.inputs['Base Color'].default_value=(*rgb,1);p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal
    return m
white=material('Pintura mineral clara','E8E7E0');frame=material('Esquadrias brancas','F0EFE9',.38,.15)
concrete=material('Concreto aparente','ACADA6',.92);stone=material('Piso cimenticio','C0BEB6',.85)
roof=material('Telhas grafite','414449',.68);roof2=material('Variacao telhas','4B4E50',.72)
wood=material('Madeira pintada','DEDFD6',.65);glass=material('Vidro cinza reflexo','82969B',.18,.28)
next(n for n in glass.node_tree.nodes if n.type=='BSDF_PRINCIPLED').inputs['Coat Weight'].default_value=.5
soil=material('Terra compactada','99998C',1);grass=material('Jardim','78846A',1)
leaf=material('Folhagem','566A48',.95);pink=material('Flores rosadas','AB8A96',.92);yellow=material('Flores amarelas','D4B54E',.9)
fabric=material('Linho','B9B3A6',1);oak=material('Madeira natural','9C8063',.75)
objects=[]
def assign(o,name,mat,stage):
    o.name=name;o.data.materials.append(mat);o['buildStage']=stage
    for c in list(o.users_collection):c.objects.unlink(o)
    groups[stage].objects.link(o);objects.append(o);return o
def box(name,loc,dims,mat,stage,bevel=.008):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.dimensions=dims
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    assign(o,name,mat,stage)
    if bevel:
        mod=o.modifiers.new('Arestas com espessura real','BEVEL');mod.width=bevel;mod.segments=2
        bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=mod.name)
    return o
def beam(name,a,b,width,mat,stage,depth=None):
    a,b=Vector(a),Vector(b);o=box(name,(a+b)/2,(width,depth or width,(b-a).length),mat,stage,.004)
    o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler();return o
def mesh(name,verts,faces,mat,stage):
    me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(name,me);groups[stage].objects.link(o);o.data.materials.append(mat);o['buildStage']=stage;objects.append(o);return o

# Ground and exact visible plan silhouette: left bedroom wing + recessed living wing.
box('Terreno',(0,0,-.11),(12.7,16,.18),soil,0,.025)
for x in [-3.15,.02,3.12,4.6]:
    for y in [-4.85,-1.6,1.6,4.8]:
        if x>4 and y>3.8:continue
        box('Sapata ilustrativa',(x,y,.04),(.72,.72,.3),concrete,1)
for x in [-3.15,.02,3.12]:box('Viga baldrame',(x,0,.23),(.22,10.1,.32),concrete,1)
for y in [-4.85,-1.6,1.6,4.8]:box('Travamento baldrame',(0,y,.23),(6.5,.22,.32),concrete,1)
box('Laje ala dormitorios',(-1.65,0,.42),(3.5,10.5,.2),concrete,1)
box('Laje social',(1.7,-.7,.42),(3.2,9.1,.2),concrete,1)
box('Varanda lateral',(4.02,0,.42),(1.5,10.5,.2),stone,1)
box('Varanda frontal',(2.45,4.52,.42),(4.55,1.45,.2),stone,1)
# Framing is explicitly an illustrative construction reading, not calculated structure.
for x,y in [(-3.24,5.05),(.05,5.05),(-3.24,-5.05),(.05,-5.05),(3.15,3.65),(3.15,-5.05),(-3.24,0),(.05,0),(3.15,0)]:
    box('Pilar ilustrativo',(x,y,1.99),(.18,.18,2.94),concrete,2)
for x in [-3.24,.05,3.15]:box('Cinta superior',(x,-.7 if x>3 else 0,3.39),(.19,8.9 if x>3 else 10.3,.2),concrete,2)
for y in [-5.05,3.65]:box('Viga transversal',(-.05,y,3.39),(6.58,.18,.2),concrete,2)
for y in [-4.8,-2.1,.6,3.0,5.08]:
    box('Pilar varanda',(4.6,y,1.94),(.14,.14,2.84),wood,2)
box('Pilar frontal varanda',(1.94,5.08,1.94),(.14,.14,2.84),wood,2)
box('Frechal lateral',(4.6,.12,3.32),(.14,10.25,.18),wood,2)
box('Frechal frontal',(2.43,5.08,3.32),(4.5,.14,.18),wood,2)

# Wall panels have actual empty openings and 18 cm thickness.
def panel(name,x0,x1,y0,y1,z0,z1):
    if min(x1-x0,y1-y0,z1-z0)>.001:box(name,((x0+x1)/2,(y0+y1)/2,(z0+z1)/2),(x1-x0,y1-y0,z1-z0),white,3,.004)
def wall_x(y,x0,x1,height,openings=[]):
    edges=sorted(set([x0,x1]+[v for a,b,c,d in openings for v in(a,b)]))
    for a,b in zip(edges,edges[1:]):
        opening=next((o for o in openings if o[0]<=a+.001 and o[1]>=b-.001),None)
        if opening:
            panel('Peitoril',a,b,y-.09,y+.09,.52,opening[2]);panel('Verga',a,b,y-.09,y+.09,opening[3],height)
        else:panel('Parede',a,b,y-.09,y+.09,.52,height)
def wall_y(x,y0,y1,height,openings=[]):
    edges=sorted(set([y0,y1]+[v for a,b,c,d in openings for v in(a,b)]))
    for a,b in zip(edges,edges[1:]):
        op=next((o for o in openings if o[0]<=a+.001 and o[1]>=b-.001),None)
        if op:
            panel('Peitoril lateral',x-.09,x+.09,a,b,.52,op[2]);panel('Verga lateral',x-.09,x+.09,a,b,op[3],height)
        else:panel('Parede lateral',x-.09,x+.09,a,b,.52,height)
wall_x(5.05,-3.25,.05,3.5,[(-2.45,-.8,1.57,2.61)])
wall_x(3.65,.05,3.15,3.5,[(.8,2.35,.52,2.78)])
wall_x(-5.05,-3.25,3.15,3.5)
wall_y(-3.25,-5.05,5.05,3.5,[(-3.8,-2.4,1.6,2.62),(-.7,.7,1.6,2.62),(2.8,4.1,1.6,2.62)])
wall_y(.05,3.65,5.05,4.61)
wall_y(3.15,-5.05,3.65,3.5,[(-3.4,-2.45,1.64,2.64),(-1.3,.3,1.54,2.64),(1.4,2.65,.52,2.78)])
# Unscaled published plan: three bedrooms on left, living/dining on right.
for y in [-2.32,.6,1.97]:wall_x(y,-3.25,.05,3.35)
wall_y(.05,-5.05,3.65,3.35,[(-1.9,-1.05,.52,2.6),(.85,1.6,.52,2.6),(2.65,3.45,.52,2.6)])
wall_x(-2.45,.05,3.15,3.35,[(.3,1.1,.52,2.6)])
# Sloping upper walls match the two stepped shed roofs visible in both references.
def wedge(y,x0,x1,z0,z1):
    verts=[(x0,y-.09,3.49),(x1,y-.09,3.49),(x1,y-.09,z1),(x0,y-.09,z0),(x0,y+.09,3.49),(x1,y+.09,3.49),(x1,y+.09,z1),(x0,y+.09,z0)]
    mesh('Empena inclinada',verts,[(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)],white,3)
for y in [-5.05,5.05]:wedge(y,-3.25,.05,3.5,4.68)
for y in [-5.05,3.65]:wedge(y,.05,3.15,4.48,3.5)
# Fine horizontal shadow joints interrupt only opaque parts; openings remain clear.
for o in list(objects):
    if o.get('buildStage')!=3 or o.type!='MESH' or 'Empena' in o.name:continue
    # Panel edges provide controlled, subtle cladding scale without a heavy texture.
    dims=o.dimensions
    if dims.z<.22:continue
    if dims.y<.21:
        for k in range(1,int(dims.z/.21)+1):
            z=o.location.z-dims.z/2+k*.21
            box('Junta horizontal',(o.location.x,o.location.y+.094,z),(dims.x,.006,.006),stone,3,0)
    elif dims.x<.21:
        for k in range(1,int(dims.z/.21)+1):
            z=o.location.z-dims.z/2+k*.21
            box('Junta lateral',(o.location.x+.094,o.location.y,z),(.006,dims.y,.006),stone,3,0)

# Four roof planes. Corrugation is real geometry, plus fine seams across rows.
def roof_plane(name,x0,x1,y0,y1,zleft,zright):
    slope=(zright-zleft)/(x1-x0)
    verts=[(x0,y0,zleft),(x1,y0,zright),(x1,y1,zright),(x0,y1,zleft)]
    o=mesh(name,verts,[(0,1,2,3)],roof,4)
    sol=o.modifiers.new('Espessura cobertura','SOLIDIFY');sol.thickness=.055
    bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=sol.name)
    for y in [y0,y1]:beam('Testeira branca',(x0,y,zleft-.075),(x1,y,zright-.075),.15,wood,4,.09)
    for x,z in [(x0,zleft),(x1,zright)]:beam('Beiral longitudinal',(x,y0,z-.075),(x,y1,z-.075),.14,wood,4,.09)
    # Tiles run down the slope, repeated along Y. A shallow curved profile avoids a plastic plane.
    count=math.ceil((y1-y0)/.24)
    for j in range(count):
        ya=y0+j*(y1-y0)/count;yb=y0+(j+1)*(y1-y0)/count
        vv=[]
        for x in [x0,x1]:
            for k in range(7):
                y=ya+(yb-ya)*k/6;z=zleft+(x-x0)*slope+.025+.035*math.sin(math.pi*k/6)
                vv.append((x,y,z))
        mesh('Telha perfil ondulado',vv,[(k,k+1,8+k,7+k) for k in range(6)],roof if j%4 else roof2,4)
    for i in range(1,math.ceil((x1-x0)/.38)):
        x=x0+i*.38
        if x<x1:beam('Sobreposicao telhas',(x,y0,zleft+(x-x0)*slope+.045),(x,y1,zleft+(x-x0)*slope+.045),.015,roof2,4,.015)
    for y in [y0+.22+i*.55 for i in range(int((y1-y0)/.55))]:beam('Caibro',(x0,y,zleft-.19),(x1,y,zright-.19),.065,wood,4,.09)
roof_plane('Cobertura ala esquerda',-3.68,.30,-5.5,5.48,3.49,4.92)
roof_plane('Cobertura ala social',.02,3.57,-5.5,4.0,4.72,3.58)
roof_plane('Cobertura varanda lateral',3.10,5.08,-5.5,5.48,3.63,3.21)
# Front lean-to falls toward the observer (Y+). Geometry rotated from standard roof helper.
before=set(objects)
roof_plane('Cobertura varanda frontal',3.50,5.48,-3.10,-.08,3.63,3.21)
for o in [o for o in objects if o not in before]:
    # Swap X,Y with orientation so front roof spans X=.08..3.10, Y=3.5..5.48.
    for v in o.data.vertices:
        wx=o.matrix_world@v.co;v.co=Vector((-wx.y,wx.x,wx.z))
    o.location=(0,0,0);o.rotation_euler=(0,0,0);o.scale=(1,1,1)
box('Chamine referencia',(-1.3,-3.75,4.87),(1.05,.8,1.1),stone,4)
box('Capa chamine',(-1.3,-3.75,5.46),(1.16,.91,.09),concrete,4)

def window(name,x,y,w,h,bottom,side=False,shutters=True):
    made=[];start=len(objects)
    box(name+' vidro',(x,y,bottom+h/2),(w,.04,h),glass,5,.002)
    for xx in [x-w/2,x,x+w/2]:box('Montante',(xx,y+.03,bottom+h/2),(.045,.075,h+.08),frame,5,.003)
    for zz in [bottom,bottom+h]:box('Travessa',(x,y+.03,zz),(w+.08,.075,.055),frame,5,.003)
    if shutters:
        sw=w*.35
        for direction in [-1,1]:
            xx=x+direction*(w/2+sw/2+.08)
            box('Folha veneziana',(xx,y-.005,bottom+h/2),(sw,.055,h+.08),wood,5,.004)
            for zz in [bottom,bottom+h]:box('Moldura veneziana',(xx,y+.035,zz),(sw+.04,.055,.045),frame,5,.003)
            for k in range(int(h/.052)):
                box('Lamina veneziana',(xx,y+.034,bottom+.035+k*.052),(sw-.035,.055,.017),frame,5,.002)
    if side:
        # Rotate the just-created front assembly around its centre to the right facade.
        for o in objects[start:]:
            dx=o.location.x-x;dy=o.location.y-y;o.location.x=x+dy;o.location.y=y-dx;o.rotation_euler.z=-math.pi/2
window('Janela frontal',-1.625,5.16,1.65,1.04,1.57)
window('Porta de correr',1.575,3.76,1.55,2.26,.52)
for y,w,h,z in [(-2.925,.95,1,1.64),(-.5,1.6,1.1,1.54),(2.025,1.25,2.26,.52)]:window('Janela varanda',3.26,y,w,h,z,True,True)
for y in [-3.1,0,3.45]:window('Janela dormitorios',-3.36,y,1.3,1.02,1.6,True,False)
# Railings have real intersections and unobstructed front entrance.
def rail(a,b):
    a,b=Vector((*a,.55)),Vector((*b,.55));length=(b-a).length;count=max(1,round(length/1.35))
    for i in range(count+1):
        p=a+(b-a)*i/count;beam('Balaustre',p,p+Vector((0,0,1.0)),.065,wood,6)
    beam('Corrimao',a+Vector((0,0,1.0)),b+Vector((0,0,1.0)),.065,wood,6)
    beam('Travessa inferior',a+Vector((0,0,.11)),b+Vector((0,0,.11)),.05,wood,6)
    for i in range(count):
        p=a+(b-a)*i/count;q=a+(b-a)*(i+1)/count
        beam('Cruzeta',p+Vector((0,0,.14)),q+Vector((0,0,.94)),.06,wood,6,.04)
        beam('Cruzeta',p+Vector((0,0,.94)),q+Vector((0,0,.14)),.06,wood,6,.04)
rail((1.96,5.09),(4.60,5.09));rail((4.60,5.09),(4.60,-4.80))
for i in range(3):box('Degrau',(1.03,5.28+i*.29,.43-i*.14),(2.05,.6,.14),stone,6)
box('Caminho entrada',(1.02,6.43,.015),(2.12,2.0,.05),stone,6,.012)
box('Acesso lateral',(-4.40,.4,.015),(2.0,12.5,.05),stone,6,.012)
for x,y,w,d in [(3.5,6.45,2.7,2.3),(-.9,6.9,1.65,1.45),(5.45,0,1.25,12.5)]:box('Gramado',(x,y,.018),(w,d,.055),grass,6,.02)
# Low, irregular planting rather than giant spherical shrubs.
for i in range(70):
    x=2.3+random.random()*2.3;y=5.65+random.random()*.68
    for j in range(3):
        angle=random.random()*math.tau;h=.12+random.random()*.22
        beam('Folha jardim',(x,y,.05),(x+math.cos(angle)*.18,y+math.sin(angle)*.18,h),.025,leaf,6,.013)
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,radius=.035+random.random()*.025,location=(x,y,.16+random.random()*.12))
    assign(bpy.context.object,'Flor',yellow if i%3 else pink,6)
# Restrained furnishing follows plan, only revealed with finishes.
box('Sofa',(2.52,2.27,.80),(.74,1.9,.50),fabric,6,.09)
box('Encosto sofa',(2.91,2.27,1.05),(.18,1.9,.76),fabric,6,.045)
box('Mesa centro',(1.65,2.08,.77),(.62,.65,.07),oak,6,.015)
box('Mesa jantar',(1.62,-.65,1.23),(.80,1.7,.065),oak,6,.02)
for y in [-1.25,-.05]:
    for x in [.95,2.29]:box('Cadeira',(x,y,.88),(.38,.43,.10),fabric,6,.02)
for y in [-3.6,-.9,3.4]:
    box('Cama',(-1.70,y,.82),(1.45,1.9,.45),fabric,6,.055)

# Studio presentation, natural daylight and contact shadows, no external texture dependencies.
scene.world.use_nodes=True;scene.world.node_tree.nodes.get('Background').inputs[0].default_value=(.72,.79,.85,1);scene.world.node_tree.nodes.get('Background').inputs[1].default_value=.45
bpy.ops.object.light_add(type='AREA',location=(-5,3,12));bpy.context.object.data.energy=1800;bpy.context.object.data.shape='DISK';bpy.context.object.data.size=7
bpy.ops.object.light_add(type='SUN',location=(-7,2,10));sun=bpy.context.object;sun.rotation_euler=(.48,-.45,-.5);sun.data.energy=2;sun.data.angle=.12
bpy.ops.object.camera_add(location=(17,23,15));cam=bpy.context.object;cam.rotation_euler=(Vector((.3,0,1.8))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=20.3;scene.camera=cam
scene.render.engine='CYCLES';scene.cycles.samples=32;scene.cycles.use_denoising=True
scene.render.resolution_x=1600;scene.render.resolution_y=1200;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG';scene.render.film_transparent=True
scene.view_settings.view_transform='AgX'
scene['study_notice']='Reconstruction from public renders and unscaled plan; approximate dimensions and illustrative concealed structure. Not an executive project.'
scene['reference']='https://www.instagram.com/dellapucker/p/DXfLBPXj5nQ/'
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'blender','residencia-rincao.blend'))
# Merge only export copies by stage/material to keep web draw calls low. Editable source is saved above.
bpy.ops.object.select_all(action='DESELECT')
export=[]
for stage in range(7):
    mats=set(o.data.materials[0] for o in objects if o['buildStage']==stage)
    for mat in mats:
        copies=[]
        for o in objects:
            if o['buildStage']==stage and o.data.materials[0]==mat:
                du=o.copy();du.data=o.data.copy();scene.collection.objects.link(du);du.select_set(True);copies.append(du)
        bpy.context.view_layer.objects.active=copies[0];bpy.ops.object.join();joined=bpy.context.object
        joined.name='stage_%d_%s'%(stage,mat.name);joined['buildStage']=stage
        bpy.ops.object.transform_apply(location=True,rotation=True,scale=True);export.append(joined);joined.select_set(False)
for o in export:o.select_set(True)
bpy.ops.export_scene.gltf(filepath=os.path.join(ROOT,'assets','models','residencia-rincao.glb'),export_format='GLB',use_selection=True,export_extras=True,export_cameras=False,export_lights=False)
for o in export:bpy.data.objects.remove(o,do_unlink=True)
scene.render.filepath=os.path.join(ROOT,'blender','residencia-rincao-render.png')
bpy.ops.render.render(write_still=True)
print('RESIDENCE_READY',len(objects))
