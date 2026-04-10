

export const index = 0;
let component_cache;
export const component = async () => component_cache ??= (await import('../entries/pages/_layout.svelte.js')).default;
export const universal = {
  "ssr": false,
  "prerender": false,
  "load": null
};
export const universal_id = "src/routes/+layout.js";
export const imports = ["app/immutable/nodes/0.D6POMAZc.js","app/immutable/chunks/DHGMREDu.js","app/immutable/chunks/Cct7HUUX.js","app/immutable/chunks/CaI4iHRb.js","app/immutable/chunks/C-iQ1oky.js","app/immutable/chunks/CP_jNz0b.js","app/immutable/chunks/WRdPc4vH.js","app/immutable/chunks/DXeWTTGy.js"];
export const stylesheets = ["app/immutable/assets/0.DvNgyyCY.css"];
export const fonts = [];
