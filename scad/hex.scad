module hex1(d1,k,s,h,l){
	//hex sidelength
	a = s/tan(60);
	union(){
		//hex head
		cube([a,s,k],true);
		rotate([0,0,120]) cube([a,s,k],true);
		rotate([0,0,240]) cube([a,s,k],true);
		//possibly unthreaded shaft
		cylinder(r=d1/2,h=k+h);
		//threaded shaft
		color(thread_color) translate([0,0,k+h]) cylinder(r=d1/2,h= l-h);
	}
}

module hex2(d1, k, s, b1, b2, b3, l){
	b = (l < 125) ? b1 :
		(l < 200) ? b2 :
		b3;
	if(b == "None"){
		echo("Warning! Unspecified dimension encountered");
	}

	//hex sidelength
	a = s/tan(60);

	union(){
		//hex head
		cube([a,s,k],true);
		rotate([0,0,120]) cube([a,s,k],true);
		rotate([0,0,240]) cube([a,s,k],true);
		//unthreaded shaft
		cylinder(r=d1/2,h=k+l-b);
		//threaded shaft
		color([255,0,0]) translate([0,0,k+l-b]) cylinder(r=d1/2,h= b);
	}
}

