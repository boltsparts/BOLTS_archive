
module nut1(d1, s, m_max){
	//hex sidelength
	a = s/tan(60);
	difference(){
		hex_head(m_max,s);
		translate([0,0,-d1]) cylinder(r=d1/2,h=m_max+ 2*d1);
	}
}

module nut1_sketch(){
	union(){
		translate([0,0,0]){
			xz_view(0,false) nut1(4,7,2.2);
			vertical_measure_right([10,-2.2],2.2,4,["m"],1);
		}
		translate([0,10,0]){
			xy_view(-1,true) nut1(4,7,2.2);
			horizontal_measure_bottom([-3.5,-5],7,4,["s"],1);
			vertical_measure_right([10,-2],4,4,["d","1"],2);
		}
	}
}
