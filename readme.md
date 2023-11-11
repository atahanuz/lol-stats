# lol-stats
Python script to find your League of Legends ranked statistics across all of your accounts.
This script finds your all time ranked statistics (Season 1 to Season 13) across all of your accounts and merges them. You will see your:
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


## Installation
```
pip install lol-stats
```

Google Chrome must be installed on your system. The program automatically installs ChromeDriver binaries required for Selenium web scrapping.

## Usage
Lauch the program:

```
import lol_stats

lol_stats.launch()
```
In console you'll see that the program is launched. Go to
http://localhost:8126 from a browser to interact with the program.

To run the program on a different port, you pass an optional argument to launch() function:

```
lol_stats.launch(port=1234)
```




- Enter all of your LOL accounts and their servers (euw, na, tr, kr etc.) and press "Submit". You can submit without any account to see an example result (Faker's account "Hide on bush" 😀)
- Now you should see "Gathering data for x accounts" and the program is working. You can see the progress in Python program's console. Each time a season data for an account is fetched, it is printed to the console. The program should usually take 20-60 seconds.
- Upon completion, you'll see the results in your browser. You can also download them using the "Download CSV" button. Python will automatically download it as result.csv for your convenience.
- If you want to rerun it for different accounts, refresh the browser.

Note: The program is multithreaded to process multiple accounts as quickly as possible. This may cause high CPU and RAM usage, which is normal.

## Example Output
<img src="https://i.imgur.com/4CDufV2.png" width="100%" height="100%">



## How it works
The program uses Selenium for web scrapping. It opens Google Chrome in background, visits op.gg page for each account and scrapes the data. Since op.gg doesn't provide an API for fast data retrieval, the only option is physically visiting it from browser. This is why the program is resource-intensive and can take some time.



# Notes
- The program fetches data from op.gg. If op.gg is unavailable the program won't work. If the data on op.gg is wrong so will be the program's results.

- Sometimes it takes long for op.gg to respond. In that case you may need to wait for 5-10 minutes, or you can try again later. Track the progress from Python console, it should print the progress like:

```
Data for accounts:
https://www.op.gg/summoners/kr/hide%20on%20bush/champions
started processing
installing chromedriver
installed chromedriver
concurrent execution
started https://www.op.gg/summoners/kr/hide%20on%20bush/champions
Page is fully loaded.
time=  0.1226658821105957 seconds
1
hide_on_bush
Recorded Season 2023 S2 for https://www.op.gg/summoners/kr/hide%20on%20bush/champions
time=  0.705498218536377 seconds
2
hide_on_bush
Recorded Season 2023 S1 for https://www.op.gg/summoners/kr/hide%20on%20bush/champions
time=  0.6393542289733887 seconds
...
--- 18.71 seconds ---
ENDED !
```





  





