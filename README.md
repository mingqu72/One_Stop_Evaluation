# 一站式评测工具 (Auto-Eval Pro)

全自动问答生成与质量评测工作流工具，基于 Streamlit 和 LLM 构建。

## ✨ 核心功能

*   **直连 LLM**：支持 OpenRouter 或任意兼容 OpenAI 格式的 API。
*   **一站式工作流**：
    1.  **Step 1**: 批量生成答案。
    2.  **Step 2**: 智能生成打分标准（自动生成 Prompt，强制 0-5 分纯数字输出）。
    3.  **Step 3**: 批量自动打分。
*   **隐私安全**：API Key 仅保存在本地配置文件中，支持临时使用。
*   **极简设计**：深色沉浸式 UI，专注于数据处理。

## 🚀 快速开始

### 1. 安装依赖

确保已安装 Python 3.8+。

```bash
pip install -r requirements.txt
```

### 2. 启动工具

**方法 A：直接运行脚本**
双击 `start_tool.bat`。

**方法 B：命令行运行**
```bash
streamlit run app.py
```

### 3. 使用指南

1.  在左侧栏配置 **API Key** 和 **Model Name**。
2.  上传 Excel 数据文件。
3.  确认列名映射（数据源、问题集等）。
4.  按照页面引导依次执行 Step 1, 2, 3。
5.  下载处理完成的 Excel 报表。

## 📂 目录说明

*   `app.py`: 主程序
*   `processor.py`: 核心逻辑处理
*   `config.py`: 配置管理
*   `api_config_v2.json`: 配置文件（请在此填入 API Key，或在界面填写）
*   `.streamlit/`: Streamlit 样式配置

---
*Designed for Efficiency.*