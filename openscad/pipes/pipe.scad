/* Pipe module for OpenSCAD
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

module pipe(id,od,l){
	difference(){
		cylinder(r=od/2,h=l,center=true);
		cylinder(r=id/2,h=l+1,center=true);
	}
}

module pipe_wall(od,wall,l){
	difference(){
		cylinder(r=od/2,h=l,center=true);
		cylinder(r=(od - 2*wall)/2,h=l+1,center=true);
	}
}

function pipeConn(l,location) =
	(location == "front-in")  ? [[0,0,-l/2],[[0,0,1],[1,0,0]]] :
	(location == "front-out") ? [[0,0,-l/2],[[0,0,-1],[-1,0,0]]] :
	(location == "back-in")   ? [[0,0,+l/2],[[0,0,-1],[-1,0,0]]] :
	(location == "back-out")  ? [[0,0,+l/2],[[0,0,1],[1,0,0]]] :
	"Error";
	
