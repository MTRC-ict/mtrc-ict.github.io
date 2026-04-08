# MTRC Website

微处理器研究中心（MTRC）主页项目，使用 Jekyll 构建并通过 GitHub Actions 发布到 GitHub Pages。

这个仓库的目标不是做成一个“单次上线的静态网页”，而是作为团队长期维护的站点工程：
- 首页和栏目页负责统一展示中心信息
- `_people/` 负责维护成员页面
- `_research/` 负责维护研究方向页面
- `_news/` 和 `_articles/` 负责维护动态内容与出版物

## 站点结构

- [index.html](index.html)：首页
- [about/index.zh.html](about/index.zh.html)：中心概况
- [research/index.zh.html](research/index.zh.html)：研究方向总览
- [team/index.zh.html](team/index.zh.html)：团队成员总览
- [projects/index.zh.html](projects/index.zh.html)：开放项目
- [updates/index.zh.html](updates/index.zh.html)：动态内容入口
- [news/index.zh.html](news/index.zh.html)：新闻列表
- [articles/index.zh.html](articles/index.zh.html)：文章/出版物列表
- [contact/index.zh.html](contact/index.zh.html)：联系页面
- [\_people](_people)：成员页面数据
- [\_research](_research)：研究方向数据
- [\_news](_news)：新闻内容
- [\_articles](_articles)：文章与出版物内容
- [\_layouts](_layouts)：页面布局
- [styles.css](styles.css)：站点样式

## 本地预览

如果本机已经有 Ruby / Bundler 环境，可以直接运行：

```bash
bundle exec jekyll serve --host 127.0.0.1 --port 8000
```

访问：

```text
http://127.0.0.1:8000
```

如果当前环境使用的是已有 conda 配置，也可以运行：

```bash
conda run -n base bundle exec jekyll serve --host 127.0.0.1 --port 8000
```

只验证构建时使用：

```bash
bundle exec jekyll build
```

## GitHub Pages 发布

仓库通过 [pages.yml](.github/workflows/pages.yml) 自动发布。

推送到 `master` 或 `main` 后，GitHub Actions 会自动：
1. 安装 Ruby 依赖
2. 计算 GitHub Pages 的 `baseurl`
3. 执行 `bundle exec jekyll build`
4. 将 `_site` 发布到 GitHub Pages

当前远端仓库是 `MTRC-ict/mtrc-ict.github.io`，因此它会被当作项目页发布到：

```text
https://mtrc-ict.github.io
```

## 成员如何通过 Pull Request 更新个人页面

推荐流程：

1. Fork 本仓库，或在有权限的情况下直接新建分支。
2. 在自己的分支中修改成员页面文件。
3. 本地执行 `bundle exec jekyll build`，确保构建通过。
4. 提交后发起 Pull Request。
5. 在 PR 描述中写清楚“更新了哪些信息”。

### 成员页面放在哪里

成员页面统一放在 [\_people](_people) 下，按维护目录组织：

- 员工：`_people/员工/<role>/<slug>/`
- 学生：`_people/学生/<role>/<年份>/<slug>/`

例如：

- [zhangfuxin](_people/员工/研究员／正高级工程师/zhangfuxin/index.zh.md)
- [haomiao](_people/学生/硕士研究生/2023/haomiao/index.zh.md)

说明：

- 员工目录中的“或”关系使用全角斜杠 `／` 作为目录名的一部分，例如 `研究员／正高级工程师`
- 成员页 front matter 中的 `role` 仍然使用半角斜杠 `/`，例如 `研究员/正高级工程师`

每个成员目录通常至少包含：

- `index.zh.md`
- `index.en.md`

照片统一放在：

- [assets/people](assets/people)

### 成员页面字段说明

以 `index.zh.md` 为例，一个常见成员页至少应包含：

```yaml
---
layout: person_profile
name: [姓名中文]
image: /assets/people/[your-photo.jpg]
role: [硕士研究生]
blog: [https://example.com]
email: [your_email@example.com]
github: https://github.com/[yourname]
alumni: [false]
advisors:
  - [导师姓名中文]
date: [2023-09-01]
permalink: people/[姓名拼音]
lang: zh
---
```

### 这些字段必须人工改写

下面这些字段不能直接复制模板，新增成员时必须逐项检查并改成真实值：

- `name`：成员姓名
- `image`：头像路径，必须指向 `assets/people/` 下真实存在的图片
- `blog`：个人主页；没有可删除，不要保留占位链接
- `email`：真实邮箱
- `github`：GitHub 主页；没有可删除，不要保留占位链接
- `advisors`：导师列表；没有可删除
- `date`：入组/入学年份对应日期，当前团队页按年份分组时会使用这个字段
- `permalink`：成员页面固定地址，通常写成 `people/<slug>`，其中 `<slug>` 应与目录名一致
- 正文 Markdown：个人简介、研究方向、项目经历、主要论著等内容都需要人工整理

### 这些字段是受限字段，只能用固定选项

#### `layout`

成员页统一使用：

- `person_profile`

#### `lang`

只能是：

- `zh`
- `en`

#### `alumni`

只能是：

- `false`：在读/在岗
- `true`：已毕业

#### 中文页面 `role` 可选项

员工：

- `研究员/正高级工程师`
- `副研究员/高级工程师`
- `工程师`
- `博士后`

学生：

- `博士研究生`
- `硕士研究生`

说明：

- 已毕业成员的 `role` 仍然保持其毕业前身份，一般仍写 `博士研究生` 或 `硕士研究生`
- “已毕业”不是 `role` 的一个取值，而是通过 `alumni: true` 控制

#### 英文页面 `role` 可选项

员工：

- `Professor / Senior Engineer`
- `Associate Researcher / Senior Engineer`
- `Engineer`
- `Postdoc`

学生：

- `PhD Student`
- `Masters Student`

### 不同成员类型应如何填写

#### 员工

目录结构：

- `_people/员工/<role>/<slug>/`

要求：

- `role` 必须与目录语义一致；如果目录名中使用了全角斜杠 `／`，则 `role` 中对应使用半角斜杠 `/`
- `alumni` 固定为 `false`
- 一般不需要 `alumni_since`

#### 在读学生

目录结构：

- `_people/学生/<role>/<年份>/<slug>/`

要求：

- `role` 只能是 `博士研究生` / `硕士研究生`，英文页对应 `PhD Student` / `Masters Student`
- `alumni` 固定为 `false`
- `date` 应落在对应年份内，例如目录是 `2023`，则 `date` 应为 `2023-xx-xx`

#### 已毕业学生

目录结构：

- `_people/学生/已毕业/<毕业年份>/<slug>/`

要求：

- `alumni` 必须为 `true`
- 必须补充 `alumni_since: <毕业年份>`
- `role` 仍保持原身份，不要写成“已毕业”

示例：

```yaml
alumni: true
alumni_since: 2023
role: 硕士研究生
```

### 不要保留模板占位值

提交前请特别检查并删除下面这些占位内容：

- `example@example.com`
- `https://www.baidu.com`
- “没有，我一句都不想说”
- 空的 `advisors`
- 不存在的头像路径

### 更新个人简介与研究方向

front matter 下方的 Markdown 正文就是成员页内容。常见需要人工改写的部分包括：

- 个人简介
- 研究方向
- 联系方式
- 项目经历
- 主要论著

如果只是更新个人页面，不需要改 layout 或样式文件。

## 如何新增或维护出版物

当前站点里“近期文章/出版物”使用 [\_articles](_articles) 维护。

每篇文章按年份放在一个目录中，例如：

- [zeno](_articles/2023/zeno/index.zh.md)

推荐目录结构：

```text
_articles/<year>/<slug>/index.zh.md
```

示例 front matter：

```yaml
---
layout: article_item
lang: zh
title: "论文标题"
summary: 一句话简介
authors:
  - 作者A
  - 作者B
venue: MICRO 2025
date: 2025-10-01
permalink: /articles/paper-slug/
---
```

说明：

- `title`：论文或文章标题
- `authors`：作者列表
- `venue`：会议、期刊或技术报告名称
- `date`：发布日期或发表日期
- `summary`：首页/列表页展示的摘要
- `permalink`：文章详情页地址，建议保持稳定，不要因为目录调整而修改已有链接

### 出版物 PR 建议

如果是新增一篇文章或论文，PR 描述里建议写清楚：

- 论文标题
- 发表 venue
- 作者列表
- 是否需要同时更新成员页中的“主要论著”

如果某篇出版物需要同时出现在成员个人页里，请同步更新对应成员的 `index.zh.md` 内容。

## 对维护者的建议

- 不要直接在 `_site/` 下修改内容，那里只是构建产物
- 不要随意改已有成员页的 `permalink`
- 新增成员时优先复用现有字段命名，不要临时发明新字段
- 页面结构变更优先改 collection 和 layout，不要重新引入分散的静态 HTML

## 常见修改场景

### 1. 新成员加入

需要修改：

- 在 `_people/` 下新增成员目录和 `index.zh.md`
- 在 `assets/people/` 下新增头像

### 2. 成员更新邮箱或研究方向

只需要修改：

- 对应成员的 `index.zh.md`

### 3. 新增一篇论文或文章

只需要修改：

- 在 `_articles/<年份>/` 下新增一个目录和 `index.zh.md`

### 4. 新增一条新闻

只需要修改：

- 在 `_news/` 下新增一个目录和 `index.zh.md`

## 后续工作

- 补充更多英文页面
- 继续完善研究方向详情页内容
- 统一整理成员页中的出版物格式
- 仓库重命名为 `mtrc-ict.github.io` 后切换到根域名部署
