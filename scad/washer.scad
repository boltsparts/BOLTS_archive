module washer1(d1,d2,s){
	difference(){
		cylinder(r=d2/2,h=s);
		translate([0,0,-0.1*s])
			cylinder(r=d1/2,h=1.2*s);
	}
}

module washer1_sketch(){
	union(){
		translate([0,0,0]){
			xz_view(0,true) washer1(4.3,9,0.8);
			vertical_measure_right([10,0],0.8,4,["s"],1);
		}
		translate([0,10,9]){
			xy_view(0.4,true) washer1(4.3,9,0.8);
			vertical_measure_right([10,-2.15],4.3,4,["d","1"],2);
			vertical_measure_right([-10,-4.5],9,4,["d","1"],2);
		}
	}
}

module washer2(d1,d2,s){
	intersection(){
		difference(){
			cylinder(r=d2/2,h=s);
			translate([0,0,-0.1*s])
				cylinder(r=d1/2,h=1.2*s);
			cylinder(r1=d1/2-s,r2 = d1/2+s,1.1*s);
		}
		cylinder(r1 = d2/2+s, r2 = d2/2-s,1.1*s);
	}
}

module washer2_sketch(){
	union(){
		translate([0,0,0]){
			xz_view(0,true) washer2(4.3,9,0.8);
			vertical_measure_right([10,0],0.8,4,["s"],1);
		}
		translate([0,10,9]){
			xy_view(0.4,true) washer2(4.3,9,0.8);
			vertical_measure_right([10,-2.15],4.3,4,["d","1"],2);
			vertical_measure_right([-10,-4.5],9,4,["d","1"],2);
		}
	}
}
