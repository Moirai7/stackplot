#--coding:utf8
import numpy as np

def smooth(x,y):
	from scipy.interpolate import spline
	xs = np.linspace(0,len(x),len(x)*10)
	new_y = []
	for i in range(len(y)):
		new_y.append(spline(x,y[i],xs))
	return (xs,np.array(new_y))

def designBase(y,stack):
	#'''
	m = y.shape[0]
	baseline = (y * (m - 0.5 - np.arange(m)[:, None])).sum(0)
	baseline /= -m
	#'''
	#baseline = -np.sum(y, 0) * 0.5
	'''
	#个人觉得weighted wiggle不是很好看
	m, n = y.shape
        center = np.zeros(n)
        total = np.sum(y, 0)
        # multiply by 1/total (or zero) to avoid infinities in the division:
        inv_total = np.zeros_like(total)
        mask = total > 0
        inv_total[mask] = 1.0 / total[mask]
        increase = np.hstack((y[:, 0:1], np.diff(y)))
        below_size = total - stack
        below_size += 0.5 * y
        move_up = below_size * inv_total
        move_up[:, 0] = 0.5
        center = (move_up - 0.5) * increase
        center = np.cumsum(center.sum(0))
        baseline = center - 0.5 * total
	'''
	return baseline

def changeRow(y):
	new_y = []
	maxindex = np.max(y, axis = 1)
	maxindex = maxindex.argsort()#[::-1]
	#maxindex = np.take(y, mddaxindex, axis=0)

	sumindex = np.sum(y, axis = 1)
	#sumindex = sumindex.argsort()[::-1]
	#sumindex = np.take(y, sumindex, axis=0)

	top = 0
	bottom = 0
	tops = []
	bottoms = []
	for i in range(len(y)):
		j = maxindex[i]
		if (top < bottom) :
			top += sumindex[j]
			tops.append(j)
		else:
			bottom += sumindex[j]
			bottoms.append(j)
	bottoms.reverse()
	return np.take(y,bottoms+tops,axis=0)
		

def showData(x,y,check=0,change=0):
	import  matplotlib.pyplot as plt
	from matplotlib import colors
	#plt.style.use('ggplot')
	lens = len(y)-1
	z = np.row_stack(range(lens+1))
	normalize = colors.Normalize(vmax=z.max(),vmin=z.min()-5)
	stack = np.cumsum(y, axis=0, dtype=np.promote_types(y.dtype, np.float32))
	if check!=0:
		baseline = designBase(y,stack)
		stack += baseline[None, :]
	else:
		baseline = 0
	fig = plt.figure()
	axes = fig.add_subplot(111)
	cmap=plt.get_cmap('Blues')
	
	color = cmap(normalize(z[lens]))
	#color = axes._get_lines.get_next_color()
	axes.fill_between(x, baseline, stack[0, :],color = color,alpha=1) 
	for i in range(1,len(y)):
		if change!=0:
			if i<len(y)/2:
				color = cmap(normalize(z[lens-i]))
			else:
				color = cmap(normalize(z[i]))
		else:
			color = cmap(normalize(z[lens-i]))
		#color = axes._get_lines.get_next_color()
		axes.fill_between(x, stack[i-1,:], stack[i, :],color=color) 
	#axes.plot(np.zeros(50),'--',color='r')
	plt.show()

def procData():
	import json
	with open('data.json') as y_file:	
		y = json.load(y_file)
	y = np.row_stack(y)
	x = range(len(y[0]))
	print 'pic without smoothing...'
	showData(x,y)
	print 'pic with smooth...'
	x,y = smooth(x,y)
	showData(x,y)
	print 'pic with novel design...'
	showData(x,y,1)
	print 'pic with novel design...'
	y = changeRow(y)
	showData(x,y,1,0)
	print 'pic with novel design...'
	showData(x,y,1,1)
	pass

if __name__ == '__main__':
	procData()
