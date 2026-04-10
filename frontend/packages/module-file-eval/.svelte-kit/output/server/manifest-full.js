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
		client: {start:"app/immutable/entry/start.CAQcpzAT.js",app:"app/immutable/entry/app.eS8O1MsQ.js",imports:["app/immutable/entry/start.CAQcpzAT.js","app/immutable/chunks/C9yFcxF2.js","app/immutable/chunks/Cct7HUUX.js","app/immutable/chunks/C-iQ1oky.js","app/immutable/entry/app.eS8O1MsQ.js","app/immutable/chunks/CaI4iHRb.js","app/immutable/chunks/Cct7HUUX.js","app/immutable/chunks/vuI-lkp0.js","app/immutable/chunks/DHGMREDu.js","app/immutable/chunks/BbUYQaii.js","app/immutable/chunks/DXeWTTGy.js"],stylesheets:[],fonts:[],uses_env_dynamic_public:false},
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
