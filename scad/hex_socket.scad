module hex_socket1(d1,d2,b1,b2,b3,k_max,s,t,L,h_max,l){
	b = (l <= L) ? l - k_max - h_max : 
		l < 125 ? b1 :
		l < 200 ? b2 :
		b3;
	h = l - k_max - b;

	//TODO: These checks are not very careful
	check_dimension_defined(b,"threaded shaft length");
	check_dimension_defined(t,"socket depth");
	check_dimension_defined(h_max,"unthreaded shaft length");

	difference(){
		union(){
			//Head
			cylinder(r1=d2/2,r2=d1/2,h = k_max);
			//unthreaded shaft
			cylinder(r=d1/2,h=k_max+h);
			//threaded shaft
			translate([0,0,k_max+h]) thread_external(d1,b);
		}
		hex_socket_neg(t,s);
	}
}

module hex_socket2(d1,d2,b,k,s,t_min,L,l){
	h = (l<= L) ? 0 : l - b;

	check_dimension_positive(h,"l too short");

	difference(){
		union(){
			//Head
			translate([0,0,-k]) cylinder(r=d2/2,h = k);
			//unthreaded shaft
			cylinder(r=d1/2,h=h);
			//threaded shaft
			translate([0,0,h]) thread_external(d1,b);
		}
		translate([0,0,-k]) hex_socket_neg(t_min,s);
	}
}

