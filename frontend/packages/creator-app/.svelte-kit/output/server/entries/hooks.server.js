import { $ as $locale } from "../chunks/configStore.js";
import "@sveltejs/kit/internal";
import "../chunks/exports.js";
import "../chunks/utils2.js";
import "@sveltejs/kit/internal/server";
import "../chunks/root.js";
import "../chunks/state.svelte.js";
const handle = async ({ event, resolve }) => {
  const lang = event.request.headers.get("accept-language")?.split(",")[0] || "en";
  $locale.set(lang);
  return resolve(event);
};
export {
  handle
};
