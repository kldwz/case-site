# _excluded/ —— 被剔除案例归档

本目录存放从 `src/content/cases/` 移出的、**不符合 case-site 内容规范**的案例。
- 移动（非删除），可逆：需要恢复时把文件移回 `src/content/cases/` 即可。
- 剔除标准与逐条原因见 `docs/剔除记录.md`。
- 自动生成脚本：`pipeline/audit_cases.py`（审计）、`pipeline/archive_cases.py`（归档）。
- 归档操作日志：`pipeline/_archive_log.txt`。

结构：
- `cases/<slug>.md`  被剔除的案例正文
- `public/<slug>/`   对应配图（若有）
