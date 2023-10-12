## Flow problem.

We have a *flow graph*, i.e. 

- A directed graph G = (V,E)
- where each edge e has nonnegative weight c(e) (also called capacity)
- and two nodes s, d in V (s =/= v) s.t. s has no *incoming* edges (e s.t. omega(e) = s) and v has no *outgoing* edges (e s.t. alpha(e) = d). We call them the source node s and the sink/destination/exit node d.

Note that if we pick a node s as our source but there are any incoming edges into s, we can always append a new node s' with one arrow from s' into s, which will make the problem equivalent but also make the network satisfy our definition (the same goes for extending d to d').

A *flow* is a function f : E -> R assigning to every edge e a nonnegative real number f(e) that satisfies 0 <= f(e) <= c(e) and for every vertex v except s, d, we have sum(f(e) : e incoming in v) = sum(f(e) : f outgoing from v).

A *maximum flow* is a flow *f* s.t. sum(f(e) : e outgoing from s) is maximum, or equivalently s.t. sum(f(e) : e incoming to d) is maximum.

Like with many graph problems, we can formulate this as an LP-problem:

Let A be the *incidence matrix* of the graph, i.e. We label all edges e_1 to e_m, m = |E| and all vertices except s and d: v_1 to v_n, n = |V| - 2. Then A is the matrix of n rows and m columns where entry `Aij = {-1 if e_j = (v_i, _), 1 if e_j = (_, v_i), 0 otherwise}`, and we see that a vector f in R^m can be a flow (where f(e_i) = f_i) if and only if Af = 0 (i.e. iff. the in-flow of every non-terminal vertex is equal to the out-flow) and 0 <= f_i <= c(e_i) for all i. 

This gives linear constraints on the flow vector f, and we can also see that the function to be optimized is `sum ({-1 if s = (v_i, _), 1 if s = (_, v_i), 0 otherwise} * f_i : i = 0, ... , m)`, which is in fact the incidence row of s (not included in the matrix A). We could equivalently have picked the incidence row of d (also not included in A). This is the total flow out of s (or into d) and thus the function that needs to be optimized.

However, solving as an LP problem (using the simplex algorithm) ignores the unique structure of the problem. There exists a specific algorithm that can exploit this structure and thus solve the max-flow problem more efficiently than raw linear programming would do.

## Flow-augmenting chains

We will now use the notation as described above, numbering all nodes unequal to s or d from 1 to m = |V| - 2. But we will number the edges according to the nodes they connect, i.e. we will label e = (v_i, v_j) as e_ij. A flow is a vector R^n that assigns to every edge in the network a flow along that edge (satisfying the flow constraints). We will index x at (v_i, v_j) as x_ij. This is poor notation because not for all i and j there is an edge connecting v_i and v_j, but it is convenient for our future purposes.

A *flow-augmenting chain* (or flow-augmenting path) for a given flow x in R^n, is an <u>undirected </u> (!) path through the graph which has

x_ij < c_ij for all forward arrows in the chain
x_ij > 0 for all backward arrows in the chain

We see that we can easily increase the total flow by a maximum a = min{ min (c_ij - x_ij : ij forward the path), min (x_ij : ij backward in the path )} without violating the flow constraints: by increasing the flow along all forward arrows with a and decreasing the flow along all backward arrows with a, we will obtain a new vector which by the choice of a satisfies the capacity constraints, and by the fact that every node in the path 

- either has a forward arrow entering and a forward arrow leaving => in which case the netto flow will be augmented with +a -a = 0
- or a backward arrow entering and a backward arrow leaving => in which case the netto flow will be augmented with -a +a = 0
- or a backward arrow entering and a forward arrow entering: in which case the netto flow will be augmented with -a +a = 0
- or a forward arrow leaving and a backward arrow leaving: in which case the netto flow will be augmented with -a +a = 0

So in all cases, the augmented flow will satisfy *conservation* and *capacity*, and we will have improved the flow.

## No augmenting path => local optimality => global optimality ?

The difficult part is now to prove that if we cannot augment the flow any further, we must have reached a global maximum flow.

But it is not even formally clear yet that the nonexistence of a flow-augmenting path implies the flow being a local maximum.




## Searching for Augmenting paths