import { defineCollection, z } from 'astro:content';

// 内容类型：决定正文模板与必填字段（见进度文档第四节）
//   收入案例   - 有收入数字 + 官网 + 独立核验来源（存量 190 篇属此类）
//   国内实践   - 不要求官方披露收入，靠平台硬数据或作者自述
//   获奖作品   - 大赛/黑客松获奖，无收入，讲想法与解法，必须能查到赛事官方公示页
//   插件       - 浏览器扩展/小工具，安装数公开可查，收入可只给估算区间
//   开源变现   - GitHub 数据可查 + 有商业化动作
export const CASE_TYPES = ['收入案例', '国内实践', '获奖作品', '插件', '开源变现'] as const;

// 证据等级（首页/详情页 badge 展示，读者自行判断可信度）
//   官方披露       - 公司/创始人自己公布，或权威媒体报道的公司口径数字
//   平台数据可查   - App Store 排名评分 / Steam 销量 / 商店安装数 / 众筹金额 / 工商可查
//   作者自述       - 本人公开说过（微博/知乎/公众号/推），附原文链接
//   第三方估算     - SimilarWeb / Chrome-Stats 类推算，只给区间不给精确数
//   公开资料       - 公开报道/官网/赛事公示等可查资料（国内实践非平台类案例常用）
export const EVIDENCE_LEVELS = ['官方披露', '平台数据可查', '作者自述', '第三方估算', '公开资料'] as const;

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
    // ↓ 2026-09-12 新增：类型体系 + 证据等级
    类型: z.enum(CASE_TYPES).default('收入案例'),
    证据等级: z.enum(EVIDENCE_LEVELS).default('官方披露'),
    // 具体可查的平台硬数据，如「App Store 效率榜 Top 20 / 4.8 分 1.2 万评价」
    平台数据: z.string().optional(),
    // 获奖作品专用：什么比赛、什么场景/赛道、拿了什么奖
    赛事: z.string().optional(),
    场景: z.string().optional(),
    奖项: z.string().optional(),
  }),
});

export const collections = { cases };
