import streamlit as st
import config
import processor
import pandas as pd
import time
import os

# 页面配置
st.set_page_config(
    page_title="一站式评测",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 隐藏 Streamlit 默认的菜单和页脚 (加强版 CSS)
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stApp > header {display: none;} /* 强制隐藏顶部 header */
    div[data-testid="stToolbar"] {display: none;} /* 隐藏工具栏 */
    </style>
    """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# 加载配置
cfg = config.load_config()

# --- 东方神秘美学 CSS (健忘村风格) ---
st.markdown("""
<style>
    /* 引入更有韵味的字体 */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;700&display=swap');

    /* 全局背景与字体 */
    .stApp {
        background-color: #0F1C2E; /* 深海墨蓝 */
        background-image: linear-gradient(180deg, #0F1C2E 0%, #08101A 100%);
        color: #E0E6ED; /* 苍白 */
        font-family: 'Noto Serif SC', 'Source Han Serif CN', serif;
    }
    
    /* 隐藏顶部装饰条 */
    header[data-testid="stHeader"] {background-color: transparent;}

    /* 标题区域 */
    .main-title {
        font-size: 2.8rem;
        font-weight: 700;
        color: #F0F4F8;
        letter-spacing: 2px;
        margin-bottom: 0.5rem;
        text-shadow: 0 0 10px rgba(231, 76, 60, 0.3); /* 淡淡的红晕 */
    }
    .sub-title {
        font-size: 1.1rem;
        color: #8B9BB4; /* 雾霾蓝灰 */
        font-weight: 400;
        margin-bottom: 2.5rem;
        border-bottom: 1px solid #2C3E50;
        padding-bottom: 1rem;
    }

    /* 侧边栏美化 */
    section[data-testid="stSidebar"] {
        background-color: #162436; /* 比背景稍亮的墨色 */
        border-right: 1px solid #2C3E50;
        box-shadow: 5px 0 15px rgba(0,0,0,0.3);
    }
    section[data-testid="stSidebar"] .stMarkdown h3 {
        color: #E74C3C; /* 霞红 */
        font-family: 'Noto Serif SC', serif;
    }

    /* 隐藏密码框眼睛 & 禁止复制 (保留功能) */
    button[aria-label="Show password"] {
        display: none !important;
        visibility: hidden !important;
    }
    input[type="password"] {
        user-select: none !important;
    }

    /* 卡片式容器 - 磨砂玻璃感 */
    .stExpander, .step-container {
        background-color: rgba(30, 42, 59, 0.7); /* 半透明深蓝灰 */
        border: 1px solid #2C3E50;
        border-radius: 8px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px); /* 毛玻璃效果 */
        color: #E0E6ED;
        padding: 24px;
        margin-bottom: 24px;
    }
    
    /* 步骤标题 */
    .step-header {
        font-size: 1.3rem;
        font-weight: 700;
        color: #E74C3C; /* 晚霞橘红 */
        display: flex;
        align-items: center;
        margin-bottom: 20px;
        text-shadow: 0 0 5px rgba(231, 76, 60, 0.4);
    }
    .step-header::before {
        content: "✦"; /* 更有仪式感的符号 */
        display: inline-block;
        margin-right: 12px;
        color: #E74C3C;
    }

    /* 输入框优化 - 深色模式 */
    .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
        border-radius: 4px;
        border: 1px solid #4A5568;
        background-color: #0F1621; /* 极深背景 */
        color: #E0E6ED;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #E74C3C; /* 聚焦时发红光 */
        box-shadow: 0 0 8px rgba(231, 76, 60, 0.2);
    }
    /* 下拉框选项颜色修正 */
    ul[data-baseweb="menu"] {
        background-color: #1A2634;
    }

    /* 按钮优化 */
    .stButton button {
        border-radius: 4px;
        font-family: 'Noto Serif SC', serif;
        font-weight: 600;
        letter-spacing: 1px;
        transition: all 0.3s ease;
    }
    /* Primary 按钮 (霞红) */
    .stButton button[kind="primary"] {
        background-color: #9A2E22; /* 深红 */
        background-image: linear-gradient(135deg, #C0392B 0%, #8E261D 100%);
        color: #FFECEC;
        border: 1px solid #E74C3C;
    }
    .stButton button[kind="primary"]:hover {
        background-color: #E74C3C;
        box-shadow: 0 0 15px rgba(231, 76, 60, 0.4);
        transform: translateY(-1px);
    }
    /* Secondary 按钮 (幽蓝) */
    .stButton button[kind="secondary"] {
        background-color: #2C3E50;
        color: #AAB7C4;
        border: 1px solid #4A5568;
    }
    .stButton button[kind="secondary"]:hover {
        background-color: #34495E;
        color: #FFFFFF;
        border-color: #6C7A89;
    }

    /* 进度条颜色 */
    .stProgress > div > div > div > div {
        background-color: #E74C3C;
        background-image: linear-gradient(90deg, #E74C3C, #F39C12); /* 红橙渐变 */
    }
    
    /* 数据表格美化 */
    div[data-testid="stDataFrame"] {
        border: 1px solid #2C3E50;
        border-radius: 4px;
    }
</style>
""", unsafe_allow_html=True)

# 初始化 Session State
if "df" not in st.session_state:
    st.session_state.df = None
if "current_step" not in st.session_state:
    st.session_state.current_step = 1
if "generated_eval_prompt" not in st.session_state:
    st.session_state.generated_eval_prompt = ""

# --- 侧边栏：全局配置 ---
with st.sidebar:
    st.markdown("### ⚙️ 全局设置")
    st.caption("配置 LLM 服务端点")
    
    # 自动加载 Config 中的值作为默认值
    default_api_base = cfg.get("api_base_url", "https://openrouter.ai/api/v1")
    default_api_key = cfg.get("api_key", "")
    default_model_name = cfg.get("model_name", "")

    api_base = st.text_input("API Base URL", value=default_api_base)
    
    # API Key: type="password" 配合 CSS 隐藏眼睛
    api_key = st.text_input("API Key", value=default_api_key, type="password", help="您的 API 密钥将仅在本地使用")
    
    # Model Name: 如果 Config 里有值，就显示值；否则显示 placeholder
    # 这里我们直接把 default_model_name 填入 value，因为用户要求“下次打开就默认还是上次这个”
    model_name = st.text_input("Model Name", value=default_model_name, placeholder="请输入模型名字 (例如: openai/gpt-3.5-turbo)")
    
    st.write("") # Spacer
    if st.button("💾 保存配置", use_container_width=True):
        if not model_name:
            st.toast("请输入模型名称", icon="⚠️")
        else:
            cfg.update({
                "api_base_url": api_base,
                "api_key": api_key,
                "model_name": model_name
            })
            config.save_config(cfg)
            st.toast("配置已保存！下次打开将自动加载。", icon="✅")
    
    st.divider()
    st.markdown("""
    <div style="font-size: 0.8rem; color: #ADB5BD; text-align: center;">
        Auto-Eval Pro v2.2<br>
        Designed for Efficiency
    </div>
    """, unsafe_allow_html=True)

# --- 主界面 ---

st.markdown('<div class="main-title">一站式评测</div>', unsafe_allow_html=True)
st.caption("全自动问答生成与质量评测工作流")
st.markdown("---")

# 0. 文件上传区域
with st.container():
    st.markdown("#### 📂 数据导入")
    uploaded_file = st.file_uploader("请上传 Excel 数据文件 (.xlsx)", type=["xlsx"], label_visibility="collapsed")

if uploaded_file:
    # 读取文件
    if st.session_state.df is None:
        try:
            st.session_state.df = pd.read_excel(uploaded_file)
        except Exception as e:
            st.error(f"读取失败: {e}")
            st.stop()

    df = st.session_state.df
    all_cols = list(df.columns)

    # 1. 列映射区域
    with st.expander("🛠️ 列名映射配置 (如有不符请手动调整)", expanded=True):
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            col_source = st.selectbox("数据源列", all_cols, index=all_cols.index(cfg["col_source"]) if cfg["col_source"] in all_cols else 0)
        with c2:
            col_eval = st.selectbox("问题集列", all_cols, index=all_cols.index(cfg["col_eval"]) if cfg["col_eval"] in all_cols else 0)
        with c3:
            col_answer = st.text_input("生成答案列名 (输出)", value=cfg["col_answer"])
        with c4:
            col_result = st.text_input("评测结果列名 (输出)", value=cfg["col_result"])
            
        # 确保输出列存在
        if col_answer not in df.columns:
            df[col_answer] = ""
        if col_result not in df.columns:
            df[col_result] = ""

    # 更新临时配置
    temp_cfg = cfg.copy()
    temp_cfg.update({
        "col_source": col_source,
        "col_eval": col_eval,
        "col_answer": col_answer,
        "col_result": col_result,
        "api_base_url": api_base,
        "api_key": api_key,
        "model_name": model_name
    })

    st.write("") # Spacer

    # === Step 1: 批量生成答案 ===
    st.markdown('<div class="step-container">', unsafe_allow_html=True)
    st.markdown('<div class="step-header">Step 1: 批量生成答案</div>', unsafe_allow_html=True)
    
    c_left, c_right = st.columns([2, 1])
    with c_left:
        qa_prompt = st.text_area("问答 System Prompt", value=cfg.get("qa_system_prompt", ""), height=120, placeholder="请输入用于生成回答的系统提示词...")
    with c_right:
        st.markdown("<br>", unsafe_allow_html=True) # Spacer
        st.info("💡 提示: 此 Prompt 将用于指导模型如何回答 Excel 中的问题。")
    
    if st.button("执行生成 (Step 1)", type="primary", use_container_width=True, disabled=(not api_key or not model_name)):
        # 注意：此处不再自动保存配置，仅使用临时配置运行
        # temp_cfg["qa_system_prompt"] = qa_prompt 
        # config.save_config(temp_cfg) <--- 已移除自动保存
        
        # 将当前的 Prompt 更新到临时配置中用于本次运行
        temp_cfg["qa_system_prompt"] = qa_prompt
        
        progress = st.progress(0)
        status = st.empty()
        
        try:
            new_df = processor.process_step1_qa(df, temp_cfg, progress.progress, status.info)
            st.session_state.df = new_df
            st.session_state.current_step = 2
            status.success("✅ 答案生成完毕！")
            time.sleep(1)
            st.rerun()
        except Exception as e:
            st.error(f"执行出错: {e}")
    
    # 结果预览
    if not df[col_answer].astype(str).str.strip().eq("").all():
        with st.expander("👀 预览生成的答案 (前 5 行)"):
            st.dataframe(df[[col_eval, col_answer]].head(), use_container_width=True)
            
    st.markdown('</div>', unsafe_allow_html=True) # End Step 1

    # === Step 2: 自动生成评测 Prompt 并审核 ===
    st.markdown('<div class="step-container">', unsafe_allow_html=True)
    st.markdown('<div class="step-header">Step 2: 评测 Prompt 生成与审核</div>', unsafe_allow_html=True)
    
    if st.session_state.current_step >= 2:
        c_gen_btn, c_space = st.columns([1, 3])
        with c_gen_btn:
            if st.button("自动生成评测 Prompt", use_container_width=True):
                if not api_key:
                    st.error("请配置 API Key")
                else:
                    with st.spinner("正在分析数据特征..."):
                        # 强制重新加载最新配置，确保 Prompt 是最新的
                        latest_cfg = config.load_config()
                        
                        sample_data = df[[col_source, col_eval, col_answer]].head(3).to_string()
                        client = processor.get_client(api_base, api_key)
                        prompt_gen = processor.generate_eval_prompt(client, model_name, latest_cfg["eval_gen_system_prompt"], sample_data)
                        st.session_state.generated_eval_prompt = prompt_gen
                        st.rerun()

        final_eval_prompt = st.text_area(
            "📝 审核并编辑 Prompt", 
            value=st.session_state.generated_eval_prompt,
            height=180,
            placeholder="点击上方按钮自动生成，或在此直接输入评测 Prompt..."
        )
        
        if st.button("确认 Prompt 并继续", type="primary", use_container_width=True, disabled=(not final_eval_prompt)):
            st.session_state.generated_eval_prompt = final_eval_prompt
            st.session_state.current_step = 3
            st.rerun()
    else:
        st.info("请先完成 Step 1 以解锁此步骤")
        
    st.markdown('</div>', unsafe_allow_html=True) # End Step 2

    # === Step 3: 执行评测 ===
    st.markdown('<div class="step-container">', unsafe_allow_html=True)
    st.markdown('<div class="step-header">Step 3: 执行批量评测</div>', unsafe_allow_html=True)
    
    if st.session_state.current_step >= 3:
        if st.button("开始评测 (Step 3)", type="primary", use_container_width=True):
            progress = st.progress(0)
            status = st.empty()
            
            try:
                final_df = processor.process_step2_eval(
                    st.session_state.df, 
                    temp_cfg, 
                    st.session_state.generated_eval_prompt, 
                    progress.progress, 
                    status.info
                )
                st.session_state.df = final_df
                status.success("✅ 全流程处理完成！")
                st.balloons()
            except Exception as e:
                st.error(f"评测出错: {e}")

        if not df[col_result].astype(str).str.strip().eq("").all():
            st.success("🎉 所有任务已完成")
            output_io = processor.dataframe_to_bytes(st.session_state.df)
            timestamp = time.strftime("%H%M")
            st.download_button(
                label="📥 下载最终结果 (.xlsx)",
                data=output_io,
                file_name=f"AutoEval_Result_{timestamp}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                type="primary",
                use_container_width=True
            )
    else:
        st.info("请先完成 Step 2 的 Prompt 确认")
        
    st.markdown('</div>', unsafe_allow_html=True) # End Step 3

else:
    # 空状态页
    st.markdown(
        """
        <div style="
            border: 2px dashed #DEE2E6; 
            border-radius: 12px; 
            padding: 60px; 
            text-align: center; 
            background-color: #FFFFFF;
            margin-top: 20px;
        ">
            <h3 style="color: #ADB5BD; font-weight: 400;">👋 欢迎使用 Auto-Eval Pro</h3>
            <p style="color: #CED4DA;">请点击上方“Browse files”上传您的 Excel 数据集开始工作</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
