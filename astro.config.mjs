import { defineConfig } from 'astro/config';

// 部署到 GitHub Pages 时，取消下一行注释并把 <repo> 改成你的仓库名。
// 例如仓库是 github.com/yourname/case-site，则 base: '/case-site/'
// 用 Vercel / Cloudflare Pages / Netlify 时保持注释即可（它们自动处理）。
export default defineConfig({
  base: '/case-site/',
  site: 'https://kldwz.github.io',
});
