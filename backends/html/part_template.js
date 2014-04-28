var camera, controls, scene, renderer;
function attach_renderer(target) {

	var SCREEN_WIDTH = 300, SCREEN_HEIGHT = 300;
	var VIEW_ANGLE = 35, ASPECT = SCREEN_WIDTH / SCREEN_HEIGHT, NEAR = 0.1, FAR = 20000;

	renderer = new THREE.WebGLRenderer();
	renderer.setSize( SCREEN_WIDTH, SCREEN_HEIGHT );
	target.appendChild( renderer.domElement );

	scene = new THREE.Scene();
	camera = new THREE.PerspectiveCamera(
		VIEW_ANGLE, // Field of view
		ASPECT, // Aspect ratio
		NEAR, // Near plane
		FAR // Far plane
	);
	$CameraData // placeholder for the FreeCAD camera
	controls = new THREE.TrackballControls( camera );

	controls.rotateSpeed = 1.0;
	controls.zoomSpeed = 1.2;
	controls.panSpeed = 0.8;
	controls.noZoom = false;
	controls.noPan = false;
	controls.staticMoving = true;
	controls.dynamicDampingFactor = 0.3;
	controls.keys = [ 65, 83, 68 ];

	$ObjectsData // placeholder for the FreeCAD objects

	var light = new THREE.PointLight( 0xFFFF00 );
	light.position.set( -10000, -10000, 10000 );
	scene.add( light );
	renderer.render( scene, camera );
	animate();
};

function animate(){
	requestAnimationFrame( animate );
	render();
};

function render(){
	controls.update();
	renderer.render( scene, camera );
};
