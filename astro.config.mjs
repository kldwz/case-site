import { defineConfig } from 'astro/config';
import mdImageBase from './plugins/md-image-base.ts';

// base 从环境变量读：线上 build 传 ASTRO_BASE=/case-site/，本地 dev 不传用根路径
// deploy.yml 构建时设置 ASTRO_BASE，保证 GitHub Pages 子路径正确
const base = process.env.ASTRO_BASE || '/';

export default defineConfig({
  base,
  site: 'https://kldwz.github.io',
  markdown: {
    rehypePlugins: [[mdImageBase, { base }]],
  },
});
