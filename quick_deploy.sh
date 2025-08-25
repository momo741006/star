#!/bin/bash
# 🌟 虹靈御所占星系統 - 快速部署腳本
# Quick Deploy Script v2.0

set -e  # 遇到錯誤立即退出

echo "🌟 虹靈御所占星系統快速部署腳本"
echo "==============================================="

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 檢查必要檔案
check_files() {
    echo -e "${BLUE}🔍 檢查必要檔案...${NC}"

    required_files=(
        "main.py"
        "requirements.txt" 
        "Procfile"
        "index.html"
        "service_worker.js"
        "site.webmanifest"
    )

    missing_files=()

    for file in "${required_files[@]}"; do
        if [ ! -f "$file" ]; then
            missing_files+=("$file")
        fi
    done

    if [ ${#missing_files[@]} -ne 0 ]; then
        echo -e "${RED}❌ 缺少必要檔案:${NC}"
        printf '%s\n' "${missing_files[@]}"
        echo -e "${YELLOW}請確認檔案已正確命名和放置${NC}"
        exit 1
    fi

    echo -e "${GREEN}✅ 所有必要檔案都存在${NC}"
}

# 檢查依賴
check_dependencies() {
    echo -e "${BLUE}🔍 檢查依賴...${NC}"

    # 檢查 Python
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}❌ Python3 未安裝${NC}"
        exit 1
    fi

    # 檢查 Git
    if ! command -v git &> /dev/null; then
        echo -e "${RED}❌ Git 未安裝${NC}"
        exit 1
    fi

    echo -e "${GREEN}✅ 依賴檢查完成${NC}"
}

# 更新檔案
update_files() {
    echo -e "${BLUE}🔄 更新檔案到最新版本...${NC}"

    # 檢查更新檔案是否存在
    if [ -f "index_updated.html" ]; then
        cp index_updated.html index.html
        echo "✅ 更新 index.html"
    fi

    if [ -f "service_worker_updated.js" ]; then
        cp service_worker_updated.js service_worker.js
        echo "✅ 更新 service_worker.js"
    fi

    if [ -f "site_webmanifest_updated.json" ]; then
        cp site_webmanifest_updated.json site.webmanifest
        echo "✅ 更新 site.webmanifest"
    fi

    if [ -f "offline_updated.html" ]; then
        cp offline_updated.html offline.html
        echo "✅ 更新 offline.html"
    fi

    if [ -f "main_enhanced.py" ]; then
        cp main_enhanced.py main.py
        echo "✅ 更新 main.py"
    fi

    echo -e "${GREEN}✅ 檔案更新完成${NC}"
}

# 創建圖標目錄
create_icons() {
    echo -e "${BLUE}📁 準備圖標目錄...${NC}"

    if [ ! -d "icons" ]; then
        mkdir -p icons
        echo "✅ 創建 icons/ 目錄"
        echo -e "${YELLOW}⚠️ 請手動添加PWA圖標到 icons/ 目錄${NC}"
        echo "   需要的尺寸: 72x72, 96x96, 128x128, 144x144, 152x152, 192x192, 384x384, 512x512"
    else
        echo "✅ icons/ 目錄已存在"
    fi
}

# Git 操作
git_operations() {
    echo -e "${BLUE}📝 Git 操作...${NC}"

    # 檢查是否已初始化Git
    if [ ! -d ".git" ]; then
        git init
        echo "✅ 初始化 Git 倉庫"
    fi

    # 添加檔案
    git add .
    echo "✅ 添加檔案到暫存區"

    # 提交
    commit_message="🚀 虹靈御所占星系統 v2.0 - 準備部署 $(date +'%Y-%m-%d %H:%M:%S')"
    git commit -m "$commit_message"
    echo "✅ 提交變更"
}

# Railway 部署
deploy_railway() {
    echo -e "${BLUE}🚄 Railway 部署...${NC}"

    read -p "請輸入你的 GitHub 倉庫 URL (例如: https://github.com/用戶名/專案名.git): " repo_url

    if [ -n "$repo_url" ]; then
        # 檢查是否已設定遠程倉庫
        if ! git remote get-url origin &> /dev/null; then
            git remote add origin "$repo_url"
            echo "✅ 添加遠程倉庫"
        fi

        # 推送到 GitHub
        git push -u origin main
        echo "✅ 推送到 GitHub"

        echo -e "${GREEN}🎉 代碼已推送到 GitHub!${NC}"
        echo -e "${YELLOW}接下來請到 Railway 控制台完成部署:${NC}"
        echo "1. 前往 https://railway.app/"
        echo "2. 點擊 'New Project'"
        echo "3. 選擇 'Deploy from GitHub repo'"
        echo "4. 選擇你的倉庫並點擊 'Deploy'"
    else
        echo -e "${RED}❌ 未提供 GitHub 倉庫 URL${NC}"
    fi
}

# Heroku 部署
deploy_heroku() {
    echo -e "${BLUE}🟣 Heroku 部署...${NC}"

    # 檢查 Heroku CLI
    if ! command -v heroku &> /dev/null; then
        echo -e "${RED}❌ Heroku CLI 未安裝${NC}"
        echo "請前往 https://devcenter.heroku.com/articles/heroku-cli 安裝"
        return 1
    fi

    read -p "請輸入 Heroku 應用名稱: " app_name

    if [ -n "$app_name" ]; then
        # 創建 Heroku 應用
        heroku create "$app_name"
        echo "✅ 創建 Heroku 應用: $app_name"

        # 部署到 Heroku
        git push heroku main
        echo "✅ 部署到 Heroku"

        # 擴展 dyno
        heroku ps:scale web=1
        echo "✅ 啟動 Web Dyno"

        # 開啟應用
        heroku open
        echo -e "${GREEN}🎉 Heroku 部署完成!${NC}"
    else
        echo -e "${RED}❌ 未提供應用名稱${NC}"
    fi
}

# 主選單
main_menu() {
    echo -e "${YELLOW}請選擇部署平台:${NC}"
    echo "1) 🚄 Railway (推薦)"
    echo "2) 🟣 Heroku"
    echo "3) 📁 僅準備檔案 (不部署)"
    echo "4) ❌ 退出"

    read -p "請選擇 (1-4): " choice

    case $choice in
        1)
            deploy_railway
            ;;
        2)
            deploy_heroku
            ;;
        3)
            echo -e "${GREEN}✅ 檔案準備完成，可以手動部署了${NC}"
            ;;
        4)
            echo -e "${BLUE}👋 感謝使用！${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}❌ 無效選擇${NC}"
            main_menu
            ;;
    esac
}

# 主程序
main() {
    check_dependencies
    check_files
    update_files
    create_icons
    git_operations
    main_menu

    echo -e "${GREEN}🌟 部署準備完成！${NC}"
    echo -e "${BLUE}如需幫助，請查看部署指南文檔${NC}"
}

# 執行主程序
main "$@"