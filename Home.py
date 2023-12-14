
# Libraries
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as sp
import data

# Confit
st.set_page_config(page_title='Explore the biartisan dynamic in the US senate', page_icon=':bar_chart:', layout='wide')

# Title
st.title('Explore the biartisan dynamic in the US senate')

st.markdown("""
    Welcome to our insightful exploration of political polarization in the US Senate. 
    In recent times, there has been a growing perception that politics are becoming 
    increasingly polarized. Our website delves into this phenomenon by analyzing 
    historical data from the US Senate to understand if such polarization is reflected 
    in Senate activities.

    **What You'll Discover Here:**

    1. **Trends in Bill Statuses:** The first section presents a comprehensive line 
    graph that illustrates the trends of various bill statuses throughout different 
    congress sessions. This visualization helps in identifying patterns and shifts 
    in the legislative process.

    2. **Senate Cooperation Analysis:** In the 'Now' page, we dive deeper into the 
    cooperation levels among senators. By exploring their collaborative efforts on 
    different bills, we can gauge the extent of bipartisan cooperation and its 
    evolution over time.

    3. **Assessing Polarization Through Roll Call Votes:** Finally, in the 'Conclusion' 
    page, our focus shifts to a detailed analysis of roll call votes. This critical 
    aspect will enable us to draw more concrete conclusions about the presence and 
    impact of polarization within the Senate.

    Our aim is to provide a data-driven perspective on the dynamics of the Senate, 
    offering a clearer understanding of how political polarization, if present, shapes 
    legislative processes. Navigate through the pages to uncover these insights and 
    form your own perspective on the state of political cooperation in the US Senate.
""")


# Global Variables
theme_plotly = None # None or streamlit


# Style
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

df = data.get_bill_data()

st.header('Line Chart of Bill Numbers in the US Congress Since 1974 ')

# Excluding 'Congress' from the columns to plot
columns_to_plot = [col for col in df.columns if col != 'Congress']

# Create checkboxes for each data column
selected_columns = []
for col in columns_to_plot:
    if st.checkbox(col, True, key=col):
        selected_columns.append(col)

if selected_columns:
    # Filter the DataFrame based on selected columns
    selected_columns = selected_columns+['Congress Number']

    filtered_data = df.reset_index()  # Resetting index to use 'Congress Number' as a column in Plotly
    filtered_data = filtered_data.loc[:, selected_columns]

    # Plotting logic using Plotly
    fig = px.line(filtered_data, x='Congress Number', y=filtered_data.columns[1:],
                    labels={'value': 'Values', 'variable': 'Bill typies', 'Congress Number': 'Congress'})
    fig.update_layout(title='Multi-Line Chart of Congressional Data', xaxis_title='Congress Number', yaxis_title='Values')
    fig.update_traces(hovertemplate='%{y} <br>: %{x}th')

    st.plotly_chart(fig)
else:
    st.write("Please select at least one column to plot.")



