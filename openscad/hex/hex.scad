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
module hex1(d1,k,s,h,l){
	union(){
		BOLTS_hex_head(k,s);
		//possibly unthreaded shaft
		cylinder(r=d1/2,h=h);
		//threaded shaft
		translate([0,0,h]) BOLTS_thread_external(d1,l-h);
	}
}

module hex2(d1, k, s, b1, b2, b3, l){
	b = (l < 125) ? b1 :
		(l < 200) ? b2 :
		b3;
	BOLTS_check_dimension_defined(b, "threaded shaft length b");

	union(){
		BOLTS_hex_head(k,s);
		//unthreaded shaft
		cylinder(r=d1/2,h=l-b);
		//threaded shaft
		translate([0,0,l-b]) BOLTS_thread_external(d1,b);
	}
}

function hexConn(k,l,location) = 
	(location == "root") ? [[0,0,0],[[0,0,1],[0,1,0]]] :
	(location == "tip") ? [[0,0,l],[[0,0,1],[0,1,0]]] :
	(location == "head") ? [[0,0,-k],[[0,0,-1],[0,-1,0]]] :
	"Error";
