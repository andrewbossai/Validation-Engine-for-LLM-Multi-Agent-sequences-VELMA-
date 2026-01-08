import agent_prompts
import openai_api_agent
import calculator_tool
import weather_tool
import sql_db_tool
import vector_db_tool
import monday_tool
import asyncio
import ast



def process_task(instructions, correct_tools, correct_answer):

    planning = openai_api_agent.call_model(agent_prompts.general_task_prompt + instructions + agent_prompts.planning_prompt)
    model_tools = ast.literal_eval(planning)

    previous_tool_answers = "\n**** Previously Evaluated Tool Answers ****"

    for tool in model_tools:

        match tool:

            case "calculator":
                tool_prompt = agent_prompts.calculator_prompt
                tool_use_json = openai_api_agent.call_model(
                    agent_prompts.general_tool_prompt + instructions + f"\n **** Tools to Use****\n{model_tools}" + previous_tool_answers + tool_prompt)

                previous_tool_answers += calculator_tool.use_calculator(*ast.literal_eval(tool_use_json))

            case "weather":
                tool_prompt = agent_prompts.weather_prompt
                tool_use_json = openai_api_agent.call_model(
                    agent_prompts.general_tool_prompt + instructions + f"\n **** Tools to Use****\n{model_tools}" + previous_tool_answers + tool_prompt)

                previous_tool_answers += asyncio.run(weather_tool.use_weather(tool_use_json))

            case "sql_db":
                tool_prompt = agent_prompts.sql_db_prompt
                tool_use_json = openai_api_agent.call_model(
                    agent_prompts.general_tool_prompt + instructions + f"\n **** Tools to Use****\n{model_tools}" + previous_tool_answers + tool_prompt)

                previous_tool_answers += sql_db_tool.use_sql(*ast.literal_eval(tool_use_json))

            case "vector_db":
                tool_prompt = agent_prompts.vector_db_prompt
                tool_use_json = openai_api_agent.call_model(
                    agent_prompts.general_tool_prompt + instructions + f"\n **** Tools to Use****\n{model_tools}" + previous_tool_answers + tool_prompt)

                previous_tool_answers += vector_db_tool.query(*ast.literal_eval(tool_use_json))

            case "monday":
                tool_prompt = agent_prompts.monday_prompt
                tool_use_json = openai_api_agent.call_model(
                    agent_prompts.general_tool_prompt + instructions + f"\n **** Tools to Use****\n{model_tools}" + previous_tool_answers + tool_prompt)

                previous_tool_answers += monday_tool.use_monday(*ast.literal_eval(tool_use_json))


    model_answer = openai_api_agent.call_model(agent_prompts.answer_prompt + instructions + f"\n **** Tools Used****\n{model_tools}" + previous_tool_answers)

    return {'model_answer': model_answer, 'correct_answer': correct_answer, 'model_tools': model_tools, 'correct_tools': correct_tools}
