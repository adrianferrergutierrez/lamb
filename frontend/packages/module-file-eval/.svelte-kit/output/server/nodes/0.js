

export const index = 0;
let component_cache;
export const component = async () => component_cache ??= (await import('../entries/pages/_layout.svelte.js')).default;
export const universal = {
  "ssr": false,
  "prerender": false,
  "load": null
};
export const universal_id = "src/routes/+layout.js";
export const imports = ["app/immutable/nodes/0.C-p1L0dk.js","app/immutable/chunks/P0cRpWWh.js","app/immutable/chunks/bVHmePBy.js","app/immutable/chunks/CaI4iHRb.js","app/immutable/chunks/CW01SW3d.js","app/immutable/chunks/sAsI4S3F.js","app/immutable/chunks/DIuJFMJY.js","app/immutable/chunks/Bc__Xh5_.js"];
export const stylesheets = ["app/immutable/assets/0.B2mSRybt.css"];
export const fonts = [];
