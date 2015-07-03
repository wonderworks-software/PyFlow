def portAffects(affects_port, affected_port):
    '''
    this function for establish dependencies bitween ports,
    for simulating maya's dirty propogation
    '''
    affects_port.affects = affected_port
    affected_port.affected_by.append(affects_port)


class PortTypes(object):

    kInput = 'input_port'
    kOutput = 'output_port'

    def __init__(self, arg):
        super(PortTypes, self).__init__()


class Edge(object):

    def __init__(self, source, destination):
        super(Edge, self).__init__()
        self.source = source
        self.destination = destination

    def __str__(self):
        return self.source.parent.name + '.' + self.source.name + \
        ' >>> ' + self.destination.parent.name + '.' + self.destination.name


class Port(object):

    def __init__(self, name, parent):
        super(Port, self).__init__()
        self.type = None
        self.name = name
        self.affects = None
        self.affected_by = []
        self.__data = None
        self.parent = parent
        self.edge_list = []

    def get_data(self):

        return self.__data

    def set_data(self, data):

        self.__data = data


class Node(object):
    def __init__(self, name):
        super(Node, self).__init__()
        self.name = name
        self.inputs = []
        self.outputs = []
        self.initialize()

    def initialize(self):
        '''
        in this function define ports and dependencies bitween them
        '''
        pass

    def add_port(self, port_name, port_type):
        p = Port(port_name, self)
        if port_type == PortTypes.kInput:
            self.inputs.append(p)
            p.type = PortTypes.kInput
            return p
        else:
            self.outputs.append(p)
            p.type = PortTypes.kOutput
            return p

    def get_port_by_name(self, name):
        for p in self.inputs + self.outputs:
            if p.name == name:
                return p

    def compute(self):
        '''
        node calculations here
        '''
        # getting data from inputs

        # do stuff

        # write data to output port
        pass


class Graph(object):

    def __init__(self):

        super(Graph, self).__init__()
        self.nodes = []
        self.edges = []

    def nodes(self):

        return self.nodes

    def add_node(self, node):

        self.nodes.append(node)

    def remove_node_by_name(self, name):

        [self.nodes.remove(n) for n in self.nodes if name == n.name]

    def count(self):

        return self.nodes.__len__()

    def add_edge(self, src, dst):

        e = Edge(src, dst)
        self.edges.append(e)
        src.edge_list.append(e)
        dst.edge_list.append(e)
        dst.set_data(src.get_data())
        portAffects(src, dst)
        dst.parent.compute()
        return e

    def plot(self):
        for n in self.nodes:
            print n.name
            for inp in n.inputs:
                print '|---', inp.name, 'data - {0}'.format(inp.get_data()),\
                    'affects on {0}'.format(inp.affects.name),\
                    'affected_by ', [p.name for p in inp.affected_by]
                for e in inp.edge_list:
                    print '\t|---', e.__str__()
            for out in n.outputs:
                print '|---' + out.name, 'data - {0}'.format(out.get_data()),\
                    'affects on {0}'.format(out.affects),\
                    'affected_by ', [p.name for p in out.affected_by]
                for e in out.edge_list:
                    print '\t|---', e.__str__()
