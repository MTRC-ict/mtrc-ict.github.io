from __future__ import annotations

from dataclasses import dataclass
from html import escape
from pathlib import Path
import re
import shutil


ROOT = Path(__file__).resolve().parent.parent
SOURCE_ROOT = Path("/tmp/loongsonlab-site")
SOURCE_PEOPLE = SOURCE_ROOT / "_people"
SOURCE_IMAGES = SOURCE_ROOT / "assets" / "people"
DEST_IMAGES = ROOT / "assets" / "people"
DEST_PEOPLE = ROOT / "people"


TEAM_STRUCTURE = [
    (
        "研究员（正高级工程师）",
        [("wangjian", "王剑"), ("zhangfuxin", "张福新")],
    ),
    (
        "博士研究生",
        [
            ("liwenjin", "李文晋"),
            ("liwenqing", "李文青"),
            ("lixinyu", "李欣宇"),
            ("niugen", "牛根"),
            ("wangliangpu", "王靓璞"),
            ("xiebenyi", "谢本壹"),
            ("chengxin", "程鑫"),
            ("lanyanzhi", "兰彦志"),
        ],
    ),
    (
        "硕士研究生",
        [
            ("chengyihan", "程轶涵"),
            ("chenyang", "陈洋"),
            ("dengfan", "邓帆"),
            ("guoweiming", "郭伟明"),
            ("jiangtao", "姜涛"),
            ("liuqingtao", "刘庆涛"),
            ("temp1", "未命名"),
            ("temp2", "未命名"),
            ("temp4", "未命名"),
            ("xuhuai", "徐淮"),
            ("yanchenghao", "燕澄皓"),
            ("yanyue", "晏悦"),
            ("yejinpeng", "叶锦鹏"),
            ("youhaichao", "游海超"),
            ("zhangzhuangzhuang", "张壮壮"),
            ("zhaodongru", "赵东儒"),
            ("zhuqizheng", "朱奇正"),
            ("yangzhaoxin", "杨兆鑫"),
            ("wuyuxuan", "吴钰轩"),
        ],
    ),
    ("员工", [("wangyuji", "王宇吉")]),
    ("博士后", [("zhangtingting", "张婷婷")]),
    (
        "毕业生",
        [
            ("huqi", "胡起（2023）"),
            ("wangxin", "王鑫（2023）"),
            ("huangshuqi", "黄树琦（2023）"),
            ("chenxuehai", "陈学海（2023）"),
        ],
    ),
]


GROUP_MAP = {
    "二进制翻译组": {
        "niugen",
        "xiebenyi",
        "lixinyu",
        "lanyanzhi",
        "zhaodongru",
        "guoweiming",
        "zhangzhuangzhuang",
        "yangzhaoxin",
        "wangliangpu",
    },
    "新型体系结构": {
        "liwenqing",
        "chengxin",
        "liwenjin",
        "yanchenghao",
        "yanyue",
        "yejinpeng",
    },
    "性能分析组": {"wuyuxuan", "chengyihan"},
}


PLACEHOLDER_EMAILS = {"example@example.com"}
PLACEHOLDER_URLS = {
    "",
    "404",
    "https://www.baidu.com",
    "http://www.baidu.com",
}


PROFILE_STYLE_MARKER = "/* People profile pages */"


@dataclass
class Person:
    slug: str
    display_name: str
    name: str
    role: str
    image: str
    email: str | None
    email_note: str | None
    blog: str | None
    github: str | None
    advisors: list[str]
    alumni: bool
    body: str
    permalink: str


def parse_front_matter(markdown: str) -> tuple[dict[str, object], str]:
    _, front_matter, body = markdown.split("---", 2)
    data: dict[str, object] = {}
    current_list_key: str | None = None

    for raw_line in front_matter.splitlines():
        line = raw_line.rstrip()
        if not line.strip():
            continue

        if re.match(r"^\s+-\s+", line) and current_list_key:
            value = re.sub(r"^\s+-\s+", "", line).strip()
            data[current_list_key].append(value)  # type: ignore[index]
            continue

        if ":" not in line:
            current_list_key = None
            continue

        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value:
            data[key] = value
            current_list_key = None
        else:
            data[key] = []
            current_list_key = key

    return data, body.strip()


def normalize_email(email: str | None) -> tuple[str | None, str | None]:
    if not email or email in PLACEHOLDER_EMAILS:
        return None, "原主页未提供有效邮箱"
    return email, None


def normalize_link(url: str | None, *, github: bool = False) -> str | None:
    if not url:
        return None
    value = url.strip()
    if value in PLACEHOLDER_URLS:
        return None
    if github and "://" not in value:
        return f"https://github.com/{value.lstrip('@')}"
    return value


def cleanup_text(text: str) -> str:
    text = re.sub(r"\{%\s*link\s+[^%]+%\}", "#", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1", text)
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"\*(.+?)\*", r"\1", text)
    return text.strip()


def extract_research_notes(person: Person) -> list[str]:
    notes: list[str] = []
    lines = [cleanup_text(line) for line in person.body.splitlines()]
    lines = [line for line in lines if line]

    in_research_section = False
    for line in lines:
        heading = line.startswith("## ") or line.startswith("### ")
        if heading:
            title = line.lstrip("#").strip()
            if line.startswith("## "):
                in_research_section = "研究方向" in title
            continue

        if "研究方向" in line and ("：" in line or ":" in line or "为" in line):
            cleaned = (
                line.lstrip("*- ").replace("研究方向：", "").replace("研究方向:", "").strip()
            )
            notes.append(cleaned)
            continue

        if in_research_section:
            notes.append(line.lstrip("- ").strip())
            continue

        if any(keyword in line for keyword in ("二进制翻译", "操作系统", "体系结构", "并行计算", "多核架构")):
            notes.append(line.lstrip("*- ").strip())
            continue

        if "研究" in line and ("方向" in line or "异构系统" in line):
            notes.append(line)

    if not notes:
        for group_name, members in GROUP_MAP.items():
            if person.slug in members:
                notes.append(f"关联研究组：{group_name}（根据原站研究组页面整理）")

    deduped: list[str] = []
    for note in notes:
        if note and note not in deduped:
            deduped.append(note)
    return deduped


def markdown_to_html(markdown: str) -> str:
    lines = [cleanup_text(line) for line in markdown.splitlines()]
    parts: list[str] = []
    paragraph: list[str] = []
    bullet_list: list[str] = []
    ordered_list: list[str] = []

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            parts.append(f"<p>{escape(' '.join(paragraph))}</p>")
            paragraph = []

    def flush_bullets() -> None:
        nonlocal bullet_list
        if bullet_list:
            items = "".join(f"<li>{escape(item)}</li>" for item in bullet_list)
            parts.append(f"<ul>{items}</ul>")
            bullet_list = []

    def flush_ordered() -> None:
        nonlocal ordered_list
        if ordered_list:
            items = "".join(f"<li>{escape(item)}</li>" for item in ordered_list)
            parts.append(f"<ol>{items}</ol>")
            ordered_list = []

    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            flush_paragraph()
            flush_bullets()
            flush_ordered()
            continue

        if line.startswith("### "):
            flush_paragraph()
            flush_bullets()
            flush_ordered()
            parts.append(f"<h3>{escape(line[4:])}</h3>")
            continue

        if line.startswith("## "):
            flush_paragraph()
            flush_bullets()
            flush_ordered()
            parts.append(f"<h2>{escape(line[3:])}</h2>")
            continue

        if re.match(r"^[-*]\s+", line):
            flush_paragraph()
            flush_ordered()
            bullet_list.append(re.sub(r"^[-*]\s+", "", line))
            continue

        if re.match(r"^\d+\.\s+", line):
            flush_paragraph()
            flush_bullets()
            ordered_list.append(re.sub(r"^\d+\.\s+", "", line))
            continue

        flush_bullets()
        flush_ordered()
        paragraph.append(line)

    flush_paragraph()
    flush_bullets()
    flush_ordered()
    return "\n".join(parts)


def load_person(slug: str, display_name: str) -> Person:
    source = SOURCE_PEOPLE / slug / "index.zh.md"
    data, body = parse_front_matter(source.read_text())
    email, email_note = normalize_email(str(data.get("email", "") or ""))
    return Person(
        slug=slug,
        display_name=display_name,
        name=str(data.get("name", display_name)),
        role=str(data.get("role", "成员")),
        image=str(data.get("image", "")).replace("/assets/people/", ""),
        email=email,
        email_note=email_note,
        blog=normalize_link(str(data.get("blog", "") or "")),
        github=normalize_link(str(data.get("github", "") or ""), github=True),
        advisors=list(data.get("advisors", [])) if isinstance(data.get("advisors"), list) else [],
        alumni=str(data.get("alumni", "false")).lower() == "true",
        body=body,
        permalink=str(data.get("permalink", f"people/{slug}")),
    )


def nav_html(prefix: str, active: str) -> str:
    items = [
        ("首页", f"{prefix}index.html", "home"),
        ("中心概况", f"{prefix}overview.html", "overview"),
        ("研究方向", f"{prefix}research.html", "research"),
        ("团队成员", f"{prefix}team.html", "team"),
        ("开放项目", f"{prefix}projects.html", "projects"),
        ("动态内容", f"{prefix}updates.html", "updates"),
        ("联系", f"{prefix}contact.html", "contact"),
    ]
    links = []
    for label, href, key in items:
        active_class = ' class="is-active"' if key == active else ""
        links.append(f'<a{active_class} href="{href}">{label}</a>')
    return "\n            ".join(links)


def info_link(label: str, href: str | None) -> str:
    if not href:
        return ""
    return f'<p><strong>{escape(label)}：</strong><a href="{escape(href)}" target="_blank" rel="noreferrer">{escape(href)}</a></p>'


def render_person_page(person: Person) -> str:
    research_notes = extract_research_notes(person)
    body_html = markdown_to_html(person.body)
    email_html = (
        f'<a href="mailto:{escape(person.email)}">{escape(person.email)}</a>'
        if person.email
        else f'<span class="profile-empty">{escape(person.email_note or "原主页未公开")}</span>'
    )
    advisors = "、".join(person.advisors) if person.advisors else "原主页未标注"
    group_tags = [name for name, members in GROUP_MAP.items() if person.slug in members]
    display_note = ""
    if person.display_name != person.name:
        display_note = f'<p class="profile-caption">团队页显示名称：{escape(person.display_name)}</p>'

    research_html = ""
    if research_notes:
        items = "".join(f"<li>{escape(item)}</li>" for item in research_notes)
        research_html = f"<ul>{items}</ul>"
    else:
        research_html = '<p class="profile-empty">原主页未给出明确研究方向描述。</p>'

    group_html = ""
    if group_tags:
        chips = "".join(f"<span>{escape(tag)}</span>" for tag in group_tags)
        group_html = f'<div class="profile-tags">{chips}</div>'

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{escape(person.name)} | 微处理器研究中心（MTRC）</title>
    <meta
      name="description"
      content="MTRC 成员页：{escape(person.name)}。整理自原龙芯实验室主页，包括照片、研究方向、自述与联系方式。"
    />
    <link rel="icon" href="../assets/favicon.svg" type="image/svg+xml" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
      href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Noto+Sans+SC:wght@400;500;700;800&display=swap"
      rel="stylesheet"
    />
    <link rel="stylesheet" href="../styles.css" />
  </head>
  <body>
    <div class="page-shell">
      <header class="site-header">
        <div class="container header-inner">
          <a class="brand" href="../index.html" aria-label="返回主页">
            <span class="brand-mark">M</span>
            <span class="brand-copy">
              <strong>微处理器研究中心</strong>
              <small>Microprocessor Technology Research Center</small>
            </span>
          </a>
          <button class="nav-toggle" aria-expanded="false" aria-controls="site-nav">
            <span></span><span></span><span></span>
          </button>
          <nav id="site-nav" class="site-nav">
            {nav_html("../", "team")}
          </nav>
        </div>
      </header>

      <main>
        <section class="page-hero">
          <div class="container page-hero-inner card">
            <p class="eyebrow">Member Profile</p>
            <h1>{escape(person.name)}</h1>
            <p>{escape(person.role)} · 原龙芯实验室成员个人页重构版</p>
            <a class="back-link" href="../team.html">← 返回团队成员页</a>
          </div>
        </section>

        <section class="section">
          <div class="container profile-grid">
            <aside class="card profile-sidebar">
              <img class="profile-photo" src="../assets/people/{escape(person.image)}" alt="{escape(person.name)} 的照片" />
              <div class="profile-sidebar-copy">
                <p class="eyebrow">Profile</p>
                <h2 class="profile-name">{escape(person.name)}</h2>
                <p class="profile-role">{escape(person.role)}</p>
                {display_note}
                <div class="profile-kv">
                  <p><strong>导师：</strong>{escape(advisors)}</p>
                  <p><strong>邮箱：</strong>{email_html}</p>
                  {info_link("个人主页", person.blog)}
                  {info_link("GitHub", person.github)}
                  <p><strong>原站链接：</strong><a href="https://loongsonlab.github.io/{escape(person.permalink)}" target="_blank" rel="noreferrer">查看原页面</a></p>
                </div>
              </div>
            </aside>

            <div class="content-stack">
              <article class="card profile-section">
                <h2>研究方向</h2>
                {group_html}
                {research_html}
              </article>

              <article class="card rich-content profile-section">
                <h2>原主页个人信息整理</h2>
                {body_html}
              </article>

              <article class="card note-card">
                <h2>说明</h2>
                <p>本页内容根据原龙芯实验室成员页直接整理；若原页中的邮箱、博客或 GitHub 为占位值，则当前版本不会将其当作真实联系方式展示。</p>
              </article>
            </div>
          </div>
        </section>
      </main>

      <footer class="site-footer">
        <div class="container footer-inner">
          <div>
            <strong>微处理器研究中心（MTRC）</strong>
            <p>成员个人页 · 静态生成版本</p>
          </div>
          <div class="footer-note">
            <p>信息来源：原龙芯实验室个人页与团队页。</p>
          </div>
        </div>
      </footer>
    </div>

    <script src="../script.js"></script>
  </body>
</html>
"""


def replace_member_chips(page_path: Path, prefix: str) -> None:
    text = page_path.read_text()
    for _, members in TEAM_STRUCTURE:
        for slug, display_name in members:
            target = f'<span>{display_name}</span>'
            replacement = f'<a href="{prefix}people/{slug}.html">{display_name}</a>'
            if display_name == "未命名":
                text = text.replace(target, replacement, 1)
            else:
                text = text.replace(target, replacement)

    text = text.replace(
        "单独页面展示团队分类，便于日后扩展个人简介、邮箱和主页链接。",
        "每位成员均已提供独立页面入口，可查看照片、研究方向、自述和联系方式。",
    )
    text = text.replace(
        "以下人员列表按原龙芯实验室团队页保留，不调整人员分类与姓名内容。",
        "以下人员列表按原龙芯实验室团队页保留；点击姓名可进入对应成员页。",
    )
    page_path.write_text(text)


def ensure_profile_styles() -> None:
    styles = ROOT.joinpath("styles.css").read_text()
    if PROFILE_STYLE_MARKER in styles:
        return

    block = f"""

{PROFILE_STYLE_MARKER}
.chips a {{
  display: inline-flex;
  align-items: center;
  min-height: 34px;
  padding: 0 12px;
  border-radius: 999px;
  background: rgba(10, 86, 166, 0.08);
  color: var(--primary-strong);
  border: 1px solid rgba(10, 86, 166, 0.1);
  font-size: 0.92rem;
  text-decoration: none;
}}

.chips a:hover {{
  background: rgba(10, 86, 166, 0.14);
}}

.profile-grid {{
  display: grid;
  grid-template-columns: minmax(300px, 360px) minmax(0, 1fr);
  gap: 24px;
  align-items: start;
}}

.profile-sidebar {{
  overflow: hidden;
  padding: 0;
}}

.profile-photo {{
  width: 100%;
  aspect-ratio: 4 / 5;
  object-fit: cover;
  display: block;
  background: linear-gradient(180deg, rgba(217, 231, 248, 0.9), rgba(202, 220, 242, 0.9));
}}

.profile-sidebar-copy {{
  padding: 24px;
}}

.profile-name {{
  margin: 0;
  font-size: 2rem;
}}

.profile-role {{
  margin: 6px 0 0;
  color: var(--text-muted);
}}

.profile-caption {{
  margin: 10px 0 0;
  color: var(--text-muted);
  font-size: 0.92rem;
}}

.profile-kv {{
  display: grid;
  gap: 10px;
  margin-top: 20px;
}}

.profile-kv p {{
  margin: 0;
}}

.profile-section h2,
.note-card h2 {{
  margin: 0 0 14px;
  font-size: 1.35rem;
}}

.profile-tags {{
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 16px;
}}

.profile-tags span {{
  display: inline-flex;
  align-items: center;
  min-height: 34px;
  padding: 0 12px;
  border-radius: 999px;
  background: rgba(10, 86, 166, 0.08);
  color: var(--primary-strong);
  border: 1px solid rgba(10, 86, 166, 0.1);
  font-size: 0.92rem;
}}

.profile-empty {{
  color: var(--text-muted);
}}

.rich-content h2 {{
  margin-top: 0;
}}

.rich-content h3 {{
  margin: 18px 0 10px;
}}

.rich-content p,
.rich-content li {{
  color: var(--text-muted);
}}

@media (max-width: 900px) {{
  .profile-grid {{
    grid-template-columns: 1fr;
  }}
}}
"""
    ROOT.joinpath("styles.css").write_text(styles + block)


def main() -> None:
    if not SOURCE_ROOT.exists():
        raise SystemExit("source repo not found: /tmp/loongsonlab-site")

    DEST_PEOPLE.mkdir(exist_ok=True)
    if DEST_IMAGES.exists():
        shutil.rmtree(DEST_IMAGES)
    shutil.copytree(SOURCE_IMAGES, DEST_IMAGES)

    people: list[Person] = []
    for _, members in TEAM_STRUCTURE:
        for slug, display_name in members:
            people.append(load_person(slug, display_name))

    for person in people:
        html = render_person_page(person)
        DEST_PEOPLE.joinpath(f"{person.slug}.html").write_text(html)

    replace_member_chips(ROOT / "team.html", "")
    replace_member_chips(ROOT / "index.html", "")
    ensure_profile_styles()


if __name__ == "__main__":
    main()
