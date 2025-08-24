#!/bin/bash

# 🌟 虹靈御所占星系統 - 前端優化構建腳本
# build.sh

set -e  # 遇到錯誤立即退出

echo "🌟 虹靈御所前端優化構建開始..."
echo "================================================="

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 檢查環境
check_environment() {
    echo -e "${BLUE}🔍 檢查構建環境...${NC}"
    
    # 檢查 Node.js
    if command -v node &> /dev/null; then
        echo -e "${GREEN}✅ Node.js: $(node --version)${NC}"
    else
        echo -e "${RED}❌ Node.js 未安裝${NC}"
        exit 1
    fi
    
    # 檢查 Python
    if command -v python3 &> /dev/null; then
        echo -e "${GREEN}✅ Python: $(python3 --version)${NC}"
    else
        echo -e "${RED}❌ Python3 未安裝${NC}"
        exit 1
    fi
    
    # 檢查必要文件
    if [ ! -f "index.html" ]; then
        echo -e "${RED}❌ 找不到 index.html${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ 環境檢查通過${NC}"
}

# CSS 優化
optimize_css() {
    echo -e "${CYAN}🎨 優化 CSS 文件...${NC}"
    
    # 檢查是否有 CSS 文件
    if [ -d "assets" ]; then
        for css_file in assets/*.css; do
            if [ -f "$css_file" ]; then
                echo -e "   📄 優化: $css_file"
                
                # 移除註釋和空行（簡單版本）
                sed -i.bak 's/\/\*.*\*\///g' "$css_file"
                sed -i '/^[[:space:]]*$/d' "$css_file"
                
                # 計算大小
                original_size=$(stat -f%z "$css_file.bak" 2>/dev/null || stat -c%s "$css_file.bak")
                optimized_size=$(stat -f%z "$css_file" 2>/dev/null || stat -c%s "$css_file")
                savings=$((original_size - optimized_size))
                
                echo -e "   💾 節省: ${savings} bytes"
            fi
        done
    fi
    
    echo -e "${GREEN}✅ CSS 優化完成${NC}"
}

# JavaScript 優化
optimize_js() {
    echo -e "${YELLOW}⚡ 優化 JavaScript 文件...${NC}"
    
    if [ -d "assets" ]; then
        for js_file in assets/*.js; do
            if [ -f "$js_file" ]; then
                echo -e "   📄 檢查: $js_file"
                
                # 檢查語法（如果有 node）
                if command -v node &> /dev/null; then
                    if node -c "$js_file" 2>/dev/null; then
                        echo -e "   ✅ 語法正確"
                    else
                        echo -e "   ⚠️  語法警告"
                    fi
                fi
            fi
        done
    fi
    
    echo -e "${GREEN}✅ JavaScript 檢查完成${NC}"
}

# 生成圖標
generate_icons() {
    echo -e "${PURPLE}🎯 生成 PWA 圖標...${NC}"
    
    # 創建圖標目錄
    mkdir -p icons
    
    # 如果沒有圖標，創建一個簡單的 SVG
    if [ ! -f "icons/icon-192x192.png" ]; then
        cat > icons/icon.svg << 'EOF'
<svg width="192" height="192" viewBox="0 0 192 192" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <radialGradient id="gradient" cx="50%" cy="50%" r="50%">
      <stop offset="0%" style="stop-color:#667eea"/>
      <stop offset="100%" style="stop-color:#764ba2"/>
    </radialGradient>
  </defs>
  <circle cx="96" cy="96" r="80" fill="url(#gradient)"/>
  <text x="96" y="110" text-anchor="middle" fill="white" font-family="Arial" font-size="48" font-weight="bold">🌟</text>
</svg>
EOF
        echo -e "   📄 創建了基礎 SVG 圖標"
    fi
    
    echo -e "${GREEN}✅ 圖標準備完成${NC}"
}

# 生成離線頁面
generate_offline_page() {
    echo -e "${CYAN}📱 生成離線頁面...${NC}"
    
    cat > offline.html << 'EOF'
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>離線模式 - 虹靈御所</title>
    <style>
        body {
            font-family: 'Noto Sans TC', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            margin: 0;
            padding: 0;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
        }
        .container {
            max-width: 400px;
            padding: 40px 20px;
        }
        .icon {
            font-size: 72px;
            margin-bottom: 20px;
        }
        h1 {
            font-size: 24px;
            margin-bottom: 16px;
        }
        p {
            font-size: 16px;
            line-height: 1.6;
            opacity: 0.9;
        }
        .retry-button {
            background: rgba(255,255,255,0.2);
            border: 2px solid rgba(255,255,255,0.3);
            color: white;
            padding: 12px 24px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            margin-top: 20px;
            transition: all 0.3s ease;
        }
        .retry-button:hover {
            background: rgba(255,255,255,0.3);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="icon">🌟</div>
        <h1>虹靈御所</h1>
        <p>目前無法連接到網路，請檢查網路狀態後重試。</p>
        <p>你的星空指引將在網路恢復後繼續為你服務。</p>
        <button class="retry-button" onclick="window.location.reload()">
            重新連接
        </button>
    </div>
</body>
</html>
EOF
    
    echo -e "${GREEN}✅ 離線頁面生成完成${NC}"
}

# 驗證構建結果
validate_build() {
    echo -e "${BLUE}🔍 驗證構建結果...${NC}"
    
    # 檢查關鍵文件
    local files=(
        "index.html"
        "site.webmanifest"
        "sw.js"
        "offline.html"
    )
    
    for file in "${files[@]}"; do
        if [ -f "$file" ]; then
            echo -e "   ✅ $file"
        else
            echo -e "   ❌ $file ${RED}(缺失)${NC}"
        fi
    done
    
    # 檢查 assets 目錄
    if [ -d "assets" ]; then
        asset_count=$(find assets -name "*.css" -o -name "*.js" | wc -l)
        echo -e "   📦 Assets: $asset_count 個文件"
    fi
    
    echo -e "${GREEN}✅ 構建驗證完成${NC}"
}

# 計算總大小
calculate_size() {
    echo -e "${CYAN}📊 計算構建大小...${NC}"
    
    # 總大小
    if command -v du &> /dev/null; then
        total_size=$(du -sh . | cut -f1)
        echo -e "   📦 總大小: $total_size"
    fi
    
    # 關鍵文件大小
    for file in index.html sw.js site.webmanifest; do
        if [ -f "$file" ]; then
            if command -v ls &> /dev/null; then
                size=$(ls -lh "$file" | awk '{print $5}')
                echo -e "   📄 $file: $size"
            fi
        fi
    done
}

# 部署準備
prepare_deploy() {
    echo -e "${PURPLE}🚀 準備部署...${NC}"
    
    # 創建部署信息文件
    cat > deploy-info.json << EOF
{
  "buildTime": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "version": "1.0.0",
  "environment": "production",
  "features": [
    "PWA support",
    "Service Worker",
    "Offline mode",
    "Responsive design",
    "Performance optimized"
  ]
}
EOF
    
    echo -e "   📄 創建部署信息文件"
    echo -e "${GREEN}✅ 部署準備完成${NC}"
}

# 主執行流程
main() {
    echo -e "${BLUE}開始構建流程...${NC}"
    
    check_environment
    echo ""
    
    optimize_css
    echo ""
    
    optimize_js
    echo ""
    
    generate_icons
    echo ""
    
    generate_offline_page
    echo ""
    
    validate_build
    echo ""
    
    calculate_size
    echo ""
    
    prepare_deploy
    echo ""
    
    echo "================================================="
    echo -e "${GREEN}🎉 虹靈御所前端構建完成！${NC}"
    echo ""
    echo -e "${CYAN}下一步操作：${NC}"
    echo -e "1. ${YELLOW}git add .${NC}"
    echo -e "2. ${YELLOW}git commit -m \"🚀 前端優化構建\"${NC}"
    echo -e "3. ${YELLOW}git push origin main${NC}"
    echo -e "4. ${YELLOW}在 GitHub 設置 Pages 部署${NC}"
    echo ""
    echo -e "${PURPLE}🌟 虹靈御所 - 讓占星成為你的人生遊戲升級系統！${NC}"
}

# 執行主函數
main "$@"