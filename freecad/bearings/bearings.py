import Part
import math

def singlerowradialbearing(params,document):
	R1 = 0.5*params['d1']
	R4 = 0.5*params['d2']
	#the inner two radii seem to be not specified in the standards, so we choose usefull values
	dr = (R4 - R1)/5.
	R2= R1 + 2*dr
	R3= R4 - 2*dr    #Variables. The main body of the bearing is created from 4 cylinders
	TH=params['B']    #Ball bearing thickness
	NBall=int(math.floor(math.pi*R1/dr))    #Ball number
	RBall=2*dr  #Ball radius
	RR=R4/40.        #Bearing edges rounding value
	name = params['name']

	shapes = []

	B1=Part.makeCylinder(R1,TH)
	B2=Part.makeCylinder(R2,TH)
	IR=B2.cut(B1)                             # Creates inner ring.
	FI=IR.Edges
	IR.makeFillet(RR,FI)

	B3=Part.makeCylinder(R3,TH)
	B4=Part.makeCylinder(R4,TH)
	OR=B4.cut(B3)                         #Creates outter ring
	FO=OR.Edges
	OR=OR.makeFillet(RR,FO)

	T1=Part.makeTorus(R2+(RBall/2),RBall)
	VT=(0,0,TH/2)
	T1.translate(VT)                      #Creates ball race

	IR=IR.cut(T1)
	OR=OR.cut(T1)

	shapes.append(IR)
	shapes.append(OR)

	CBall=((R3-R2)/2)+R2
	PBall=TH/2

	for i in range(NBall):                #Creates a number of NBalls
		Ball=Part.makeSphere(RBall)
		Alpha=(i*2*math.pi)/NBall 
		BV=(CBall*math.cos(Alpha),CBall*math.sin(Alpha),TH/2)
		Ball.translate(BV)
		shapes.append(Ball)

	part = document.addObject("Part::Feature",name)
	comp = Part.Compound(shapes)
	part.Shape = comp.removeSplitter()

def axialthrustbearing(params, document):
	rin = 0.5*params['d']
	rout = 0.5*params['D']
	bth = params['T']
	name = params['name']

	fth=0.3*bth  #Thrust plate widh
	#Edge fillet value
	if rout<70:
	  RR=1
	else:
	  RR=1.5
	#shapes--
	shapes=[]
	#Lower ring--------------------------
	lr1=Part.makeCylinder(rout,fth)
	lr2=Part.makeCylinder(rin,fth)
	lr=lr1.cut(lr2)
	lre=lr.Edges
	lr=lr.makeFillet(RR,lre)
	#Upper ring--------------------------
	ur1=Part.makeCylinder(rout,fth)
	ur2=Part.makeCylinder(rin,fth)
	ur=ur1.cut(ur2)
	ure=ur.Edges
	ur=ur.makeFillet(RR,ure)
	#Positioning Vector
	Vur=(0,0,bth-fth)
	ur.translate(Vur)
	#Balltracks---------------------------
	tbigradius=((rout-rin)/2.00)+rin
	tsmradius=(bth/2.00)-(0.75*fth)
	Vtorus=(0,0,bth/2.00)
	torus=Part.makeTorus(tbigradius,tsmradius)
	#Positioning vector
	torus.translate(Vtorus)
	#Booleans------------------------------
	lr=lr.cut(torus)
	shapes.append(ur)
	shapes.append(lr)
	#Balls--------------------------------
	RBall=tsmradius
	CBall=tbigradius
	#Ball number (constant multiplied by radius and rounded)
	NBall=(2*math.pi*CBall)/(2*RBall)
	NBall=math.floor(NBall)
	NBall=NBall*0.9
	NBall=int(NBall)
	#Ball creator
	for i in range (NBall): 
		Ball=Part.makeSphere(RBall)
		Alpha=(i*2*math.pi)/NBall 
		BV=(CBall*math.cos(Alpha),CBall*math.sin(Alpha),bth/2.00)
		Ball.translate(BV)
		shapes.append(Ball)

	part = document.addObject("Part::Feature",name)
	comp = Part.Compound(shapes)
	part.Shape = comp.removeSplitter()

bases = {'singlerowradialbearing' : singlerowradialbearing,'axialthrustbearing' : axialthrustbearing}
