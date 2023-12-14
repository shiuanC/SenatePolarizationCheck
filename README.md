# SenatePolarizationCheck


**Navigating the Tides of US Senate Politics: An Insightful Visualization Journey**

## Executive Summary
In an era where political polarization often headlines our daily news, our latest visualization project offers a deep dive into the legislative dynamics of the US Senate. Harnessing the power of data visualization, this project unravels the intricate patterns of bill statuses, bipartisan cooperation, and roll call votes from 2000 to 2022. Aimed at the vibrant data visualization community, this blog post peels back the layers of our project, offering a glimpse into the data, methods, and technologies that brought our insights to life.

## Visualization Link
[US Senate Polarization Analysis Visualization](#)

## Current Context
With rising concerns about political polarization in the US, our project zeroes in on the US Senate, a crucible where national policies are debated and shaped. We explore whether this perceived polarization is mirrored in the Senate's legislative activities and roll call votes.

## Intended Audience
This project primarily targets data enthusiasts, policymakers, political analysts, and anyone intrigued by the ebb and flow of political trends in the US Senate.

## Data Sources and Transformations

### Historical Bill Statistics
- **Source:** [GovTrack Bill Statistics](https://www.govtrack.us/congress/bills/statistics)
- **License:** Openly accessible with appropriate citation.
- **Collection Methods:** Compiled by GovTrack, a civic project to track Congress.
- **Biases/Sampling:** Broad representation of congressional activities, though subject to reporting standards of GovTrack.
- **Descriptive Statistics:** Covers a wide range of legislative data including bill types, statuses, and outcomes.
- **Data Cleaning & Issues:** Standardized for uniformity; no significant issues identified.
- **Privacy:** Publicly available data; no privacy concerns.

### Sponsorship Data
- **Source:** Neal, Z. P. (2022) - 'incidentally' R package.
- **License:** Open source, available for academic and research use.
- **Collection Methods:** Derived from Neal's extensive research and data compilation.
- **Biases/Sampling:** Reflects the scope of the study conducted by Neal.
- **Descriptive Statistics:** Involves data on bill sponsorships and co-sponsorships in the Senate.
- **Data Cleaning & Issues:** Adapted to suit visualization needs; minimal discrepancies noted.
- **Privacy:** Data is aggregated and anonymized.

### Roll Call Votes
- **Source:** [ProPublica Congress API](https://www.propublica.org/datastore/api/propublica-congress-api)
- **License:** Free for educational and non-commercial use.
- **Collection Methods:** Aggregated by ProPublica from official congressional records.
- **Biases/Sampling:** Comprehensive coverage of roll call votes; relies on ProPublica's data integrity.
- **Descriptive Statistics:** Extensive dataset of vote counts, decisions, and party lines.
- **Data Cleaning & Issues:** Consistency checks conducted; alignment with congressional records confirmed.
- **Privacy:** Public domain data, no individual privacy issues.

## Technologies/Platforms Used
- **Streamlit:** For creating an interactive web application.
- **Plotly and Altair:** For robust and insightful visualizations.
- **Pandas and NumPy:** For efficient data manipulation and analysis in Python.
- **R (incidentally package):** For sponsorship data processing and analysis.

## Analysis Summary
Our goal was to illuminate the trends in Senate voting and cooperation over the last two decades. Key insights include an uptick in roll call votes, a marked decline in bipartisan support post-2018, and shifting patterns in legislative sponsorships. These findings not only reflect the political pulse of the Senate but also serve as a barometer for understanding broader political narratives in the US.

## Conclusion
This visualization project transcends mere number-crunching, offering a narrative on the Senate's political landscape. It's a tool for dialogue and discovery in the realms of policy-making and political analysis, highlighting key stories and trends that shape our understanding of Senate politics.

