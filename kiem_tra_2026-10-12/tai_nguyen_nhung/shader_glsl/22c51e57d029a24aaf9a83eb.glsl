float luminance( const in vec3 rgb ) {
	const vec3 weights = vec3( ${e}, ${t}, ${n} );
	return dot( weights, rgb );
}