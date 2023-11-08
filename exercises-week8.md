### Ex. 1
a)

For a recurrence relation $T(n) = cT(n-1) + d, n>0, T(0) = 1$, we can do a few steps to see how it behaves:
$$
T(0) = 1 \\
T(1) = c + d \\
T(2) = c(c+d) + d \\
T(3) = c(c(c+d)+d)+d \\
T(n) = c^n + \sum_{m=0}^{n-1}c^n\cdot d
$$
By the geometric formula (which I will not reprove here, since, come on, we are second years now):
$$
\sum_{m=0}^{n-1}c^n = \frac{c^n-1}{c-1}
$$
Which holds for any $c>0$. So we have in general:
$$
T(n) = c^n + d(c^n-1) = (d+1)c^n-d
$$
Hence 
$$
T_A(n) = 38\cdot 2^n - 37 \\
T_B(n) = 43\cdot 3^n - 42
$$

Hence $T_A \in \Theta(2^n)$, $T_B \in \Theta(3^n)$, because $2^n < 38\cdot  2^n - 37 < 38\cdot 2^n$ for $n$ sufficiently large, and $T_B \in \Theta(3^n)$, because $3^n < 43\cdot 3^n - 42 < 43\cdot 3^n$ for $n$ sufficiently large.

Also, we have $\Theta(2^n) \subset O(3^n)$, but not $\Theta(3^n)\subset O(2^n)$, since if there are $n_0$ and $c$ such that $$3^n \leq c\cdot 2^n \text{ for } n> n_0$$, that would imply:
$$
c \geq (\frac32)^n \text{ for all }n >n_0
$$ 
, but the right hand side will eventually grow bigger than any $c$ for $n$ sufficiently large, so that gives the required contradition..
