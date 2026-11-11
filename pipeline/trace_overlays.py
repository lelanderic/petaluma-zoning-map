import numpy as np
from PIL import Image
from scipy import ndimage as ndi
from collections import Counter
p3=np.array(Image.open('full-3.png')).astype(np.int16)
H,W,_=p3.shape
city=np.load('city.npy')
def disk(r):
    y,x=np.ogrid[-r:r+1,-r:r+1]; return x*x+y*y<=r*r
furn=np.zeros((H,W),bool); furn[680:2020,0:850]=True; furn[2070:H,0:900]=True; furn[0:520,2350:W]=True
R,G,B=p3[...,0],p3[...,1],p3[...,2]
def near(c,t): return (np.abs(p3-np.array(c)).max(2)<=t)&~furn
f100=near((112,160,232),22)
f500=near((124,240,210),28)
hist=near((0,34,112),30)
brown=(R>G+25)&(G>B+15)&(R>100)&(R<220)&~furn
c=Counter(map(tuple,(p3[brown]//8*8))); print('brown',[(tuple(int(v) for v in k),n) for k,n in c.most_common(5)], brown.sum())
gdot=near((36,110,6),30)
print({k:int(v.sum()) for k,v in dict(f100=f100,f500=f500,hist=hist,gdot=gdot).items()})
# region masks
m100=ndi.binary_opening(ndi.binary_closing(f100,disk(7)),disk(3))
m500=ndi.binary_opening(ndi.binary_closing(f500,disk(7)),disk(3))
def fill(mask,r=2):
    d=ndi.binary_dilation(mask,disk(r)); f=ndi.binary_fill_holes(d); return ndi.binary_erosion(f,disk(r))|mask
mh=fill(hist)
ms=fill(ndi.binary_closing(brown,disk(3)))
lab,n=ndi.label(ms); sz=ndi.sum(ms,lab,range(1,n+1)); ms=np.isin(lab,[i+1 for i,s in enumerate(sz) if s>1500]); print('smh comps',[int(s) for s in sz if s>1500])
lab,n=ndi.label(mh); sz=ndi.sum(mh,lab,range(1,n+1)); print('hist comps',[int(s) for s in sz if s>300]); mh=np.isin(lab,[i+1 for i,s in enumerate(sz) if s>300])
# fairgrounds: dark grey outline (60-90) thick, component containing green dots
dg=(p3.max(2)<95)&(p3.max(2)>50)&((p3.max(2)-p3.min(2))<12)
dg=ndi.binary_opening(dg,disk(1))
lab,n=ndi.label(ndi.binary_dilation(dg,disk(1)))
ys,xs=np.where(gdot); print('gdot bbox',xs.min(),xs.max(),ys.min(),ys.max())
sub=np.zeros((H,W),bool); sub[ys.min()-80:ys.max()+80, xs.min()-80:xs.max()+80]=True
ids=Counter(lab[sub&(lab>0)]).most_common(3); print('fair ids',ids)
fo=lab==ids[0][0]
mf=ndi.binary_fill_holes(fo)
print('fair area',mf.sum())
# T6-O: black outline within CPSP that is not the dashed boundary: black comps inside city interior
blk=(p3.max(2)<45)
sub=np.zeros((H,W),bool); sub[1440:1580,1540:1660]=True
lab,n=ndi.label(blk&sub); sz=ndi.sum(blk&sub,lab,range(1,n+1)); print('t6o comps',[int(s) for s in sz])
to=np.isin(lab,[i+1 for i,s in enumerate(sz) if s>200])
mt=ndi.binary_fill_holes(ndi.binary_dilation(to,disk(1)))
print('t6o area',mt.sum())
np.savez_compressed('ov.npz',m100=m100,m500=m500,mh=mh,ms=ms,mf=mf,mt=mt,f100=f100,f500=f500,hist=hist,brown=brown,gdot=gdot,fo=fo,to=to)
vis=np.full((H,W,3),255,np.uint8)
vis[city]=[235,235,235]
vis[m500]=[150,235,215]; vis[m100]=[130,170,235]; vis[mh]=[60,80,160]; vis[ms]=[170,120,60]; vis[mf]=[60,140,40]; vis[mt]=[0,0,0]
Image.fromarray(vis).resize((1100,850)).save('render/ov.png')
