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
module washer1(d1,d2,s){
	difference(){
		cylinder(r=d2/2,h=s);
		translate([0,0,-0.1*s])
			cylinder(r=d1/2,h=1.2*s);
	}
}

module washer2(d1,d2,s){
	intersection(){
		difference(){
			cylinder(r=d2/2,h=s);
			translate([0,0,-0.1*s])
				cylinder(r=d1/2,h=1.2*s);
			cylinder(r1=d1/2-s,r2 = d1/2+s,1.1*s);
		}
		cylinder(r1 = d2/2+s, r2 = d2/2-s,1.1*s);
	}
}

function washerConn(d2,s,location) =
	(location == "bottom") ? [[0,0,0],[[0,0,1],[0,1,0]]] :
	(location == "top")    ? [[0,0,s],[[0,0,1],[0,1,0]]] :
	(location == "outer")  ? [[d2/2,0,0],[[1,0,0],[0,1,0]]] :
	"Error";
