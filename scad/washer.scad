module washer(d1,d2,s,chamfer){
	echo(d1,d2,s,chamfer);
	intersection(){
		difference(){
			cylinder(r=d2/2,h=s);
			translate([0,0,-0.1*s])
				cylinder(r=d1/2,h=1.2*s);
			if(chamfer){
				cylinder(r1=d1/2-s,r2 = d1/2+s,1.1*s);
			}
		}
		if(chamfer){
			cylinder(r1 = d2/2+s, r2 = d2/2-s,1.1*s);
		}
	}
}

