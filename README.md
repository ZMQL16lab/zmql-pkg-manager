# zmql-pkg-manager
[ 中文 ]一个简单的图形化包管理器，可以查看和删除不想要的包或者依赖或者任何从pacman／aur下载的东西 : )  [English] : A simple graphical package manager that allows you to view and remove unwanted packages, dependencies, or anything downloaded from pacman/AUR.  : )




---

## 🚀 安装脚本 `install.sh`

```bash
#!/bin/bash
set -e

GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}lztOS Package Manager Installer${NC}"
echo -e "${GREEN}========================================${NC}"

# 创建目录
mkdir -p ~/.local/bin
mkdir -p ~/.local/share/applications
mkdir -p ~/.local/share/icons

# 下载主程序
echo -e "\n${GREEN}[1/3] 下载主程序...${NC}"
curl -o ~/.local/bin/pkg-manager-gui.py \
    https://raw.githubusercontent.com/ZMQL16lab/lztos-pkg-manager/main/src/pkg-manager-gui.py

chmod +x ~/.local/bin/pkg-manager-gui.py

# 下载图标（可选）
echo -e "\n${GREEN}[2/3] 下载图标...${NC}"
curl -o ~/.local/share/icons/pkg-manager.png \
    https://raw.githubusercontent.com/ZMQL16lab/lztos-pkg-manager/main/icons/pkg-manager.png

# 创建 .desktop 文件
echo -e "\n${GREEN}[3/3] 创建桌面快捷方式...${NC}"
cat > ~/.local/share/applications/pkg-manager-gui.desktop << EOF
[Desktop Entry]
Name=lztOS Package Manager
Comment=Manage installed packages
Exec=/home/${USER}/.local/bin/pkg-manager-gui.py
Icon=/home/${USER}/.local/share/icons/pkg-manager.png
Terminal=false
Type=Application
Categories=System;Utility;
EOF

echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}安装完成！${NC}"
echo -e "${GREEN}========================================${NC}"
echo -e "\n在应用菜单中搜索 'lztOS Package Manager' 启动"

read -p "是否立即启动？ (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    ~/.local/bin/pkg-manager-gui.py &
fi
