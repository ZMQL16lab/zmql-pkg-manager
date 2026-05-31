#!/usr/bin/env python3
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox

class PackageManager:
    def __init__(self, root):
        self.root = root
        self.root.title("lztOS Package Manager")
        self.root.geometry("800x500")
        
        # 获取软件包列表
        self.packages = self.get_packages()
        
        # 创建界面
        self.create_widgets()
        
    def get_packages(self):
        """获取手动安装的软件包列表"""
        result = subprocess.run(['pacman', '-Qe'], capture_output=True, text=True)
        packages = []
        for line in result.stdout.strip().split('\n'):
            if line:
                parts = line.split()
                packages.append({'name': parts[0], 'version': parts[1]})
        return packages
    
    def create_widgets(self):
        # 搜索框
        search_frame = ttk.Frame(self.root)
        search_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(search_frame, text="搜索:").pack(side=tk.LEFT, padx=5)
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_packages)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # 列表
        list_frame = ttk.Frame(self.root)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 滚动条
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree = ttk.Treeview(list_frame, columns=('version',), show='tree headings', yscrollcommand=scrollbar.set)
        self.tree.heading('#0', text='软件包名')
        self.tree.heading('version', text='版本')
        self.tree.column('#0', width=300)
        self.tree.column('version', width=150)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.tree.yview)
        
        # 刷新列表
        self.refresh_list()
        
        # 按钮
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(btn_frame, text="卸载选中软件包", command=self.remove_package).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="刷新列表", command=self.refresh_list).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="退出", command=self.root.quit).pack(side=tk.RIGHT, padx=5)
        
    def refresh_list(self):
        """刷新软件包列表"""
        # 清空现有列表
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # 重新获取数据
        self.packages = self.get_packages()
        self.filter_packages()
    
    def filter_packages(self, *args):
        """根据搜索关键词过滤"""
        keyword = self.search_var.get().lower()
        
        # 清空列表
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # 插入过滤后的数据
        for pkg in self.packages:
            if keyword in pkg['name'].lower():
                self.tree.insert('', tk.END, text=pkg['name'], values=(pkg['version'],))
    
    def remove_package(self):
        """卸载选中的软件包"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("警告", "请先选中要卸载的软件包")
            return
        
        pkg_name = self.tree.item(selected[0])['text']
        
        # 确认对话框
        if not messagebox.askyesno("确认卸载", f"确定要卸载 '{pkg_name}' 吗？\n\n这可能会同时卸载其依赖项。"):
            return
        
        # 执行卸载
        try:
            result = subprocess.run(['sudo', 'pacman', '-Rns', pkg_name], capture_output=True, text=True)
            if result.returncode == 0:
                messagebox.showinfo("成功", f"'{pkg_name}' 已成功卸载")
                self.refresh_list()
            else:
                messagebox.showerror("错误", f"卸载失败:\n{result.stderr}")
        except Exception as e:
            messagebox.showerror("错误", f"执行出错: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PackageManager(root)
    root.mainloop()