import { s as setupI18n } from "../../chunks/configStore.js";
import "@sveltejs/kit/internal";
import "../../chunks/exports.js";
import "../../chunks/utils.js";
import "@sveltejs/kit/internal/server";
import "../../chunks/root.js";
import "../../chunks/state.svelte.js";
import { w as waitLocale } from "../../chunks/runtime.js";
const ssr = false;
const prerender = false;
const load = async () => {
  setupI18n();
  await waitLocale();
  return {};
};
export {
  load,
  prerender,
  ssr
};
