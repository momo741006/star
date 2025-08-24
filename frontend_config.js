// config/frontend-config.js
// 🌟 虹靈御所前端配置優化

// ==================== API 配置 ====================
export const API_CONFIG = {
  // 環境偵測
  development: {
    baseURL: 'http://localhost:5000',
    timeout: 10000,
    debug: true
  },
  production: {
    baseURL: 'https://rainbow-spirit-api.railway.app',
    timeout: 15000,
    debug: false
  },
  
  // 當前環境
  get current() {
    const isDevelopment = 
      location.hostname === 'localhost' || 
      location.hostname === '127.0.0.1' ||
      location.hostname.includes('local');
    
    return isDevelopment ? this.development : this.production;
  },
  
  // API 端點
  endpoints: {
    health: '/api/health',
    calculate: '/api/calculate_chart',
    test: '/api/test'
  }
};

// ==================== UI 配置 ====================
export const UI_CONFIG = {
  // 動畫配置
  animations: {
    duration: {
      fast: 200,
      normal: 300,
      slow: 500
    },
    easing: 'cubic-bezier(0.4, 0, 0.2, 1)'
  },
  
  // 響應式斷點
  breakpoints: {
    mobile: 768,
    tablet: 1024,
    desktop: 1280
  },
  
  // 主題配置
  theme: {
    colors: {
      primary: '#6366f1',
      secondary: '#8b5cf6',
      accent: '#06b6d4',
      background: '#1e1b4b',
      surface: '#312e81',
      text: '#ffffff'
    },
    gradients: {
      primary: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      cosmic: 'linear-gradient(135deg, #1e3c72 0%, #2a5298 100%)',
      aurora: 'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)'
    }
  }
};

// ==================== 性能配置 ====================
export const PERFORMANCE_CONFIG = {
  // 圖片懶載入
  lazyLoading: {
    rootMargin: '50px',
    threshold: 0.1
  },
  
  // 預載入配置
  preload: {
    fonts: [
      'https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@300;400;500;700&display=swap'
    ],
    critical: [
      '/assets/index-Bo06WAJY.css'
    ]
  },
  
  // 快取配置
  cache: {
    version: '1.0.0',
    maxAge: 24 * 60 * 60 * 1000, // 24小時
    endpoints: [
      '/api/health',
      '/api/test'
    ]
  }
};

// ==================== 錯誤處理配置 ====================
export const ERROR_CONFIG = {
  // 錯誤類型
  types: {
    NETWORK_ERROR: 'NETWORK_ERROR',
    API_ERROR: 'API_ERROR',
    VALIDATION_ERROR: 'VALIDATION_ERROR',
    CALCULATION_ERROR: 'CALCULATION_ERROR'
  },
  
  // 錯誤訊息
  messages: {
    NETWORK_ERROR: '網路連線異常，請檢查網路狀態後重試',
    API_ERROR: '服務暫時無法使用，請稍後再試',
    VALIDATION_ERROR: '輸入資料有誤，請檢查後重新輸入',
    CALCULATION_ERROR: '占星計算發生錯誤，請重新嘗試',
    UNKNOWN_ERROR: '發生未知錯誤，請聯繫客服'
  },
  
  // 重試配置
  retry: {
    maxAttempts: 3,
    delay: 1000,
    backoff: 2
  }
};

// ==================== 分析配置 ====================
export const ANALYTICS_CONFIG = {
  // Google Analytics
  ga: {
    trackingId: 'G-XXXXXXXXXX', // 替換為實際 ID
    config: {
      anonymize_ip: true,
      send_page_view: false
    }
  },
  
  // 事件追蹤
  events: {
    CHARACTER_GENERATED: 'character_generated',
    CHART_CALCULATED: 'chart_calculated',
    ERROR_OCCURRED: 'error_occurred',
    USER_INTERACTION: 'user_interaction'
  }
};

// ==================== 工具函數 ====================
export const Utils = {
  // API 請求封裝
  async apiRequest(endpoint, options = {}) {
    const config = API_CONFIG.current;
    const url = `${config.baseURL}${endpoint}`;
    
    const defaultOptions = {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      timeout: config.timeout
    };
    
    const mergedOptions = { ...defaultOptions, ...options };
    
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), mergedOptions.timeout);
      
      const response = await fetch(url, {
        ...mergedOptions,
        signal: controller.signal
      });
      
      clearTimeout(timeoutId);
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('API Request Error:', error);
      throw this.handleError(error);
    }
  },
  
  // 錯誤處理
  handleError(error) {
    if (error.name === 'AbortError') {
      return new Error(ERROR_CONFIG.messages.NETWORK_ERROR);
    }
    
    if (error.message.includes('fetch')) {
      return new Error(ERROR_CONFIG.messages.NETWORK_ERROR);
    }
    
    return new Error(ERROR_CONFIG.messages.UNKNOWN_ERROR);
  },
  
  // 載入狀態管理
  loadingManager: {
    element: null,
    
    show(message = '載入中...') {
      if (!this.element) {
        this.element = document.createElement('div');
        this.element.className = 'loading-overlay';
        this.element.innerHTML = `
          <div class="loading-content">
            <div class="loading-spinner"></div>
            <div class="loading-message">${message}</div>
          </div>
        `;
        document.body.appendChild(this.element);
      }
      this.element.style.display = 'flex';
    },
    
    hide() {
      if (this.element) {
        this.element.style.display = 'none';
      }
    },
    
    update(message) {
      if (this.element) {
        const messageEl = this.element.querySelector('.loading-message');
        if (messageEl) messageEl.textContent = message;
      }
    }
  },
  
  // 通知系統
  notification: {
    show(message, type = 'info', duration = 3000) {
      const notification = document.createElement('div');
      notification.className = `notification notification-${type}`;
      notification.textContent = message;
      
      document.body.appendChild(notification);
      
      // 動畫進入
      requestAnimationFrame(() => {
        notification.classList.add('notification-show');
      });
      
      // 自動消失
      setTimeout(() => {
        notification.classList.remove('notification-show');
        setTimeout(() => {
          document.body.removeChild(notification);
        }, 300);
      }, duration);
    },
    
    success(message) {
      this.show(message, 'success');
    },
    
    error(message) {
      this.show(message, 'error');
    },
    
    warning(message) {
      this.show(message, 'warning');
    }
  },
  
  // 數據驗證
  validation: {
    birthData(data) {
      const errors = [];
      
      if (!data.name || data.name.trim().length === 0) {
        errors.push('請輸入姓名');
      }
      
      if (!data.year || data.year < 1900 || data.year > new Date().getFullYear()) {
        errors.push('請輸入有效的出生年份');
      }
      
      if (!data.month || data.month < 1 || data.month > 12) {
        errors.push('請輸入有效的出生月份');
      }
      
      if (!data.day || data.day < 1 || data.day > 31) {
        errors.push('請輸入有效的出生日期');
      }
      
      if (data.hour < 0 || data.hour > 23) {
        errors.push('請輸入有效的出生時間（小時）');
      }
      
      if (data.minute < 0 || data.minute > 59) {
        errors.push('請輸入有效的出生時間（分鐘）');
      }
      
      return {
        isValid: errors.length === 0,
        errors
      };
    }
  },
  
  // 分析追蹤
  track(event, data = {}) {
    if (typeof gtag !== 'undefined') {
      gtag('event', event, {
        ...data,
        app_name: '虹靈御所',
        app_version: '1.0.0'
      });
    }
    
    if (API_CONFIG.current.debug) {
      console.log('Track Event:', event, data);
    }
  }
};

// ==================== 初始化 ====================
export function initializeFrontend() {
  console.log('🌟 虹靈御所前端配置載入完成');
  console.log('環境:', API_CONFIG.current.debug ? '開發' : '生產');
  console.log('API 端點:', API_CONFIG.current.baseURL);
  
  // 全域錯誤處理
  window.addEventListener('error', (event) => {
    console.error('全域錯誤:', event.error);
    Utils.track(ANALYTICS_CONFIG.events.ERROR_OCCURRED, {
      error_message: event.message,
      error_filename: event.filename,
      error_lineno: event.lineno
    });
  });
  
  // 網路狀態監控
  window.addEventListener('online', () => {
    Utils.notification.success('網路連線已恢復');
  });
  
  window.addEventListener('offline', () => {
    Utils.notification.warning('網路連線中斷，部分功能可能受限');
  });
}

// 自動初始化
if (typeof window !== 'undefined') {
  document.addEventListener('DOMContentLoaded', initializeFrontend);
}