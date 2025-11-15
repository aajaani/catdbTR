// idea:
// get exports from gen types @ "@/gen_types/sdk.gen"
// add a middleware error wrapper for each export key
// on unauthorized, push to login page

import * as sdk from "@/gen_types/sdk.gen.ts";
import router from "@/router/index.js";

const onResponse = async ( res: any ) => {
	// todo: handle other error codes too :p
	// todo: what if we're in an auth route already, need meta for those (simple)
	if ( [ 401, 403 ].includes( res.response.status ) ) {
        if ( router.currentRoute.value.name === "Login" ) return res;
		const currentRoute = router.currentRoute.value;

		await router.push({ name: "Login", query: {
            redirect: encodeURIComponent( currentRoute.fullPath )
        } });
	}

	return res;
}

// so we take each module export and map it to a wrapper
const api = {} as typeof sdk;

for ( const key in sdk ) {
	const func = sdk[ key ];

	if ( typeof func === "function" ) {
		// rawset the api key to a wrapped function
		api[ key ] = ( options: any ) => {
			return func( options ).then( ( res: any ) => onResponse( res ) );
		};
	}
}

export default api as typeof sdk;