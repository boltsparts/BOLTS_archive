//  Modules for the Bosch Rexroth series of aluminium profiles
//  Sourced from http://www.kjnltd.co.uk/
//  Author - Damian Axford
//  Public Domain


eta = 0.01;


// Bore Types
BR_20x20_Bore = [5.5, 1.5, 7];

function aluProBore_r(boreType) = boreType[0]/2;
function aluProBore_outsetW(boreType) = boreType[1];
function aluProBore_outsetR(boreType) = boreType[2]/2;

// Core Types
BR_20x20_Core = [9,2,0.75];

function aluProCore_w(coreType) = coreType[0];
function aluProCore_keyW(coreType) = coreType[1];
function aluProCore_keyD(coreType) = coreType[2];

//Corner Types
BR_20x20_Corner = [20, 7, 1.5, 0.5, 4];

// Side Types  - for closed slots
BR_20x20_Side = [20, 1.5];

// Side Styles
BR_0 = [0,0,0,0];
BR_1S = [0,1,1,1];
BR_2S = [0,1,0,1];
BR_3S = [0,1,0,0];
BR_2SA = [1,1,0,0];

// Profiles - combination of elements

BR_20x20 = [BR_20x20_Bore, BR_20x20_Core, BR_20x20_Corner, BR_20x20_Side, BR_0, 1, 1, "BR_20x20"];
BR_20x20_1S = [BR_20x20_Bore, BR_20x20_Core, BR_20x20_Corner, BR_20x20_Side, BR_1S, 1, 1, "BR_20x20_1S"];
BR_20x20_2S = [BR_20x20_Bore, BR_20x20_Core, BR_20x20_Corner, BR_20x20_Side, BR_2S, 1, 1, "BR_20x20_2S"];
BR_20x20_3S = [BR_20x20_Bore, BR_20x20_Core, BR_20x20_Corner, BR_20x20_Side, BR_3S, 1, 1, "BR_20x20_3S"];
BR_20x20_2SA = [BR_20x20_Bore, BR_20x20_Core, BR_20x20_Corner, BR_20x20_Side, BR_2SA, 1, 1, "BR_20x20_2SA"];

BR_20x40 = [BR_20x20_Bore, BR_20x20_Core, BR_20x20_Corner, BR_20x20_Side, BR_0, 1, 2, "BR_20x40"];

BR_20x60 = [BR_20x20_Bore, BR_20x20_Core, BR_20x20_Corner, BR_20x20_Side, BR_0, 1, 3, "BR_20x60"];

BR_20x80 = [BR_20x20_Bore, BR_20x20_Core, BR_20x20_Corner, BR_20x20_Side, BR_0, 1, 4, "BR_20x80"];

function aluPro_label(type) = type[7];

//twistLockNutType

BR_20x20_TwistLockNut = [5.8,11.3,4,0.8,1.5];


// gussets
// width, wall_thickness, slot width, slot height, slot offset from base, nib depth
BR_20x20_Gusset = [18, 3, 4.5, 7, 7.7, 1, "BR20x20Gusset"];

module aluProBore(boreType, $fn=16) {
	union() {
		circle(r=aluProBore_r(boreType));
	
		intersection() {
			circle(r=aluProBore_outsetR(boreType));
			for (i=[0:3]) 
				rotate([0,0,i*90 + 45]) 	
				square([aluProBore_outsetR(boreType)*2,aluProBore_outsetW(boreType)], center=true);
		}
	}
}


module aluProCore(coreType) {
	w = aluProCore_w(coreType);
	keyW = aluProCore_keyW(coreType);
	keyD = aluProCore_keyD(coreType);

	difference() {
		square([w,w],center=true);

		// remove keys
		for (i=[0:3]) 
			rotate([0,0,i*90])
			translate([w/2,0,0])
			polygon([[eta,keyW/2], 
                      [-keyD,0], 
                      [eta,-keyW/2]]); 
	}
}


module aluProCorner(cornerType, $fn=8) {
	// xy corner
	w1 = cornerType[0];
	w2 = cornerType[1];
	t = cornerType[2];
	cham = cornerType[3];
	w3 = cornerType[4];	

	union() {	
		// radial arm
		rotate([0,0,45]) translate([0,-t/2,0]) square([w1/2+t,t]);

		// outer radius
		translate([w1/2-t,w1/2-t,0]) circle(r=t);

		// corner block
		translate([w1/2-w3,w1/2-w3]) square([w3-t+eta,w3-t+eta]);

		// returns
		for (i=[0,1]) mirror([i,i,0]) {
			translate([w1/2-w2,w1/2-t,0]) square([w2-t,t-cham]);
			translate([w1/2-w2+cham,w1/2-cham-eta,0]) square([w2-t-cham,cham+eta]);
		}
	}
}

module aluProSide(sideType) {
	// x side
	w = sideType[0];
	t = sideType[1];
	translate([w/2-t-eta,-w/4,0]) square([t+eta,w/2]);	
}

module aluProHollow(cornerType) {
	// x hollow
	w1 = cornerType[0];
	t = cornerType[2];
	w3 = cornerType[4];	

	translate([w1/2,0]) square([2*w3 - 2*t, w1 - 2*t],center=true);
}

// TSlot - to be unioned onto a printed part for engaging tightly with the aluprofile
//  same centre and orientation as a full profile section, x+ side
// protrudes eta beyond external boundary of section to allow for union
// requires linear_extrude'ing
module aluProTSlot(profileType, $fn=8) {
	//BR_20x20_Corner = [20, 7, 1.5, 0.5, 4];
	//BR_20x20_Core = [9,2,0.75];
	
	coreType = profileType[1];
	cornerType = profileType[2];
	 
	w1 = cornerType[0];
	w2 = cornerType[1];
	t = cornerType[2];
	cham = cornerType[3];
	w3 = cornerType[4];	

	tol = 0.5;  // mm tolerance, total per gap

	slotW = w1- 2*w2 - tol;
	slotD = (w1 - coreType[0]) / 2 - tol;
	slotOffset = coreType[0]/2 + tol;
	
	wingW = w1 - 2*w3 - 4*tol;
	wingInset = t + tol/2;

	union() {	
		// central block
		translate([slotOffset,-slotW/2,0]) square([slotD+eta, slotW]);
	
		// wings
		for (i=[0,1]) mirror([0,i,0]) {
			polygon(points=[[slotOffset,slotW/2],[w1/2-w3/2-tol,wingW/2],[w1/2-wingInset,wingW/2],[w1/2-wingInset, slotW/2]], paths=[[0,1,2,3]]);
		}
	}
}

// TSlotLug - to be unioned onto a printed part for engaging tightly with the aluprofile slot
//  same centre and orientation as a full profile section, x+ side
// protrudes eta beyond external boundary of section to allow for union
// NB: solid part
module aluProTSlotLug(profileType, l=5, $fn=8) {
	//BR_20x20_Corner = [20, 7, 1.5, 0.5, 4];
	//BR_20x20_Core = [9,2,0.75];
	
	coreType = profileType[1];
	cornerType = profileType[2];
	 
	w1 = cornerType[0];
	w2 = cornerType[1];
	t = cornerType[2];
	cham = cornerType[3];
	w3 = cornerType[4];	

	tol = 0.5;  // mm tolerance, total per gap

	slotW = w1- 2*w2 - tol;
	slotD = (w1 - coreType[0]) / 2 - tol;
	slotD2 = l < slotD ? l : slotD;
	slotOffset = coreType[0]/2 + tol;
	
	wingW = w1 - 2*w3 - 4*tol;
	wingInset = t + tol/2;

	union() {	
		// central block
		translate([slotOffset,-slotW/2,0]) square([slotD2+eta, slotW]);
	}
}



module aluProBasicSection(profileType) {
	difference() {
		union() {
			aluProCore(profileType[1]);
			
			for (i=[0:3]) rotate([0,0,i*90]) {
				aluProCorner(profileType[2]);

				if (profileType[4][i] == 1)
					aluProSide(profileType[3]);
			}
		}
		aluProBore(profileType[0]);
	}
}

module aluProSection(profileType,detailed) {
	x = profileType[5];
	y = profileType[6];
	w = profileType[3][0];
	sx = -(x-1)*w/2;
	sy = -(y-1)*w/2;
	
	w1 = profileType[2][0];
	
	if (!detailed) {
		// simple rectangle
		square([w1 * x,w1 * y],center=true);
	
	} else {
		difference() {
			union() {
				for (i=[0:x-1])
					for (j=[0:y-1])
						translate([sx + w * i, sy + w * j,0]) aluProBasicSection(profileType);
			
				// fill-in sides
				if (y > 1)
					for (i=[0:y-2])
						for (j=[0,1]) 
							mirror([j,0,0])
								translate([sx + (x-1) * w/2, sy + i*w + w/2,0])
									aluProSide(profileType[3]);
			}

			// remove hollows
			if (y > 1)
				for (i=[0:y-2])
					for (j=[0,1]) 
						mirror([j,0,0])
							translate([sx + (x-1) * w/2, sy + i*w,0])
								rotate([0,0,90]) aluProHollow(profileType[2]);
		}
	}
		
}


module aluProExtrusion(profileType, l, detailed) {
	render()
	    translate([0,0,center?-l/2:0]) 
		linear_extrude(height=l)
		aluProSection(profileType, detailed=detailed);
}



// utility functions to generate common profiles with gussets
// set gusset array values to 1 to indicate where a gusset should be present
// numbering is anticlockwise from y+
module BR20x20WG(l=100, startGussets=[0,0,0,0], endGussets=[0,0,0,0], screws=true) {
	gussetType=BR_20x20_Gusset;
	profileType = BR_20x20;
	
	aluProExtrusion(profileType, l);
	
	// gussets
	for (i=[0:3]) {
		//start
		if (startGussets[i]==1)
			rotate([0,0,i*90]) 
			translate([0,10,0]) 
			aluProGusset(gussetType, screws=screws);
		
		
		//end
		if (endGussets[i]==1)
			rotate([0,0,i*90]) 
			translate([0,10,l]) 
			mirror([0,0,1])
			aluProGusset(gussetType, screws=screws);
	}
}

// same as above, but between points
module BR20x20WGBP(p1,p2,roll=0,startGussets=[0,0,0,0], endGussets=[0,0,0,0], screws=true) {
	v = subv(p2,p1);
	l = mod(v);
	translate(p1) orientate(v,roll=roll) BR20x20WG(l, startGussets, endGussets, screws);
}

// for 20x40...  gusset numbering is from y+ anticlockwise
module BR20x40WG(l=100, startGussets=[0,0,0,0,0,0], endGussets=[0,0,0,0,0,0], screws=true) {
	gussetType=BR_20x20_Gusset;
	profileType = BR_20x40;
	
	aluProExtrusion(profileType, l);
	
	// gussets
	
	for (i=[0,1]) {
	
		//y+
		if (i==0?startGussets[0]==1:endGussets[0]==1)
			translate([0,20,i==0?0:l]) 
			rotate([0,0,0])
			mirror([0,0,i]) 
			aluProGusset(gussetType, screws=screws);
	
	
		//y-
		if (i==0?startGussets[3]==1:endGussets[3]==1)
			translate([0,-20,i==0?0:l]) 
			rotate([0,0,180])
			mirror([0,0,i]) 
			aluProGusset(gussetType, screws=screws);
		
		// x-
		for (j=[0,1])
			if (i==0?startGussets[1+j]==1:endGussets[1+j]==1)
			translate([-10,10-j*20,i==0?0:l]) 
			rotate([0,0,90])
			mirror([0,0,i]) 
			aluProGusset(gussetType, screws=screws);
	
		// x+
		for (j=[0,1])
			if (i==0?startGussets[4+j]==1:endGussets[4+j]==1)
			translate([10,-10+j*20,i==0?0:l]) 
			rotate([0,0,270])
			mirror([0,0,i]) 
			aluProGusset(gussetType, screws=screws);
	
	}
}

// same as above, but between points
module BR20x40WGBP(p1,p2,roll=0,startGussets=[0,0,0,0,0,0], endGussets=[0,0,0,0,0,0], screws=true) {
	v = subv(p2,p1);
	l = mod(v);
	translate(p1) orientate(v,roll=roll) BR20x40WG(l, startGussets, endGussets, screws);
}




module aluProExtrusionBetweenPoints(p1,p2,profileType=BR_20x20,roll=0) {
	v = subv(p2,p1);
	l = mod(v);
	translate(p1) orientate(v,roll=roll) aluProExtrusion(profileType, l);
}



// width, wall_thickness, slot width, slot height, slot offset from base, nib depth
//BR_20x20_Gusset = [18, 3, 4.5, 7, 7.7, 1];

module aluProGusset(tg,screws=false) {
	// sits on z=0
	// faces along y+ and z+	
	
	w = tg[0];
	t = tg[1];
	slotw = tg[2];
	sloth = tg[3];
	sloto = tg[4];
	nib = tg[5];
	
	vitamin(str(tg[6],": ",tg[6]));
	
	color(grey80)
	render()
	union() {
		// ends
		for (i=[0,1])
			mirror([0,-i,i])
			linear_extrude(t) {
				difference() {
					translate([-w/2,0,0]) square([w,w]);
					translate([(-w/2+slotw)/2,sloto,0]) square([slotw,sloth]);
				}
			}
			
		// nibs - must add these at some point!
		
		//sides
		for (i=[0,1])
			mirror([i,0,0])
			translate([w/2-t/2,t,t])
			rotate([0,-90,0])
			right_triangle(width=w-t, height=w-t, h=t, center = true);
	}
	
	if (screws) {
		for (i=[0,1])
			mirror([0,-i,i]) {
				translate([0,12,t]) screw(M4_cap_screw,8);
				translate([0,12,0]) aluProTwistLockNut(BR_20x20_TwistLockNut);
			}
	}
}


//BR_20x20_TwistLockNut = [5.8,11.3,4,0.8,1.5];
// aligned such that the origin is level with the surface of the profile when the nut is locked
module aluProTwistLockNut(tlnt) {
	vitamin(str("AluExtTwistNut: Aluminium Extrusion Twist Nut"));

	if (simplify) {
		color("silver")
		render()
		translate([0,0,-tlnt[2] -tlnt[3] - (tlnt[4] - tlnt[3])])
		translate([0,0,(tlnt[2]-1)/2]) rotate([90,0,0]) trapezoidPrism(tlnt[1],tlnt[0],tlnt[2]-1,-(tlnt[1] - tlnt[0])/2,tlnt[0],center=true);
	
	} else {
		color("silver")
		render()
		translate([0,0,-tlnt[2] -tlnt[3] - (tlnt[4] - tlnt[3])]) 
		difference() {
			union() {
				translate([0,0,tlnt[2]-0.5-eta]) cube([tlnt[1],tlnt[0],1+2*eta],center=true);
				translate([0,0,(tlnt[2]-1)/2]) rotate([90,0,0]) trapezoidPrism(tlnt[1],tlnt[0],tlnt[2]-1,-(tlnt[1] - tlnt[0])/2,tlnt[0],center=true);
			
				translate([0,0,tlnt[3]/2 + tlnt[2]-eta]) cube([tlnt[0],tlnt[0],tlnt[3] + eta],center=true);
			}
	
			translate([0,0,-1]) cylinder(h=20, r=tlnt[2]/2, $fn=8);
		}
	}
}

module tslot_20x20_base(l,detailed){
	aluProExtrusion(BR_20x20, l=l, detailed=detailed);
}

module tslot_20x20_1s_base(l,detailed){
	aluProExtrusion(BR_20x20_1S, l=l, detailed=detailed);
}

module tslot_20x20_2s_base(l,detailed){
	aluProExtrusion(BR_20x20_2S, l=l, detailed=detailed);
}

module tslot_20x20_2sa_base(l,detailed){
	aluProExtrusion(BR_20x20_2SA, l=l, detailed=detailed);
}

module tslot_20x20_3s_base(l,detailed){
	aluProExtrusion(BR_20x20_3S, l=l, detailed=detailed);
}

//	aluProExtrusion(BR_20x40, l=70, center=false);
//	aluProExtrusion(BR_20x60, center=true);
// aluProExtrusion(BR_20x80, center=false);
