# Elementary School Student Battle Simulator 🥋✨

A multi-agent conversational system simulating playful arguments between elementary school students using DeepSeek API. Features dynamic role-playing, turn-based dialogue, and automated judging with scoring.

## 🌟 Project Showcase
![Battle Simulation Workflow](https://via.placeholder.com/800x400.png?text=Battle+Agent+Workflow)
*(Example workflow visualization - replace with actual screenshot)*

## 🔥 Core Features
- **Multi-Agent Workflow**: Two characters battle using distinct combat styles
- **Turn-Based Dialogue**: Simulates creative arguments through multiple rounds
- **Automated Judging**: Third agent evaluates performance with scores
- **Persistent Logging**: Automatic save to `battle_records.txt`
- **Customizable Personalities**: Easily modify character traits and rules

## ⚙️ Technical Implementation
```python
from openai import OpenAI
from typing import List, Dict
import os

# ===== CORE CONFIGURATION =====
BATTLE_ROUNDS = 15  # Total exchanges between agents
TEMPERATURE = 2     # Reply randomness for Xiao Ming/Hong
TEACHER_TEMPERATURE = 0.5  # Judge's scoring strictness

PROMPT0 = "Base personality: Elementary student using fictional moves..."
PROMPT1 = "Xiao Ming: Prefers physical attacks and brute force"
PROMPT2 = "Xiao Hong: Specializes in magical defenses and counters"

# Agent definitions and workflow logic...
