

export const index = 0;
let component_cache;
export const component = async () => component_cache ??= (await import('../entries/pages/_layout.svelte.js')).default;
export const universal = {
  "ssr": false,
  "prerender": false
};
export const universal_id = "src/routes/+layout.js";
export const imports = ["app/immutable/nodes/0.DMIi1kE9.js","app/immutable/chunks/DGMqFuIU.js","app/immutable/chunks/DUaEK6Cc.js","app/immutable/chunks/FDWSqlQb.js","app/immutable/chunks/kGk1_tuU.js","app/immutable/chunks/hf8CdYhj.js","app/immutable/chunks/CWX3ZlMD.js"];
export const stylesheets = ["app/immutable/assets/0.BcizSyZ2.css"];
export const fonts = [];
