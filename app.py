import streamlit as st
import statistics
import pandas as pd
import altair as alt
import agent_workflow
import numpy as np
import ast

# file parser
@st.cache_data
def parse_files(dataset_file):
    df = pd.read_csv(dataset_file)

    df['correct_tools'] = df['correct_tools'].apply(ast.literal_eval)

    parsed_data = pd.DataFrame(
        columns=['model_answer', 'correct_answer', 'model_tools', 'correct_tools'])

    for index, row in df.iterrows():
        try:
            task_output = agent_workflow.process_task(row["instructions"], row["correct_tools"], row["correct_answer"])
            new_row = pd.DataFrame([{'model_answer': task_output['model_answer'],
                                     'correct_answer': task_output['correct_answer'],
                                     'model_tools': task_output['model_tools'],
                                     'correct_tools': task_output['correct_tools'], }])
        except Exception:
            new_row = pd.DataFrame([{'model_answer': 0,
                                     'correct_answer': 1,
                                     'model_tools': ['calculator'],
                                     'correct_tools': ['vector'], }])


        parsed_data = pd.concat([parsed_data, new_row], ignore_index=True)

    return parsed_data

@st.cache_data
def calculate_correct_steps(parsed_data):
    correct_lengths = []

    for index, row in parsed_data.iterrows():
        correct_lengths.append(len(row["correct_tools"]))

    correct_lengths = set(correct_lengths)

    correct_lengths = list(correct_lengths)

    correct_steps = {index: [] for index in correct_lengths}

    for index, row in parsed_data.iterrows():
        if row["model_answer"] == str(row["correct_answer"]):
            new_arr = correct_steps[len(row["correct_tools"])]
            new_arr.append(100)
            correct_steps[len(row["correct_tools"])] = new_arr
        else:
            new_arr = correct_steps[len(row["correct_tools"])]
            new_arr.append(0)
            correct_steps[len(row["correct_tools"])] = new_arr

    for key in correct_steps:
        correct_steps[key] = statistics.mean(correct_steps[key])

    output_df = pd.DataFrame(correct_steps.items(), columns=['Step', 'Success_Rate'])

    return output_df


@st.cache_data
def calculate_final_answer_rate(parsed_data):
    success_rows = []
    for index, row in parsed_data.iterrows():

        if row["model_answer"] == str(row["correct_answer"]):
            success_rows.append(100)
        else:
            success_rows.append(0)

    return statistics.mean(success_rows)

@st.cache_data
def calculate_task_planning_rate(parsed_data):
    success_rows = []
    for index, row in parsed_data.iterrows():
        if np.array_equal(row["model_tools"], row["correct_tools"]):
            success_rows.append(100)
        else:
            success_rows.append(0)

    return statistics.mean(success_rows)

def make_donut(input_response, input_text, input_color):
    if input_color == 'blue':
        chart_color = ['#29b5e8', '#155F7A']
    if input_color == 'green':
        chart_color = ['#27AE60', '#12783D']
    if input_color == 'orange':
        chart_color = ['#F39C12', '#875A12']
    if input_color == 'red':
        chart_color = ['#E74C3C', '#781F16']

    source = pd.DataFrame({
        "Topic": ['', input_text],
        "% value": [100 - input_response, input_response]
    })
    source_bg = pd.DataFrame({
        "Topic": ['', input_text],
        "% value": [100, 0]
    })

    plot = alt.Chart(source).mark_arc(innerRadius=45, cornerRadius=25).encode(
        theta="% value",
        color=alt.Color("Topic:N",
                        scale=alt.Scale(
                            # domain=['A', 'B'],
                            domain=[input_text, ''],
                            # range=['#29b5e8', '#155F7A']),  # 31333F
                            range=chart_color),
                        legend=None),
    ).properties(width=130, height=130)

    text = plot.mark_text(align='center', color="#29b5e8", font="Lato", fontSize=32, fontWeight=700,
                          fontStyle="normal").encode(text=alt.value(f'{input_response} %'))
    plot_bg = alt.Chart(source_bg).mark_arc(innerRadius=45, cornerRadius=20).encode(
        theta="% value",
        color=alt.Color("Topic:N",
                        scale=alt.Scale(
                            # domain=['A', 'B'],
                            domain=[input_text, ''],
                            range=chart_color),  # 31333F
                        legend=None),
    ).properties(width=130, height=130)
    return plot_bg + plot + text


# Streamlit app
def main():
    st.set_page_config(
        page_title="VELMA",
        page_icon="🏂",
        layout="wide",
        initial_sidebar_state="expanded")

    alt.themes.enable("dark")

    if 'clicked' not in st.session_state:
        st.session_state.clicked = False

    def click_button():
        st.session_state.clicked = True

    # File uploader
    with st.sidebar:
        st.title('🏂 VELMA')

        dataset_file = st.file_uploader("Dataset File", type=["csv"], accept_multiple_files=False)
        st.button('Submit', on_click=click_button)

    col = st.columns((1.5, 4.5, 2), gap='medium')

    if dataset_file is not None and st.session_state.clicked:

        with st.spinner("Generating Responses..."):
            parsed_data = parse_files(dataset_file)

        if len(parsed_data.index) > 0:
            with col[1]:
                line_data = calculate_correct_steps(parsed_data)
                line_chart = alt.Chart(line_data).mark_line().encode(
                    y=alt.Y('Success_Rate', title='Success Rate (%)'),
                    x=alt.X('Step', title='Step'),
                ).properties(
                    height=500, width=700,
                    title="Success Rate (%) vs Steps"
                )

                st.altair_chart(line_chart, use_container_width=True)

                options = ['Calculator Tool', 'Weather Tool', 'Monday Tool', 'SQL DB Tool', 'Vector DB Tool']
                #option = st.selectbox("Select an option:", options)

                #category_df = parsed_data
                #category_df['events'] = parsed_data[option]




            with col[0]:
                st.markdown('#### Final Answer Success Rate ####')
                donut_chart_greater = make_donut(
                    round(float(calculate_final_answer_rate(parsed_data))),
                    'Average Score', 'green')
                st.altair_chart(donut_chart_greater)

                st.markdown('#### Task Planning Success Rate ####')
                donut_chart_greater = make_donut(
                    round(float(calculate_task_planning_rate(parsed_data))),
                    'Average Score', 'green')
                st.altair_chart(donut_chart_greater)



            with col[2]:
                with st.container(height=1000):
                    # Display the download button
                    if st.button("Download Output as CSV"):
                        parsed_data.to_csv('output.csv', index=False)


if __name__ == "__main__":
    main()