import math, json, time
import numpy as np
import jax
jax.config.update('jax_enable_x64', True)
import jax.numpy as jnp

def make_params(C0=10.0, Delta=0.3, Rmid=0.5, r0=1.0, V=0.0, L0=0.0, eps=1e-5):
    return jnp.array([float(C0), float(Delta), float(Rmid), float(r0), float(V), float(L0), float(eps), float(Delta/6.0)], dtype=jnp.float64)

def scalars(x,p):
    C0,Delta,Rmid,r0,V,L0,eps,w=p
    t,l,th,ph=x
    L=L0+V*t
    rho=jnp.sqrt((l-L)**2+eps**2)
    # Use squared radius in the transition to avoid an artificial cusp at the shell center.
    S=0.5*(1.0-jnp.tanh((((l-L)**2) - Rmid**2)/(2.0*Rmid*w)))
    A=jnp.exp(S*jnp.log(C0))
    r=jnp.sqrt(r0**2+l**2)
    return S,A,r,rho

def metric(x,p):
    S,A,r,rho=scalars(x,p)
    V=p[4]; th=x[2]
    return jnp.array([
        [-1.0 + A*A*V*V*S*S, -A*A*V*S, 0.0, 0.0],
        [-A*A*V*S, A*A, 0.0, 0.0],
        [0.0, 0.0, A*A*r*r, 0.0],
        [0.0, 0.0, 0.0, A*A*r*r*jnp.sin(th)**2],
    ], dtype=jnp.float64)

def gamma(x,p):
    g=metric(x,p)
    dg=jax.jacfwd(metric, argnums=0)(x,p)  # dg[b,c,dcoord]
    ginv=jnp.linalg.inv(g)
    Gamma=(jnp.einsum('ad,cdb->abc',ginv,dg)+
           jnp.einsum('ad,bdc->abc',ginv,dg)-
           jnp.einsum('ad,bcd->abc',ginv,dg))*0.5
    return Gamma

def R_eff(x,p):
    S,A,r,rho=scalars(x,p)
    return A*r

def curvature_raw(x,p):
    g=metric(x,p)
    ginv=jnp.linalg.inv(g)
    Gam=gamma(x,p)
    dGam=jax.jacfwd(gamma, argnums=0)(x,p) # [a,b,c,coord]
    deriv=jnp.transpose(dGam,(0,2,3,1))-jnp.transpose(dGam,(0,2,1,3))
    prod1=jnp.einsum('ame,ens->asmn',Gam,Gam)
    prod2=jnp.einsum('ane,ems->asmn',Gam,Gam)
    Riem=deriv+prod1-prod2
    Ric=jnp.einsum('asan->sn', Riem)
    Rsc=jnp.einsum('ab,ab->', ginv, Ric)
    G=Ric-0.5*g*Rsc
    Rdown=jnp.einsum('pa,asmn->psmn',g,Riem)
    Ricci2=jnp.einsum('ab,cd,ac,bd->',Ric,Ric,ginv,ginv)
    Kretsch=jnp.einsum('abcd,efgh,ae,bf,cg,dh->',Rdown,Rdown,ginv,ginv,ginv,ginv)
    S,A,r,rho=scalars(x,p)
    V=p[4]
    nvec=jnp.array([1.0,V*S,0.0,0.0])
    kp=jnp.array([1.0,V*S+1.0/A,0.0,0.0])
    km=jnp.array([1.0,V*S-1.0/A,0.0,0.0])
    Gnn=jnp.einsum('a,b,ab->',nvec,nvec,G)
    Gkp=jnp.einsum('a,b,ab->',kp,kp,G)
    Gkm=jnp.einsum('a,b,ab->',km,km,G)
    dR=jax.grad(R_eff, argnums=0)(x,p)
    beta=-V*S
    theta_p=2/(A*r)*((dR[0]-beta*dR[1])+(1/A)*dR[1])
    theta_m=2/(A*r)*((dR[0]-beta*dR[1])-(1/A)*dR[1])
    det=jnp.linalg.det(g)
    gtt=g[0,0]
    return jnp.array([Rsc,Ricci2,Kretsch,Gnn,Gkp,Gkm,gtt,det,theta_p,theta_m,S,A,r,rho], dtype=jnp.float64)

curvature_one=jax.jit(curvature_raw)
curvature_grid=jax.jit(jax.vmap(curvature_raw, in_axes=(0,None)))

names=['R','Ricci2','Kretsch','Gnn','Gkp','Gkm','gtt','det','theta_p','theta_m','S','A','r','rho']

def scan_case(p, lmin=-1.5,lmax=1.5,N=121):
    ls=np.linspace(lmin,lmax,N)
    xs=jnp.array([[0.0,float(l),math.pi/2,0.0] for l in ls], dtype=jnp.float64)
    arr=np.array(curvature_grid(xs,p))
    summary={}
    for i,key in enumerate(names[:10]):
        a=arr[:,i]
        idx=int(np.nanargmax(np.abs(a)))
        summary['maxabs_'+key]=float(np.nanmax(np.abs(a)))
        summary['l_at_maxabs_'+key]=float(ls[idx])
        summary['min_'+key]=float(np.nanmin(a))
        summary['max_'+key]=float(np.nanmax(a))
    summary['min_det']=float(np.nanmin(arr[:,7]))
    summary['max_A']=float(np.nanmax(arr[:,11]))
    summary['min_gtt']=float(np.nanmin(arr[:,6])); summary['max_gtt']=float(np.nanmax(arr[:,6]))
    # throat scan: use cheap vectorized R_eff
    lfine=np.linspace(lmin,lmax,2001)
    xs2=jnp.array([[0.0,float(l),math.pi/2,0.0] for l in lfine], dtype=jnp.float64)
    Reff=np.array(jax.vmap(R_eff, in_axes=(0,None))(xs2,p))
    summary['throat_l_min_Reff']=float(lfine[int(np.argmin(Reff))])
    summary['throat_min_Reff']=float(np.min(Reff))
    prod=arr[:,8]*arr[:,9]
    summary['theta_product_min']=float(np.nanmin(prod)); summary['theta_product_max']=float(np.nanmax(prod))
    return summary

def main():
    # warm compile
    p=make_params()
    print('warmup')
    print(curvature_one(jnp.array([0.0,0.0,math.pi/2,0.0], dtype=jnp.float64), p))
    cases=[]
    # Focused sweep
    for C0 in [2,10,100,1e4]:
      for Delta in [1.0,0.3,0.1]:
        for V in [0.0,0.1,0.5]:
          for L0 in [0.0,0.5]:
            p=make_params(C0=C0,Delta=Delta,Rmid=0.5,r0=1.0,V=V,L0=L0)
            s=scan_case(p,N=121)
            s.update(C0=float(C0),Delta=float(Delta),V=float(V),L0=float(L0),Rmid=0.5,r0=1.0)
            cases.append(s)
            print(json.dumps({k:s[k] for k in ['C0','Delta','V','L0','maxabs_R','maxabs_Kretsch','min_Gkp','min_Gkm','max_gtt','throat_l_min_Reff','theta_product_max']}))
    with open('/mnt/data/ansatz_first_pass_results.json','w') as f: json.dump(cases,f,indent=2)

if __name__=='__main__':
    main()
