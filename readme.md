# lol-stats
Python script to find your League of Legends ranked statistics across all of your accounts.
This script finds your all time ranked statistics (Season 1 to Season 13) across all of your accounts and merges them. You will see your
- Total Games
- Total Wins
- Total Loses
- Win rate
- Average kills
- Average deaths
- Average assists
- Average KDA
- Average gold
- Average CS
- Most kills in game
- Most deaths in a game
- Total double,triple, quadra and penta kills
- Average damage dealt
- Average damage received

for each champion and a grand total.


## Requirements
The program needs some libraries to work. You can easily install them with a single command
```
pip install numpy pandas Flask selenium beautifulsoup4
```

You need Google Chrome and Chromedriver to be installed in your system, install Chromedriver from here
https://googlechromelabs.github.io/chrome-for-testing/#stable

## Usage

- Download the repo and run main.py
- Go to http://localhost:8123/ from your browser, you can interact with the program in browser.
- Enter all of your LOL accounts and their servers (euw, na, tr, kr etc.) and press "Submit". You can submit without any account to see an example result (Faker's account Hide on bush 😀)
- Now you should see "Gathering data for x accounts" and the program is working. You can see the progress in python program's console. Each time a season data for an account is fetched, it is printed to the console. The program should usually take 20-60 seconds.
- When it is completed you'll see the results in the browser. You can also download them using the "Download CSV" button. Python automatically downloads it as result.csv for your
- If you want to rerun it for different accounts, refresh the browser.

  Note: The program is multithreaded to process multiple accounts as fast as possible. It may consume a lot of CPU and RAM, this is normal.



## How it works
The program uses Selenium for web scrapping. It opens Google Chrome in background, visits op.gg page for each account and scrapes the data. Since op.gg doesn't provide an API for fast data retrieval, the only option is physically visiting it from browser. That's why the program is resource intensive and it takes long.





# Notes
- The program fetches data from op.gg . If op.gg is unavailable the program won't work.

- Sometimes it takes long for op.gg to respond. In that case you may need to wait for 5-10 minutes. Track the progress from Python console, it should print the progress like:
-
```
driver created
Recorded Season 2022 for https://www.op.gg/summoners/kr/hide%20on%20bush/champions
Recorded Season 2021 for https://www.op.gg/summoners/kr/hide%20on%20bush/champions
```

If it never prints "driver created", Chromedriver may not be correctly installed.


  





