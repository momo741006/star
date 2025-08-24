// 🌟 虹靈御所占星系統 Service Worker v2.0
// 修正版 - 增強錯誤處理和快取策略

const CACHE_NAME = 'rainbow-spirit-v2.0.0';
const API_CACHE_NAME = 'rainbow-spirit-api-v2.0.0';

// 靜態資源清單
const STATIC_CACHE_URLS = [
    '/',
    '/index.html',
    '/offline.html',
    '/site.webmanifest',
    '/favicon.ico',
    // 字體資源
    'https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@300;400;500;700&family=Inter:wght@300;400;500;600;700&display=swap'
];

// API端點清單
const API_ENDPOINTS = [
    '/api/health',
    '/api/test'
];

// 安裝事件 - 預快取靜態資源
self.addEventListener('install', (event) => {
    console.log('🌟 虹靈御所 SW v2.0: 正在安裝...');

    event.waitUntil(
        Promise.all([
            // 快取靜態資源
            caches.open(CACHE_NAME).then((cache) => {
                console.log('🌟 虹靈御所 SW: 正在快取靜態資源...');
                return cache.addAll(STATIC_CACHE_URLS.map(url => new Request(url, {
                    cache: 'reload'
                })));
            }),
            // 初始化API快取
            caches.open(API_CACHE_NAME).then((cache) => {
                console.log('🌟 虹靈御所 SW: 初始化API快取...');
                return Promise.resolve();
            })
        ]).then(() => {
            console.log('🌟 虹靈御所 SW: 安裝完成');
            return self.skipWaiting(); // 立即激活新的SW
        }).catch((error) => {
            console.error('🌟 虹靈御所 SW: 安裝失敗', error);
            // 發送錯誤訊息到主執行緒
            self.clients.matchAll().then(clients => {
                clients.forEach(client => {
                    client.postMessage({
                        type: 'SW_ERROR',
                        message: '服務工作者安裝失敗',
                        error: error.message
                    });
                });
            });
        })
    );
});

// 啟動事件 - 清理舊快取
self.addEventListener('activate', (event) => {
    console.log('🌟 虹靈御所 SW v2.0: 正在啟動...');

    event.waitUntil(
        Promise.all([
            // 清理舊版本快取
            caches.keys().then((cacheNames) => {
                return Promise.all(
                    cacheNames.map((cacheName) => {
                        if (cacheName !== CACHE_NAME && cacheName !== API_CACHE_NAME) {
                            console.log('🌟 虹靈御所 SW: 清理舊快取', cacheName);
                            return caches.delete(cacheName);
                        }
                    })
                );
            }),
            // 立即控制所有客戶端
            self.clients.claim()
        ]).then(() => {
            console.log('🌟 虹靈御所 SW: 啟動完成');
            // 通知主執行緒SW已就緒
            self.clients.matchAll().then(clients => {
                clients.forEach(client => {
                    client.postMessage({
                        type: 'SW_READY',
                        message: '服務工作者已就緒'
                    });
                });
            });
        }).catch((error) => {
            console.error('🌟 虹靈御所 SW: 啟動失敗', error);
        })
    );
});

// 攔截請求 - 實施快取策略
self.addEventListener('fetch', (event) => {
    const request = event.request;
    const url = new URL(request.url);

    // 只處理 GET 請求
    if (request.method !== 'GET') {
        return;
    }

    // 根據請求類型選擇策略
    if (url.pathname.startsWith('/api/')) {
        // API請求 - 網路優先策略
        event.respondWith(networkFirstStrategy(request));
    } else if (url.pathname === '/' || url.pathname.endsWith('.html')) {
        // HTML請求 - 網路優先，離線後備
        event.respondWith(networkFirstWithOfflineFallback(request));
    } else if (url.origin === location.origin) {
        // 靜態資源 - 快取優先策略
        event.respondWith(cacheFirstStrategy(request));
    } else if (url.hostname === 'fonts.googleapis.com' || url.hostname === 'fonts.gstatic.com') {
        // 字體資源 - 快取優先策略
        event.respondWith(cacheFirstStrategy(request, CACHE_NAME));
    }
});

// 快取優先策略
async function cacheFirstStrategy(request, cacheName = CACHE_NAME) {
    try {
        // 先檢查快取
        const cache = await caches.open(cacheName);
        const cachedResponse = await cache.match(request);

        if (cachedResponse) {
            console.log('🌟 虹靈御所 SW: 從快取載入', request.url);

            // 背景更新快取
            updateCacheInBackground(request, cache);

            return cachedResponse;
        }

        // 快取未命中，從網路獲取
        console.log('🌟 虹靈御所 SW: 從網路載入', request.url);
        const networkResponse = await fetch(request);

        // 快取成功的回應
        if (networkResponse.ok) {
            cache.put(request, networkResponse.clone());
        }

        return networkResponse;

    } catch (error) {
        console.error('🌟 虹靈御所 SW: 快取優先策略失敗', error);

        // 回傳離線頁面
        if (request.headers.get('accept').includes('text/html')) {
            const cache = await caches.open(CACHE_NAME);
            return cache.match('/offline.html');
        }

        throw error;
    }
}

// 網路優先策略
async function networkFirstStrategy(request) {
    try {
        const networkResponse = await fetch(request.clone(), {
            headers: {
                ...request.headers
            }
        });

        if (networkResponse.ok) {
            // 快取API回應（有限時間）
            const cache = await caches.open(API_CACHE_NAME);
            const clonedResponse = networkResponse.clone();

            // 為快取的回應添加時間戳
            const responseWithTimestamp = new Response(clonedResponse.body, {
                status: clonedResponse.status,
                statusText: clonedResponse.statusText,
                headers: {
                    ...clonedResponse.headers,
                    'sw-cache-timestamp': Date.now().toString()
                }
            });

            cache.put(request, responseWithTimestamp);
            console.log('🌟 虹靈御所 SW: API回應已快取', request.url);
        }

        return networkResponse;

    } catch (error) {
        console.log('🌟 虹靈御所 SW: 網路失敗，嘗試快取', request.url);

        // 網路失敗，檢查快取
        const cache = await caches.open(API_CACHE_NAME);
        const cachedResponse = await cache.match(request);

        if (cachedResponse) {
            // 檢查快取是否過期（5分鐘）
            const cacheTimestamp = cachedResponse.headers.get('sw-cache-timestamp');
            const isExpired = cacheTimestamp && (Date.now() - parseInt(cacheTimestamp)) > 5 * 60 * 1000;

            if (!isExpired) {
                console.log('🌟 虹靈御所 SW: 使用快取的API回應', request.url);
                return cachedResponse;
            }
        }

        throw error;
    }
}

// 網路優先帶離線後備
async function networkFirstWithOfflineFallback(request) {
    try {
        const networkResponse = await fetch(request);

        if (networkResponse.ok) {
            const cache = await caches.open(CACHE_NAME);
            cache.put(request, networkResponse.clone());
        }

        return networkResponse;

    } catch (error) {
        console.log('🌟 虹靈御所 SW: 網路失敗，使用離線頁面');

        const cache = await caches.open(CACHE_NAME);
        return cache.match('/offline.html') || cache.match('/');
    }
}

// 背景更新快取
async function updateCacheInBackground(request, cache) {
    try {
        const networkResponse = await fetch(request);
        if (networkResponse.ok) {
            cache.put(request, networkResponse.clone());
            console.log('🌟 虹靈御所 SW: 背景更新完成', request.url);
        }
    } catch (error) {
        console.log('🌟 虹靈御所 SW: 背景更新失敗', request.url);
    }
}

// 背景同步
self.addEventListener('sync', (event) => {
    console.log('🌟 虹靈御所 SW: 背景同步觸發', event.tag);

    if (event.tag === 'background-sync') {
        event.waitUntil(doBackgroundSync());
    } else if (event.tag === 'cache-update') {
        event.waitUntil(updateAllCaches());
    }
});

// 推送通知
self.addEventListener('push', (event) => {
    console.log('🌟 虹靈御所 SW: 收到推送通知', event);

    let notificationData = {
        title: '🌟 虹靈御所',
        body: '你的星空指引已準備完成！',
        icon: '/icons/icon-192x192.png',
        badge: '/icons/badge-72x72.png',
        tag: 'rainbow-spirit-notification',
        renotify: true,
        requireInteraction: false,
        vibrate: [100, 50, 100],
        data: {
            url: '/',
            timestamp: Date.now()
        },
        actions: [
            {
                action: 'open',
                title: '立即查看',
                icon: '/icons/action-open.png'
            },
            {
                action: 'close',
                title: '稍後提醒',
                icon: '/icons/action-close.png'
            }
        ]
    };

    if (event.data) {
        try {
            const data = event.data.json();
            notificationData = { ...notificationData, ...data };
        } catch (error) {
            console.error('🌟 虹靈御所 SW: 推送數據解析失敗', error);
        }
    }

    event.waitUntil(
        self.registration.showNotification(notificationData.title, {
            body: notificationData.body,
            icon: notificationData.icon,
            badge: notificationData.badge,
            tag: notificationData.tag,
            renotify: notificationData.renotify,
            requireInteraction: notificationData.requireInteraction,
            vibrate: notificationData.vibrate,
            data: notificationData.data,
            actions: notificationData.actions
        })
    );
});

// 通知點擊處理
self.addEventListener('notificationclick', (event) => {
    console.log('🌟 虹靈御所 SW: 通知被點擊', event);

    event.notification.close();

    const actionHandlers = {
        'open': () => {
            const url = event.notification.data?.url || '/';
            event.waitUntil(
                clients.matchAll({ type: 'window' }).then(clients => {
                    // 檢查是否已有打開的窗口
                    for (const client of clients) {
                        if (client.url === url && 'focus' in client) {
                            return client.focus();
                        }
                    }
                    // 開啟新窗口
                    if (clients.openWindow) {
                        return clients.openWindow(url);
                    }
                })
            );
        },
        'close': () => {
            // 稍後提醒 - 可以設定稍後的提醒邏輯
            console.log('用戶選擇稍後提醒');
        }
    };

    const handler = actionHandlers[event.action];
    if (handler) {
        handler();
    } else {
        // 預設行為 - 開啟應用
        actionHandlers.open();
    }
});

// 背景同步函數
async function doBackgroundSync() {
    try {
        console.log('🌟 虹靈御所 SW: 執行背景同步');

        // 可以在這裡同步離線時的操作
        // 例如：上傳用戶在離線時生成的角色數據

        const cache = await caches.open(API_CACHE_NAME);

        // 清理過期的API快取
        const keys = await cache.keys();
        for (const request of keys) {
            const response = await cache.match(request);
            const timestamp = response?.headers.get('sw-cache-timestamp');

            if (timestamp && (Date.now() - parseInt(timestamp)) > 60 * 60 * 1000) {
                await cache.delete(request);
                console.log('🌟 虹靈御所 SW: 清理過期快取', request.url);
            }
        }

        console.log('🌟 虹靈御所 SW: 背景同步完成');

    } catch (error) {
        console.error('🌟 虹靈御所 SW: 背景同步失敗', error);
        throw error;
    }
}

// 更新所有快取
async function updateAllCaches() {
    try {
        console.log('🌟 虹靈御所 SW: 更新所有快取');

        const cache = await caches.open(CACHE_NAME);

        // 更新靜態資源
        for (const url of STATIC_CACHE_URLS) {
            try {
                const response = await fetch(url);
                if (response.ok) {
                    await cache.put(url, response);
                }
            } catch (error) {
                console.log('🌟 虹靈御所 SW: 更新快取失敗', url, error);
            }
        }

        console.log('🌟 虹靈御所 SW: 快取更新完成');

    } catch (error) {
        console.error('🌟 虹靈御所 SW: 快取更新失敗', error);
    }
}

// 錯誤處理
self.addEventListener('error', (event) => {
    console.error('🌟 虹靈御所 SW: Service Worker錯誤', event.error);
});

self.addEventListener('unhandledrejection', (event) => {
    console.error('🌟 虹靈御所 SW: 未處理的Promise拒絕', event.reason);
});

console.log('🌟 虹靈御所 Service Worker v2.0 已載入');