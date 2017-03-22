import numpy as np
import matplotlib
matplotlib.use('PS')
import  matplotlib.pyplot as plt


def showData(y):
	x = xrange(50)
	stack = np.cumsum(y, axis=0, dtype=np.promote_types(y.dtype, np.float32))

	fig = plt.figure()
	axes = fig.add_subplot(111)
	axes.fill_between(x, 0, stack[0, :],facecolor="#CC6666", alpha=.7) 
	for i in xrange(len(y)-1):
		label = 1.0/(1.0+exp(-i))
		axes.fill_between(x, stack[i,:], stack[i+1, :],facecolor=plt.cm.RdYlBu(label), alpha=.7) 
	plt.show()

def procData():
	import json
	with open('data.json') as data_file:    
		data = json.load(data_file)
	data = np.row_stack(data)
	print len(data)
	showData(data)
	pass

if __name__ == '__main__':
	procData()
