import "../../../chunks/runtime.js";
import { marked } from "marked";
function _page($$renderer, $$props) {
  $$renderer.component(($$renderer2) => {
    marked.use({ gfm: true, breaks: true });
    $$renderer2.push(`<div class="bg-gray-50 min-h-screen"><div class="max-w-5xl mx-auto px-4 py-6">`);
    {
      $$renderer2.push("<!--[-1-->");
    }
    $$renderer2.push(`<!--]--> `);
    {
      $$renderer2.push("<!--[-1-->");
    }
    $$renderer2.push(`<!--]--> `);
    {
      $$renderer2.push("<!--[0-->");
      $$renderer2.push(`<div class="flex justify-center p-12"><div class="h-8 w-8 animate-spin rounded-full border-b-2 border-blue-600"></div></div>`);
    }
    $$renderer2.push(`<!--]--></div></div>`);
  });
}
export {
  _page as default
};
