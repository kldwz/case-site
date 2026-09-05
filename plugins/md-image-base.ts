// rehype 插件：给 md 正文里的图片路径加 base 前缀
// md 里写无前缀绝对路径（/cases/xxx/site.png），这里根据 BASE_URL 拼成 /case-site/cases/xxx/site.png
// 本地 dev（base=/）不加前缀，线上 build（base=/case-site/）加前缀
import { visit } from 'unist-util-visit';

export default function (options: { base: string }) {
  const base = options.base === '/' ? '' : options.base.replace(/\/$/, '');
  return (tree: any) => {
    visit(tree, 'element', (node: any) => {
      if (node.tagName === 'img' && node.properties?.src?.startsWith?.('/cases/')) {
        node.properties.src = base + node.properties.src;
      }
    });
  };
}
