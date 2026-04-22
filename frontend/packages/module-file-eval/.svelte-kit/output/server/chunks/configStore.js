import { w as writable } from "./index.js";
import { r as registerLocaleLoader, i as init } from "./runtime.js";
const storedUser = { token: null, name: null, email: null, owiUrl: null, data: null };
const createUserStore = () => {
  const { subscribe, set, update } = writable({
    isLoggedIn: false,
    ...storedUser
  });
  return {
    subscribe,
    /**
     * Logs the user in and updates the store and localStorage.
     * @param {object} userData - User data from the API.
     * @param {string} userData.token - Authentication token.
     * @param {string} userData.name - User's name.
     * @param {string} userData.email - User's email.
     * @param {string} [userData.launch_url] - Optional OpenWebUI launch URL.
     * @param {any} [userData.role] - User role (within nested data, actual structure might vary)
     */
    login: (userData) => {
      set({
        isLoggedIn: true,
        token: userData.token,
        name: userData.name,
        email: userData.email,
        owiUrl: userData.launch_url || null,
        // Handle potential undefined
        data: userData
      });
    },
    /**
     * Sets just the auth token (for LTI login scenarios where we don't have full user data yet).
     * After setting the token, call fetchAndPopulateProfile() to load user info.
     * @param {string} token - Authentication token.
     */
    setToken: (token) => {
      update((state) => ({
        ...state,
        isLoggedIn: true,
        token
      }));
    },
    /**
     * Fetches the user profile from the backend and populates the store.
     * Should be called after setToken() for LTI login flows.
     */
    fetchAndPopulateProfile: async () => {
      const { authService } = await import("./authService.js");
      return;
    },
    // Logout function
    logout: () => {
      set({
        isLoggedIn: false,
        token: null,
        name: null,
        email: null,
        owiUrl: null,
        data: null
      });
    }
  };
};
createUserStore();
const __variableDynamicImportRuntimeHelper = (glob, path, segs) => {
  const v = glob[path];
  if (v) {
    return typeof v === "function" ? v() : Promise.resolve(v);
  }
  return new Promise((_, reject) => {
    (typeof queueMicrotask === "function" ? queueMicrotask : setTimeout)(
      reject.bind(
        null,
        new Error(
          "Unknown variable dynamic import: " + path + (path.split("/").length !== segs ? ". Note that variables only represent file names one level deep." : "")
        )
      )
    );
  });
};
const browser = typeof window !== "undefined";
let isInitialized = false;
const supportedLocales = ["en", "es", "ca", "eu"];
const fallbackLocale = "en";
supportedLocales.forEach((lang) => {
  registerLocaleLoader(lang, () => __variableDynamicImportRuntimeHelper(/* @__PURE__ */ Object.assign({ "../locales/ca.json": () => import("./ca.js"), "../locales/en.json": () => import("./en.js"), "../locales/es.json": () => import("./es.js"), "../locales/eu.json": () => import("./eu.js") }), `../locales/${lang}.json`, 3));
});
function getInitialLocale() {
  if (!browser) {
    return fallbackLocale;
  }
  const savedLocale = localStorage.getItem("lang");
  if (savedLocale && supportedLocales.includes(savedLocale)) {
    return savedLocale;
  }
  return fallbackLocale;
}
function setupI18n() {
  if (isInitialized) return;
  const initial = getInitialLocale();
  console.log(`Initializing svelte-i18n with initial locale: ${initial}, fallback: ${fallbackLocale}`);
  init({
    fallbackLocale,
    initialLocale: initial
  });
  isInitialized = true;
}
({
  buildDate: (/* @__PURE__ */ new Date()).toISOString().split("T")[0]
});
function createConfigStore() {
  const { subscribe, set } = writable({
    api: {
      baseUrl: "/creator",
      lambServer: "http://localhost:9099"
    },
    assets: {
      path: "/static"
    },
    features: {
      enableOpenWebUi: true,
      enableDebugMode: false
    }
  });
  return {
    subscribe,
    setConfig: (config) => set(config)
  };
}
createConfigStore();
export {
  setupI18n as s
};
