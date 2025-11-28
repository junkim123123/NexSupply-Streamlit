// service-worker.js
const CACHE_VERSION = 'nexsupply-cache-v1';
const URLS_TO_CACHE = ['/', '/manifest.json'];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_VERSION).then((cache) => {
      return cache.addAll(URLS_TO_CACHE);
    })
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_VERSION) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
  self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);
  
  // API 요청은 네트워크 우선
  if (event.request.method !== 'GET' ||
      url.pathname.includes('/api') ||
      url.pathname.includes('_stcore')) {
    event.respondWith(fetch(event.request));
    return;
  }

  // 정적 자산: 캐시 우선
  event.respondWith(
    caches.match(event.request).then((response) => {
      return response || fetch(event.request).then((res) => {
        if (res.ok) {
          caches.open(CACHE_VERSION).then((c) => c.put(event.request, res.clone()));
        }
        return res;
      });
    })
  );
});
