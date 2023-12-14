# Libraries
import streamlit as st
import pandas as pd
import glob
import os
import re

def reformat_name(name):
    parts = name.replace('Sen. ', '').split(', ')
    last_name = parts[0]
    first_name = parts[1].split(' [')[0]  

    # Reformatting the name
    reformatted_name = f"{first_name} {last_name}"
    return reformatted_name

def get_senator_data():
    path = '/data/sponsor/'  # Make sure this is the correct path to your folder
    matrix_df = pd.read_csv(path + 'matrix.csv', index_col=0)
    legislator_df = pd.read_csv(path + 'legislator.csv', index_col=0)
    bills_df = pd.read_csv(path + 'bills.csv', index_col=0)


    name_to_id = dict(zip(legislator_df['name'], legislator_df['id']))

    # Replace index names with ids
    matrix_df.index = [name_to_id[name] for name in matrix_df.index]

    legislator_df['full_info'] = legislator_df['name'] 
    
    legislator_df['name'] = legislator_df['full_info'].apply(reformat_name)

    network_data = []
    for i in range(len(matrix_df)):
        for j in range(i+1, len(matrix_df)):
            # Count the number of co-sponsored bills
            co_sponsored = sum(matrix_df.iloc[i] & matrix_df.iloc[j])

            # Append this data to the network_data list
            if co_sponsored > 0:
                network_data.append({
                    'senator1': matrix_df.index[i],
                    'senator2': matrix_df.index[j],
                    'edge_weight': co_sponsored
                })

    # Convert the list of dictionaries to a DataFrame
    network_df = pd.DataFrame(network_data)

    id_to_name = dict(zip(legislator_df['id'].astype(str), legislator_df['name']))
    # id_to_name[network_df.senator1[0]]
    network_df['senator1'] = network_df['senator1'].map(id_to_name)
    network_df['senator2'] = network_df['senator2'].map(id_to_name)

    # Initialize an empty list to store the sponsors for each bill
    sponsors = []

    # Iterate over each bill in bills_df
    for index, row in bills_df.iterrows():
        bill_id = row['bill']  # Assuming 'bill' contains bill IDs like 'SRES157'

        # Find sponsors from matrix_df where the bill column is 1
        sponsor_ids = matrix_df.index[matrix_df[bill_id] == 1].tolist()
        sponsors.append(sponsor_ids)

    # Add the sponsors list as a new column in bills_df
    bills_df['sponsors'] = sponsors

    return network_df, legislator_df, bills_df


def remove_text_after_newline(cell):
    return cell.split('\n')[0] if pd.notna(cell) else cell

def remove_text_in_parentheses(text):
    return re.sub(r'\(.*?\)', '', text).strip()

def convert_to_int(cell):
    try:
        # Convert cell to integer
        return int(cell)
    except ValueError:
        # If conversion fails, try removing non-numeric characters and convert again
        numeric_part = ''.join(filter(str.isdigit, cell))
        return int(numeric_part) if numeric_part else None
  

def get_bill_data():
        
    path_name = '/data/'
    df = pd.read_csv(path_name + 'history_bill.csv', index_col=0)
    # Apply the function to each cell in the DataFrame
    df = df.applymap(remove_text_after_newline)

    # Apply the function to the index if it's of object type (i.e., string)
    if df.index.dtype == 'O':  # 'O' stands for object
        df.index = df.index.map(remove_text_after_newline)
        

    # Remove text within parentheses from column names
    df.columns = [remove_text_in_parentheses(col) for col in df.columns]

        
    # Convert all cell values to integers
    df = df.applymap(convert_to_int)
    df = df.reset_index()
    df['Congress Number'] = df.Congress.str.extract('(\d+)').astype(int)

    # Move 'Congress Number' to the first column
    # df = df[ ['Congress Number'] + [ col for col in df.columns if col != 'Congress Number' ] ]
    df= df.set_index('Congress Number')
    duplicated_columns = df.columns[df.columns.duplicated(keep=False)]

    df = df.loc[:, ~df.columns.duplicated(keep='first')]
    return df


def get_vote_df():
    path_name = '/data/'
    df = pd.read_csv(path_name + 'roll_call.csv', index_col=0)
    # Aggregate data by congress
    df['democratic_total'] = df['democratic_yes'] + df['democratic_no'] + df['democratic_not_voting']
    df['republican_total'] = df['republican_yes'] + df['republican_no'] + df['republican_not_voting']

    df['bipartisan_support'] = ((df['democratic_yes'] >= df['democratic_total'] / 2) &
                            (df['republican_yes'] >= df['republican_total'] / 2))


    congress_data = df.groupby('congress').agg(
        total_roll_call_votes= pd.NamedAgg(column='congress', aggfunc='count'),
        passed_roll_call_votes=pd.NamedAgg(column='pass', aggfunc=lambda x: (x == 'pass').sum()),
        bipartisan_supported_votes=pd.NamedAgg(column='bipartisan_support', aggfunc='sum')
    ).reset_index()

    return congress_data
