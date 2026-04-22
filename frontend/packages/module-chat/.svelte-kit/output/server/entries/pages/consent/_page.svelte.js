import "@sveltejs/kit/internal";
import "../../../chunks/exports.js";
import "../../../chunks/utils2.js";
import "@sveltejs/kit/internal/server";
import "../../../chunks/root.js";
import "../../../chunks/state.svelte.js";
function _page($$renderer, $$props) {
  $$renderer.component(($$renderer2) => {
    $$renderer2.push(`<div class="min-h-screen flex items-center justify-center p-4"><div class="bg-white rounded-xl shadow-lg max-w-lg w-full p-8">`);
    {
      $$renderer2.push("<!--[0-->");
      $$renderer2.push(`<div class="flex justify-center p-8"><span class="text-gray-500">Loading Notice...</span></div>`);
    }
    $$renderer2.push(`<!--]--></div></div>`);
  });
}
export {
  _page as default
};
