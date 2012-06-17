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

module hex_socket1_sketch(){
	union(){
		translate([0,0,0]){
			xz_view(0,true) hex_socket1(4,8,14,"None","None",2.3, 2.5,1.8,30, 4.4, 20);
			vertical_measure_right([7,0],2.3,4,["k","m","a","x"],4);
			vertical_measure_right([7,2.3],4.4,4,["h","m","a","x"],4);
			vertical_measure_left([-15,0],20,4,["L"],1);
			vertical_measure_left([-7,0],1.8,4,["t"],1);
		}
		translate([0,25,0]){
			xy_view(2.5, true) hex_socket1(4,8,14,"None","None",2.3, 2.5,1.8,30, 4.4, 20);
			horizontal_measure_top([-2,5],4,4,["d","0"], 2);
		}
		translate([0,-10,0]){
			xy_view(0.01,true) hex_socket1(4,8,14,"None","None",2.3, 2.5,1.8,30, 4.4, 20);
			horizontal_measure_top([-1.25,6],2.5,4,["s"], 1);
			horizontal_measure_bottom([-4,-5],8,4,["d","2"], 2);
		}
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

module hex_socket2_sketch(){
	union(){
		translate([0,0,0]){
			xz_view(0,true) hex_socket2(4,7,20,4,3,2,25,30);
			vertical_measure_left([-10,0],30,4,["l"],1);
			vertical_measure_left([-10,-4],2,4,["t","m","i","n"],4);
			vertical_measure_right([10,10],20,4,["b"],1);
			vertical_measure_right([10,-4],4,4,["k"],1);
		}
		translate([0,35,0]){
			xy_view(2.5, true) hex_socket2(4,7,20,4,3,2,25,30);
			horizontal_measure_top([-2,5],4,4,["d","0"], 2);
		}
		translate([0,-15,0]){
			xy_view(-3,true) hex_socket2(4,7,20,4,3,2,25,30);
			horizontal_measure_top([-1.25,6],2.5,4,["s"], 1);
			horizontal_measure_bottom([-3.5,-5],7,4,["d","2"], 2);
		}
	}
}
