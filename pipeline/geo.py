import numpy as np, glob, sys
S=11.6386; X0,Y0=6365751.8,1865556.9; PX0,PY0=448,62
def load():
    segs=[]
    for f in sorted(glob.glob('gis/*.txt')):
        for ln in open(f):
            ln=ln.strip()
            if ';' not in ln: continue
            name,pts=ln.split(';',1)
            try: p=[tuple(float(v) for v in q.split(',')) for q in pts.split()]
            except: print('bad',ln); continue
            segs.append((name.strip(),np.array(p)))
    return segs
def topx(P,s=S,dx=0,dy=0):
    return np.c_[PX0+(P[:,0]-X0)/s+dx, PY0+(Y0-P[:,1])/s+dy]
def sample(segs,step=4):
    out=[]
    for n,P in segs:
        for a,b in zip(P[:-1],P[1:]):
            L=np.hypot(*(b-a)); k=max(2,int(L/11.6/step))
            for t in np.linspace(0,1,k): out.append(a+(b-a)*t)
    return np.array(out)
if __name__=='__main__':
    dt=np.load('dt.npy'); segs=load(); pts=sample(segs)
    best=None
    for s in np.arange(11.50,11.80,0.02):
        for dx in range(-14,15,2):
            for dy in range(-14,15,2):
                q=topx(pts,s,dx,dy).round().astype(int)
                ok=(q[:,0]>=0)&(q[:,0]<3300)&(q[:,1]>=0)&(q[:,1]<2550)
                sc=(dt[q[ok,1],q[ok,0]]>=1.5).mean()
                if best is None or sc>best[0]: best=(sc,s,dx,dy)
    print('best on-street share, scale, dx, dy:',best)
    q=topx(pts).round().astype(int); ok=(q[:,0]>=0)&(q[:,0]<3300)&(q[:,1]>=0)&(q[:,1]<2550)
    print('default share',(dt[q[ok,1],q[ok,0]]>=1.5).mean(), len(pts))
