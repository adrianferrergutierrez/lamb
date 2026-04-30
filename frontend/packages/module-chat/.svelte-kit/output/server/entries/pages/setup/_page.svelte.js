import "@sveltejs/kit/internal";
import "../../../chunks/exports.js";
import "../../../chunks/utils.js";
import "@sveltejs/kit/internal/server";
import "../../../chunks/root.js";
import "../../../chunks/state.svelte.js";
function _page($$renderer, $$props) {
  $$renderer.component(($$renderer2) => {
    $$renderer2.push(`<div class="min-h-screen flex items-center justify-center p-4"><div class="bg-white rounded-xl shadow-lg max-w-2xl w-full p-8"><div class="flex items-center gap-3 mb-6"><div class="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center text-xl">🚀</div> <div><h1 class="text-xl font-bold text-gray-900">LAMB Activity Setup</h1> `);
    {
      $$renderer2.push("<!--[-1-->");
    }
    $$renderer2.push(`<!--]--></div></div> `);
    {
      $$renderer2.push("<!--[0-->");
      $$renderer2.push(`<div class="flex justify-center p-8"><span class="text-gray-500">Loading Configuration...</span></div>`);
    }
    $$renderer2.push(`<!--]--></div></div>`);
  });
}
export {
  _page as default
};
