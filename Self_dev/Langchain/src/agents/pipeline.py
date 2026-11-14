from src.agents.agent import (
    build_analyse_agent,
    build_exercise_agent,
    build_diet_agent,
    build_sleep_agent,
    writer_chain
)
def run_research_pipeline(User_info : str) -> dict:

    state = {}
    #step 1 - analyse agent working 
    print("\n"+" ="*50)
    print("step 1 - analyse agent is working ...")
    print("="*50)

    analyse_agent = build_analyse_agent()
    analyse_result = analyse_agent.invoke({
        "messages" : [("user", f"Analyse the following user data and create action plans for three different agents: {User_info}")]
    })
    print("test **************??????????????????????????????")
    print(analyse_result['messages'])
    state["analyse_results"] = analyse_result['messages'][-1].content

    print("\n analyse result ",state['analyse_results'])

    #step 2 - exercise agent
    print("\n"+" ="*50)
    print("step 2 - exercise agent is working ...")
    print("="*50)
    exercise_agent = build_exercise_agent()
    exercise_result = exercise_agent.invoke({
        "messages" : [("user", f"Based on the following user data and analyse results, create a structured exercise plan: {User_info} \n\n Analyse Results:\n{state['analyse_results'][:800]}")]
    })
    state["exercise_results"] = exercise_result['messages'][-1].content
    print("\n exercise result ",state['exercise_results'])

    #step 3 - diet agent
    print("\n"+" ="*50) 
    print("step 3 - diet agent is working ...")
    print("="*50)
    diet_agent = build_diet_agent()
    diet_result = diet_agent.invoke({
        "messages" : [("user", f"Based on the following user data and analyse results, create a structured diet plan: {User_info} \n\n Analyse Results:\n{state['analyse_results'][:800]}")]
    })
    state["diet_results"] = diet_result['messages'][-1].content
    print("\n diet result ",state['diet_results'])

    #step 4 - sleep agent
    print("\n"+" ="*50)
    print("step 4 - sleep agent is working ...")
    print("="*50)
    sleep_agent = build_sleep_agent()
    sleep_result = sleep_agent.invoke({
        "messages" : [("user", f"Based on the following user data and analyse results, create a structured sleep and stress management plan: {User_info} \n\n Analyse Results:\n{state['analyse_results'][:800]}")]
    })
    state["sleep_results"] = sleep_result['messages'][-1].content
    print("\n sleep result ",state['sleep_results'])

    #step 5 - writer chain
    print("\n"+" ="*50) 
    print("step 5 - Writer is drafting the report ...")
    print("="*50)
    writer_combined = (
        f"EXERCISE RESULTS : \n {state['exercise_results']} \n\n"
        f"DIET RESULTS : \n {state['diet_results']} \n\n"
        f"SLEEP RESULTS : \n {state['sleep_results']} \n\n"
    )
    state["report"] = writer_chain.invoke({
        "Name" : User_info,
        "Recommendations" : writer_combined
    })

    return state