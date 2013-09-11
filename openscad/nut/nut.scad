
module nut1(d1, s, m_max){
	//hex sidelength
	a = s/tan(60);
	difference(){
		hex_head(m_max,s);
		translate([0,0,-d1]) cylinder(r=d1/2,h=m_max+ 2*d1);
	}
}
