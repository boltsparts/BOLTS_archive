// 2D sketches must be in the z=0 plane and should be arranged as follows
//              top (xy+)
// side left    front (xz)    side right     back side
//              bottom (xy-)

module origin(){
	polygon(points=[[-1,-0.01],[-1,0.01],[-0.01,0.01],[-0.01,1],[0.01,1],[0.01,0.01],[1,0.01],[1,-0.01],[0.01,-0.01],[0.01,-1],[-0.01,-1],[-0.01,-0.01]],paths=[[0,1,2,3,4,5,6,7,8,9,10,11]],convexity=6);
}

//views
//a view maps a coordinate plane
module xz_view(offset, cut){
	difference(){
		union(){
			projection(cut=cut)
			translate([0,0,-offset])
			rotate([-90,0,0])
			child(0);
		}
		origin();	}
}
module xy_view(offset, cut){
	difference(){
		union(){
			projection(cut=cut)
			translate([0,0,-offset])
			child(0);
		}
		origin();
	}
}

module yz_view(offset, cut){
	difference(){
		union(){
			projection(cut=cut)
			translate([0,0,offset])
			rotate([-90,0,0])
			rotate([0,0,-90])
			child(0);
		}
		origin();
	}
}


//Measures

//x and y coordinates for start and end
module vertical_measure_left(start, length, width, label, label_count){
	translate(start){
		union(){
			polygon(points=[[-width/2,0],[width/2,0],[width/2,0.01],[0.01,0.01],[0.01,length-0.01],[width/2,length-0.01],[width/2,length],[-width/2,length],[-width/2,length-0.01],[-0.01,length-0.01],[-0.01,0.01],[-width/2,0.01]],paths=[[0,1,2,3,4,5,6,7,8,9,10,11]],convexity=4);
			translate([-width,length/2])
			rotate([0,0,-90])
			projection(true)
			8bit_str(label,label_count,0.3,1.0);
		}
	}
}

module vertical_measure_right(start, length, width, label, label_count){
	translate(start){
		union(){
			polygon(points=[[-width/2,0],[width/2,0],[width/2,0.01],[0.01,0.01],[0.01,length-0.01],[width/2,length-0.01],[width/2,length],[-width/2,length],[-width/2,length-0.01],[-0.01,length-0.01],[-0.01,0.01],[-width/2,0.01]],paths=[[0,1,2,3,4,5,6,7,8,9,10,11]],convexity=4);
			translate([width,length/2])
			rotate([0,0,-90])
			projection(true)
			8bit_str(label,label_count,0.3,1.0);
		}
	}
}

//x and y coordinates for start and end
module horizontal_measure_bottom(start, length, width, label, label_count){
	translate(start){
		union(){
			polygon(points=[[0,-width/2],[0,width/2],[0.01,width/2],[0.01,0.01],[length-0.01,0.01],[length-0.01,width/2],[length,width/2],[length,-width/2],[length-0.01,-width/2],[length-0.01,-0.01],[0.01,-0.01],[0.01,-width/2]],paths=[[0,1,2,3,4,5,6,7,8,9,10,11]],convexity=4);
			//label
			translate([length/2,-width])
			rotate([0,0,-90])
			projection(true)
			8bit_str(label,label_count,0.3,1.0);
		}
	}
}

module horizontal_measure_top(start, length, width, label, label_count){
	translate(start){
		union(){
			polygon(points=[[0,-width/2],[0,width/2],[0.01,width/2],[0.01,0.01],[length-0.01,0.01],[length-0.01,width/2],[length,width/2],[length,-width/2],[length-0.01,-width/2],[length-0.01,-0.01],[0.01,-0.01],[0.01,-width/2]],paths=[[0,1,2,3,4,5,6,7,8,9,10,11]],convexity=4);
			//label
			translate([length/2,width])
			rotate([0,0,-90])
			projection(true)
			8bit_str(label,label_count,0.3,1.0);
		}
	}
}

