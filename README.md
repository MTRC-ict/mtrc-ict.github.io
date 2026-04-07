# MTRC 主页

这是一个将原“龙芯实验室”主页整理为“微处理器研究中心（MTRC）”主页的站点工程。当前仓库使用 Jekyll 构建，并可通过 GitHub Actions 发布到 GitHub Pages。

## 当前实现

- 保留原龙芯实验室主页中的主要人员与内容信息
- 整体视觉改为 ICT 蓝色系
- 首页内容完整保留
- 导航栏跳转到若干独立子页面
- 成员页与研究方向页统一由 Jekyll collection 管理
- 站点整体采用 ICT 蓝色系视觉风格
- 已补齐 GitHub Pages 自动部署工作流

## 页面结构

- `index.html`：Jekyll 框架主页入口
- `about/index.zh.html`：中心概况页
- `research/index.zh.html`：研究方向总览页
- `team/index.zh.html`：团队成员总览页
- `projects/index.zh.html`：开放项目页
- `updates/index.zh.html`：动态内容页
- `contact/index.zh.html`：联系页
- `_people/`：成员 collection
- `_research/`：研究方向 collection

## 本地预览

如果本机已经具备 Ruby / Bundler 环境，推荐直接运行：

```bash
bundle exec jekyll serve --host 127.0.0.1 --port 8000
```

浏览器访问：

```text
http://127.0.0.1:8000
```

如果当前机器使用的是本仓库前面已经准备好的 conda 环境，也可以运行：

```bash
conda run -n base bundle exec jekyll serve --host 127.0.0.1 --port 8000
```

如果只是想验证构建是否正常，可以使用：

```bash
bundle exec jekyll build
```

## GitHub Pages 发布

仓库中已经新增工作流 [pages.yml](/home/haooops/Documents/webpage/.github/workflows/pages.yml)。推送到 `master` 或 `main` 后，GitHub Actions 会自动：

1. 安装 Ruby 和 Bundler 依赖。
2. 根据仓库名计算 GitHub Pages 的 `baseurl`。
3. 执行 `bundle exec jekyll build`。
4. 将 `_site` 发布到 GitHub Pages。

当前远端仓库是 `MTRC-ict/mtrc-itc.github.io`，因此工作流会按“项目页”处理，发布地址将是：

```text
https://mtrc-ict.github.io/mtrc-itc.github.io/
```

如果后续把仓库重命名为 `MTRC-ict.github.io`，工作流会自动切换为“用户/组织主页”模式，发布地址会变成：

```text
https://mtrc-ict.github.io/
```

首次启用时，还需要在 GitHub 仓库设置里确认：

1. `Settings -> Pages`
2. `Source` 选择 `GitHub Actions`

## 文件说明

- `_layouts/`：Jekyll 布局模板
- `_includes/`：公共页头页脚
- `_config.yml`：Jekyll 站点配置
- `.github/workflows/pages.yml`：GitHub Pages 自动部署工作流
- `styles.css`：ICT 蓝色系视觉样式
- `script.js`：移动端导航交互
- `assets/favicon.svg`：站点图标

## 后续可选工作

1. 将“新型操作系统组”专题页内容补齐到详情页。
2. 为团队成员补上个人主页链接。
3. 补上英文页面入口，与现有 `index.en.md` / `index.en.html` 风格统一。
4. 整理仓库命名，决定是否切换为 `MTRC-ict.github.io` 根域名部署。
