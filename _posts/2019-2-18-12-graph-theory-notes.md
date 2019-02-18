---
layout: post
title: graph theory notes
---

Below are the notes I'd taken from a week's worth of learning graph theory using both online resources and a book I'd bought named `Introduction to graph theory` by Richard Trudeau, which is an amazing book for idiots like me, since it manages an equilibrium between intuitive and managing to be somewhat rigorous.

Graph theory itself is the study of data structures, not the specific algorithms themselves per se, however the intrinsicities and, conversely, the broader details of certain structures such as spanning trees, bipartities, cycles, and in general any form of graph which has any special property. It limits itself to two primitive concepts, the edge(s) and the vert{ex}{ices}, the edges can be thought of as functions or interrelations between vertices, the vertices can be thought of as datum, or a significant point in a certain algorithm, e.g., the start and end point in a closed Hamiltonian walk; the edges themselves may come in various qualities and quantities, an edge may be directed, this sort of graph would be called a digraph (directed-graph), it may have a weight associated to it, e.g.: a cost of travelling across it, a length, or any sort of traversal cost, this graph would be called a weighted graph.
Graphs whose vertices have multiple edges adjacent to the same other adjacent vertex, is called a multigraph, relevant in scenarios where you are trying to derive a dual graph, wish to be able to cross an edge more than once (in a walk, say), or in a double-y linked list. There is also a connection wherein the vertex will connect to itself, called a loop, in this case the graph would be considered a pseudo-graph.

Now to begin, this isn't structured at all really, but it does give some general notions, and necessary derivations.

{% raw %}

A set is an aggregation of distinct objects, those of which cannot be the set itself:
That is, let `S` be a set of arbitrary elements to size `i`, i.e.:

\(S = \{a_0, a_1, ..., a_i\}\)

In set notation, we may self-define the set as:

$\forall s_a, s_b \in S: S = \{s_a | s_a \neq S \land s_a \neq s_b\}$

For any arbitrary elements, `s_a` and `s_b` of the set S, the set S is defined as having elements which are distinct (`s_a` != `s_b`), and that the element `s_a` is not the set itself, i.e. a set S cannot be `S = {1, S}`

A set's elements may not be integral, as it may be any abstract object.

A set with no defined elements, is defined as an empty/null-set.

A set `A` is a subset of set `B` iff $\forall a \in A: (a \in B)$, note that the subset operator is non-commutative as $\forall a \in A: (a \in B)$ does not imply $\forall b \in B: (b in A)$.
Every set is a subset of itself, as $\forall a \in A: (a \in A)$ is intuitively satisfied.
The empty set is a subset of all sets, including itself.

A set `A` is equal to set `B` iff $A \subset B \land B \subset A$, that is, if all members of A are in all members of B, and if all members of B are in all members of A.
This definition implies that a set does not have a property of orderedness, as the \in operator does not associate with order, rather existence regardless of position.

An empty set is a unique set to its name, let A and B be empty sets, as A contains the empty-set, and so does B, A is in B, and B is in A, therefore A = B, and thus the empty-set is unique.

Let AB, CD and XY be three finite lines, and define XY as a measure such that if we repeated the line XY `m` times, we will get the length of line AB, and respectively, if we laid out the line XY `n` times, we will get the length of line CD. That is, line XY = AB/m and XY = CD/n, so m*XY = AB, n*XY = CD, so AB/CD = (m*XY)/(n*XY) = m/n, implying that the ratio between the two lines is rational, however take the example AB = 1, CD = 1, and so deriving that the distance between the lines if they were perpendicular to each other, would be sqrt(2), therefore implying that sqrt(2) = m/n, which implies that sqrt(2) is rational.
Take sqrt(2) = a/b, thence square, 2 = a^2/b^2, isolate a^2, 2b^2 = a^2, as we can see, `a` must be an even number as its square has a factor of 2, proven by:

take some even `a`, represented as `2b`, hence square, `4b^2`, implying that the square of all even numbers has a divisor of 4, which we can trivially prove for say $a \in \{2, 4, 6, 8\}: \{4, 16, 36, 64\}$, divided by 4 yields {1, 4, 9, 16}, as 4 is the prime factorization 2*2, we can see that therefore all squares of a number whose factors contain 2 will also have a factor of 2 in its square.

And so, 2b^2 = a^2, we may set a = 2k, and acquire 2b^2 = 4k^2, thence simplify, b^2 = 2k^2, then simplify for b = 2m, 4m^2 = 2k^2, 2m^2 = k^2, and continue until we have run out of symbols, this is a never-ending cycle of reduction shows that the sqrt(2) is unable to be represented in the form a/b for whole numbers a, b in its simplest form, as we wil find ourselves in a loop.

Russell's paradox works off the definition of a set as merely a collection of distinct objects, categorized into two types of sets, ordinary and extraordinary. An ordinary set is not an element of itself, that is, A = {1, A} is not an ordinary set whereas A = {1, 2, 3} is, however A = {1, A} is an extraordinary set.
Now define a set which contains all ordinary sets as U, that is, if U does not contain itself, it implies that U is in U as it is an ordinary set, and hence U must be of itself, but then this implies that U is an extraordinary set, as it contains itself, however contrary to the definition that U is a set which contains ordinary sets.

$U = {x | x \nin x}, \therefore R \in R \implies R \notin R$

To resolve this, we define U as a non-set, rather a class, as if U was a set it would mean that it is a set of itself, therefore leading to the above paradox.

A graph is consistent of two sets called a vertex set and the edge set, the vertex set is a
a nonempty set, unlike the edge set which may be empty, otherwise being a set of two-set respective to the vertex set.

Given that {x, y} is an edge of some graph we say that {x, y} joins the vertices x and y, and that x and y are adjacent to one another, hence {x, y} is incident to vertices x and y, and respectively, x and y and incident to {x, y}. Adjacent edges are those that are incident to the same vertex, i.e. H = ({a, b, c}, {{a, b}, {b, c}}), the edges {a, b} and {b, c} are adjacent as they share the common vertex b.

Two graphs are equal if their vertex and edge sets are equal. A permutation of ordering of sets whose ordered vertex/edge sets are equal are still equal, regardless of any permutation into the order of the sets, or the elements of the set of two-sets of edge vertices.

A graph, by the definition of sets, may not have looped vertices (i.e. edge sets {{a, a}}), nor skeins (i.e. edge sets {{a, b}, {a, b}}) as this would go against the definition of a set having distinct elements. A graph without loops, yet with skeins, is called a multigraph, allowing both creates a pseudograph.

A graph's edges are undirected, i.e. an edge-set {{a, b}, {b, c}} does not imply that the vertex a is forwardly connected to the vertex b, nor the converse, as there is no explicit direction due to the fact that {a, b} = {b, a}, a directed graph whose order matters is called a digraph.

A common graph occurrence is one called a cyclic graph, denoted by the notation C_v, for v >= 3, defined as having vertex set {1, 2, 3, ..., v} and edge set {{1, 2}, {3, 4}, ..., {(v-1), v}, {v, 1}}, which connects back to itself, hence cyclic.
Another graph, called the null-graph, is one that has no edges, denoted as N_v, having edge-set {}, and vertex set {1, 2, 3, ..., v} for v >= 1, as a graph must have a nonzero vertex set implying N_1 is the trivial graph.
Another graph, called K_v for v >= 1 has vertex set {1, 2, 3, ..., v} and an edge-set with all possible edges producible from the vertex set.

Null graphs and complete graphs are complementary, so for any N_k: k >= 1, the complement of N_k is K_k, and inversely true for the complement of K_k being N_k.
The complement of any graph G, is also a graph, and the complement of the complement is the original graph G.

A subgraph H of a graph G is only true iff the vertex and edge setsof H are respective subsets of G.

It is obvious to deduce that K_n is a sort-of power-set graph, as it is a supergraph to any graph whose vertex set's magnitude, k, is 1 <= k <= n.

A one-to-one correspondence between two sets A and B is defined as:
	a) for all a in A, there must be an associating b in B
	b) for all b in B, there must be an associating a in A
Hence, an isomorphism between a graph is defined as the association of adjacency, that is, regardless of the labels, if two graphs have equivalent adjacency, then they are isomorphic, and hence equal aside the labels given, which determines true equality.
Isomorphic graphs must have preserved edge-count and vertex-count, as is expected from a one-to-one correspondence where it is expected that a certain edge must have two incident vertices, which defines a certain structure in relation to the rest of the graph, hence in unison with the other adjacent edges, it creates a structure of connectivity.
Conclusively, the number of vertices and edges must be preserved across isomorphisms.

The degree property of a certain vertex is the amount of edges incident to it, i.e., the amount of sets in the edge-set containing the vertex.

The amount of 'pieces' that a graph has is defined as the amount of disjoint graphs that are not connected to other structures, i.e.:

v: {A, B, C, D, E, F, G, H}
e: {{A,B}, {B, D}, {D, C}, {C, A}, {E, F}, {F, H}, {H, G}, {G, E}}

Which are essentially two graphs of C_4 (which is not a related property for graphs to be disjoint). However, this graph is in two pieces, as the cyclic graph EFHG has no incidence/adjacency with ABDC. And so, in order for another graph H to be isomorphic to graph G, it must at least follow the properties:

(a) The vertex-set has equal magnitude
(b) The edge-set has equal magnitude
(c) The degrees of vertices have equal magnitude
(d) The parts have to be equal

In graphs, a structure mayn't be isomorphic if the 4 properties are satisfied, the general structure of the graph must be preserved as well as if it were a rigid body transformation, the adjacency edges cannot mutate, and must remain constant across isomorphisms.

The subsets of {1, 2, 3} are {1}, {2}, {3}, {1, 2}, {2, 3}, {1, 3}, {1, 2, 3}, {}

Let A be a set, and J the null-set, assume J is not a subset of A, and take A as the nullset, J \notin A and also A \notin J implies A != J implying that the nullset is not the nullset, and hence creating a contradiction as we defined J as a null-set, therefore J must be in A and hence for any A.

A graph is planar iff it is provably isomorphic to a graph that has been illustrated in a plane to be without edge-crossings, otherwise the graph is nonplanar.

The Jordan Curve theorem & its corollary indicates that a continuous simple closed curve C, and two points A, inside the region enclosed by C, and a point B outwith C, with a continuous curve connecting A and B, it is provable that the curve from A to B must intersect the curve C.
The corollary indicates that a continuous curve between A and B on the continuous simple closed curve C must lie either within or outside the curve, and can be simply reduced to a line that does not cross C.
By these two definitions, we can prove trivial nonplanar graphs, such as the UG graph, and graphs K_n for n >= 5, as because it is provable that K_5 is nonplanar, and given that a supergraph of any nonplanar graph is nonplanar, then K_6 is simply a supergraph of K_5 plus a vertice and edges, therefore K_6 is nonplanar, and since that is nonplanar, so is K_7, K_8, ..., K_n.
Conversely, it is provable that any subgraph of a planar graph is also going to be planar, however not always true for supergraphs, as by removing vertices/edges we cannot create intersections, therefore the subgraph of a planar graph cannot suddenly become nonplanar.

A supergraph A of some graph B is one from B such that augmentation is applied, so that it is either isomorphic to itself (A is a supergraph of B if A = B).

A method of proving planarity of a graph, is by making an assumption that it is planar and hence disproving it, or the converse. For example take a K_5 graph where the bottom-most edge is split in the middle by another vertex, this is not isomorphic to the K_5 graph because it has an extra edge and vertex, therefore it is neither a supergraph (subgraphs of isomorphisms are isomorphic to the supergraph), but if we took this as the original figure, and wanted to prove that it was nonplanar, then take the following steps:

(a) Assume it is planar
(b) Remove the bottom vertex, and combine the two edges, into one (creating K_5). This graph is not a subgraph of the first graph, and it is neither isomorphic. However, our augmentation of the graph did not make it any less planar than we assumed it to be to begin with, because we erased an edge, which cannot possibly make something nonplanar.
(c) By this, we say that K_5 is planar, which is obviously untrue as it is provable that K_5 is nonplanar, and hence the augmentation from some graph to the graph K_5 whilst performing a planar augmentation can lead to proving that the graph is nonplanar by contradiction
(d) Therefore, the original graph is nonplanar

An expansion of a graph G is an addition of vertices to the graph of order two, analogous to cutting an edge into two edges with intermittent incidence into a point. A supergraph is however asimilar to expansion, as a supergraph cannot splice edges into two as that would unpreserve the original structure of the graph, and hence declining the property of subsettance from the subset into the supergraph. However, an expansion does do this, but it also preserves the planarity of the original graph, however not the structure, whereas a supergraph may introduce nonplanarity (never planarity from nonplanarity).
An intuitive example is to take the graphs C_4 and K_3, C_4 is not isomorphic to K_3 therefore it cannot be a subset of it, nor can K_3 be a subset of C_4 due to the same property of anisomorphism, this implies that no supergraph of K_3 nor C_4 could ever be isomorphic to one another, as it would involve changing the intrinsic internal structure.
However, C_4 is an expansion of K_3, as if we spliced one edge in K_3 we would create a graph isomorphic to C_4, and hence declared as an expansion to it.

To prove that any expansion of the UG or n >= 5: K_n is planar, we may use the same argument, suppose that we implement any amount of expansions within either graphs, and allow us to assume that it is planar to disprove it; if we remove the correspondent expansion-points, and revert to our original graph by method of erasal (and hence preserving our alleged planarity property) then we assume that the original graph is planar, which is untrue, as both the UG and n >= 5: K_n graphs are nonplanar.

Expansions and supergraphs are not commutative functions, a trivial counterexample that a supergraph of an expansion of G is not always equivalent to the expansion of a supergraph of G is as follows:

(a)	Take a graph G and add an edge dangling from it, hereafter expand the edge by splitting it into two edges, define this as the supergraph of the expansion of G.
(b)	Take the original graph G and attempt to expand the non-existent edge, this is impossible as there is no edge that has been defined because the edge was created by the supergraph.

Kuratowski's theorem proves that the set of all nonplanar graphs is equal to set of all graphs that are supergraphs of expansions of UG and K_5.

1) To prove that a graph with v = 5, e = 3, will always have at least two adjacent edges, we must consider that an edge will occupy at least 2 points, if the edges were separate then it would mean we would have v = 6, as 3 * 2 = 6, however if we were to have at least two edges adjacent we would only use 3 points, hence the third edge will occupy 2 points, and 3 + 2 = 5, therefore a graph of v = 5, e = 3 will have at least 2 adjacent edges to satisfy the v.

A walk across a graph is a sequence of vertices (not necessarily distinct) such that A_1, A_2, A_3, ..., A_n are all consecutive and/or equal vertices to the prior. The walk A_1 to A_n is considered to join A_1 and A_n.

A graph is connected if each vertex in the vertex-set has a place in the edge-set, i.e., each vertex is incident to an edge. Otherwise, the graph is disconnected. N_1 is connected, because the definition of connection is so that each two vertices, A, B imply there is a subset {A, B} in the edge-set, however, by the law of the excluded middle, an N_1 graph has no two vertices, and therefore cannot be not disconnected as there are no two vertices to be disconnected; and so, it is connected. However, all other N_n for n > 1 are disconnected for the same logic.
All cyclic graphs C_n are connected, and all k-regular graphs K_n are connected.

If a planar graph is drawn without edge crossings, we let `f` denote the number of faces subsected by the curves formed by the planar graph, i.e. K_3 has two faces, the inner and outer. Occasionally one may coin the outer-most face as the infinite face.
Nonplanar graphs can not have a determined face quantity.

A graph is defined as polygonal if it is planar, connected and each edge borders two unique faces. From this, we exclude planar connected graphs that border only one face, i.e. a graph v={1, 2, 3} e={{1, 2}, {2, 3}} or e={{1, 2}}, or for intuition, any graph that is not a closed, continuous and planar graph, is not polygonal.

Euler's formula for graphs was that for any planar connected graph, the equation v + f - e = 2 always held true. This is provable using inductive reasoning:

(a)	Let `f` be the subject of the inductive proof that v + f - e = 2 for all `f`, hence to test the base case: for f = 1, take a polygon N_1 (this is polygonal as it does not have enough edges to be considered non-polygonal, as per the law of the excluded middle, and it is connected, due to the same reasoning, it is also obviously planar), with v=1 e=0, then 1 + 1 - 0 = 2 holds true
(b) 	Hence, if v + f - e = 2 for some `k = 1`, then allow us to prove that it holds for `k + 1`, suppose graphs G and H, where:
		- H_f = G_f + 1
		- H_e - G_e = x
		- H_v - G_v = x - 1
	Therefore, to set H_??? as the subjects:
		- H_f = G_f + 1
		- H_e = x + G_e
		- H_v = G_v + x - 1
	And to finally substitute:
		1) G_v + G_f - G_e 	= H_v + H_f - H_e 			= 2
		2) G_v + G_f - G_e 	= (G_v + x - 1) + (G_f + 1) - (G_e + x) = 2
					= G_v + x - 1 + G_f +  1 - G_e - x	= 2
		   G_v + G_f - G_e	= G_v + G_f - G_e			= 2

Euler's formula additionally proves that non-polygonal, connected and planar graphs also follow v + f - e = 2, and so do simply any planar and connected graphs. A useful consequence from the Euler's formula is the inequality:

$\frac{3f}{2} <= e <= 3v - 6$

To derive this, we must prove that for any connected planar graph with v >= 3 that (3/2)f <= e, first note that the minimum number of vertices required to define bounds for a face is 3, with a closed curve across the vertices, however we may use any other amount of vertices beyond 3 as long as it is cyclic.
Also note that a C_4 graph bounds the internal face by 4 edges, and the outside face also by 4 edges, so in total we bind 2 faces with  8 edges, hence observe the inequality:
	3 <= <edges-binding-face-1>
	3 <= <edges-binding-face-2>
	...
	3 <= <edges-binding-face-n>
As we can see, and as I've said, all faces binding a face must be at least 3 vertices connected (3 edges consequently), and so that is our left-side of the inequality, and the count of edges is on the RHS. Therefore, if we sum both sides, we will get 3n <= 2e, where `e` is the amount of edges in the graph, so for 2 faces (in C_3) and 3 edges, we will get the inequality 6 <= 6 as 3*2 = 2*3, for a graph:
	Let G be a graph, G_v = {1, 2, 3, 4} and G_e = {{1, 2}, {1, 4}, {1, 3}, {2, 4}, {3, 4}}
This graph has 5 edges, and 4 vertices, it is planar, closed and creates three faces including the infinite face. Face one is bounded by the subset {{1, 4}, {4, 3}, {3, 1}} and the other face is bounded by {{1, 2}, {2, 4}, {4, 1}}, hence both faces are bounded by 3 edges (and the infinite face is bounded by 4, as the perimeter of the structure is {{1, 2}, {2, 4}, {4, 3}, {3, 1}}, so our inequality looks as follows:
	3 <= 3
	3 <= 3
	3 <= 4
To simplify:
	3*3 <= (3 + 3 + 4) ... 9 <= 10
And so, an intuition is that our inequality 3f <= 2e uses the duality of edges to define boundedness, and hence set restraints relative to the faces vs. edges.
{% endraw %}
