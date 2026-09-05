# 案例库 (CaseLib)

收集国内外真实的小生意 / 独立产品案例，拆解它们怎么起步、怎么赚钱、流量从哪来。每个案例都讲清模式，方便对照、借鉴。

## 网站结构

```
case-site/                    # Astro 静态站点
├── src/
│   ├── content/
│   │   ├── config.ts         # 案例字段定义（8 个结构化字段）
│   │   └── cases/            # 每个案例一个 Markdown
│   │       └── calculator-net.md
│   ├── layouts/
│   │   └── Base.astro        # 全站布局
│   └── pages/
│       ├── index.astro       # 首页（案例列表 + 标签筛选）
│       └── cases/
│           └── [slug].astro  # 详情页（数据卡 + 正文 + 图片）
├── public/
│   └── cases/                # 案例配图（构建时直接拷贝到 dist）
└── astro.config.mjs
```

## 新增一个案例

1. 在 `case-site/src/content/cases/` 创建一个 Markdown 文件，文件名用英文/拼音（如 `myinstants.md`）。
2. **frontmatter 必填 8 个字段**（与用户约定）：
   - `name` 名称
   - `一句话` 一句话说明
   - `创始人地区` 创始人/地区
   - `营收模式` 怎么赚钱
   - `月收入估算` 收入数字（未披露就标"未官方披露"）
   - `流量来源` 流量从哪来
   - `可迁移点` 你能学什么
   - `原文链接` 数据/案例原始来源 URL
   - `数据口径` 数据来自哪个平台、什么时间
   - `分类` 用 `/` 分隔多个标签，如 `工具站 / 模板化 SEO / 广告变现 / 英文`
   - `封面` 案例封面图路径，如 `/cases/myinstants/01_site.png`
3. 正文用 Markdown 写，按以下结构组织：
   - 网站是什么（配首页截图）
   - 怎么赚的钱（配收入/流量数据截图）
   - 流量从哪来
   - 站长是谁
   - 模式拆解
   - 这个案例能学到什么
   - 来源与数据
4. 图片放到 `case-site/public/cases/<案例slug>/` 对应目录，正文里引用 `/cases/<slug>/xxx.png`。

## 本地开发

```bash
cd case-site
npm install
npm run dev          # 开发模式 http://localhost:4321
npm run build        # 构建静态站点到 dist/
npm run preview      # 本地预览构建产物
```

## 部署

通过 GitHub Actions 自动部署到 GitHub Pages：

- 推送 `main` 分支 → 自动构建 → 自动部署
- 工作流文件：`.github/workflows/deploy.yml`
- 部署路径：`case-site/dist/`

### 第一次部署步骤

1. 在 GitHub 新建仓库（例如 `case-lib`）。
2. 本仓库根目录首次提交并推送到 `main`：
   ```bash
   git init
   git add .
   git commit -m "init"
   git branch -M main
   git remote add origin git@github.com:<你的用户名>/case-lib.git
   git push -u origin main
   ```
3. 仓库 Settings → Pages → Source 选择 "GitHub Actions"。
4. 等 Actions 跑完，访问 `https://<你的用户名>.github.io/case-lib/` 即可。
5. （可选）如需自定义域名或自定义仓库名，编辑 `case-site/astro.config.mjs` 把 `base: '/case-site/'` 取消注释并改成你的仓库名。

## 案例字段口径（务必遵守）

- **数据来源**：所有收入/流量数字必须来自公开渠道（官方披露、第三方估算如 SimilarWeb/SEMrush、创始人公开贴）。
- **未披露的字段**：不要瞎编，写"未官方披露"或"第三方估算约 X"。
- **来源链接**：每个案例必须有原文链接，方便读者验证。
- **图片**：配图必须真实截图，不要伪造收入数字图。