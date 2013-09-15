module check_dimension_defined(dim, descr){
	if(dim == "None"){
		echo("Error: Unspecified ",descr);
	}
}

module check_dimension_positive(dim, message){
	if(dim < 0){
		echo(message);
	}
}


module thread_external(d1,l){
	if(BOLTS_MODE == "sketch"){
		translate([0,0,0.01])
		color(BOLTS_THREAD_COLOR) difference() {
			cylinder(r=0.5*d1,h= l-0.01);
			translate([0,0,0.01]) cylinder(r=0.4*d1,h= l-0.03);
		}
	} else {
		color(BOLTS_THREAD_COLOR)
		cylinder(r=0.5*d1,h= l);
	}
}

module hex_head(k,s){
	a = s/tan(60);
	translate([0,0,-k/2]) union(){
		rotate([0,0, 30]) cube([a,s,k],true);
		rotate([0,0,150]) cube([a,s,k],true);
		rotate([0,0,270]) cube([a,s,k],true);
	}
}

module hex_socket_neg(t,s){
	a = s/tan(60);
	//The fudging here is to avoid coincident faces wehn subtracting from a
	//body (see e.g. hex_socket)
	translate([0,0,t/2-0.01]) union(){
		rotate([0,0, 30]) cube([a,s,t+0.01],true);
		rotate([0,0,150]) cube([a,s,t+0.01],true);
		rotate([0,0,270]) cube([a,s,t+0.01],true);
	}
}
