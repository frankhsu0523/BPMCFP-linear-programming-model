import networkx as nx

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
        self.set_param_c_p()
        self.read_path(path_Name)
        self.set_param_exist_edge_PK()

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
        self.set_E = [['0' for i in range(len(self.set_V))] for y in range(len(self.set_V))]

        for i, j in self.G.edges():
            self.set_E[int(i)][int(j)] = '1'

    def set_set_P(self, num):
        self.set_P = tuple([i for i in range(num)])
        
    def set_set_K(self):
        self.set_K = tuple([i for i in range(len(self.demand))])
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
        
    def set_param_c_p(self):
        self.param_c_p = [[d[2] for i in self.set_P] for d in self.demand]

    def set_param_exist_edge_PK(self):
        self.param_exist_edge_PK = []
        for i, d in enumerate(self.path[:500]):
            k, p = divmod(i,5)
            if p == 0 and d[0] == self.path[i-1][0] and d[-1] == self.path[i-1][-1]:
                pass
            if d[0] == '1' and d[-1] == '0':
                print(d)
                #print(i,d)
            #print(k,p)

    def __str__(self):
        for i,j, d in self.G.edges(data=True):
            print(i,j,d)
        return 'Information'

if __name__ == '__main__':
    lp = LP('abilene_graph.txt','abilene_demands.txt','abilen_5_shortest_path.csv')
