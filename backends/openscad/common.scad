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

module BOLTS_error(msg){
	echo(str("BOLTS Error: ",msg));
}

module BOLTS_warning(msg){
	echo(str("BOLTS Warning: ",msg));
}


module BOLTS_check_dimension_defined(dim, descr){
	if(dim == "None"){
		BOLTS_error(str("Dimension unspecified",descr));
	}
}

module BOLTS_check_dimension_positive(dim, message){
	if(dim < 0){
		BOLTS_error(message);
	}
}

function BOLTS_convert_to_default_unit(value,unit) =
	(BOLTS_DEFAULT_UNIT == unit) ? value :
		(unit == "in") ? value*25.4 :
			value/25.4;

function get_dim(dims,pname) = dims[search([pname],dims,1)[0]][1];

//see http://rocklinux.net/pipermail/openscad/2013-September/005522.html
function type(P) =
	(len(P) == undef)
	?	(P == true || P == false)
		? "boolean"
		: (P == undef)
			? "undef"
			: "number"
	:	(P + [1] == undef)
		?	"string"
		:	"vector";

module BOLTS_check_parameter_type(part_name,name,value,param_type){
	if(param_type=="Length (mm)"){
		if(type(value) != "number"){
			BOLTS_error(str("Expected a Length (mm) as parameter ",name," for ",part_name,", but ",value," is not numerical"));
		} else if(value < 0){
			BOLTS_error(str("Expected a Length (mm) as parameter ",name," for ",part_name,", but ",value," is negative"));
		}
	} else if(param_type=="Length (in)"){
		if(type(value) != "number"){
			BOLTS_error(str("Expected a Length (in) as parameter ",name," for ",part_name,", but ",value," is not numerical"));
		} else if(value < 0){
			BOLTS_error(str("Expected a Length (in) as parameter ",name," for ",part_name,", but ",value," is negative"));
		}
	} else if(param_type=="Number"){
		if(type(value) != "number"){
			BOLTS_error(str("Expected a Number as parameter ",name," for ",part_name,", but ",value," is not numerical"));
		}
	} else if(param_type=="Bool"){
		if(type(value) != "boolean"){
			BOLTS_error(str("Expected a Bool as parameter ",name," for ",part_name,", but ",value," is not boolean"));
		}
	} else if(param_type=="Table Index"){
		if(type(value) != "string"){
			BOLTS_error(str("Expected a Table Index as parameter ",name," for ",part_name,", but ",value," is not a string"));
		}
	} else if(param_type=="String"){
		if(type(value) != "string"){
			BOLTS_error(str("Expected a String as parameter ",name," for ",part_name,", but ",value," is not a string"));
		}
	} else {
		BOLTS_error(str("Unknown type in parameter check. This should not happen, please report this bug to BOLTS"));
	}
}


module BOLTS_thread_external(d1,l){
	color(BOLTS_THREAD_COLOR)
		cylinder(r=0.5*d1,h= l);
}

module BOLTS_hex_head(k,s){
	a = s/tan(60);
	translate([0,0,-k/2]) union(){
		rotate([0,0, 30]) cube([a,s,k],true);
		rotate([0,0,150]) cube([a,s,k],true);
		rotate([0,0,270]) cube([a,s,k],true);
	}
}

module BOLTS_hex_socket_neg(t,s){
	a = s/tan(60);
	//The fudging here is to avoid coincident faces when subtracting from a
	//body (see e.g. hex_socket)
	translate([0,0,t/2-0.01]) union(){
		rotate([0,0, 30]) cube([a,s,t+0.01],true);
		rotate([0,0,150]) cube([a,s,t+0.01],true);
		rotate([0,0,270]) cube([a,s,t+0.01],true);
	}
}
