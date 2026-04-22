import * as universal from '../entries/pages/_layout.js';

export const index = 0;
let component_cache;
export const component = async () => component_cache ??= (await import('../entries/pages/_layout.svelte.js')).default;
export { universal };
export const universal_id = "src/routes/+layout.js";
export const imports = ["app/immutable/nodes/0.BOZXKMOA.js","app/immutable/chunks/D5XnjlQs.js","app/immutable/chunks/CKo3SdCT.js","app/immutable/chunks/CA-A2sUk.js","app/immutable/chunks/FOUscKbI.js","app/immutable/chunks/BRDyC_FN.js","app/immutable/chunks/C3SvWKh1.js","app/immutable/chunks/Dn5T1RL2.js","app/immutable/chunks/CU2VBiMv.js","app/immutable/chunks/42ANG6Sg.js"];
export const stylesheets = ["app/immutable/assets/0.DvFuvoDQ.css"];
export const fonts = [];
