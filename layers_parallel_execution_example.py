from threading import Thread
from time import sleep
from random import randint


def worker(n):
	sleep_time = randint(1, 3)
	sleep(sleep_time)


def calc_nodes_layer(ls):
	print 'START', ls
	threads = []
	for n in ls:
		t = Thread(target=worker, args=(n,), name='{0}_thread'.format(n))
		threads.append(t)
		t.start()
		print n, 'started in', t.name

	print '_WAITING FOR ALL LAYER NODES FINISH'
	[t.join() for t in threads]

	print 'DONE', ls, '\n'



layers = {1: ['1nodeA', '1nodeB'], 2: ['2NodeA', '2NodeB', '2NodeC', '2NodeD'], 0: ['0NodeA', '0NodeB']}


for l in [i for i in reversed(sorted([n for n in layers.iterkeys()]))]:
	calc_nodes_layer(layers[l])
