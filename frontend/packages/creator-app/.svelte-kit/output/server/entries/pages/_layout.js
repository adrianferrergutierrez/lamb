import { s as setupI18n, w as waitLocale } from "../../chunks/configStore.js";
import "@sveltejs/kit/internal";
import "../../chunks/exports.js";
import "../../chunks/utils2.js";
import "@sveltejs/kit/internal/server";
import "../../chunks/root.js";
import "../../chunks/state.svelte.js";
const load = async () => {
  console.log("Running i18n setup in +layout.js load...");
  setupI18n();
  await waitLocale();
  return {};
};
export {
  load
};
