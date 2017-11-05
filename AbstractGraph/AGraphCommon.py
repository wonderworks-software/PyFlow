'''
common defines, functions and structures
'''
import math


FLAG_SYMBOL = "~"


def roundup(x, to):
    return int(math.ceil(x / to)) * to


def portAffects(affects_port, affected_port):
    '''
    this function for establish dependencies bitween ports,
    for simulating dirty propogation
    '''
    affects_port.affects.append(affected_port)
    affected_port.affected_by.append(affects_port)


def calc_multithreaded(ls, debug=False):
    if debug:
        print('START', [n.name for n in ls])

    def compute_executor():
        for n in ls:
            n.compute()
    threads = []
    for n in ls:
        t = Thread(target=compute_executor, name='{0}_thread'.format(n.name))
        threads.append(t)
        t.start()
        if debug:
            print(n.name, 'started in', t.name)

    if debug:
        print('_WAITING FOR ALL LAYER NODES TO FINISH')
    [t.join() for t in threads]

    if debug:
        print('DONE', [n.name for n in ls], '\n')


def cycle_check(src, dst):

    if src.type == AGPortTypes.kInput:
        src, dst = dst, src
    start = src
    if src in dst.affects:
        return True
    for i in dst.affects:
        if cycle_check(start, i):
            return True
    return False


def find_ports_behind(start_from):
    out = []

    def foo(start_from):
        if not start_from.affected_by == []:
            for p in start_from.affected_by:
                out.append(p)
                foo(p)
    foo(start_from)
    return out


def push(start_from):
    if not start_from.affects == []:
        start_from.set_dirty()
        for i in start_from.affects:
            i.set_dirty()
            push(i)


class AGPortDataTypes(object):

    tNumeric = 'numeric_data'
    tString = 'string_data'
    tBool = 'boolean_data'
    tArray = 'array_data'
    tAny = 'all'
    tReroute = 'reroute'
    tExec = 'exec'

    def __init__(self):
        super(AGPortDataTypes, self).__init__()


class AGObjectTypes(object):

    tPort = 'port_object'
    tNode = 'node_object'
    tGraph = 'graph_object'
    tGrouper = 'group_object'
    tConnectionLine = 'connection_line_object'
    tGridLine = 'grid_line_object'
    tNodeName = 'node_name_object'

    def __init__(self):
        super(AGObjectTypes, self).__init__()


class AGPortTypes(object):

    kInput = 'input_port'
    kOutput = 'output_port'

    def __init__(self, arg):
        super(AGPortTypes, self).__init__()
