import json, sys, numpy as np
sys.argv=[sys.argv[0]]+sys.argv[1:]
from PIL import Image, ImageDraw, ImageChops
from scipy import ndimage as ndi
import importlib.util
D=json.load(open(sys.argv[1]))
X0,Y0=6365751.8,1865556.9
def mk(S,dx,dy,div): return lambda p:((448+dx+(p[0]-X0)/S)/div,(62+dy+(Y0-p[1])/S)/div)
def draw_feature(img,rings,val,T):
    if not rings: return
    if len(rings)==1: ImageDraw.Draw(img).polygon([T(p) for p in rings[0]],fill=val); return
    m=Image.new('1',img.size,0)
    for r in rings:
        t=Image.new('1',img.size,0); ImageDraw.Draw(t).polygon([T(p) for p in r],fill=1); m=ImageChops.logical_xor(m,t)
    img.paste(val,mask=m)
def rast(S,dx,dy,div,layer='gp'):
    W,H=3300//div,2550//div; T=mk(S,dx,dy,div); im=Image.new('L',(W,H),0)
    if layer=='gp':
        for k in sorted(D['gp'],key=lambda k:-len(D['gp'][k])):
            if int(k)==55: continue
            for rings in D['gp'][k]: draw_feature(im,rings,int(k)-31,T)
    else:
        for i,f in enumerate(D['pud']): draw_feature(im,f['g'],i+1,T)
    return np.array(im)
meta=json.load(open('gis/gpmeta.json')); codes=json.load(open('gis/codes.json'))
cls=np.load('cls_full.npy')
# zone id -> implied gp id
imp=np.zeros(40,np.uint8)
alias={'T4-NC':'MU-NC','T5-TC':None,'T6-UC':'MU-UC','CS-PK':'P-PK','CS-PSP':'P-PSP','CS-FW':'P-FW'}
for zi,c in enumerate(codes):
    c2=alias.get(c,c)
    if c=='T5-TC': imp[zi+1]=29; continue
    if c2 in meta['usual']: imp[zi+1]=meta['usual'].index(c2)+1
c4=cls[::4,::4][:637,:825]; want=imp[c4]; ok=want>0
best=(0,)
for S in (11.62,11.63,11.64,11.65,11.66):
    for dx in range(4,13,2):
        for dy in range(-6,3,2):
            g=rast(S,dx,dy,4)[:637,:825]; v=((g==want)&ok).sum()/ok.sum()
            if v>best[0]: best=(float(v),S,dx,dy)
print('best agreement',best)
_,S,dx,dy=best; json.dump(dict(S=S,dx=dx,dy=dy),open('gis/georef.json','w'))
gp=rast(S,dx,dy,2); pud=rast(S,dx,dy,2,'pud')
np.save('gis/gp_full.npy',gp); np.save('gis/pud_full.npy',pud)
c2=cls[::2,::2][:1275,:1650]; want=imp[c2]; ok=(want>0)&(gp>0)
# erode to ignore boundary slop
core=np.zeros_like(ok)
for z in np.unique(c2[c2>0]): core|=ndi.binary_erosion(c2==z,iterations=3)
ok&=core
print('interior agreement %.2f%%'%(100*(gp[ok]==want[ok]).mean()))
mm=ok&(gp!=want); lab,n=ndi.label(mm); sz=ndi.sum(mm,lab,range(1,n+1))
print('mismatch blobs >150 cells:',int((sz>150).sum()))
rows=[]
for i in np.argsort(-sz)[:25]:
    if sz[i]<150: break
    ys,xs=np.where(lab==i+1); z=np.bincount(c2[ys,xs]).argmax(); g=np.bincount(gp[ys,xs]).argmax()
    rows.append((int(sz[i]),codes[z-1],meta['names'][g-1],int(xs.mean()*2),int(ys.mean()*2)))
for r in rows: print(r)
json.dump(rows,open('gis/mismatch.json','w'))
pd=(c2==codes.index('PUD')+1)|(c2==codes.index('PCD')+1)
print('proposed PUD/PCD covered by 2008 PUD layer: %.1f%%; 2008 PUD layer land now PUD/PCD: %.1f%%'%(100*(pud[pd]>0).mean(),100*pd[(pud>0)&(c2>0)].mean()))
