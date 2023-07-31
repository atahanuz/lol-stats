import os

from flask import Flask, render_template, request, send_file
import urllib.parse
from multiprocessing import Manager
import pickle

import numpy as np
from urllib.parse import urlparse, unquote

import concurrent.futures
from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


from time import sleep
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.support.wait import WebDriverWait


app = Flask(__name__)
df=None
table_ready = False


@app.route('/', methods=['GET', 'POST'])
def index():
    print("11:45")
    global df
    global table_ready
    global arguments

    if request.method == 'POST':
        global arguments
        arguments = request.form['arguments']
        print(arguments)
        print("06:32")
        usernames = request.form.getlist('usernames')
        servers = request.form.getlist('servers')
        links = ["https://www.op.gg/summoners/tr/Fight4Glory/champions",
                 "https://www.op.gg/summoners/tr/AFC%20Unbreakable/champions",
                 "https://www.op.gg/summoners/euw/Rammus%20Hates%20Us/champions",
                 "https://www.op.gg/summoners/euw/JUNGLER%201%20vs%209/champions",
                 "https://www.op.gg/summoners/tr/quankiLLeR/champions",
                 "https://www.op.gg/summoners/tr/None%20Shall%20Live/champions"
                 ]

        #links=[]
        flag=False
        for username, server in zip(usernames, servers):
            if username=="0":
                flag=True
                break

            if username and server:
                name = urllib.parse.quote(username)
                string = f"https://www.op.gg/summoners/{server}/{name}/champions"
                links.append(string)

        if flag:
            print("reading mode")
            links=[]
        df = run(links,flag)
        table_ready=True
        #df = pd.read_csv('output.csv')
    if request.method == 'GET':
        table_ready=False
        df=None




    # result_table will be accessible here now
    if df is not None:
        return render_template('index.html', table=df.to_html(classes='data'),table_ready=table_ready)
    else:
        return render_template('index.html')

@app.route('/download')
def download():
    global df
    # Write DataFrame to CSV
    df.to_csv('output.csv', index=False)

    return send_file('output.csv', as_attachment=True)


def run(links,flag=False):
    with Manager() as manager:
        tables_list = manager.list()  # Shared list

        print("started processing")

        global arguments

        with concurrent.futures.ProcessPoolExecutor() as executor:
            print("concurrent execution")
            executor.map(worker, links, [tables_list]*len(links))



        return merger(list(tables_list),flag)











def worker(k,tables_list):

    options = webdriver.ChromeOptions()
    print("options created", options)

    options.add_argument("--headless")
    print("headless added")
    options.add_argument("window-size=1920,1080")
    print("window size added")
    driver = webdriver.Chrome(options=options)
    print("driver created")

    print("sequential execution")

    print(f"started {k}")
    driver.get(k)
    WebDriverWait(driver, 10).until(
        lambda driver: driver.execute_script('return document.readyState') == 'complete')


    main_button = driver.find_element(By.XPATH, '//span[text()="Season 2023 S2"]')

    driver.execute_script("arguments[0].click();", main_button)

    season_buttons = driver.find_elements(By.XPATH, '//button[starts-with(text(), "Season")]')

    season_names = [button.text for button in season_buttons]

    main_button.click()
    for j in range(0, len(season_names)):

        driver.execute_script("arguments[0].click();", main_button)

        button = driver.find_element(By.XPATH, f'//button[normalize-space()="{season_names[j]}"]')

        driver.execute_script("arguments[0].click();", button)

        # click the button

        sleep(1)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # suppose we're looking for a table on the web page
        table = soup.find('table')

        # get the page source and parse it with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # find all tables on the web page
        tables = soup.find_all('table')

        # convert the first table to a Pandas DataFrame and print it
        df = pd.read_html(str(tables[0]))[0]
        if df.shape == (1, 1):
            print(f"no data for {k} at {season_names[j]}")
            continue
        ## EDIT
        # extract 'Wins', 'Losses' and 'WinRate' from 'Column1'
        df['Wins'], df['Losses'], df['WinRate'] = df['Played'].str.extract('(?:(\d+)W)?(?:(\d+)L)?(\d+)%').T.values

        # replace missing 'Wins' and 'Losses' values with zeros
        df['Wins'].fillna(0, inplace=True)
        df['Losses'].fillna(0, inplace=True)

        # convert 'Wins' and 'Losses' to integers
        df['Wins'] = df['Wins'].astype(int)
        df['Losses'] = df['Losses'].astype(int)

        df['KDA'] = df['KDA'].str.split(":1").str[1]  # keep only the part after ":"
        df['Kill'], df['Death'], df['Assist'] = df['KDA'].str.split('/', expand=True).T.values

        # drop the original 'KDA' and 'Played' columns
        df.drop(columns=['KDA', 'Played', 'WinRate'], inplace=True)

        df['Death'] = df['Death'].str[1:]
        df['Assist'] = df['Assist'].str[1:]

        df['Kill'] = df['Kill'].astype(float)
        df['Assist'] = df['Assist'].astype(float)
        df['Death'] = df['Death'].astype(float)

        # get the list of columns
        cols = df.columns.tolist()


        # create the new order of columns
        cols = cols[:2] + cols[12:18] + cols[2:12] + cols[18:]

        # rearrange the columns
        df = df.reindex(columns=cols)

        df['Double Kill'] = df['Double Kill'].fillna(0).astype(int)
        df['Triple Kill'] = df['Triple Kill'].fillna(0).astype(int)
        df['Quadra Kill'] = df['Quadra Kill'].fillna(0).astype(int)
        df['Penta Kill'] = df['Penta Kill'].fillna(0).astype(int)

        df['Games'] = df['Wins'] + df['Losses']

        # Set the 'Games' column as the first column
        games_column = df['Games']  # Extract the 'Games' column
        df.drop(columns=['Games'], inplace=True)  # Drop the 'Games' column
        df.insert(2, 'Games', games_column)  # Insert the 'Games' column as the first column

        df = df.sort_values(by=['Games', 'Wins'], ascending=[False, False])

        # Reset the index to reindex the DataFrame with sorted order
        df.reset_index(drop=True, inplace=True)

        df['#'] = range(1, len(df) + 1)

        df = df.round(3)
        tables_list.append(df)
        print(len(tables_list))
        filename = unquote(urlparse(k).path.split('/')[3]).replace(' ', '_')
        print(filename)
        print(f"Recorded {season_names[j]} for {k}")


    print(f"finished {k}")

    driver.quit()


def merger(tables_list,flag):

    if flag:
        with open('file.pkl', 'rb') as file:

        # Call load method to deserialze
            tables_list = pickle.load(file)


    print(len(tables_list))
    # MERGING DATA ############
    #######################

    merged = pd.concat(tables_list)

    # add a new column for weighted kills
    merged['weighted_kills'] = merged['Kill'] * merged['Games']
    merged['weighted_deaths'] = merged['Death'] * merged['Games']
    merged['weighted_assists'] = merged['Assist'] * merged['Games']

    # update the aggregation rules to include the new column
    aggregation_rules = {
        'Games': 'sum',
        'Wins': 'sum',
        'Losses': 'sum',
        'Gold': 'mean',
        'CS': 'mean',
        'Double Kill': 'max',
        'Triple Kill': 'max',
        'Quadra Kill': 'max',
        'Penta Kill': 'max',
        'Max Kills': 'max',
        'Max Deaths': 'max',
        'Average Damage Dealt': 'mean',
        'Average Damage Taken': 'mean',
        'weighted_kills': 'sum',  # sum of weighted kills
        'weighted_deaths': 'sum',  # sum of weighted deaths
        'weighted_assists': 'sum',  # sum of weighted assists
    }


    result = merged.groupby('Champion').agg(aggregation_rules).reset_index()
    total_kills=result['weighted_kills'].sum()
    total_deaths=result['weighted_deaths'].sum()
    total_assists=result['weighted_assists'].sum()

    # compute the actual weighted average kills
    result['Kill'] = result['weighted_kills'] / result['Games']
    result['Death'] = result['weighted_deaths'] / result['Games']
    result['Assist'] = result['weighted_assists'] / result['Games']

    del result['weighted_kills']
    del result['weighted_deaths']
    del result['weighted_assists']

    result = result.sort_values(by=['Games', 'Wins'], ascending=[False, False])
    result['Winrate']=result['Wins']/result['Games']*100
    result.reset_index(drop=True, inplace=True)
    result['#'] = range(1, len(result) + 1)

    cols = result.columns.tolist()
    cols.insert(0, cols.pop(cols.index('#')))
    cols.insert(5, cols.pop(cols.index('Winrate')) )
    result = result[cols]


    result['KDA'] = (result['Kill'] + result['Assist']) / np.where(result['Death'] == 0, 1, result['Death'])

    # current order of columns
    cols = result.columns.tolist()

    # define positions to move 'kills', 'Death', and 'Assist'
    kill_idx = cols.index('Kill')
    death_idx = cols.index('Death')
    assist_idx = cols.index('Assist')
    kda_idx = cols.index('KDA')

    # move 'kills', 'Death', and 'Assist' to the 6th, 7th and 8th positions
    cols.insert(6, cols.pop(kill_idx))
    cols.insert(7, cols.pop(death_idx))
    cols.insert(8, cols.pop(assist_idx))
    cols.insert(9, cols.pop(kda_idx))
    # reindex the DataFrame
    result = result[cols]
    sum_wins = result['Wins'].sum()
    sum_loses = result['Losses'].sum()
    sum_games = sum_wins + sum_loses
    #add a new row to the table to show the total wins, loses and games
    # Create a new DataFrame for total row
    total = pd.DataFrame({

        'Champion': ['TOTAL'],
        'Games': [sum_games],
        'Wins': [sum_wins],
        'Losses': [sum_loses],
        'Winrate': [sum_wins/sum_games*100],
        'Kill': total_kills/sum_games,
        'Death': total_deaths/sum_games,
        'Assist': total_assists/sum_games,
        'KDA': (total_kills+total_assists)/(total_deaths),
        'Gold': [result['Gold'].mean()],
        'CS': [result['CS'].mean()],
        'Double Kill': [result['Double Kill'].sum()],
        'Triple Kill': [result['Triple Kill'].sum()],
        'Quadra Kill': [result['Quadra Kill'].sum()],
        'Penta Kill': [result['Penta Kill'].sum()],
        'Max Kills': [result['Max Kills'].max()],
        'Max Deaths': [result['Max Deaths'].max()],
        'Average Damage Dealt': [result['Average Damage Dealt'].mean()],
        'Average Damage Taken': [result['Average Damage Taken'].mean()],
    })

    # Setting other columns to NaN since they are not relevant for the 'Total' row
    for column in result.columns:
        if column not in total.columns:
            total[column] = np.nan

    # Append total row to the bottom of the result DataFrame
    result = pd.concat([total, result], ignore_index=False, sort=False)
    #drop the column named '#'
    del result['#']

    result.insert(0, '#', np.arange(len(result)))


    result = result.round(2)
    result.to_csv('data.csv', index=False)

    print(result)
    print("final recorded")
    return result





if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)