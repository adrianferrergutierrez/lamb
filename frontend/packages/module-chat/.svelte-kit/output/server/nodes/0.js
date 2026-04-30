

export const index = 0;
let component_cache;
export const component = async () => component_cache ??= (await import('../entries/pages/_layout.svelte.js')).default;
export const universal = {
  "ssr": false,
  "prerender": false
};
export const universal_id = "src/routes/+layout.js";
export const imports = ["app/immutable/nodes/0.Cab6KmPl.js","app/immutable/chunks/Bajkaokr.js","app/immutable/chunks/Q91LBU2d.js","app/immutable/chunks/CApJxbG6.js","app/immutable/chunks/kGk1_tuU.js","app/immutable/chunks/NvrPXAqV.js"];
export const stylesheets = ["app/immutable/assets/0.CSLkg5Cw.css"];
export const fonts = [];
