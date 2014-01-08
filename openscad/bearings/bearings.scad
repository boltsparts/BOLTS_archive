/*
 * BOLTS - Open Library of Technical Specifications
 * Copyright (C) 2013 Johannes Reinhardt <jreinhardt@ist-dein-freund.de>
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2.1 of the License, or any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
 */

//square torus, r1 is big radius, r2 is small radius
module makeSquorus(r1,r2){
	difference(){
		cylinder(r=r1+r2,h=2*r2,center=true);
		cylinder(r=r1-r2,h=3*r2,center=true);
	}
}

//r1 is inner, r2 is outer
module makeRing(r1,r2,h){
	difference(){
		cylinder(r=r2,h=h,center=true);
		cylinder(r=r1,h=2*h,center=true);
	}
}

module singlerowradialbearing(d1,d2,B){
	rb = B/4;
	n = ceil((d2-d1)/rb);
	translate([0,0,B/2]){
		union(){
			difference(){
				cylinder(r=d2/2,h=B,center=true);
				cylinder(r=d1/2,h=B+0.01,center=true);
				//gap
				makeRing(d1/2+0.3*(d2-d1)/2,d1/2+0.6*(d2-d1)/2,2*B);
				//track
				makeSquorus((d2-d1)/2,rb);
			}
			for ( i = [0 : n-1] ){
				rotate( i * 360 / n, [0, 0,1])
				translate([0, (d2-d1)/2, 0])
					sphere(r = rb);
			}
		}
	}
}

module axialthrustbearing(d1_w,d2_w,d1_g,d2_g,B){
	rb = B/4;
	n = ceil((d2_w+d1_w)/2/rb);
	union(){
		difference(){
			union(){
				translate([0,0,-0.35*B]) makeRing(d1_g/2,d2_g/2,0.3*B);
				translate([0,0,+0.35*B]) makeRing(d1_w/2,d2_w/2,0.3*B);
			}
			//track
			makeSquorus((d2_w+d1_w)/4,rb);
		}
		for ( i = [0 : n-1] ){
			rotate( i * 360 / n, [0, 0,1])
			translate([0, (d2_w+d1_w)/4, 0])
				sphere(r = rb);
		}
	}
}
