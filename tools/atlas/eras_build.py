# Historiapp · Atlas. Capas políticas por época a partir de historical-basemaps (A. Ourednik, GPL-3.0).
import json, sys, warnings; warnings.filterwarnings('ignore')
from shapely.geometry import shape, box, Polygon, MultiPolygon
from shapely.ops import transform, unary_union, polylabel
from shapely.validation import make_valid
from pyproj import Transformer
pj=dict(lat1=32,lat2=46,lat0=38,lon0=24,x0=-3300000,y1=2350000,W=2000,x1=4400000)
tr=Transformer.from_crs("EPSG:4326",f"+proj=lcc +lat_1={pj['lat1']} +lat_2={pj['lat2']} +lat_0={pj['lat0']} +lon_0={pj['lon0']} +datum=WGS84 +units=m",always_xy=True)
x0,x1,y1=pj['x0'],pj['x1'],pj['y1']; s=pj['W']/(x1-x0); y0=y1-1312/s
win=box(x0,y0,x1,y1).buffer(60000); ll=box(-25,10,75,65)
def P(g): return transform(lambda x,y,z=None: tr.transform(x,y), g)
def tp(x,y): return (round((x-x0)*s,1), round((y1-y)*s,1))
def ring(c):
    pts=[tp(x,y) for x,y in c]; o=[f'M{pts[0][0]} {pts[0][1]}']; pv=pts[0]
    for a,b in pts[1:]:
        if (a,b)!=pv: o.append(f'L{a} {b}'); pv=(a,b)
    return ''.join(o)+'Z'
def polys(g): return [g] if isinstance(g,Polygon) else [q for q in getattr(g,'geoms',[]) if isinstance(q,Polygon)]
def path(g,mina):
    o=[]
    for q in polys(g):
        if q.area<mina: continue
        o.append(ring(q.exterior.coords)); o+= [ring(r.coords) for r in q.interiors if Polygon(r).area>mina]
    return ''.join(o)
def lab(g):
    b=max(polys(g),key=lambda q:q.area); p=polylabel(b,tolerance=4000); return tp(p.x,p.y)
# familia y nombre en castellano de cada entidad (None = no se dibuja)
FAM={
 'Egypt':('egi','Egipto','Egypt'),'Ptolemaic Kingdom':('egi','Reino ptolemaico','Ptolemaic Kingdom'),
 'Kush':('nub','Kush','Kush'),'Kerma':('nub','Kerma','Kerma'),'Meroe':('nub','Meroe','Meroë'),
 'Ur':('mes','Ur','Ur'),'city-states':('mes','Ciudades sumerias','Sumerian city-states'),'Babylonia':('mes','Babilonia','Babylonia'),
 'Assyria':('mes','Asiria','Assyria'),'Elam':('ela','Elam','Elam'),'Hurrian Kingdoms':('mes','Reinos hurritas','Hurrian kingdoms'),
 'Hittites':('hit','Hititas','Hittites'),'Urartu':('hit','Urartu','Urartu'),'Phrygians':('hit','Frigia','Phrygia'),
 'Achaemenid Empire':('per','Imperio aqueménida','Achaemenid Empire'),'Parthia':('per','Partia','Parthia'),'Parthian Empire':('per','Imperio parto','Parthian Empire'),
 'Persia':('per','Imperio sasánida','Sasanian Empire'),'Sasanian Empire':('per','Imperio sasánida','Sasanian Empire'),'Atropatene':('per','Atropatene','Atropatene'),
 'Greek city-states':('gre','Ciudades griegas','Greek city-states'),'Greek colonies':('gre','Colonias griegas','Greek colonies'),
 'Empire of Alexander':('mac','Imperio de Alejandro','Empire of Alexander'),'Kingdom of Antigonus':('mac','Reino de Antígono','Kingdom of Antigonus'),
 'Kingdom of Kassander':('mac','Reino de Casandro','Kingdom of Cassander'),'Kingdom of Lysimachus':('mac','Reino de Lisímaco','Kingdom of Lysimachus'),
 'Macedon and Hellenic League':('mac','Macedonia y la Liga helénica','Macedon and the Hellenic League'),'Bosporan Kingdom':('gre','Reino del Bósforo','Bosporan Kingdom'),
 'Seleucid Kingdom':('sel','Reino seléucida','Seleucid Kingdom'),
 'Carthaginian Empire':('fen','Cartago','Carthage'),'Carthage':('fen','Cartago','Carthage'),'Canaan':('fen','Canaán','Canaan'),
 'Etrurians':('etr','Etruria','Etruria'),
 'Roman Republic':('rom','República romana','Roman Republic'),'Rome':('rom','República romana','Roman Republic'),'Roman Empire':('rom','Imperio romano','Roman Empire'),
 'Rome (Diocletianus)':('rom','Imperio romano (tetrarquía)','Roman Empire (Tetrarchy)'),'Rome (Maximian)':('rom','Imperio romano (tetrarquía)','Roman Empire (Tetrarchy)'),
 'Rome (Constantinus)':('rom','Imperio romano (tetrarquía)','Roman Empire (Tetrarchy)'),'Rome (Galerius)':('rom','Imperio romano (tetrarquía)','Roman Empire (Tetrarchy)'),
 'Western Roman Empire':('rom','Imperio romano de Occidente','Western Roman Empire'),'Eastern Roman Empire':('rom2','Imperio romano de Oriente','Eastern Roman Empire'),
 'Numidia':('num','Numidia','Numidia'),'Mauretania':('num','Mauritania','Mauretania'),'Kingdom of Syphax':('num','Reino de Sífax','Kingdom of Syphax'),'Kingdom of Gala':('num','Reino de Gala','Kingdom of Gala'),
 'Armenia':('otr','Armenia','Armenia'),'Cappadocia':('otr','Capadocia','Cappadocia'),'Colchis':('otr','Cólquide','Colchis'),'Nabatean Kingdom':('otr','Reino nabateo','Nabataean Kingdom'),
 'Kingdom of David and Solomon':('otr','Israel y Judá','Israel and Judah'),'Dacia':('otr','Dacia','Dacia'),'Dacians':('pue','Dacios','Dacians'),'Thrace':('pue','Tracios','Thracians'),
 'Odrysian Kingdom':('otr','Reino odrisio','Odrysian Kingdom'),'Judea':('otr','Judea','Judaea'),'Dardania':('otr','Dardania','Dardania'),'Saba':('otr','Saba','Saba'),
 'Himyarite Kingdom':('otr','Reino himyarí','Himyarite Kingdom'),'Hadramaut':('otr','Hadramaut','Hadramawt'),'Qataban':('otr','Qatabán','Qataban'),'Axum':('otr','Aksum','Aksum'),
 'Arameans':('pue','Arameos','Aramaeans'),'state societies and Aramaean kingdoms':('otr','Reinos arameos','Aramaean kingdoms'),
 'Celtiberians':('pue','Celtíberos','Celtiberians'),'Celts':('pue','Celtas','Celts'),'Illyrians':('pue','Ilirios','Illyrians'),'Berbers':('pue','Bereberes','Berbers'),
 'Scythians':('pue','Escitas','Scythians'),'Sarmates':('pue','Sármatas','Sarmatians'),'Cimerians':('pue','Cimerios','Cimmerians'),'Hallstatt culture':('pue','Cultura de Hallstatt','Hallstatt culture'),
 'La Tène culture':('pue','Cultura de La Tène','La Tène culture'),'Urnfield cultures':('pue','Campos de urnas','Urnfield cultures'),'Beaker':('pue','Campaniforme','Bell Beaker'),
 'Yamnaya culture':('pue','Cultura Yamna','Yamnaya culture'),'Semites':('pue','Pueblos semitas','Semitic peoples'),'Anatolian tribes':('pue','Pueblos de Anatolia','Anatolian peoples'),
 'Germanic tribes':('pue','Germanos','Germanic peoples'),'Alans':('pue','Alanos','Alans'),'Caucasian Alans':('pue','Alanos','Alans'),'Hunnic Empire':('otr','Imperio huno','Hunnic Empire'),
 'Visigoths':('ger','Visigodos','Visigoths'),'Ostrogoths':('ger','Ostrogodos','Ostrogoths'),'Vandals':('ger','Vándalos','Vandals'),'Franks':('ger','Francos','Franks'),
 'Burgundians':('ger','Burgundios','Burgundians'),'Suebi':('ger','Suevos','Suebi'),'Gepids':('ger','Gépidos','Gepids'),'Saxons':('pue','Sajones','Saxons'),'Anglo-Saxons':('pue','Anglosajones','Anglo-Saxons'),
 'Saharan pastoral nomads':('pue','Pastores del Sáhara','Saharan pastoralists'),'Arabian pastoral nomads':('pue','Pastores de Arabia','Arabian pastoralists'),'Arabs':('pue','Árabes','Arabs'),
 'Iranian pastoralists':('pue','Pastores iranios','Iranian pastoralists'),'Blemmyes':('pue','Blemios','Blemmyes'),'Basques':('pue','Vascones','Basques'),
'Minoan':('ege','Creta minoica','Minoan Crete'),'Cycladic':('ege','Cultura cicládica','Cycladic culture'),'Crete':('gre','Creta','Crete'),
 'Bithynia':('otr','Bitinia','Bithynia'),'Pergamon':('mac','Reino de Pérgamo','Kingdom of Pergamon'),'Bosporian Kingdom':('gre','Reino del Bósforo','Bosporan Kingdom'),
 'Sabini':('pue','Sabinos','Sabines'),'Sabines':('pue','Sabinos','Sabines'),'Samnites':('pue','Samnitas','Samnites'),'Boii':('pue','Boyos','Boii'),'Alamans':('ger','Alamanes','Alamanni'),
 'Indus valley civilization':('otr','Civilización del Indo','Indus Valley civilisation'),'Bactria':('otr','Bactriana','Bactria'),'Kushan Empire':('otr','Imperio kushán','Kushan Empire'),
 'Mauryan Empire':('otr','Imperio maurya','Maurya Empire'),'Suren Kingdom':('otr','Reino suren','Suren Kingdom'),'Saka Kingdom':('otr','Reino saka','Saka Kingdom'),
}
COL={'egi':'#E1A01C','nub':'#B88A2E','mes':'#A6743A','ela':'#8C6A4A','hit':'#8E4E32','per':'#2E62AE','gre':'#C8643B','mac':'#9A4F8C','sel':'#2C7F7A','fen':'#6B3F86','etr':'#5E7B37','rom':'#B6402C','rom2':'#8F2F3F','num':'#A08A55','otr':'#7E7468','ger':'#6F7F5A','pue':'#6E6A5E'}
ERAS=[('bc3000',-3000,-2001),('bc2000',-2000,-1201),('bc1000',-1200,-701),('bc700',-700,-551),('bc500',-550,-401),('bc400',-400,-335),('bc323',-334,-301),('bc300',-300,-201),('bc200',-200,-101),('bc100',-100,-28),('bc1',-27,99),('200',100,299),('300',300,394),('400',395,475),('500',476,700)]
out=[]; faltan={}
for eid,a,b in ERAS:
    groups={}
    for ft in json.load(open(f'world_{eid}.geojson'))['features']:
        n=(ft['properties'].get('NAME') or '').strip()
        if not n: continue
        if n not in FAM:
            faltan[n]=faltan.get(n,[])+[eid]; continue
        try:
            g=make_valid(shape(ft['geometry'])).intersection(ll)
            if g.is_empty: continue
            g=make_valid(P(g)).intersection(win)
        except Exception: continue
        if g.area<2e9: continue
        fam,es,en=FAM[n]
        if eid=='300' and n=='Parthian Empire': fam,es,en='per','Imperio sasánida','Sasanian Empire'
        if eid in ('bc1000','bc700') and n=='Hittites': fam,es,en='hit','Reinos neohititas','Neo-Hittite kingdoms'
        if eid in ('bc1000','bc700') and n=='Greek city-states': fam,es,en='gre','Pueblos griegos','Greek peoples'
        groups.setdefault(es,[n,[],fam,en])[1].append(g)
    pols=[]
    for es,(n,gs,f,en) in groups.items():
        g=unary_union([make_valid(x).buffer(0) for x in gs]).simplify(2500)
        d=path(g,4e8 if f!='pue' else 3e9)
        if not d: continue
        pols.append({'f':f,'n':{'es':es,'en':en},'d':d,'lab':lab(g),'a':round(g.area/1e9)})
    pols.sort(key=lambda p:-p['a'])
    out.append({'id':eid,'from':a,'to':b,'pols':pols})
    print(eid,len(pols),[p['n']['es'] for p in pols][:14])
json.dump({'ecol':COL,'eras':out},open('atlas_eras.json','w'),ensure_ascii=False,separators=(',',':'))
import os; print('KB',os.path.getsize('atlas_eras.json')//1024)
big={k:v for k,v in faltan.items()}
print('sin traducir:',sorted(big)[:80])
