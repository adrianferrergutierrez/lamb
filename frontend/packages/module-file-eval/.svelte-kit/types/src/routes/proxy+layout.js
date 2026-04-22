// @ts-nocheck
import { browser } from '$app/environment';
import {
	setupI18n,
	setLocale,
	waitLocale,
	supportedLocales,
	fallbackLocale,
} from '@lamb/ui';

export const ssr = false;
export const prerender = false;

/** */
export const load = async () => {
	setupI18n();

	if (browser) {
		const storedLocale = localStorage.getItem('lang');
		const localeToSet =
			storedLocale && supportedLocales.includes(storedLocale) ? storedLocale : fallbackLocale;
		setLocale(localeToSet);
	}

	await waitLocale();

	return {};
};
