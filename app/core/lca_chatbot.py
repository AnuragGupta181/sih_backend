# # app/core/lca_chatbot.py
# """
# Chat-based insights generator using Groq LLM.
# """
# import json
# import re
# from langchain.prompts import PromptTemplate
# from langchain_groq import ChatGroq
# from langchain.schema import HumanMessage
# from app.config import get_settings

# settings = get_settings()
# llm = ChatGroq(model="llama-3.1-8b-instant", api_key=settings.GROQ_API_KEY)
# lca_prompt = PromptTemplate(
#     template="""
# You are an LCA Insights Expert for companies. You are NOT explaining what LCA is. 
# You are ONLY providing actionable, data-driven insights and recommendations based on the company's input data. 
# Your goal is to help the company **reduce GHG emissions, optimize resource use, and save costs**.

# Use the following data:

# {sample_row}

# Instructions:

# 1. Calculate total GHG emissions, energy consumption, water use, and other relevant metrics.
# 2. Highlight any inconsistencies in the data if present.
# 3. Provide specific improvement suggestions, for example:
#    - Switching transport modes (truck → rail) and estimate savings.
#    - Improving energy efficiency.
#    - Circularity improvements (reuse, recycling, remanufacturing).
# 4. Provide a concise summary of key metrics.
# 5. Respond **only in valid JSON** (no markdown, no extra text).
# 6. Use this exact JSON structure:

# {
#   "summary_table": [
#     {"metric": "Total GHG emissions (kgCO2)", "value": 0},
#     {"metric": "Energy consumption (MJ)", "value": 0},
#     {"metric": "Water use (m3)", "value": 0}
#   ],
#   "data_inconsistencies": [
#     "List any inconsistencies or [] if none"
#   ],
#   "recommendations": [
#     {"id": 1, "title": "Recommendation title", "details": "Detailed explanation"},
#     {"id": 2, "title": "...", "details": "..."}
#   ],
#   "estimated_savings": {
#     "energy_MJ": 0,
#     "emissions_kgCO2": 0,
#     "water_m3": 0,
#     "cost_usd_per_year": "0 - 0"
#   },
#   "overall_summary": "1-2 sentence professional summary of the analysis"
# }

# Question:
# {question}

# Answer:
# """,
#     input_variables=["sample_row", "question"]
# )


# def lca_chat(sample_row: dict, question: str) -> str:
#     """
#     Generates insights from the LCA data using Groq LLM.
#     """
#     prompt_text = lca_prompt.format(sample_row=sample_row, question=question)
#     messages = [HumanMessage(content=prompt_text)]
#     response = llm.invoke(messages)
#     return response.content



# app/core/lca_chatbot.py
"""
Chat-based insights generator using Groq LLM.
"""

from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage
from app.config import get_settings

settings = get_settings()
llm = ChatGroq(model="llama-3.1-8b-instant", api_key=settings.GROQ_API_KEY)

lca_prompt = PromptTemplate(
    template="""
You are an LCA Insights Expert for companies. You are NOT explaining what LCA is. 
You are ONLY providing actionable, data-driven insights and recommendations based on the company's input data. 
Your goal is to help the company **reduce GHG emissions, optimize resource use, and save costs**.

Use the following data:

{sample_row}

Instructions:

1. Calculate total GHG emissions, energy consumption, water use, and any other relevant metrics.
2. Highlight any inconsistencies in the data if present.
3. Provide specific suggestions for improvement, for example:
   - Using alternative transport (truck → rail) and estimating possible cost or emission savings.
   - Optimizing energy efficiency.
   - Recycling strategies or circularity improvements.
4. Provide a concise summary table of key metrics at the top.
5. Give recommendations in numbered actionable points.

Respond in a professional, business-oriented style.

Question:
{question}

Answer:
""",
    input_variables=["sample_row", "question"]
)


def lca_chat(sample_row: dict, question: str) -> str:
    """
    Generates insights from the LCA data using Groq LLM.
    """
    prompt_text = lca_prompt.format(sample_row=sample_row, question=question)
    messages = [HumanMessage(content=prompt_text)]
    response = llm.invoke(messages)
    return response.content



'''
trial

/predict/
{
    "Process_Type": "Primary",
    "Metal": "Aluminium",
    "Energy_MJ_per_kg": 210.5,
    "Quantity_kg": 1200,
    "Energy_MJ_total": null,
    "Transport_km": 150.0,
    "Transport_Mode": "Truck",
    "Transport_emissions_kgCO2": 45.7,
    "Water_use_m3_per_ton": 6.8,
    "End_of_Life": "Recycle",
    "Circularity_option": "Closed-loop",
    "Process_emissions_kgCO2": 520.3,
    "Total_emissions_kgCO2": null,
    "Emission_factor_kgCO2_per_MJ": 0.0021
}


/insights/
{
  "sample_row": {
    "Process_Type": "Primary",
    "Metal": "Aluminium",
    "Energy_MJ_per_kg": 210.5,
    "Quantity_kg": 1200,
    "Energy_MJ_total": null,
    "Transport_km": 150.0,
    "Transport_Mode": "Truck",
    "Transport_emissions_kgCO2": null,
    "Water_use_m3_per_ton": 6.8,
    "End_of_Life": "Recycle",
    "Circularity_option": "Closed-loop",
    "Process_emissions_kgCO2": null,
    "Total_emissions_kgCO2": 1096.46,
    "Emission_factor_kgCO2_per_MJ": 0.0021
  },
  "question": "tell summary how i can save my money"
}


output expected for /insights/:
{
  "summary_table": [
    {"metric": "Total GHG emissions (kgCO2)", "value": 552812.38},
    {"metric": "Energy consumption (MJ)", "value": 203767.95},
    {"metric": "Water use (m3)", "value": 910.0}
  ],
  "data_inconsistencies": [
    "Emission factor (0.02 kgCO2/MJ) seems unusually low for steel production."
  ],
  "recommendations": [
    {"id": 1, "title": "Optimize energy efficiency", "details": "Review furnaces and process control."},
    {"id": 2, "title": "Improve circularity", "details": "Consider recycling or remanufacturing."},
    {"id": 3, "title": "Switch transport mode", "details": "Switching from truck to rail may reduce emissions by 75%."}
  ],
  "estimated_savings": {
    "energy_MJ": 20377,
    "emissions_kgCO2": 55881,
    "water_m3": 70,
    "cost_usd_per_year": "15000 - 30000"
  },
  "overall_summary": "The metallurgy process shows high GHG emissions and energy use. Optimizing efficiency and improving circularity can yield significant savings."
}



'''