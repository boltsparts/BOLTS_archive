module hex1(d1,k,s,h,l){
	union(){
		hex_head(k,s);
		//possibly unthreaded shaft
		cylinder(r=d1/2,h=h);
		//threaded shaft
		translate([0,0,h]) thread_external(d1,l-h);
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

