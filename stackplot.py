import numpy as np

def smooth(x,data):
	from scipy.interpolate import spline
	xs = np.linspace(0,len(x),len(x)*10)
	new_data = []
	for i in range(len(data)):
		new_data.append(spline(x,data[i],xs))
	return (xs,np.array(new_data))

def changeRow(data):
	pass
		

def showData(x,y,baseline=0):
	import  matplotlib.pyplot as plt
	from matplotlib import colors
	#plt.style.use('ggplot')
	lens = len(y)-1
	z = np.row_stack(range(lens+1))
	normalize = colors.Normalize(vmax=z.max(),vmin=z.min()-5)
	stack = np.cumsum(y, axis=0, dtype=np.promote_types(y.dtype, np.float32))

	fig = plt.figure()
	axes = fig.add_subplot(111)
	cmap=plt.get_cmap('Blues')
	axes.fill_between(x, baseline, stack[0, :],color=cmap(normalize(z[lens])),where=stack[0, :]>baseline ,alpha=1,edgecolor='k') 
	for i in range(1,len(y)):
		color = cmap(normalize(z[lens-i]))
		axes.fill_between(x, stack[i-1,:], stack[i, :],color=color,edgecolor='k',where=stack[0, :]>baseline) 
	plt.show()

def procData():
	import json
	with open('data.json') as data_file:	
		data = json.load(data_file)
	data = np.row_stack(data)
	x = range(len(data[0]))
	print 'pic without smoothing...'
	showData(x,data)
	print 'pic with smooth...'
	x,data = smooth(x,data)
	showData(x,data)
	print 'pic with novel design...'
	data = changeRow(data)
	showData(x,data)
	pass

if __name__ == '__main__':
	procData()
