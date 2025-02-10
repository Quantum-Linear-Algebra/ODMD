This repository will contain all the code to run observable dynamic mode decomposition (ODMD) algorithm as specified in https://arxiv.org/pdf/2306.01858

General Algorithm Overview
Input: time step $\Delta t$, noise threshold $\tilde{\delta}$
Output: estimated energy $\tilde{E_0}$

$k \leftarrow 0$

**while**  $\tilde{E_0}$ not converged **do**
    $s_k \leftarrow Rs(k\Delta t), 0 \le k \le K+1$
    $o_{t_k,d} \leftarrow$ 
    $$
    \begin{bmatrix}
        s_0 \\
        s_1 \\
        \vdots \\
        s_k
    \end{bmatrix} $$
    $$
    \textbf{X}_{k_1:k_2} \leftarrow
    \begin{bmatrix}
        o_{t_{k_1},d}\\
        o_{t_{k_1+1},d}\\
        \dots \\
        o_{t_{k_2},d}
    \end{bmatrix} $$
    $\textbf{X}, \textbf{X}' \in \mathbb{C}^{d\times(K+1)}, d = \lfloor\alpha(K+1)\rfloor$
    $\textbf{X} \leftarrow \textbf{X}_{0,K} = \sum_{l=0}^{d-1} \sigma_l\textbf{u}_l\textbf{v}_l^\dagger$ (SVD)
    $\textbf{X}' \leftarrow \textbf{X}_{1,K+1}$
    $\textbf{X}_\tilde{\delta} \leftarrow \sum_{l:\sigma_l>\tilde{\delta}\sigma_{\text{max}}} \sigma_l\textbf{u}_l\textbf{v}_l^\dagger, \sigma_{\text{max}} = \max_l\sigma_l$
    $A \leftarrow \textbf{X}'\left(\textbf{X}_\tilde{\delta} \right)^+$ (pseudoinverse)
    Solve for $\tilde{\lambda}$ using $A\textbf{\Psi}_l = \tilde{\lambda}_l\textbf{\Psi}_l$
    $\tilde{E}_0\Delta t \leftarrow - \max_{1\le l \le d_kk} I \log\left(\tilde{\lambda}_l\right)$
    $k \leftarrow k+1$

Todo:
1. Generate Samples Using Real Hadamard Test
    1. Create Operator for a System (most likely TFIM)
    2. Create Circuit with all timesteps ($d \le d_* \le 2N+1$)
    3. Store results in a convient manner that represents statevector manifold ($s_k$)
2. Create code to create and optimize **X** matrices
3. Create code to solve eigenvalue problem using system matrix A
4. Create code to calculate energy