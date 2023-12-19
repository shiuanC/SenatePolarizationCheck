# Libraries
import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as sp
import altair as alt
import data

# Global Variables
theme_plotly = None # None or streamlit


# Config
# Title
st.set_page_config(page_title='The Senator\'s Activities 2015', page_icon=':bar_chart:', layout='wide')

# Title
st.title('Congressional Activities Analysis 2015')

# Short Description
st.markdown("""
This dashboard provides insights into the activities of US Congress members in 2015.
Explore the cooperation among congresspeople, their party affiliations, and the bills they sponsored.
""")

# Style
with open('style.css')as f: 
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

# Data Sources

network_df, legislator_df, bills_df = data.get_senator_data()

def create_cooperation_chart(network_df, legislator_df, selected_senator, party_filter):

    party_map = {'Democrat': 'D', 'Republican': 'R'}
    party_abbr = party_map[party_filter]

    # Filter the DataFrame based on the selected senator
    filtered_df = network_df[(network_df['senator1'] == selected_senator) | (network_df['senator2'] == selected_senator)]

    # Calculate cooperation weights
    cooperator_weights = filtered_df.apply(
        lambda row: (row['senator1'], row['edge_weight']) if row['senator2'] == selected_senator else (row['senator2'], row['edge_weight']), 
        axis=1
    )
    cooperator_weights_df = pd.DataFrame(cooperator_weights.tolist(), columns=['cooperator', 'weight'])

    # Aggregate weights by cooperator
    total_weights = cooperator_weights_df.groupby('cooperator').sum().sort_values(by='weight', ascending=False)

    # Merge party information from legislator_df
    total_weights = total_weights.merge(legislator_df[['name', 'party']], left_index=True, right_on='name')

    # Filter the top cooperators by the selected party
    top_cooperators = total_weights[total_weights['party'] == party_abbr]

    # Prepare data for bar chart
    chart_data = top_cooperators.head(10).set_index('name')['weight']

    chart_data = top_cooperators[['name', 'weight', 'party']].head(10)

    # Convert to long-form data for Altair
    long_form_data = pd.melt(chart_data,id_vars=['name', 'party'],  value_vars=['weight'])

    # Create Altair horizontal bar chart
    chart = (
        alt.Chart(long_form_data)
        .mark_bar()
        .encode(
            x=alt.X('value:Q', title='Cooperation Weight'),
            y=alt.Y('name:N', title='Senator', sort='-x'),         
            color=alt.Color('party:N', legend=None, scale=alt.Scale(domain=['D', 'R'], range=['blue', 'red']))
        )
    )

    return total_weights, chart

def get_sponsored_bills(selected_senator, legislator_df, bills_df):
    # Find the ID of the selected senator
    selected_senator_id = legislator_df[legislator_df['name'] == selected_senator]['id'].values[0]

    # Filter the bills where the selected senator is in the sponsor list
    sponsored_bills = bills_df[bills_df['sponsors'].apply(lambda x: selected_senator_id in x)]
    sponsored_bills = sponsored_bills[[ 'introduced', 'title', 'area','status']]

    return sponsored_bills

def create_pie_chart(top_cooperators):
    # Mapping abbreviations to full party names
    party_full_names = {'D': 'Democrat', 'R': 'Republican', 'I': 'Independent'}

    # Sum of weights by party
    party_weights = top_cooperators.groupby('party')['weight'].sum().reset_index()

    # Replace party abbreviations with full names
    party_weights['party'] = party_weights['party'].map(party_full_names)

    # Define colors for each party
    colors = {'Democrat': 'blue', 'Republican': 'red', 'Independent': 'green'}

    # Create a pie chart
    fig = px.pie(party_weights, values='weight', names='party', title='Total Bill Cooperation by Party', 
                 color='party', color_discrete_map=colors)

    return fig

full_info_to_name = pd.Series(legislator_df['name'].values, index=legislator_df['full_info']).to_dict()
full_info_list = legislator_df['full_info'].tolist()
selected_senator_info = st.selectbox('Select a Senator', full_info_list)
selected_senator = full_info_to_name[selected_senator_info]
   
# Checkbox to select the party
party_filter = st.radio("Choose a party to filter", ['Democrat', 'Republican'])



if selected_senator:
    total_weights, altair_chart = create_cooperation_chart(network_df, legislator_df, selected_senator, party_filter)
    pie_chart = create_pie_chart(total_weights)
    
    st.plotly_chart(pie_chart, use_container_width=True)
    st.altair_chart(altair_chart, use_container_width=True)

    sponsored_bills = get_sponsored_bills(selected_senator, legislator_df, bills_df).reset_index(drop=True)

    st.write(f"Bills Sponsored by the {selected_senator}:")
    st.dataframe(sponsored_bills)

