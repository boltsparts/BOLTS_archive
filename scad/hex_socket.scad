module hex_socket1(d1,d2,b1,b2,b3,k_max,s,t,L,h_max,l){
	b = l < 125 ? b1 :
		l < 200 ? b2 :
		b3;

	//TODO: These checks are not very careful
	if(b == "None"){
		echo("Error: Unspecified threading length");
	}
	if(t == "None"){
		echo("Error: Unspecified socket depth");
	}

	if(h_max == "None"){
		echo("Error: Unspecified unthreaded length");
	}

	h = (l <= L) ? h_max : l - k_max - b;

	//hex sidelength
	a = s/tan(60);

	difference(){
		union(){
			//Head
			cylinder(r1=d2/2,r2=d1/2,h = k_max);
			//unthreaded shaft
			cylinder(r=d1/2,h=k_max+h);
			//threaded shaft
			color([255,0,0]) translate([0,0,k_max+h]) cylinder(r=d1/2,h= b);
		}
		union(){
			//hex hole
			cube([a,s,t],true);
			rotate([0,0,120]) cube([a,s,t],true);
			rotate([0,0,240]) cube([a,s,t],true);
		}
	}
}


module hex_socket2(d1,d2,b,k,s,t_min,L,l){
	h = (l<= L) ? 0 : l- b;

	//hex sidelength
	a = s/tan(60);

	difference(){
		union(){
			//Head
			cylinder(r=d2/2,h = k);
			//unthreaded shaft
			cylinder(r=d1/2,h=k+h);
			//threaded shaft
			color([255,0,0]) translate([0,0,k+h]) cylinder(r=d1/2,h= b);
		}
		union(){
			//hex hole
			cube([a,s,t_min],true);
			rotate([0,0,120]) cube([a,s,t_min],true);
			rotate([0,0,240]) cube([a,s,t_min],true);
		}
	}
}

