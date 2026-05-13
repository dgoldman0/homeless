import json, math, importlib.util
import jax, jax.numpy as jnp
jax.config.update('jax_enable_x64', True)

spec=importlib.util.spec_from_file_location('rtest','/mnt/data/composite_r_flare_gate_tests.py')
rtest=importlib.util.module_from_spec(spec); spec.loader.exec_module(rtest)
_ = rtest.raw_one(jnp.array([0.0,0.0,math.pi/2,0.0], dtype=jnp.float64), rtest.make_p())

rows=[]
for V,lam in [(5.0,None),(10.0,None),(5.0,3.0),(10.0,6.0)]:
    base=rtest.scan_variant('baseline', rtest.make_p(V=V,lam=lam))
    def add(label, **kw):
        p=rtest.make_p(V=V,lam=lam,**kw)
        out=rtest.scan_variant(label,p)
        for metric in ['packet_boundary_maxabs_tidal_angular','packet_boundary_maxabs_tidal_radial','packet_boundary_maxabs_Kretsch','support_edge_maxabs_tidal_angular','support_edge_maxabs_Kretsch','support_edge_max_theta_prod']:
            denom=base[metric]
            out[metric+'_ratio_to_base']=out[metric]/denom if abs(denom)>1e-300 else float('nan')
        rows.append(out)
    add('slim_short_hold_Ropen_halfB_halfN', R_mode=1, hold_scale=0.35, eta_B=0.5, eta_N=0.5)
    add('very_slim_nohold_Ropen_noB_noN', R_mode=1, hold_scale=0.0, eta_B=0.0, eta_N=0.0)
    add('very_slim_plus_pbeta2', R_mode=1, hold_scale=0.0, eta_B=0.0, eta_N=0.0, p_beta=2.0)
    add('flat_very_slim_nohold_noB_noN', R_mode=2, hold_scale=0.0, eta_B=0.0, eta_N=0.0)
    add('baseline_plus_pbeta2', p_beta=2.0)
    # p_beta sweep under baseline and under late catch stress
    for pb in [1.0,1.25,1.5,2.0,3.0,4.0]:
        add(f'pbeta_sweep_{pb:g}', p_beta=pb)
    # Delayed catch + edge reinforcement: force catch to shift fade by changing hold? Need custom mutate p.
    # We mutate x_catch to x_beta or near x_beta in returned p array.
    for pb in [1.0,1.5,2.0,3.0,4.0]:
        p=rtest.make_p(V=V,lam=lam,p_beta=pb)
        pp=list(map(float,p))
        # indices: x_catch=9, x_beta=10, x_q=11, keep beta/q but delay catch to beta
        pp[9]=pp[10]
        out=rtest.scan_variant(f'latecatch_at_beta_pbeta_{pb:g}', jnp.array(pp,dtype=jnp.float64))
        for metric in ['packet_boundary_maxabs_tidal_angular','packet_boundary_maxabs_tidal_radial','packet_boundary_maxabs_Kretsch','support_edge_maxabs_tidal_angular','support_edge_maxabs_Kretsch','support_edge_max_theta_prod']:
            denom=base[metric]
            out[metric+'_ratio_to_base']=out[metric]/denom if abs(denom)>1e-300 else float('nan')
        rows.append(out)

with open('/mnt/data/composite_extra_slim_and_edge_tests.json','w') as f: json.dump(rows,f,indent=2)
# markdown
bykey={}
for r in rows: bykey.setdefault((r['V'],r['lam']),[]).append(r)
with open('/mnt/data/composite_extra_slim_and_edge_tests.md','w') as f:
    f.write('# Extra composite slim-architecture and edge-gating tests\n\n')
    f.write('Small add-on screen focused on whether multiple relaxations combine safely, and whether stronger W^p_beta edge shift gating rescues late-catch failures.\n\n')
    for key,rr in sorted(bykey.items()):
        V,lam=key
        f.write(f'## V={V:g}, lambda={lam:g}\n\n')
        f.write('| variant | packet fail | passive gtt fail | packet max norm | edge max gtt | packet angular tidal ×base | edge angular tidal ×base | edge theta-prod ×base |\n')
        f.write('|---|---:|---:|---:|---:|---:|---:|---:|\n')
        for r in rr:
            if not (r['label'].startswith('pbeta_sweep') or r['label'].startswith('latecatch') or r['label'] in ['slim_short_hold_Ropen_halfB_halfN','very_slim_nohold_Ropen_noB_noN','very_slim_plus_pbeta2','flat_very_slim_nohold_noB_noN','baseline_plus_pbeta2']):
                continue
            f.write(f"| {r['label']} | {int(r['hard_packet_fail'])} | {int(r['passive_gtt_fail'])} | {r['packet_max_norm']:.3g} | {r['edge_max_gtt']:.3g} | {r['packet_boundary_maxabs_tidal_angular_ratio_to_base']:.3g} | {r['support_edge_maxabs_tidal_angular_ratio_to_base']:.3g} | {r['support_edge_max_theta_prod_ratio_to_base']:.3g} |\n")
        f.write('\n')
print('/mnt/data/composite_extra_slim_and_edge_tests.md')
