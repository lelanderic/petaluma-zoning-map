import numpy as np, sys, json
sys.path.insert(0,'gis'); import geo
S,DX,DY=11.65,6,-4
st={n:geo.topx(P,S,DX,DY) for n,P in geo.load()}
def snap(name,target=None,frac=None):
    q=st[name]; seg=np.diff(q,axis=0); L=np.hypot(seg[:,0],seg[:,1])
    if target is not None:
        best=None
        for i,(a,v,l) in enumerate(zip(q[:-1],seg,L)):
            t=np.clip(((np.array(target)-a)@v)/(l*l),0.1,0.9); p=a+t*v; d=np.hypot(*(p-target))
            if best is None or d<best[0]: best=(d,p,v)
        d,p,v=best
    else:
        c=np.cumsum(L); s=frac*c[-1]; i=int(np.searchsorted(c,s)); prev=c[i-1] if i else 0
        t=(s-prev)/L[i]; p=q[i]+t*seg[i]; v=seg[i]; d=0
    a=np.degrees(np.arctan2(v[1],v[0]))
    if a>90: a-=180
    if a<-90: a+=180
    return round(float(p[0])),round(float(p[1])),round(float(a),1),round(float(d))
spec=[('E Washington St',(1697,1320),None,1),('E Washington St',(1925,1008),None,0),('N McDowell Blvd',(1330,754),None,0),('S McDowell Blvd',(2150,1340),None,1),
('Sonoma Mountain Pkwy',(1720,681),None,1),('Ely Blvd S',(2330,1118),None,0),('Lakeville Hwy',(2530,1588),None,0),('Petaluma Blvd N',(1385,1285),None,0),('Petaluma Blvd N',(1000,820),None,2),
('Petaluma Blvd S',(1680,1696),None,1),('D St',(1490,1811),None,1),('Western Ave',(1290,1676),None,2),('Bodega Ave',(1165,1581),None,2),('Lakeville St',(1668,1510),None,2),
('Payran St',(1775,1415),None,2),('Casa Grande Rd',(2490,1428),None,2),('Frates Rd',(2656,1544),None,2),('Old Redwood Hwy',(781,262),None,2),
('Caulfield Ln',None,0.5,2),('Corona Rd',None,0.42,2),('Rainier Ave',None,0.55,2),('Magnolia Ave',None,0.18,2)]
out=[]
for n,tg,fr,lvl in spec:
    x,y,a,d=snap(n,tg,fr); print(f'{n:22s} {x:5d} {y:5d} {a:6.1f}  moved {d}px')
    out.append(dict(t=n,x=x,y=y,a=a,lvl=lvl))
for tg,lvl in (((1085,707),1),((1503,994),0),((1953,1417),0),((640,290),1)):
    x,y,a,d=snap('US-101',tg); print('101',x,y,'moved',d); out.append(dict(t='101',x=x,y=y,kind='shield',lvl=lvl))
mile=5280/S
out+= [dict(t="Petaluma River",x=1010,y=790,a=36,kind="water",lvl=1),dict(t="Petaluma River",x=2780,y=2215,a=42,kind="water",lvl=0),
 dict(t="Downtown",x=1405,y=1612,kind="place",lvl=1),dict(t="Fairgrounds",x=1800,y=1345,kind="place",lvl=2),
 dict(t="0",x=560,y=2392,kind="scale",lvl=0),dict(t="1 mile",x=round(560+mile),y=2392,kind="scale",lvl=0),dict(t="N",x=500,y=2400,kind="north",lvl=0)]
json.dump(dict(labels=out,mile=mile),open('gis/labels.json','w'))
print('mile px',mile)
