import pandas as pd
from openai import OpenAI
import time
import io

def get_client(base_url, api_key):
    return OpenAI(base_url=base_url, api_key=api_key)

def call_llm(client, model, system_prompt, user_content):
    """
    通用 LLM 调用函数
    """
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            timeout=60
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def generate_eval_prompt(client, model, meta_system_prompt, sample_data):
    """
    生成评测 Prompt
    sample_data: 包含少量样本的字符串描述
    """
    user_content = f"请根据以下数据样本，按照System Prompt的要求，生成一个严格的打分System Prompt：\n\n{sample_data}"
    return call_llm(client, model, meta_system_prompt, user_content)

def process_step1_qa(df, config, progress_callback=None, status_callback=None):
    """
    第一步：批量生成答案
    """
    client = get_client(config["api_base_url"], config["api_key"])
    model = config["model_name"]
    system_prompt = config["qa_system_prompt"]
    
    col_eval = config["col_eval"]
    col_answer = config["col_answer"]
    
    total = len(df)
    
    for index, row in df.iterrows():
        if progress_callback:
            progress_callback((index + 1) / total)
            
        question = str(row[col_eval]) if pd.notna(row[col_eval]) else ""
        
        if status_callback:
            status_callback(f"[{index+1}/{total}] Generating Answer...")
            
        answer = call_llm(client, model, system_prompt, question)
        df.at[index, col_answer] = answer
        
    return df

def process_step2_eval(df, config, eval_system_prompt, progress_callback=None, status_callback=None):
    """
    第二步：批量评测
    """
    client = get_client(config["api_base_url"], config["api_key"])
    model = config["model_name"]
    
    col_source = config["col_source"]
    col_eval = config["col_eval"]
    col_answer = config["col_answer"]
    col_result = config["col_result"]
    
    total = len(df)
    
    for index, row in df.iterrows():
        if progress_callback:
            progress_callback((index + 1) / total)
            
        source = str(row[col_source]) if pd.notna(row[col_source]) else "无"
        question = str(row[col_eval]) if pd.notna(row[col_eval]) else ""
        model_ans = str(row[col_answer]) if pd.notna(row[col_answer]) else ""
        
        # 构造评测输入
        user_content = f"【数据源】：{source}\n【问题】：{question}\n【模型回答】：{model_ans}"
        
        if status_callback:
            status_callback(f"[{index+1}/{total}] Evaluating...")
            
        result = call_llm(client, model, eval_system_prompt, user_content)
        df.at[index, col_result] = result
        
    return df

def dataframe_to_bytes(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    output.seek(0)
    return output
