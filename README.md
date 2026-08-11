# Portfolio Optimizer
A short Python project implementing mean-variance portfolio optimization from first principles using a custom matrix library.

## Overview
The purpose of this project is to:
- Calculate portfolio expected return
- Calculate portfolio variance and volatility
- Find the global minimum-variance portfolio
- Find the minimum-variance portfolio for a specified target return
- Generate the minimum-variance/efficient frontier

## Mathematical Background
The mathematical foundation of this project is based on the following mathematical results:

### Expected Portfolio Return
$$E(R_p) = \vec{w}^T\vec{\mu}$$
where:
- $\vec{w}$ is the vector of weights assigned to each asset in the portfolio:

$$\vec{w} = \begin{bmatrix}
\vec{w_1} \\
\vec{w_2} \\
\vdots \\
\vec{w_n}
\end{bmatrix}
$$

where $w_i$ is the weight assigned to the $i$-th asset

- $\vec{\mu}$ is the vector of expected asset returns:

$$\vec{\mu} = \begin{bmatrix}
E(R_1) \\
E(R_2) \\
\vdots \\
E(R_n)
\end{bmatrix}
$$

where $E(R_i)$ is the expected return on the $i$-th asset

### Portfolio Variance
$$\operatorname{Var}(R_p) = \vec{w}^T\Sigma\,\vec{w}$$
where:
- $\vec{w}$ is the vector of weights assigned to each asset in the portfolio
- $\Sigma$ is the covariance matrix

If we have $n$ assets, the Covariance matrix is a $n \times n$ matrix whose $(i, j)^{th}$ entry is the Covariance between the returns of assets $i$ and $j$:

$$ \Sigma_{ij} = \operatorname{Cov}(R_i, R_j)$$
where $R_k$ is the return on the $k^{th}$ asset  

### Optimization

This projects contains two functions to find the optimal weights: 

1) optimal_weights

this function takes the Covariance matrix as an input and outputs the weight vector $\vec{w}^*$. The weight vector can be found by minimising the portfolio variance subject to the constraint that the weights assigned to each asset all add up to 1:

$$
\min_w \; \vec{w}^T\Sigma\,\vec{w}
\qquad \text{subject to} \qquad
\vec{1}^T \vec{w} = 1
$$

where $\vec{1}$ is a vector of ones with the same dimension as $\vec{w}$.

The solution for this problem can be found using a Lagrange Multiplier method.

Using a Lagrange multiplier $\lambda$, define the Lagrangian:

$$
L(\vec{w},\lambda)
=
\vec{w}^{\,T}\Sigma\vec{w}
-
\lambda(\vec{1}^{\,T}\vec{w}-1)
$$

Setting the derivative with respect to $\vec{w}$ equal to zero gives the first-order condition:

$$
\frac{\partial L}{\partial \vec{w}}
=
2\Sigma\vec{w}-\lambda\vec{1}
=
0
$$

Rearranging and multiplying by $\Sigma^{-1}$ gives:

$$
\vec{w}
=
\frac{\lambda}{2}\Sigma^{-1}\vec{1}
$$

We can determine $\lambda$ by applying the constraint $\vec{1}^{\,T}\vec{w}=1$:

$$
\vec{1}^{\,T}
\left(
\frac{\lambda}{2}\Sigma^{-1}\vec{1}
\right)
=1
$$

which gives:

$$
\lambda
=
\frac{2}
{\vec{1}^{\,T}\Sigma^{-1}\vec{1}}
$$

Substituting this back into the expression for $\vec{w}$ gives the global minimum-variance portfolio weights:

$$
\boxed{
\vec{w}^{\,*}
=
\frac{\Sigma^{-1}\vec{1}}
{\vec{1}^{\,T}\Sigma^{-1}\vec{1}}
}
$$

This expression is independent of the Lagrange multiplier, so it can be directly implemented using the matrix operations provided by the custom matrix library.

2) optimal_weights_for_return

A more general optimization problem is to minimize portfolio variance while
requiring the portfolio to achieve a specified target expected return $r$:

$$
\min_{\vec{w}} \; \vec{w}^{\,T}\Sigma\vec{w}
\qquad \text{subject to} \qquad
\vec{1}^{\,T}\vec{w}=1,
\qquad
\vec{\mu}^{\,T}\vec{w}=r
$$

The first constraint makes sure that all portfolio weights sum to one, while the second requires the portfolio to have an expected return of $r$.

Using two Lagrange multipliers, $\lambda_1$ and $\lambda_2$, the Lagrangian is:

$$
L(\vec{w},\lambda_1,\lambda_2)
=
\vec{w}^{\,T}\Sigma\vec{w}
-
\lambda_1(\vec{1}^{\,T}\vec{w}-1)
-
\lambda_2(\vec{\mu}^{\,T}\vec{w}-r)
$$

Setting the derivative with respect to $\vec{w}$ equal to zero gives:

$$
2\Sigma\vec{w}
-
\lambda_1\vec{1}
-
\lambda_2\vec{\mu}
=
0
$$

Rearranging and multiplying by $\Sigma^{-1}$ gives:

$$
\vec{w}
=
\frac{\lambda_1}{2}\Sigma^{-1}\vec{1}
+
\frac{\lambda_2}{2}\Sigma^{-1}\vec{\mu}
$$

Substituting this expression into the two constraints produces a system of equations in $\lambda_1$ and $\lambda_2$:

$$
\begin{bmatrix}
\vec{1}^{\,T}\Sigma^{-1}\vec{1}
&
\vec{1}^{\,T}\Sigma^{-1}\vec{\mu}
\\
\vec{\mu}^{\,T}\Sigma^{-1}\vec{1}
&
\vec{\mu}^{\,T}\Sigma^{-1}\vec{\mu}
\end{bmatrix}
\begin{bmatrix}
\lambda_1 \\
\lambda_2
\end{bmatrix}
=
\begin{bmatrix}
2 \\
2r
\end{bmatrix}
$$

The coefficients of this system are calculated using matrix operations and
the system is solved using the custom linear system solver.

Once $\lambda_1$ and $\lambda_2$ have been obtained, they are substituted
back into

$$
\boxed{
\vec{w}
=
\frac{\lambda_1}{2}\Sigma^{-1}\vec{1}
+
\frac{\lambda_2}{2}\Sigma^{-1}\vec{\mu}
}
$$

to obtain the minimum-variance portfolio for the specified target return.