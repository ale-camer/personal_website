import { useState, useEffect } from 'react';

const LOCALE_CACHE = {};
const IN_FLIGHT = {};
const LISTENERS = new Set();

let activeSiteLang = 'ES';
let globalTick = 0;

function notifyListeners() {
  globalTick += 1;
  LISTENERS.forEach((fn) => {
    try {
      fn(globalTick);
    } catch {
      // ignore listener errors
    }
  });
}

function normalizeFileCode(langCode) {
  const code = (langCode || 'ES').toUpperCase();
  if (code === 'ZH-TW') return 'zht';
  if (code === 'CA') return 'cat';
  return code.toLowerCase();
}

export function preloadSiteLocale(langCode) {
  const code = (langCode || 'ES').toUpperCase();
  if (code === 'ES' || code === 'EN') return Promise.resolve(null);
  if (LOCALE_CACHE[code]) return Promise.resolve(LOCALE_CACHE[code]);
  if (IN_FLIGHT[code]) return IN_FLIGHT[code];

  const slug = normalizeFileCode(code);
  const url = `/locales/${slug}.json`;
  IN_FLIGHT[code] = fetch(url)
    .then((res) => {
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return res.json();
    })
    .then((data) => {
      LOCALE_CACHE[code] = data || {};
      delete IN_FLIGHT[code];
      notifyListeners();
      return LOCALE_CACHE[code];
    })
    .catch(() => {
      delete IN_FLIGHT[code];
      return null;
    });

  return IN_FLIGHT[code];
}

export function setActiveSiteLang(langCode) {
  const code = (langCode || 'ES').toUpperCase();
  activeSiteLang = code;
  if (code !== 'ES' && code !== 'EN' && !LOCALE_CACHE[code]) {
    preloadSiteLocale(code);
  }
}

export function useSiteLocale(langCode) {
  const code = (langCode || activeSiteLang || 'ES').toUpperCase();
  setActiveSiteLang(code);
  const [tick, setTick] = useState(globalTick);

  useEffect(() => {
    const listener = (nextTick) => setTick(nextTick);
    LISTENERS.add(listener);
    if (code !== 'ES' && code !== 'EN' && !LOCALE_CACHE[code]) {
      preloadSiteLocale(code);
    }
    return () => {
      LISTENERS.delete(listener);
    };
  }, [code]);

  return {
    langCode: code,
    isES: code === 'ES',
    localeReady: code === 'ES' || code === 'EN' || Boolean(LOCALE_CACHE[code]),
    localeTick: tick
  };
}

export function tx(esText, enText, explicitLang) {
  const code = (explicitLang || activeSiteLang || 'ES').toUpperCase();
  if (code === 'ES') return esText;
  if (code === 'EN') return enText;
  const dict = LOCALE_CACHE[code];
  if (dict && typeof dict[enText] === 'string' && dict[enText].length > 0) {
    return dict[enText];
  }
  return enText;
}

export function txList(esArr, enArr, explicitLang) {
  const code = (explicitLang || activeSiteLang || 'ES').toUpperCase();
  if (code === 'ES') return esArr;
  if (code === 'EN') return enArr;
  return enArr.map((enItem, idx) => tx(esArr[idx] ?? enItem, enItem, code));
}
