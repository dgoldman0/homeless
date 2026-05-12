# Model Equations Used in the Branch Screen

Metric:

```math
ds^2=-dt^2+B(l,t)^2dl^2+R(l,t)^2d\Omega^2.
```

B actuator:

```math
B(l,t)=1+(B_0-1)F_B(l)A_B(t),
\qquad F_B(l)=\exp[-(|l|/w_B)^4].
```

Access areal profile:

```math
R_{\rm access}(l)=\sqrt{1+l^2}.
```

Standby profile:

```math
R_{\rm standby}(l)=R_{\rm access}(l)+W_R(l)(R_c-R_{\rm access}(l)),
\qquad W_R(l)=\exp[-(|l|/w_R)^4].
```

R schedule:

```math
R(l,t)=R_{\rm standby}(l)+A_R(t)(R_{\rm access}(l)-R_{\rm standby}(l)).
```

For the branch test, `A_B` and `A_R` are minimum-jerk ramps. The main ordering is:

```math
B\text{-setup}\rightarrow R\text{-open}\rightarrow\text{hold}\rightarrow R\text{-close}\rightarrow B\text{-reset}.
```

The source-history score is:

```math
I^-_{\rm core}=\int[-T^{\rm min}_{kk}(l=0,t)]_+dt.
```
