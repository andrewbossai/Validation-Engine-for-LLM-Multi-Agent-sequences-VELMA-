import asyncio
from weather_tool import get_temp, get_hum, get_precip
import pandas as pd
import ast

async def generate_dataset(batch):
    generated_data = pd.DataFrame(
        columns=['instructions', 'correct_tools', 'correct_answer'])
    match batch:
        case 1:
            new_row = pd.DataFrame([{'instructions': "What is the temperature in New York City?",
                                     'correct_tools': ["weather"],
                                     'correct_answer': await get_temp("New York"), }])
        case 2:
            new_row = pd.DataFrame([{'instructions': "What is the temperature in Tokyo?",
                                      'correct_tools': ["weather"],
                                      'correct_answer': await get_temp("Tokyo"), }])
        case 3:
            new_row = pd.DataFrame([{'instructions': "What is the sum of the temperature in Tokyo and the temperature in New York?",
                                      'correct_tools': ["weather","weather","calculator"],
                                      'correct_answer': await get_temp("New York") + await get_temp("Tokyo"), }])

        case 4:
            new_row = pd.DataFrame([{'instructions': "What is the humidity in London?",
                                      'correct_tools': ["weather"],
                                      'correct_answer': await get_hum("London"), }])
        case 5:
            new_row = pd.DataFrame([{'instructions': "What is the precipitation in Sydney?",
                                      'correct_tools': ["weather"],
                                      'correct_answer': await get_precip("Sydney"), }])
        case 6:
            new_row = pd.DataFrame(
                [{'instructions': "What is the multiplicative product of the precipitation in Dallas and the humidity in Houston?",
                  'correct_tools': ["weather", "weather", "calculator"],
                  'correct_answer': await get_precip("Dallas") * await get_hum("Houston"), }])

        case 7:
            new_row = pd.DataFrame([{'instructions': "What is the precipitation in Cairo?",
                                      'correct_tools': ["weather"],
                                      'correct_answer': await get_precip("Cairo"), }])
        case 8:
            new_row = pd.DataFrame([{'instructions': "Is it raining in Orlando?",
                                      'correct_tools': ["weather"],
                                      'correct_answer': "Yes" if await get_precip("Orlando") > 0 else "No", }])

    generated_data = pd.concat([generated_data, new_row], ignore_index=True)
    dataset_df = pd.read_csv('dataset_with_weather.csv')
    dataset_df['correct_tools'] = dataset_df['correct_tools'].apply(ast.literal_eval)

    new_dataset_df = pd.concat([dataset_df, generated_data], ignore_index=True)

    new_dataset_df.to_csv('dataset_with_weather.csv', index=False)


asyncio.run(generate_dataset(6))