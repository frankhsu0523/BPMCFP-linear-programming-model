set V;
/* vertices */

set E within V cross V;
/* edges */

set P;
/* maximum number of paths */

set K;
/* demands */
/* d1 d2 d3 ... */

param c_e{i in V, j in V};
/* capacity of edges */

param b_v{v in V};
/* capacity of vertices */

param d{k in K};
/* size of demands */

param exist_PK{k in K, p in P};
/* tell path p demand k exist or not */

param c_p{k in K, p in P};
/* each paths flow size */

param exist_edge_PK{k in K, p in P, i in V, j in V};

param exist_node_PK{k in K, p in P, i in V};

var x{k in K, p in P}, >= 0, <= 1;

var y{k in K, p in P}, binary;

var lambda, >= 0;

maximize LANBDA: lambda;

s.t. c1{k in K}: sum{p in P} exist_PK[k,p] * x[k,p] * c_p[k,p] >= lambda * d[k];

s.t. c2{k in K}: sum{p in P} exist_PK[k,p] * x[k,p] * c_p[k,p] <= d[k];

s.t. c3{(i,j) in E}: sum{k in K, p in P} exist_PK[k,p] * exist_edge_PK[k,p,i,j] * x[k,p] * c_p[k,p] <=  c_e[i,j];

s.t. c4{v in V}: sum{k in K, p in P} exist_PK[k,p] * exist_node_PK[k,p,v] * y[k,p] <= b_v[v];

s.t. c5{k in K, p in P}: x[k,p] <= y[k,p];
