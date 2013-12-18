/*
Copyright (c) 2013 Johannes Reinhardt <jreinhardt@ist-dein-freund.de>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
*/

/*
local.scad local coordinate systems for OpenSCAD

for more information, see https://github.com/jreinhardt/local-scad
*/

//a few utility functions
function norm(a) = sqrt(a*a);
function unit_vector(v) = v/norm(v);
function clamp(v,lower_bound,upper_bound) = min(max(v,lower_bound),upper_bound);
function cross_product(a,b) = [
	a[1]*b[2]-a[2]*b[1],
	a[2]*b[0]-a[0]*b[2],
	a[0]*b[1]-a[1]*b[0]
];

//works for both numbers and vectors
function almost_equal(number, ref, tol) = sqrt((number-ref)*(number-ref)) < tol;

function _rotation_angle(a,b) = (a*b > 0) ? 
	asin(clamp(norm(cross_product(b,a))/norm(a)/norm(b),-1,1)) :
	180 - asin(clamp(norm(cross_product(b,a))/norm(a)/norm(b),-1,1));

//The (non-unit) rotation axis and angle around which a has to be rotated to be colinear to b
function calculate_rotation_axis(a,b) =
	//if the two vectors are not colinear find a rotation axis using the cross product
	(norm(cross_product(b,a)) != 0) ? [unit_vector(cross_product(b,a)),_rotation_angle(a,b)] :
	//if they are colinear and do not lie in the yz plane, choose the rotation axis from the yz plane
	(a*[1,0,0] < 0) ? [unit_vector([0,-a[1],+a[0]]),acos(clamp(a*b/norm(a)/norm(b),-1,1))] :
	(a*[1,0,0] > 0) ? [unit_vector([0,+a[1],-a[0]]),acos(clamp(a*b/norm(a)/norm(b),-1,1))] :
	//otherwise use the x axis
	[[1,0,0],acos(clamp(a*b/norm(a)/norm(b),-1,1))];

function calculate_axes(x,y) = [unit_vector(x),unit_vector(y), unit_vector(cross_product(x,y))];

function new_cs(origin=[0,0,0],axes=[[1,0,0],[0,1,0],[0,0,1]]) = (len(axes) == 2) ?
	[origin,calculate_axes(axes[0],axes[1])] :
	is_orthonormal([origin,axes]) ?
		[origin,axes] :
		"Error: Axes are not orthonormal";

function is_orthonormal(cs,tol=1e-3) =
	(almost_equal(norm(cs[1][0]),1,tol)) &&
	(almost_equal(norm(cs[1][1]),1,tol)) &&
	(almost_equal(norm(cs[1][2]),1,tol)) &&
	(almost_equal(cross_product(cs[1][0],cs[1][1]),cs[1][2],tol)) &&
	(almost_equal(cross_product(cs[1][1],cs[1][2]),cs[1][0],tol)) &&
	(almost_equal(cross_product(cs[1][2],cs[1][0]),cs[1][1],tol));

function unit_matrix3() = [
[1,0,0],
[0,1,0],
[0,0,1]];

function tensor_product_matrix3(u,v) = [
[u[0]*v[0], u[0]*v[1], u[0]*v[2]],
[u[1]*v[0], u[1]*v[1], u[1]*v[2]],
[u[2]*v[0], u[2]*v[1], u[2]*v[2]]];

function cross_product_matrix3(v) = [
[   0 , -v[2], +v[1]],
[+v[2],    0 , -v[0]],
[-v[1],  v[0],    0 ]];

function rotation_matrix3(n,angle) =
	cos(angle)*unit_matrix3() +
	sin(angle)*cross_product_matrix3(n) +
	(1-cos(angle))*tensor_product_matrix3(n,n);

//the modules are used directly by the user
module show_cs(cs){
	origin = cs[0];
	axes = cs[1];
	x_rot = calculate_rotation_axis(axes[0],[0,0,1]);
	y_rot = calculate_rotation_axis(axes[1],[0,0,1]);
	z_rot = calculate_rotation_axis(axes[2],[0,0,1]);
	translate(origin){
		color("Gray") sphere(0.2);
		rotate(x_rot[1],x_rot[0]) color("Red") cylinder(r=0.1,h=norm(axes[0]));
		rotate(y_rot[1],y_rot[0]) color("Green") cylinder(r=0.1,h=norm(axes[1]));
		rotate(z_rot[1],z_rot[0]) color("Blue") cylinder(r=0.1,h=norm(axes[2]));
	}
}

module translate_local(cs,v=[0,0,0]){
	origin = cs[0];
	axes = cs[1];
	x_rot = calculate_rotation_axis(axes[0],[1,0,0]);
	y_rot = calculate_rotation_axis(axes[1],
		rotation_matrix3(x_rot[0],x_rot[1])*[0,1,0]);
	translate(origin+v*axes){
		//align y axes
		rotate(y_rot[1],y_rot[0]){
			//align x axes
			rotate(x_rot[1],x_rot[0]){
				child(0);
			}
		}
	}
}

module in_cs(cs){
	origin = cs[0];
	axes = cs[1];
	x_rot = calculate_rotation_axis(axes[0],[1,0,0]);
	y_rot = calculate_rotation_axis(axes[1],
		rotation_matrix3(x_rot[0],x_rot[1])*[0,1,0]);
	translate(origin){
		//align y axes
		rotate(y_rot[1],y_rot[0]){
			//align x axes
			rotate(x_rot[1],x_rot[0]){
				child(0);
			}
		}
	}
}

module align(cs, cs_dst, displacement=[0,0,0]){
	x_rot = calculate_rotation_axis(cs[1][0],cs_dst[1][0]);
	y_rot = _rotation_angle(cs[1][1],
		rotation_matrix3(x_rot[0],x_rot[1])*cs_dst[1][1]);
	translate(cs_dst[0]+displacement*cs_dst[1])
		//align x axes
		rotate(-x_rot[1],x_rot[0])
				//align y axes
				rotate(-y_rot,cs[1][0])
				translate(-cs[0])
					child(0);
}


