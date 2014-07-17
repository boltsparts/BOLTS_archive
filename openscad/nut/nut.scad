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
module nut1(d1, s, m_max){
	//hex sidelength
	a = s/tan(60);
	translate([0,0,m_max]){
		difference(){
			BOLTS_hex_head(m_max,s);
			translate([0,0,-d1]) cylinder(r=d1/2,h=m_max+ 2*d1);
		}
	}
}

function nutConn(m_max,location) =
	(location == "bottom") ? [[0,0,0],[[0,0,1],[0,1,0]]] :
	(location == "top")    ? [[0,0,m_max],[[0,0,1],[0,1,0]]] :
	"Error";
