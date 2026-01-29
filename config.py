import json
import os

CONFIG_FILE = "api_config_v2.json"

DEFAULT_CONFIG = {
    # 全局 API 设置
    "api_base_url": "https://openrouter.ai/api/v1",
    "api_key": "",
    "model_name": "openai/gpt-3.5-turbo", # 默认模型，可修改

    # Prompts
    "qa_system_prompt": "你是一个智能助手，请根据问题提供准确、简洁的回答。",
    "eval_gen_system_prompt": """# 角色 

你是专业的【打分prompt】生成专家，核心职责是根据我提供的「system prompt」，生成一份对应的「打分prompt」，确保两者完全对齐，无任何表述冲突、无规范遗漏，且「打分prompt」只能输出一个最终分数数字。 

# 核心前提（必须优先明确，严格遵循） 

明确「system prompt」的核心作用的：作为「system prompt」专属应答智能体的规范，指导智能体根据问题集、模型回答答案来回应相关问题，智能体应答的唯一参考答案为“数据源”，所有应答需依托数据源、结合数据集及模型回答答案，不编造、不遗漏关键信息。且「打分prompt」只能输出一个最终分数数字 

# 打分prompt生成核心要求（严格执行，逐条落实） 

1.  对齐一致性：生成的判断prompt，所有条款必须完全对齐「system prompt」的所有规范，不放宽、不提高评测标准，不添加「system prompt」以外的任何判断依据。「打分prompt」只能输出一个最终分数数字。 

2.  同步新作用：必须将「system prompt」的新作用（结合数据集、模型回答答案，参考答案为数据源）同步到判断prompt的所有相关模块，重点调整： 

    - 核心判断依据：明确评测时，需判断应答答案是否“依托数据源、结合数据集及模型回答答案”精准应答； 

    - 具体判断标准：将所有“依托数据集”“调用知识库”的表述，统一改为“依托数据源、结合数据集及模型回答答案”； 

    - 特殊情况规范：同步「system prompt」中“提问未在数据源内”的应答要求，确保评测标准与system prompt完全一致。 

3.  核心功能保留：生成的判断prompt，核心用途为「检测system prompt对应的应答答案」，需明确判断员身份、判断目的、具体判断标准、打分规则、判断注意事项，缺一不可。 

4.  打分规则强制要求：严禁出现“分”“得分”“打分原因”“标注”等任何多余表述，且「打分prompt」只能输出一个最终分数数字。 

5.  格式要求：生成的判断prompt，需与我提供的「system prompt」格式保持一致——采用markdown格式，保留#号、**加粗**符号，标题层级清晰（一级标题#、二级标题##），排版整洁。 

6.  无冗余要求：不添加任何与“生成打分prompt”无关的内容，不编造判断条款，不偏离「system prompt」的核心规范，确保生成的判断prompt可直接落地使用，无需二次修改。 

7.「打分prompt」只能输出一个最终分数数字。""",
    
    # 默认列映射
    "col_source": "数据源",
    "col_eval": "问题集",
    "col_answer": "模型回答答案",
    "col_result": "答案评测"
}

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                # 合并默认配置，防止新版本缺少字段
                loaded = json.load(f)
                config = DEFAULT_CONFIG.copy()
                config.update(loaded)
                return config
        except Exception:
            return DEFAULT_CONFIG
    return DEFAULT_CONFIG

def save_config(config):
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving config: {e}")
        return False
