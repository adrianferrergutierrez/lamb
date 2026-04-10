import { e as escape_html, a3 as store_get, a4 as unsubscribe_stores } from "../../../chunks/index.js";
import { $ as $format } from "../../../chunks/runtime.js";
function _page($$renderer, $$props) {
  $$renderer.component(($$renderer2) => {
    var $$store_subs;
    $$renderer2.push(`<div class="mx-auto max-w-7xl px-4 py-8"><h1 class="mb-6 text-2xl font-bold text-gray-800">${escape_html(store_get($$store_subs ??= {}, "$_", $format)("fileEval.grading.title"))}</h1> `);
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
      $$renderer2.push(`<div class="flex items-center justify-center py-12"><div class="h-8 w-8 animate-spin rounded-full border-b-2 border-blue-600"></div></div>`);
    }
    $$renderer2.push(`<!--]--></div>`);
    if ($$store_subs) unsubscribe_stores($$store_subs);
  });
}
export {
  _page as default
};
