module hex1(d1,k,s,h,l){
	//hex sidelength
	a = s/tan(60);
	union(){
		//hex head
		translate([0,0,-k/2]) union(){
			rotate([0,0, 30]) cube([a,s,k],true);
			rotate([0,0,150]) cube([a,s,k],true);
			rotate([0,0,270]) cube([a,s,k],true);
		}
		//possibly unthreaded shaft
		cylinder(r=d1/2,h=h);
		//threaded shaft
		color(thread_color) translate([0,0,h]) cylinder(r=d1/2,h= l-h);
	}
}

module hex1_sketch(){
	union(){
		translate([0,0,0]){
			xz_view(0,true) hex1(4,2.8,7,2.1,15);
			vertical_measure_right([10,-2.8], 2.8, 4, ["k"], 1);
			vertical_measure_right([10,0], 2.1, 4, ["h"], 1);
			vertical_measure_left([-10,0], 15, 4, ["l"], 1);
		}
		translate([0,20,0]){
			xy_view(5, true) hex1(4,2.8,7,2.1,15);
			horizontal_measure_top([-2,5],4,4, ["d","0"], 2);
		}
		translate([0,-10,0]){
			xy_view(-2, true) hex1(4,2.8,7,2.1,15);
			horizontal_measure_bottom([-3.5,-7],7,4, ["s"], 1);
		}
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

