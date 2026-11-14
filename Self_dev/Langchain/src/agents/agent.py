from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from .tools import web_search
from dotenv import load_dotenv


load_dotenv()

# Model Initialization
llm = ChatOpenAI(model = "gpt-4o-mini",temperature=0)

# Agent Initialization
def build_analyse_agent():
    return create_agent(
        model= llm,
        system_prompt="You are an expert in fitness and health. You are a helpful assistant. Please analyse the users data about his fitness against and create action plans for three different agents. 1. Exercise recommendation agent 2. Diet recommendation agent as per his preferred cuisine 3. Sleep and stress management agent. Please create a plan for each agent and provide the plan in a structured format."
    )

def build_exercise_agent():
    return create_agent(
        model= llm,
        system_prompt="find the best exercise plan for the user based on his fitness data and provide a structured plan with details of exercises, sets, reps, and duration. Use tools to find the best exercises as per goal of user and provide aligned exercises with the goal of user.",
        tools=[web_search]
    )

def build_diet_agent():
    return create_agent(
        model= llm,
        system_prompt="find the best diet plan for the user based on his fitness data and provide a structured plan with details of meals, ingredients, and nutritional information. Use tools to find the best diet as per goal of user and provide aligned diet with the goal of user.",
        tools=[web_search]
    )

def build_sleep_agent():
    return create_agent(
        model= llm,
        system_prompt="find the best sleep and stress management plan for the user based on his fitness data and provide a structured plan with details of techniques, routines, and duration. Use tools to find the best strategies as per goal of user and provide aligned approaches with the goal of user.",
        tools=[web_search]
    )

#writer chain 

writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert fitness report writer. Write clear, structured and insightful reports."),
    ("human", """Write a detailed plan on the for the user.

Name: {Name}

Data Gathered:
{Recommendations}

Structure the report as:
- About his fitness data, current state and goal
- Three sections
    1. Exercise recommendation agent
    2. Diet recommendation agent as per his preferred cuisine
    3. Sleep and stress management agent
- Tentative timeline to achive this
- Conclusion
- Motivation and encouragement to follow the plan

- Sources (list all URLs found in the research)

Be detailed, factual and professional."""),
])

writer_chain = writer_prompt | llm | StrOutputParser()