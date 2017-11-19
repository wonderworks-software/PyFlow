from threading import Thread
from AGraphCommon import *
import weakref


class AGPort(object):

    def __init__(self, name, parent, data_type):
        super(AGPort, self).__init__()
        self.name = name.replace(" ", "_")
        self.parent = weakref.ref(parent)
        self.object_type = AGObjectTypes.tPort
        self.data_type = data_type
        self.allowed_data_types = [data_type]
        self.affects = []
        self.affected_by = []
        self.edge_list = []
        self.type = None
        self.dirty = True
        self._connected = False
        # set default values
        self._data = self.getDefaultDataValue()

    def getDefaultDataValue(self):
        if self.data_type == AGPortDataTypes.tFloat:
            return float()
        if self.data_type == AGPortDataTypes.tInt:
            return int()
        if self.data_type == AGPortDataTypes.tString:
            return str("none")
        if self.data_type == AGPortDataTypes.tBool:
            return bool()
        if self.data_type == AGPortDataTypes.tArray:
            return []
        if self.data_type == AGPortDataTypes.tAny:
            return None
        if self.data_type == AGPortDataTypes.tReroute:
            return None

    def set_data_overload(self, data, dirty_propagate=True):
        pass

    def port_name(self):
        return self.parent().name + '.' + self.name

    def current_data(self):
        if self._data is None:
            return self.getDefaultDataValue()
        return self._data

    def port_connected(self):
        self._connected = True

    def port_disconnected(self):
        if not self.hasConnections():
            self._connected = False

    def set_clean(self):
        self.dirty = False

    def hasConnections(self):
        if len(self.edge_list) == 0:
            return False
        else:
            return True

    def set_dirty(self):
        self.dirty = True
        for i in self.affects:
            i.dirty = True

    def get_data(self, debug=False):

        # if not connected - return data
        if not self.hasConnections():
            return self.current_data()

        if self.type == AGPortTypes.kOutput:
            if self.dirty:
                compute_order = self.parent().graph().get_evaluation_order(self.parent())
                if debug:
                    for i in reversed(sorted([i for i in compute_order.keys()])):
                        print(i, [n.name for n in compute_order[i]])
                for i in reversed(sorted([i for i in compute_order.keys()])):
                    if not self.parent().graph().is_multithreaded():
                        for n in compute_order[i]:
                            if debug:
                                print(n.name, 'calling compute')
                            n.compute()
                    else:
                        if debug:
                            print('multithreaded calc of layer', [n.name for n in compute_order[i]])
                        calc_multithreaded(compute_order[i], debug)
                return self._data
            else:
                return self._data
        if self.type == AGPortTypes.kInput:
            if self.dirty:
                out = [i for i in self.affected_by if i.type == AGPortTypes.kOutput]
                if not out == []:
                    compute_order = out[0].parent().graph().get_evaluation_order(out[0].parent())
                    if debug:
                        for i in reversed(sorted([i for i in compute_order.keys()])):
                            print(i, [n.name for n in compute_order[i]])
                    for i in reversed(sorted([i for i in compute_order.keys()])):
                        if not self.parent().graph().is_multithreaded():
                            for n in compute_order[i]:
                                if debug:
                                    print(n.name, 'calling compute')
                                n.compute()
                        else:
                            if debug:
                                print('multithreaded calc of layer', [n.name for n in compute_order[i]])
                            calc_multithreaded(compute_order[i], debug)
                    return out[0]._data
            else:
                return self._data
        else:
            return self._data

    @staticmethod
    def str2bool(v):
        return v.lower() in ("true", "1")

    def call(self):
        for p in self.affects:
            p.call()

    def set_data(self, data, dirty_propagate=True):
        if self.data_type == AGPortDataTypes.tFloat:
            self._data = float(data)
        if self.data_type == AGPortDataTypes.tInt:
            self._data = int(data)
        if self.data_type == AGPortDataTypes.tString:
            self._data = str(data)
        if self.data_type == AGPortDataTypes.tArray:
            self._data = data
        if self.data_type == AGPortDataTypes.tBool:
            if type(data) != bool().__class__:
                self._data = self.str2bool(data)
            else:
                self._data = bool(data)
        if self.data_type == AGPortDataTypes.tAny:
            self._data = data

        self.set_clean()
        if self.type == AGPortTypes.kOutput:
            for i in self.affects:
                i._data = data
                i.set_clean()
        if dirty_propagate:
            push(self)
        self.set_data_overload(data, dirty_propagate)


class AGNode(object):
    def __init__(self, name, graph):
        super(AGNode, self).__init__()
        self.graph = weakref.ref(graph)
        self.name = name
        self.object_type = AGObjectTypes.tNode
        self.inputs = []
        self.outputs = []
        self.x = 0.0
        self.y = 0.0

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = self.graph().get_uniq_node_name(name)

    def add_input_port(self, port_name, data_type, foo=None):
        p = AGPort(port_name, self, data_type, foo)
        self.inputs.append(p)
        p.type = AGPortTypes.kInput
        if foo:
            p.call = foo
        return p

    def add_output_port(self, port_name, data_type, foo=None):
        p = AGPort(port_name, self, data_type, foo)
        self.outputs.append(p)
        p.type = AGPortTypes.kOutput
        if foo:
            p.call = foo
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

        # write data to outputs
        return


class AGraph(object):

    def __init__(self, name):

        super(AGraph, self).__init__()
        self.object_type = AGObjectTypes.tGraph
        self._debug = False
        self._multithreaded = False
        self.name = name
        self.nodes = []
        self.nodesPendingKill = []
        self.edges = []

    def get_uniq_node_name(self, name):

        nodes_names = [n.name for n in self.nodes]
        if name not in nodes_names:
            return name
        idx = 0
        tmp = name
        while tmp in nodes_names:
            idx += 1
            tmp = name + str(idx)
        return name + str(idx)

    def is_debug(self):
        return self._debug

    def set_debug(self, state):
        if not isinstance(state, bool):
            print 'bool expected. skipped'
            return
        self._debug = state

    def is_multithreaded(self):
        return self._multithreaded

    def set_multithreaded(self, state):
        if not isinstance(state, bool):
            print 'bool expected. skipped'
            return
        self._multithreaded = state

    def get_evaluation_order(self, node, dirty_only=True):

        order = {0: [node]}

        def foo(n):
            next_layer_nodes = self.get_next_layer_nodes(n, AGPortTypes.kInput, dirty_only)
            layer_idx = max(order.iterkeys()) + 1
            for n in next_layer_nodes:
                if layer_idx not in order:
                    order[layer_idx] = []
                order[layer_idx].append(n)
            if not next_layer_nodes == []:
                for i in next_layer_nodes:
                    foo(i)
        foo(node)
        # make sure no copies of nodes in higher layers (non directional cycles)
        for i in reversed(sorted([i for i in order.iterkeys()])):
            for iD in range(i - 1, -1, -1):
                for check_node in order[i]:
                    if check_node in order[iD]:
                        order[iD].remove(check_node)
        return order

    @staticmethod
    def get_next_layer_nodes(node, direction=AGPortTypes.kInput, dirty_only=False):
        nodes = []
        if direction == AGPortTypes.kInput:
            if not node.inputs == []:
                for i in node.inputs:
                    if not i.affected_by == []:
                        for a in i.affected_by:
                            if not dirty_only:
                                nodes.append(a.parent())
                            else:
                                if a.dirty:
                                    nodes.append(a.parent())
            return nodes
        if direction == AGPortTypes.kOutput:
            if not node.outputs == []:
                for i in node.outputs:
                    if not i.affects == []:
                        for p in i.affects:
                            if not dirty_only:
                                nodes.append(p.parent())
                            else:
                                if not [dout for dout in p.affects if dout.dirty] == []:
                                    nodes.append(p.parent())
            return nodes

    def get_nodes(self):

        return self.nodes

    def get_node_by_name(self, name):

        for i in self.nodes:
            if i.name == name:
                return i
        return None

    def add_node(self, node, x=0.0, y=0.0):
        # generate uniq name
        if not node:
            return False
        node.set_name(node.name)
        self.nodes.append(node)
        node.set_pos(x, y)
        # node.graph = self
        return True

    def remove_node(self, node):
        node.kill()

    def remove_node_by_name(self, name):
        [self.nodes.remove(n) for n in self.nodes if name == n.name]

    def count(self):

        return self.nodes.__len__()

    def add_edge(self, src, dst):

        debug = self.is_debug()
        if src.type == AGPortTypes.kInput:
            src, dst = dst, src
        if AGPortDataTypes.tAny not in [dst.data_type, src.data_type]:
            if dst.data_type not in [AGPortDataTypes.tAny, AGPortDataTypes.tReroute]:
                if src.data_type not in dst.allowed_data_types + [AGPortDataTypes.tReroute]:
                    print('data types error')
                    print(src.data_type, dst.data_type)
                    return False
        if src in dst.affected_by:
            if debug:
                print('already connected. skipped')
            return False
        if src.type == dst.type:
            if debug:
                print('same types can not be connected')
            return False
        if src.parent == dst.parent:
            if debug:
                print('can not connect to self')
            return False
        if cycle_check(src, dst):
            if debug:
                print('cycles are not allowed')
            return False
        if len(dst.affected_by) >= 1:
            if debug:
                print('already has connection')
            for e in dst.edge_list:
                self.remove_edge(e)

        portAffects(src, dst)
        src.set_dirty()
        dst._data = src._data
        dst.port_connected()
        push(dst)
        return True

    def remove_edge(self, edge, call_connection_functions=True):

        edge.source().affects.remove(edge.destination())
        edge.source().edge_list.remove(edge)
        edge.destination().affected_by.remove(edge.source())
        edge.destination().edge_list.remove(edge)
        edge.destination().port_disconnected()
        edge.source().port_disconnected()

    def plot(self):
        print self.name + '\n----------\n'
        for n in self.nodes:
            print n.name
            for inp in n.inputs:
                print '|---', inp.name, 'data - {0}'.format(inp.current_data()), \
                    'affects on', [i.name for i in inp.affects], \
                    'affected_by ', [p.name for p in inp.affected_by], \
                    'DIRTY ', inp.dirty
                for e in inp.edge_list:
                    print '\t|---', e.__str__()
            for out in n.outputs:
                print '|---' + out.name, 'data - {0}'.format(out.current_data()), \
                    'affects on', [i.name for i in out.affects], \
                    'affected_by ', [p.name for p in out.affected_by], \
                    'DIRTY', out.dirty
                for e in out.edge_list:
                    print '\t|---', e.__str__()
