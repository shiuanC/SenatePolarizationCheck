# Libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as sp
import data


st.set_page_config(page_title='The trend of the Senate roll call vote', page_icon=':bar_chart:', layout='wide')


df = data.get_vote_df()
# Update the line chart to include bipartisan support
fig = px.line(df, x='congress', y=['total_roll_call_votes', 'passed_roll_call_votes', 'bipartisan_supported_votes'],
              labels={
                  "value": "Number of Roll Calls",
                  "variable": "Category"
              },
              title="Roll Call Votes Analysis per Congress Term")

# Streamlit app
st.title('Conclusion')
st.header('The trend of the Senate roll call vote')

# Plot the chart in the Streamlit app
st.plotly_chart(fig, use_container_width=True)

st.markdown("""
---
Reflecting on the line chart presented above, a notable observation emerges regarding the trends in Senate roll call votes. While the overall number of roll call votes has been on the rise, there is a distinctly contrasting trend concerning bills that receive bipartisan support. 

Significantly, around the year 2018, we observe a substantial decline in the number of bills that garnered backing from both major political parties. This shift marks a pivotal point in the legislative landscape, highlighting a possible increase in partisan divisions. 

The increasing frequency of roll call votes coupled with the dwindling instances of bipartisan cooperation paints a telling picture of the evolving dynamics within the US Senate. This trend potentially underscores a growing polarization, indicating that despite the higher legislative activity, the collaborative spirit across party lines may be waning.

These observations prompt deeper reflection on the state of political collaboration and partisanship in the US Senate, urging us to consider the implications of these trends on the legislative process and the broader political discourse.

---
""", unsafe_allow_html=True)
