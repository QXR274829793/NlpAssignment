
from openai import OpenAI
from typing import List, Dict
import os

# 1. 配置DeepSeek API（替换为你的密钥）
deepseek_api_key = "your api"
client = OpenAI(
    api_key=deepseek_api_key,
    base_url="https://api.deepseek.com"
)

BATTLE_ROUNDS = 15  # 对话轮数（可调整）
TEMPERATURE = 2  # 小明/小红的回复随机性
TEACHER_TEMPERATURE = 0.5  # 点评的严谨性
PROMPT0 = "你是一个小学生，现在在和同学吵架，要用虚构的招式击败对方。尽量使用更多更炫酷的技能，不要模仿对方的攻击招式和风格，打法要和对方有差异。注意说话风格，体现小学生喜欢扮酷的性格，但是不要有太多的高级词汇" #公共提示词
PROMPT1 = "你喜欢看战斗类型的动画片，擅长正面进攻，一力破万法" #小明提示词
PROMPT2 = "你喜欢看魔法动画片，擅长使用不同的魔法以柔克刚" #小红提示词

# 2. 定义智能体配置（小明、小红、老师）
agents = [
    {
        "name": "小明",
        "system_prompt": PROMPT0 + PROMPT1,
        "messages": []  # 对话历史
    },
    {
        "name": "小红",
        "system_prompt": PROMPT0 + PROMPT2,
        "messages": []  # 对话历史
    }
]

# 2.2 （点评者）
judge = {
    "name": "小刚",
    "system_prompt": """你是观战的同学，需要点评小明和小红的吵架。对小明和小红分别作出评价并且决出胜者，评判维度如下：
    1. **招式创意**（0-10分）：是否使用了新颖的虚构招式？
    2. **反驳力度**（0-10分）：是否直接回应对方的攻击，逻辑连贯？
    3. **招式合理性**（0-10分）：出招是否合理？""",
    "messages": []  # 存储对话历史
}

# 3. 定义生成回复的函数
def generate_response(agent: Dict, temperature: float = TEMPERATURE) -> str:
    messages = [
        {"role": "system", "content": agent["system_prompt"]},  # 系统提示
        *agent["messages"]  # 对话历史
    ]
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        temperature=temperature
    )
    return response.choices[0].message.content

# 4. 启动对话（小明发起第一句话）
initial_message = "来战斗吧！"
dialogue_history = [{"role": "user", "name": "小明", "content": initial_message}]  # 记录完整对话历史
agents[1]["messages"].append({"role": "user", "content": initial_message})  # 向小红传递初始消息

# 5. 运行多轮对话（小明vs小红）
print("⚔️ 小明vs小红 吵架开始！\n")
for round in range(BATTLE_ROUNDS):
    # 小红回复小明
    xiaohong_response = generate_response(agents[1])
    print(f"🔴 小红: {xiaohong_response}")
    dialogue_history.append({"role": "assistant", "name": "小红", "content": xiaohong_response})  # 保存小红的回复
    agents[0]["messages"].append({"role": "user", "content": xiaohong_response})  # 向小明传递小红的回复
    
    # 小明回复小红
    xiaoming_response = generate_response(agents[0])
    print(f"🔵 小明: {xiaoming_response}")
    dialogue_history.append({"role": "assistant", "name": "小明", "content": xiaoming_response})  # 保存小明的回复
    agents[1]["messages"].append({"role": "user", "content": xiaoming_response})  # 向小红传递小明的回复
    
    print(f"--- 第{round+1}轮结束 ---\n")

# 6. 战斗结束，老师点评
print("\n" + "="*50)
print("🔔 点评时间到！")
print("="*50 + "\n")

# 构造老师的对话输入（对话历史）
teacher_input = "以下是小明和小红的对话历史，请点评：\n" + "\n".join([f"[{msg['name']}]：{msg['content']}" for msg in dialogue_history])
judge["messages"] = [{"role": "user", "content": teacher_input}]  # 将对话历史存入老师的messages

# 生成老师的点评
teacher_response = generate_response(judge, temperature=TEACHER_TEMPERATURE)
print(f"📝 : {teacher_response}")

def save_battle_records(dialogue_history: List[Dict], teacher_feedback: str):
    """将对话历史和老师点评保存到源文件同目录"""
    # 1. 获取源文件所在目录（绝对路径）
    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)
    
    # 2. 生成唯一文件名（时间戳+前缀）
    output_filename = f"battle_records.txt"
    output_path = os.path.join(script_dir, output_filename)
    
    # 3. 格式化内容（易读格式）
    formatted_dialogue = "\n".join([
        f"[{msg['name']}]：{msg['content']}" 
        for msg in dialogue_history
    ])
    formatted_feedback = f"\n📝 同学点评：\n{teacher_feedback}"
    
    # 4. 写入文件（utf-8编码，避免中文乱码）
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("⚔️ 小明vs小红 吵架记录\n")
        f.write("="*50 + "\n")
        f.write(formatted_dialogue)
        f.write("\n" + "="*50 + "\n")
        f.write(formatted_feedback)
    
    # 5. 提示用户文件保存位置
    print(f"\n📄 战斗记录已保存到：{output_path}")

# 调用函数保存记录
save_battle_records(dialogue_history, teacher_response)
