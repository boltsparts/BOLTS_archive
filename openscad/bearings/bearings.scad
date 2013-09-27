module singlerowradialbearing(d1,d2,B){
	translate([0,0,B/2]){
		difference(){
			cylinder(r=d2/2,h=B,center=true);
			cylinder(r=d1/2,h=B+0.01,center=true);
		}
	}
}

module axialthrustbearing(d1,d2,B){
	translate([0,0,B/2]){
		difference(){
			cylinder(r=d2/2,h=B,center=true);
			cylinder(r=d1/2,h=B+0.01,center=true);
		}
	}
}
