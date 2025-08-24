// 🌟 虹靈御所占星系統 Service Worker
// sw.js

const CACHE_NAME = 'rainbow-spirit-v1.0.0';
const CACHE_URLS = [
  '/',
  '/index.html',
  '/assets/index-Bo06WAJY.css',
  '/assets/index-tykF4J72.js',
  '/site.webmanifest',
  '/favicon.ico',
  // 字體快取
  'https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@300;400;500;700&family=Inter:wght@300;400;500;600;700&display=swap'
];

// 安裝 Service Worker
self.addEventListener('install', (event) => {
  console.log('🌟 虹靈御所 SW: 正在安裝...');
  
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('🌟 虹靈御所 SW: 正在快取資源...');
        return cache.addAll(CACHE_URLS);
      })
      .then(() => {
        console.log('🌟 虹靈御所 SW: 安裝完成');
        return self.skipWaiting();
      })
      .catch((error) => {
        console.error('🌟 虹靈御所 SW: 安裝失敗', error);
      })
  );
});

// 啟動 Service Worker
self.addEventListener('activate', (event) => {
  console.log('🌟 虹靈御所 SW: 正在啟動...');
  
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            console.log('🌟 虹靈御所 SW: 清理舊快取', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => {
      console.log('🌟 虹靈御所 SW: 啟動完成');
      return self.clients.claim();
    })
  );
});

// 攔截請求
self.addEventListener('fetch', (event) => {
  // 只處理 GET 請求
  if (event.request.method !== 'GET') {
    return;
  }
  
  // 不快取 API 請求
  if (event.request.url.includes('/api/')) {
    return;
  }
  
  event.respondWith(
    caches.match(event.request)
      .then((cachedResponse) => {
        // 如果有快取，直接返回
        if (cachedResponse) {
          console.log('🌟 虹靈御所 SW: 從快取載入', event.request.url);
          return cachedResponse;
        }
        
        // 否則從網路獲取
        return fetch(event.request)
          .then((response) => {
            // 檢查是否為有效回應
            if (!response || response.status !== 200 || response.type !== 'basic') {
              return response;
            }
            
            // 複製回應以供快取
            const responseToCache = response.clone();
            
            caches.open(CACHE_NAME)
              .then((cache) => {
                cache.put(event.request, responseToCache);
              });
            
            return response;
          })
          .catch((error) => {
            console.error('🌟 虹靈御所 SW: 網路請求失敗', error);
            
            // 如果是 HTML 請求且網路失敗，返回離線頁面
            if (event.request.headers.get('accept').includes('text/html')) {
              return caches.match('/offline.html');
            }
            
            throw error;
          });
      })
  );
});

// 背景同步
self.addEventListener('sync', (event) => {
  if (event.tag === 'background-sync') {
    console.log('🌟 虹靈御所 SW: 執行背景同步');
    event.waitUntil(doBackgroundSync());
  }
});

// 推送通知
self.addEventListener('push', (event) => {
  if (event.data) {
    const data = event.data.json();
    console.log('🌟 虹靈御所 SW: 收到推送通知', data);
    
    const options = {
      body: data.body || '你的星空指引已準備完成！',
      icon: '/icons/icon-192x192.png',
      badge: '/icons/badge-72x72.png',
      vibrate: [100, 50, 100],
      data: {
        url: data.url || '/'
      },
      actions: [
        {
          action: 'open',
          title: '立即查看',
          icon: '/icons/action-open.png'
        },
        {
          action: 'close',
          title: '稍後查看',
          icon: '/icons/action-close.png'
        }
      ]
    };
    
    event.waitUntil(
      self.registration.showNotification('🌟 虹靈御所', options)
    );
  }
});

// 通知點擊
self.addEventListener('notificationclick', (event) => {
  console.log('🌟 虹靈御所 SW: 通知被點擊', event);
  
  event.notification.close();
  
  if (event.action === 'open') {
    const url = event.notification.data.url || '/';
    event.waitUntil(
      clients.openWindow(url)
    );
  }
});

// 背景同步函數
async function doBackgroundSync() {
  try {
    // 這裡可以執行背景數據同步
    console.log('🌟 虹靈御所 SW: 背景同步完成');
  } catch (error) {
    console.error('🌟 虹靈御所 SW: 背景同步失敗', error);
  }
}