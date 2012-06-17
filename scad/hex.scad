module hex1(d1,k,s,h,l){
	union(){
		hex_head(k,s);
		//possibly unthreaded shaft
		cylinder(r=d1/2,h=h);
		//threaded shaft
		translate([0,0,h]) thread_external(d1,l-h);
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
	check_dimension_defined(b, "threaded shaft length");

	union(){
		hex_head(k,s);
		//unthreaded shaft
		cylinder(r=d1/2,h=l-b);
		//threaded shaft
		translate([0,0,l-b]) thread_external(d1,b);
	}
}

module hex2_sketch(){
	union(){
		translate([0,0,0]){
			xz_view(0,true) hex2(4.,2.8,7,14,"None","None",20);
			vertical_measure_right([10,-2.8], 2.8, 4, ["k"], 1);
			vertical_measure_right([10,6], 14, 4, ["b"], 1);
			vertical_measure_left([-10,0], 20, 4, ["l"], 1);
		}
		translate([0,25,0]){
			xy_view(5, true) hex2(4.,2.8,7,14,"None","None",20);
			horizontal_measure_top([-2,5],4,4, ["d","0"], 2);
		}
		translate([0,-10,0]){
			xy_view(-2, true) hex2(4.,2.8,7,14,"None","None",20);
			horizontal_measure_bottom([-3.5,-7],7,4, ["s"], 1);
		}
	}
}

