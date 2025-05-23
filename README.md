This repository will contain all the code to run observable dynamic mode decomposition (ODMD) algorithm as specified in https://arxiv.org/pdf/2306.01858

General Algorithm Overview
Input: time step $\Delta t$, noise threshold $\tilde{\delta}$
Output: estimated energy $\tilde{E}_0$

$k \leftarrow 0$

**while**  $\tilde{E_0}$ not converged **do**
> $s_k \leftarrow Re(s(k\Delta t)), 0 \le k \le K+1$
>
> $o_{t_k,d} \leftarrow \left[s_k  s_{k+1}  \cdots  s_{k+d-1}\right]^T$
>
> $X_{k_1:k_2} \leftarrow \left[o_{t_{k_1},d}  o_{t_{k_1+1},d}  \cdots  o_{t_{k_2},d}\right]$
> 
> $X, X' \in \mathbb{C}^{d\times(K+1)}, d = \lfloor\alpha(K+1)\rfloor$
> 
> $X \leftarrow X_{0,K} = \sum_{l=0}^{d-1} \sigma_lu_lv_l^\dagger$ (SVD)
> 
> $X' \leftarrow X_{1,K+1}$
> 
> $X_\tilde{\delta} \leftarrow \sum_{l:\sigma_l>\tilde{\delta}\sigma_{\text{max}}} \sigma_lu_lv_l^\dagger, \sigma_{\text{max}} = \max_l\sigma_l$
> 
> $A \leftarrow X'\left(X_\tilde{\delta} \right)^+$ (pseudoinverse)
> 
> Solve for all $\tilde{\lambda}_l$ using $A{\Psi}_l = \tilde{\lambda}_l{\Psi}_l$
> 
> $\tilde{E}_0 \Delta t \leftarrow -\max Im(\log(\tilde{\lambda}_l), 1\le l \le d_k$
> 
> $k \leftarrow k+1$\

Todo:
1. Generate Samples Using Real Hadamard Test
    1. Create Operator for a System (most likely TFIM)
    2. Create Circuit with all timesteps ($d \le d_* \le 2N+1$)
    3. Store results in a convient manner that represents statevector manifold ($s_k$)
2. Create code to create and optimize X matrices
3. Create code to solve eigenvalue problem using system matrix A
4. Create code to calculate energy
