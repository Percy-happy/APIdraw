# GitHub上传指南

请按照以下步骤将画板项目上传到GitHub：

## 1. 创建GitHub仓库（在GitHub网站上）
1. 登录您的GitHub账号
2. 点击右上角的"+"号，选择"New repository"
3. 输入仓库名称"drawing-board"
4. 添加描述（可选）
5. 选择公开或私有
6. 点击"Create repository"

## 2. 本地初始化并上传

在项目目录下打开终端，执行以下命令：

```bash
# 初始化git仓库
git init

# 添加所有文件到暂存区
git add .

# 提交文件
git commit -m "初始化画板项目"

# 关联远程仓库（请替换YOUR_USERNAME为您的GitHub用户名）
git remote add origin https://github.com/YOUR_USERNAME/drawing-board.git

# 推送代码到GitHub
git push -u origin main
```

## 3. 后续更新（如有需要）

```bash
# 更新文件
git add .

# 提交更改
git commit -m "更新内容描述"

# 推送到GitHub
git push
```

## 4. 可能遇到的问题

- **权限错误**：确保您的GitHub账号有足够的权限，并且您已正确设置了git凭证
- **远程仓库不存在**：请确保您已在GitHub网站上创建了对应的仓库
- **分支名称问题**：如果您的默认分支是master而不是main，请使用`git push -u origin master`