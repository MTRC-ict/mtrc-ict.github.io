# MTRC 本地测试版主页

这是一个纯静态的本地可部署版本，用于将原“龙芯实验室”主页重构为“微处理器研究中心（MTRC）”主页。

## 当前实现

- 保留原龙芯实验室主页中的主要人员与内容信息
- 整体视觉改为 ICT 蓝色系
- 首页内容完整保留
- 导航栏已改为跳转到若干独立子页面
- 纯静态 HTML / CSS / JS，无需构建步骤
- 适合先本地测试，后续可直接迁移到 GitHub Pages

## 页面结构

- `index.html`：首页，保留完整总览内容
- `overview.html`：中心概况页
- `research.html`：研究方向页
- `team.html`：团队成员页
- `projects.html`：开放项目页
- `updates.html`：动态内容页
- `contact.html`：联系页

## 本地预览

在当前目录执行：

```bash
python3 -m http.server 8000
```

然后在浏览器打开：

```text
http://localhost:8000
```

## 文件说明

- `styles.css`：ICT 蓝色系视觉样式
- `script.js`：移动端导航交互
- `tools/generate_people_pages.py`：根据原龙芯实验室 `_people` 数据重新生成成员页
- `assets/favicon.svg`：站点图标

## 后续可选工作

1. 将“新型操作系统组”专题页内容补齐到详情页。
2. 为团队成员补上个人主页链接。
3. 增加 GitHub Pages 部署配置。
4. 把公共页头页脚抽成模板或静态站点生成结构，便于后续维护。
