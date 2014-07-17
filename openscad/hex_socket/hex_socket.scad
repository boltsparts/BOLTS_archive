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
module hex_socket1(d1,d2,b1,b2,b3,k_max,s,t,L,h_max,l){
	b = (l <= L) ? l - k_max - h_max : 
		l < 125 ? b1 :
		l < 200 ? b2 :
		b3;
	h = l - k_max - b;

	//TODO: These checks are not very careful
	BOLTS_check_dimension_defined(b,"threaded shaft length b");
	BOLTS_check_dimension_defined(t,"socket depth t");
	BOLTS_check_dimension_defined(h_max,"unthreaded shaft length h_max");

	difference(){
		union(){
			//Head
			cylinder(r1=d2/2,r2=d1/2,h = k_max);
			//unthreaded shaft
			cylinder(r=d1/2,h=k_max+h);
			//threaded shaft
			translate([0,0,k_max+h]) BOLTS_thread_external(d1,b);
		}
		BOLTS_hex_socket_neg(t,s);
	}
}

module hex_socket2(d1,d2,b,k,s,t_min,L,l){
	h = (l<= L) ? 0 : l - b;

	BOLTS_check_dimension_positive(h,"l too short");

	difference(){
		union(){
			//Head
			translate([0,0,-k]) cylinder(r=d2/2,h = k);
			//unthreaded shaft
			cylinder(r=d1/2,h=h);
			//threaded shaft
			translate([0,0,h]) BOLTS_thread_external(d1,b);
		}
		translate([0,0,-k]) BOLTS_hex_socket_neg(t_min,s);
	}
}

