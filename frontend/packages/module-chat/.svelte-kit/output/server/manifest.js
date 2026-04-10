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
		client: {start:"app/immutable/entry/start.S7dc3FUs.js",app:"app/immutable/entry/app.BdyFkl-4.js",imports:["app/immutable/entry/start.S7dc3FUs.js","app/immutable/chunks/BtTCjzA9.js","app/immutable/chunks/DUaEK6Cc.js","app/immutable/chunks/hf8CdYhj.js","app/immutable/entry/app.BdyFkl-4.js","app/immutable/chunks/kGk1_tuU.js","app/immutable/chunks/DUaEK6Cc.js","app/immutable/chunks/IdnAerJf.js","app/immutable/chunks/DGMqFuIU.js","app/immutable/chunks/Culad9T0.js","app/immutable/chunks/FDWSqlQb.js"],stylesheets:[],fonts:[],uses_env_dynamic_public:false},
		nodes: [
			__memo(() => import('./nodes/0.js')),
			__memo(() => import('./nodes/1.js')),
			__memo(() => import('./nodes/2.js')),
			__memo(() => import('./nodes/3.js')),
			__memo(() => import('./nodes/4.js'))
		],
		remotes: {
			
		},
		routes: [
			{
				id: "/consent",
				pattern: /^\/consent\/?$/,
				params: [],
				page: { layouts: [0,], errors: [1,], leaf: 2 },
				endpoint: null
			},
			{
				id: "/dashboard",
				pattern: /^\/dashboard\/?$/,
				params: [],
				page: { layouts: [0,], errors: [1,], leaf: 3 },
				endpoint: null
			},
			{
				id: "/setup",
				pattern: /^\/setup\/?$/,
				params: [],
				page: { layouts: [0,], errors: [1,], leaf: 4 },
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
