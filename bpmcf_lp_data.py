import networkx as nx

from copy import deepcopy
import csv

class LP:

    def __init__(self, graph_Name, demand_Name, path_Name):
        self.G = nx.DiGraph()
        self.demand = tuple()
        self.path = None

        self.set_V = None
        self.set_E = None
        self.set_P = None
        self.set_K = None
        self.param_c_e = None
        self.param_b_v = None
        self.param_d = None
        self.param_exist_PK = None
        self.param_c_p = None
        self.param_exist_edge_PK = None
        self.param_exist_node_PK = None

        self.read_graph(graph_Name)
        self.set_set_V()
        self.set_set_E()
        self.read_demand(demand_Name)
        self.set_set_P(5)
        self.set_set_K()
        self.set_param_c_e()
        self.set_param_b_v()
        self.set_param_d()
        self.read_path(path_Name)
        self.set_param_exist_PK()
        self.set_param_c_p()
        self.set_param_exist_edge_PK()
        self.set_param_exist_node_PK()

        self.output_data(graph_Name)

    def read_graph(self, f_Name):
        status = None
        with open(f_Name, 'r') as f:
            for r in f.read().splitlines():
                if '@nodes' in r or '@arcs' in r:
                    continue
                elif 'label table_size' in r:
                    status = 'nodes'
                elif 'bandwidth' in r:
                    status = 'edges'
                elif status is 'nodes':
                    node, size = tuple(r.split(' '))
                    self.G.add_node(node, size = size)
                elif status is 'edges':
                    head, tail, size = tuple(r.split(' '))
                    self.G.add_edge(head, tail, size = size)

    def read_demand(self, f_Name):
        demands = list()
        with open(f_Name, 'r') as f:
            for r in f.read().splitlines():
                if '@pair(source-destination-demand)' in r:
                    continue
                else:
                    demands.append(tuple(r.split(',')))
        self.demand = tuple(demands)

    def read_path(self, path_Name):
        with open(path_Name,'r') as f:
            self.path = list(csv.reader(f))

    def set_set_V(self):
        nodes = self.G.nodes()
        nodes.sort(key=int)
        self.set_V = tuple(nodes)

    def set_set_E(self):
        #initial the two dimensional matrix to 0
        self.set_E = [['-' for i in range(len(self.set_V))] for y in range(len(self.set_V))]

        for i, j in self.G.edges():
            self.set_E[int(i)][int(j)] = '+'

    def set_set_P(self, num):
        self.set_P = tuple([str(i) for i in range(num)])

    def set_set_K(self):
        self.set_K = tuple([str(i) for i in range(len(self.demand))])
        #print('set_K: ',self.set_K)

    def set_param_c_e(self):
        self.param_c_e = [['0' for i in range(len(self.set_V))] for y in range(len(self.set_V))]

        for i,j,d in self.G.edges(data=True):
            self.param_c_e[int(i)][int(j)] = d['size']

    def set_param_b_v(self):
        self.param_b_v = ['0' for i in range(len(self.set_V))]

        for i, d in self.G.nodes(data=True):
            self.param_b_v[int(i)] = d['size']

    def set_param_d(self):
        self.param_d = ['0' for i in range(len(self.demand))]

        for i, d in enumerate(list(self.demand)):
            self.param_d[i] = d[2]

    def set_param_exist_PK(self):
        self.param_exist_PK = [['0' for i in range(len(self.set_P))] for j in range(len(self.set_K))]

        k, p = (0, 0)
        for i, path in enumerate(self.path):
            if i > 0 and (path[0] != self.path[i-1][0] or path[-1] != self.path[i-1][-1]):
                k += 1
                p = 0

            self.param_exist_PK[k][p] = '1'
            p += 1
    def set_param_c_p(self):
        self.param_c_p = [[d[2] for i in self.set_P] for d in self.demand]

    def set_param_exist_edge_PK(self):
        initial_edge_matrix = [['0' for i in range(len(self.set_V))] for y in range(len(self.set_V))]
        self.param_exist_edge_PK = [[ deepcopy(initial_edge_matrix) for i in range(len(self.set_P))] for j in range(len(self.set_K))]

        k, p = (0, 0)
        for i, path in enumerate(self.path):
            if i > 0 and (path[0] != self.path[i-1][0] or path[-1] != self.path[i-1][-1]):
                k += 1
                p = 0

            edge_matrix = self.param_exist_edge_PK[k][p]
            for i, n in enumerate(path[:-1]):
                edge_matrix[int(path[i])][int(path[i+1])] = '1'
            p += 1
        """
        for i in self.param_exist_edge_PK:
            for j in i:
                for k in j:
                    print(k)
                print('_________________________________________________')
        """

    def set_param_exist_node_PK(self):
        initial_node_matrix = [['0' for i in range(len(self.set_V))] for y in range(len(self.set_P))]
        self.param_exist_node_PK = [ deepcopy(initial_node_matrix) for i in range(len(self.set_K))]

        k, p = (0, 0)
        for i, path in enumerate(self.path):
            if i > 0 and (path[0] != self.path[i-1][0] or path[-1] != self.path[i-1][-1]):
                k += 1
                p = 0

            node_matrix = self.param_exist_node_PK[k][p]
            for v in path[:-1]:
                node_matrix[int(v)] = '1'
            p += 1

        """
        for i in self.param_exist_node_PK:
            for j in i:
                print(j)
            print('_________________________________________________')
        """

    def output_data(self, graph_Name ):
        f_Name = graph_Name.split('_')[0] + '.dat'

        with open( f_Name, 'w' ) as f:
            f.write("data;\n\n")

            f.write("set V := {};\n\n".format(' '.join(self.set_V)))

            f.write("set E :=	(*, *)	:	{} :=\n".format(' '.join(self.set_V)))
            for i, v in enumerate(self.set_E):
                f.write("			{:2d}	{}\n".format(i, ' '.join(v)))
            f.write(";\n\n")

            f.write("set P := {};\n\n".format(' '.join(self.set_P)))

            f.write("set K := {};\n\n".format(' '.join(self.set_K)))

            f.write("param c_e :=	[*,*]	:	{} :=\n".format(' '.join(self.set_V)))
            for i, v in enumerate(self.param_c_e):
                f.write("			{:2d}	{}\n".format(i, ' '.join(v)))
            f.write(";\n\n")

            f.write("param b_v :=	\n")
            for i, v in enumerate(self.param_b_v):
                f.write("		{:2d} {}\n".format(i, v))
            f.write(";\n\n")

            f.write("param d	:=	\n")
            for i, v in enumerate(self.param_d):
                f.write("		{:2d} {}\n".format(i, v))
            f.write(";\n\n")

            f.write("param exist_PK	:=	[*, *]	:	{} :=\n".format(' '.join(self.set_P)))
            for i, k in enumerate(self.param_exist_PK):
                f.write("			{:3d}	{}\n".format(i, ' '.join(k)))
            f.write(";\n\n")

            f.write("param c_p	:=	[*, *]	:	{} :=\n".format(' '.join(self.set_P)))
            for i, k in enumerate(self.param_c_p):
                f.write("			{:3d}	{}\n".format(i, ' '.join(k)))
            f.write(";\n\n")

            f.write("param exist_edge_PK	:=\n")
            for index_k, k in enumerate(self.param_exist_edge_PK):
                for index_p, p in enumerate(k):
                    f.write("			[{}, {}, *, *]	:	{} :=\n".format(index_k,index_p,' '.join(self.set_V)))
                    for i, v in enumerate(p):
                        f.write("		{:2d} {}\n".format(i, ' '.join(v)))
            f.write(";\n\n")

            f.write("param exist_node_PK	:=\n")
            for index_k, k in enumerate(self.param_exist_node_PK):
                f.write("			[{}, *, *]	:	{} :=\n".format(index_k,' '.join(self.set_V)))
                for i, v in enumerate(k):
                    f.write("		{:2d} {}\n".format(i, ' '.join(v)))
            f.write(";\n\n")
    def __str__(self):
        for i,j, d in self.G.edges(data=True):
            print(i,j,d)
        return 'Information'

if __name__ == '__main__':
    lp = LP('abilene_graph.txt','abilene_demands.txt','abilen_5_shortest_path.csv')
