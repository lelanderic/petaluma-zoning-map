import numpy as np, json
from PIL import Image
from scipy import ndimage as ndi
p2=np.array(Image.open('full-2.png')).astype(np.int16)
H,W,_=p2.shape
def disk(r):
    y,x=np.ogrid[-r:r+1,-r:r+1]; return x*x+y*y<=r*r
# ---------- city mask ----------
black=(p2.max(2)<60)
furn=np.zeros((H,W),bool); furn[725:2075,0:870]=True; furn[2075:H,0:900]=True; furn[0:700,2380:W]=True; furn[:,3270:]=True; furn[2530:,:]=True
lab,n=ndi.label(~black); outside=lab==lab[5,5]
cand=ndi.binary_fill_holes(~outside)&~furn
lab,n=ndi.label(cand)
nb=ndi.sum(~black,lab,range(1,n+1))
city=np.isin(lab,[i+1 for i,s in enumerate(nb) if s>=150])
print('city comps',n,'kept',int((nb>=150).sum()),'px',int(city.sum()))
np.save('city.npy',city)
cpsp=np.load('cpsp.npy')&city
ov=np.load('ov.npz')
cols=json.load(open('cols.json'))
ZONES=['R-VLR','R-RLD','R-RDIV','R-RMD','R-RHD','R-MH','MU-MC','MU-NC','MU-SD','MU-DT','MU-UC','CI-NC','CI-CC','CI-BP','CI-MKR','CI-IND','CI-AG','P-PSP','P-ED','P-PK','P-OS','P-US','P-FW','PUD','PCD','T4-NC','T5-TC','T6-UC','T6-CORE','T6-ST','D1-AGS','D2-RAIL','D3-RDI','D4-TD','CS-PK','CS-PSP','CS-FW']
SMART={'T4-NC','T5-TC','T6-UC','T6-CORE','T6-ST','D1-AGS','D2-RAIL','D3-RDI','D4-TD','CS-PSP'}
GREY={'CI-IND','D2-RAIL','D4-TD'}
cp=ndi.binary_dilation(cpsp,disk(6))
# strict pass
best=np.zeros((H,W),np.uint8); bd=np.full((H,W),999,np.int16)
for i,z in enumerate(ZONES):
    if z in('CS-PK','CS-FW'): continue
    d=np.abs(p2-np.array(cols[z])).max(2)
    if z in SMART: d=np.where(cp,d,999)
    m=d<bd; bd[m]=d[m]; best[m]=i+1
strict=np.where((bd<=7)&city,best,0).astype(np.uint8)
# mix pass on remaining city pixels: p ~ t*c+(1-t)*g, g in {parcel-line grey, white}
white=(p2.min(2)>=244)
nearwhite=ndi.binary_dilation(white,disk(1))|ndi.binary_dilation(white,np.ones((3,3),bool))
ys,xs=np.where(city&(strict==0)&~nearwhite)
P=p2[ys,xs].astype(np.float32)
incp=cp[ys,xs]
bres=np.full(len(P),1e9,np.float32); bz=np.zeros(len(P),np.uint8)
for g in (np.array([110,110,110],np.float32),):
    for i,z in enumerate(ZONES):
        if z in('CS-PK','CS-FW') or z in GREY: continue
        c=np.array(cols[z],np.float32); v=c-g; vv=float(v@v)
        if vv<60*60: continue
        t=((P-g)@v)/vv
        res=np.linalg.norm(P-g-np.outer(t,v),axis=1)
        ok=(t>=0.4)&(t<=1.05)
        if z in SMART: ok&=incp
        res=np.where(ok,res+(1-np.clip(t,0,1))*6,1e9)
        m=res<bres; bres[m]=res[m]; bz[m]=i+1
mix=np.zeros((H,W),np.uint8)
good=bres<=13
mix[ys[good],xs[good]]=bz[good]
print('strict px',int((strict>0).sum()),'mix px',int((mix>0).sum()))
cls=np.where(strict>0,strict,mix)
for z,r in (('CI-IND',3),('D2-RAIL',3),('D4-TD',2)):
    i=ZONES.index(z)+1; m=cls==i
    cls[m&~ndi.binary_opening(m,disk(r))]=0
i=ZONES.index('P-FW')+1; m=cls==i
cls[m&~ndi.binary_opening(m,np.ones((3,3),bool))]=0
# drop specks
out=np.zeros_like(cls)
for i in range(1,len(ZONES)+1):
    m=cls==i
    if not m.any(): continue
    lab,n=ndi.label(m,structure=np.ones((3,3)))
    sz=ndi.sum(m,lab,range(1,n+1))
    out[np.isin(lab,np.where(sz>=10)[0]+1)]=i
cls=out
# strict seeds win in a 3x3 majority-ish cleanup: mixed pixels adopt nearest strict class if within 2px and different
# fill parcel lines / gaps
dist,(iy,ix)=ndi.distance_transform_edt(cls==0,return_indices=True)
fill=(cls==0)&city&((dist<=2.6)|((dist<=9)&~ndi.binary_dilation(p2.min(2)>=240,disk(1))&(p2.max(2)>=60)))
cls2=cls.copy(); cls2[fill]=cls[iy[fill],ix[fill]]
pk=ZONES.index('P-PK')+1; fw=ZONES.index('P-FW')+1
cls2[(cls2==pk)&cpsp]=ZONES.index('CS-PK')+1
cls2[(cls2==fw)&cpsp]=ZONES.index('CS-FW')+1
np.save('cls_full.npy',cls2)
tot=int((cls2>0).sum())
stats={z:int((cls2==i+1).sum()) for i,z in enumerate(ZONES)}
json.dump(stats,open('stats.json','w'))
print('zoned share of city',tot/city.sum())
print({z:round(100*v/tot,1) for z,v in stats.items()})
bits=np.zeros((H,W),np.uint8)
for b,k in enumerate(['m100','m500','mh','ms','mf','mt']):
    bits|=(ov[k]&city).astype(np.uint8)<<b
bits[(bits&1>0)&(bits&2>0)]&=np.uint8(255-2)
def ds(a):
    b=a[0::2,0::2].copy()
    for dy,dx in((0,1),(1,0),(1,1)):
        c=a[dy::2,dx::2]; m=b==0; b[m]=c[m]
    return b
g=ds(cls2); ob=bits[0::2,0::2]
grid=np.zeros(g.shape+(3,),np.uint8); grid[...,0]=g*6; grid[...,1]=ob*4
Image.fromarray(grid).save('grid.png',optimize=True)
# ---------- base image ----------
base=p2.astype(np.uint8).copy()
cd=ndi.binary_dilation(city,disk(7))
outm=~cd
sat=(base.max(2).astype(int)-base.min(2))
neutral=sat<14
gch=base[...,1].astype(np.float32)
small=gch[::8,::8]
bg=ndi.median_filter(small,size=25)
bg=np.kron(bg,np.ones((8,8),np.float32))[:H,:W]
lv=np.full((H,W),239,np.uint8)
lv[(gch-bg)>=5]=252
lv[(gch-bg)<=-6]=229
furnrect=np.zeros((H,W),bool); furnrect[725:2075,0:870]=True; furnrect[2075:H,0:900]=True; furnrect[0:700,2380:W]=True; furnrect[:,3270:]=True; furnrect[2480:,:1500]=True
lv[furnrect]=239
dark=ndi.binary_dilation(neutral&(gch<200),disk(3))
lv[dark]=239
m=outm&(neutral|furnrect)
for c in range(3): base[...,c][m]=lv[m]
# coloured furniture remnants inside furniture rects (legend swatches)
m2=outm&furnrect
base[m2]=239
Image.fromarray(base).save('base_f2.png')
Image.fromarray(base).resize((1100,850)).save('render/base_small.png')
pal=np.zeros((38,3),np.uint8); pal[0]=(255,255,255)
for i,z in enumerate(ZONES): pal[i+1]=cols[z]
rec=pal[cls2]; orig=p2.astype(np.uint8)
for nm,(x0,y0,w,h) in {'verify':(1250,1250,750,600),'verify2':(2000,900,750,600)}.items():
    c=Image.new('RGB',(w*2+10,h),(0,0,0)); c.paste(Image.fromarray(orig[y0:y0+h,x0:x0+w]),(0,0)); c.paste(Image.fromarray(rec[y0:y0+h,x0:x0+w]),(w+10,0)); c.save(f'render/{nm}.png')
