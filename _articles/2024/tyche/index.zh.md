---
layout: article_item
lang: zh
title: "Tyche: An Efficient and General Prefetcher for Indirect Memory Accesses"
summary: 面向间接内存访问提出通用高效的预取器 Tyche，用双向传播机制挖掘依赖关系并提升不规则访存性能。
authors:
  - Feng Xue
  - Chenji Han
  - Xinyu Li
  - Junliang Wu
  - Tingting Zhang
  - Tianyi Liu
  - Yifan Hao
  - Zidong Du
  - Qi Guo
  - Fuxin Zhang
venue: ACM TACO 2024
venue_full: ACM Transactions on Architecture and Code Optimization 2024
date: 2024-04-01
permalink: /articles/tyche/
mentors:
  - 张福新
  - 张婷婷
ict_affiliation_verified: true
doi: 10.1145/3641853
dblp: https://dblp.org/rec/journals/taco/XueHLWZLHDGZ24
verification_links:
  - https://acs.ict.ac.cn/english/people_acs_en/associateresearcher_acs_en/202509/t20250922_778052.html
  - https://dblp.org/rec/journals/taco/XueHLWZLHDGZ24
  - https://ouci.dntb.gov.ua/en/works/le1zvGWl/
---

Tyche 针对图分析、数据库和机器学习中常见的间接内存访问模式，提出一种高效且通用的硬件预取器。该方法通过双向传播机制识别生产者和消费者指令间的依赖关系，从而在较低存储开销下持续发出更准确的预取请求。

核验说明：

- ICT 官方 ACS 教师页面将该文列为 `Tianyi Liu` 的代表论文之一，可确认该成果来自 ICT 相关团队。
- DBLP 与 OUCI 可交叉确认题目、作者列表、期刊和 DOI。
- 公开来源未逐一展示所有作者单位，因此这里将 ICT 归属建立在 ICT 官方页面与多位已收录团队作者重合的基础上。

来源：

- [ACS ICT 官方教师页面](https://acs.ict.ac.cn/english/people_acs_en/associateresearcher_acs_en/202509/t20250922_778052.html)
- [DBLP 条目](https://dblp.org/rec/journals/taco/XueHLWZLHDGZ24)
- [OUCI 条目](https://ouci.dntb.gov.ua/en/works/le1zvGWl/)
