
module nut1(d1, s, m_max){
	//hex sidelength
	a = s/tan(60);
	difference(){
		union(){
			//hex head
			cube([a,s,m_max],true);
			rotate([0,0,120]) cube([a,s,m_max],true);
			rotate([0,0,240]) cube([a,s,m_max],true);
		}
		translate([0,0,-d1]) cylinder(r=d1/2,h=m_max+ 2*d1);
	}
}
