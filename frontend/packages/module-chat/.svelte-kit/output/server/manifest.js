export const manifest = (() => {
function __memo(fn) {
	let value;
	return () => value ??= (value = fn());
}

return {
	appDir: "app",
	appPath: "m/chat/app",
	assets: new Set([]),
	mimeTypes: {},
	_: {
		client: {start:"app/immutable/entry/start.JgpOiZgc.js",app:"app/immutable/entry/app.G--YQcqj.js",imports:["app/immutable/entry/start.JgpOiZgc.js","app/immutable/chunks/Clpuxtxc.js","app/immutable/chunks/Q91LBU2d.js","app/immutable/chunks/NvrPXAqV.js","app/immutable/entry/app.G--YQcqj.js","app/immutable/chunks/kGk1_tuU.js","app/immutable/chunks/Q91LBU2d.js","app/immutable/chunks/CbZQ0WoW.js","app/immutable/chunks/Bajkaokr.js","app/immutable/chunks/CWVJWJKG.js","app/immutable/chunks/CApJxbG6.js"],stylesheets:[],fonts:[],uses_env_dynamic_public:false},
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
				id: "/dashboard",
				pattern: /^\/dashboard\/?$/,
				params: [],
				page: { layouts: [0,], errors: [1,], leaf: 2 },
				endpoint: null
			},
			{
				id: "/setup",
				pattern: /^\/setup\/?$/,
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
