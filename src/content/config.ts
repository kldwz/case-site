import { defineCollection, z } from 'astro:content';

const cases = defineCollection({
  type: 'content',
  schema: z.object({
    name: z.string(),
    一句话: z.string(),
    创始人地区: z.string().optional(),
    营收模式: z.string(),
    月收入估算: z.string().optional(),
    流量来源: z.string().optional(),
    可迁移点: z.string().optional(),
    原文链接: z.string().url().optional(),
    数据口径: z.string().optional(),
    分类: z.string(),
    封面: z.string().optional(),
  }),
});

export const collections = { cases };
