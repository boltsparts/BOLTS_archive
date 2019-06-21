# released into the public domain
# 2014 Johannes Reinhardt <jreinhardt@ist-dein-freund.de>

import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as pl


def plot_circle(center,radius):
	alpha = np.linspace(0,2*np.pi,100)
	x = center[0] + radius*np.cos(alpha)
	y = center[1] + radius*np.sin(alpha)
	pl.plot(x,y)


def plot_line(a,b):
	x = np.array([a[0],b[0]])
	y = np.array([a[1],b[1]])
	pl.plot(x,y)


# ci and ri are the centers and radii of the two circles, t is a vector with the
# coordinates of the tangent points (t1x,t1y,t2x,t2y)
# this evaluates to 0 if t1,t2 fulfill the tangent condition
def constraints(c1,c2,r1,r2,t1,t2,m1,d):
	return np.linalg.norm([
		#on circle constraints
		np.dot(t1-c1, t1-c1) - r1*r1,
		np.dot(t2-c2, t2-c2) - r2*r2,
		#tangent constraints
		np.dot(t1-t2,t2-c2),
		np.dot(t1-t2,t1-c1),
		#on flange constraint for m1
		np.linalg.norm(np.cross(t1-m1,t1-t2)),
	])


# from http://b2bmetal.eu/i-sections-inp-specification
# we put the coordinate system in the middle


dims = {
	# name       b    h    s     t     r1    r2   d
	"IPN80"  : [42,  80,  3.9,  5.9,  3.9,  2.3, 59.0],
	"IPN100" : [50,  100, 4.5,  6.8,  4.5,  2.7, 75.7],
	"IPN120" : [58,  120, 5.1,  7.7,  5.1,  3.1, 92.4],
	"IPN140" : [66,  140, 5.7,  8.6,  5.7,  3.4, 109.1],
	"IPN160" : [74,  160, 6.3,  9.5,  6.3,  3.8, 125.8],
	"IPN180" : [82,  180, 6.9,  10.4, 6.9,  4.1, 142.4],
	"IPN200" : [90,  200, 7.5,  11.3, 7.5,  4.5, 159.1],
	"IPN220" : [98,  220, 8.1,  12.2, 8.1,  4.9, 175.8],
	"IPN240" : [106, 240, 8.7,  13.1, 8.7,  5.2, 192.5],
	"IPN260" : [113, 260, 9.4,  14.1, 9.4,  5.6, 208.9],
	"IPN280" : [119, 280, 10.1, 15.2, 10.1, 6.1, 225.1],
	"IPN300" : [125, 300, 10.8, 16.2, 10.8, 6.5, 241.6],
	"IPN320" : [131, 320, 11.5, 17.3, 11.5, 6.9, 257.9],
	"IPN340" : [137, 340, 12.2, 18.3, 12.2, 7.3, 274.3],
	"IPN360" : [143, 360, 13.0, 19.5, 13.0, 7.8, 290.0],
	"IPN380" : [149, 380, 13.7, 20.5, 13.7, 8.2, 306.7],
	"IPN400" : [155, 400, 14.4, 21.6, 14.4, 8.6, 322.9],
	"IPN450" : [170, 450, 16.2, 24.3, 16.2, 9.7, 363.6],
	"IPN500" : [185, 500, 18.0, 27.0, 18.0, 10., 404.38],
	"IPN550" : [200, 550, 19.0, 30.0, 19.0, 11., 445.69],
	"IPN600" : [215, 600, 21.6, 32.4, 21.6, 13., 485.80]
}


def unpack(x,dim):
	b,h,s,t,r1,r2,d = tuple(dim)

	#knowns are r1,r2, m1
	m1 = np.array([0.25*b,0.5*h-t])

	#unknown are c1, c2, t1, t2
	c1 = np.array([0.5*s+r1,0.5*d])
	c2 = np.array([0.5*b-r2,x[0]])

	t1 = x[1:3]
	t2 = x[3:]

	return c1,c2,r1,r2,t1,t2,m1,d


for name in sorted(dims.keys()):
	dim = dims[name]
	#upper right flange
	b,h,s,t,r1,r2,d = tuple(dim)

	x0 = [0.5*h,0.5*s+r1,0.5*d+r1,0.5*b-r2,0.5*h-r2]

	p = minimize(lambda x: constraints(*unpack(x,dim)),x0,method="Nelder-Mead",tol=1e-10)

	f = 0.5*h-p.x[0]

	pl.figure()
	pl.title(name)

	c1,c2,r1,r2,t1,t2,m1,d = unpack(p.x,dim)

	flange = lambda x: t1[1]*(t2[0] - x)/(t2[0] - t1[0]) + t2[1]*(x - t1[0])/(t2[0] - t1[0])

	f = flange(0.5*s)
	g = 0.5*h - flange(0.5*b)

	print('"%s" : [ %g, %g, %g, %g, %g, %g, %g, %g, %g ]' % (name,b,h,s,t,r1,r2,d,f,g))

	plot_line([0,0],[0.5*s,0])
	plot_line([0.5*s,0],[0.5*s,c1[1]])
	plot_circle(c1,r1)
	plot_line(t1,t2)
	plot_circle(c2,r2)
	pl.plot([m1[0]],[m1[1]],'x')
	plot_line([0.5*b,c2[1]],[0.5*b,0.5*h])
	plot_line([0,0.5*h],[c2[0]+r1,0.5*h])
	pl.plot([0.5*s],[f],'x')
	pl.plot([0.5*b],[0.5*h - g],'x')

	c1,c2,r1,r2,t1,t2,m1,d = unpack(x0,dim)

#	plot_line([0,0],[0.5*s,0])
#	plot_line([0.5*s,0],[0.5*s,c1[1]])
#	plot_circle(c1,r1)
#	plot_line(t1,t2)
#	plot_circle(c2,r2)
#	pl.plot([m1[0]],[m1[1]],'x')
#	plot_line([0.5*b,c2[1]],[0.5*b,0.5*h])
#	plot_line([0,0.5*h],[c2[0]+r1,0.5*h])


pl.show()
