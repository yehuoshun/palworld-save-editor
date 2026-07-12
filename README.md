# Palworld Save Editor

基于 [palworld-save-tools](https://github.com/oMaN-Rod/palworld-save-tools) 的 Web 版帕鲁存档编辑器。

## 开发计划

采用分步开发，每步验证后再推进：

1. **环境验证** — 安装 palworld-save-tools，测试存档互转
2. **读懂存档结构** — 解析 JSON，定位数据路径
3. **搭最小后端** — FastAPI + palworld-save-tools 程序化调用
4. **做一个功能** — 帕鲁列表读取 + 前端显示
5. **逐步加功能** — 编辑、保存、增删帕鲁

## 技术栈

- **后端**: Python 3.12+ / FastAPI / palworld-save-tools
- **前端**: Vue 3 + Vite（待定）
- **依赖管理**: uv (Python) / npm (前端)

## 环境要求

- Python 3.12+
- uv（`pip install uv`）
- palworld-save-tools（`uv add palworld-save-tools`）

## 运行

```bash
# 后端
uv sync
uv run uvicorn backend.main:app --reload

# 前端（待实现）
cd frontend && npm install && npm run dev
```