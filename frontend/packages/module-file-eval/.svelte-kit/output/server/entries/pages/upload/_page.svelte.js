import { e as escape_html, a3 as store_get, a5 as attr_class, a6 as attr, a4 as unsubscribe_stores, a7 as stringify } from "../../../chunks/index.js";
import { $ as $format } from "../../../chunks/runtime.js";
function _page($$renderer, $$props) {
  $$renderer.component(($$renderer2) => {
    var $$store_subs;
    let studentNote = "";
    $$renderer2.push(`<div class="mx-auto max-w-2xl px-4 py-8"><h1 class="mb-6 text-2xl font-bold text-gray-800">${escape_html(store_get($$store_subs ??= {}, "$_", $format)("fileEval.upload.title"))}</h1> `);
    {
      $$renderer2.push("<!--[0-->");
      $$renderer2.push(`<div class="flex items-center justify-center py-12"><div class="h-8 w-8 animate-spin rounded-full border-b-2 border-blue-600"></div></div>`);
    }
    $$renderer2.push(`<!--]--> `);
    {
      $$renderer2.push("<!--[-1-->");
    }
    $$renderer2.push(`<!--]--> `);
    {
      $$renderer2.push("<!--[-1-->");
    }
    $$renderer2.push(`<!--]--> `);
    {
      $$renderer2.push("<!--[-1-->");
    }
    $$renderer2.push(`<!--]--> <div class="mt-6 rounded-lg border bg-white p-6 shadow-sm">`);
    {
      $$renderer2.push("<!--[-1-->");
    }
    $$renderer2.push(`<!--]--> <div${attr_class(`rounded-lg border-2 border-dashed p-8 text-center transition-colors ${stringify("border-gray-300 bg-white")}`)} role="button" tabindex="0">`);
    {
      $$renderer2.push("<!--[-1-->");
      $$renderer2.push(`<p class="text-gray-500">${escape_html(store_get($$store_subs ??= {}, "$_", $format)("fileEval.upload.dropzone"))}</p> <p class="mt-1 text-xs text-gray-400">${escape_html(store_get($$store_subs ??= {}, "$_", $format)("fileEval.upload.formats"))}</p>`);
    }
    $$renderer2.push(`<!--]--> <input type="file" class="mt-3" accept=".pdf,.docx,.doc,.txt,.md"/></div> <div class="mt-4"><label for="file-eval-student-note" class="mb-1 block text-sm font-medium text-gray-700">${escape_html(store_get($$store_subs ??= {}, "$_", $format)("fileEval.upload.noteLabel"))}</label> <textarea id="file-eval-student-note" class="w-full rounded-lg border p-3 text-sm" rows="3"${attr("placeholder", store_get($$store_subs ??= {}, "$_", $format)("fileEval.upload.notePlaceholder"))}>`);
    const $$body = escape_html(studentNote);
    if ($$body) {
      $$renderer2.push(`${$$body}`);
    }
    $$renderer2.push(`</textarea></div> <button${attr("disabled", true, true)} class="mt-4 w-full rounded-lg bg-blue-600 px-6 py-3 font-medium text-white hover:bg-blue-700 disabled:opacity-50">${escape_html(store_get($$store_subs ??= {}, "$_", $format)("fileEval.upload.submit"))}</button></div> `);
    {
      $$renderer2.push("<!--[-1-->");
    }
    $$renderer2.push(`<!--]--></div>`);
    if ($$store_subs) unsubscribe_stores($$store_subs);
  });
}
export {
  _page as default
};
