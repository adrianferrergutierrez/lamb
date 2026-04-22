export const manifest = (() => {
function __memo(fn) {
	let value;
	return () => value ??= (value = fn());
}

return {
	appDir: "app",
	appPath: "m/file-eval/app",
	assets: new Set([]),
	mimeTypes: {},
	_: {
		client: {start:"app/immutable/entry/start.B_JPDIoL.js",app:"app/immutable/entry/app.CY5dChom.js",imports:["app/immutable/entry/start.B_JPDIoL.js","app/immutable/chunks/Bb-HC2fJ.js","app/immutable/chunks/bVHmePBy.js","app/immutable/chunks/CW01SW3d.js","app/immutable/entry/app.CY5dChom.js","app/immutable/chunks/CaI4iHRb.js","app/immutable/chunks/bVHmePBy.js","app/immutable/chunks/C_HkhFnc.js","app/immutable/chunks/P0cRpWWh.js","app/immutable/chunks/Yug-QYZZ.js","app/immutable/chunks/Bc__Xh5_.js"],stylesheets:[],fonts:[],uses_env_dynamic_public:false},
		nodes: [
			__memo(() => import('./nodes/0.js')),
			__memo(() => import('./nodes/1.js')),
			__memo(() => import('./nodes/2.js')),
			__memo(() => import('./nodes/3.js'))
		],
		remotes: {
			
		},
		routes: [
			{
				id: "/grading",
				pattern: /^\/grading\/?$/,
				params: [],
				page: { layouts: [0,], errors: [1,], leaf: 2 },
				endpoint: null
			},
			{
				id: "/upload",
				pattern: /^\/upload\/?$/,
				params: [],
				page: { layouts: [0,], errors: [1,], leaf: 3 },
				endpoint: null
			}
		],
		prerendered_routes: new Set([]),
		matchers: async () => {
			
			return {  };
		},
		server_assets: {}
	}
}
})();
