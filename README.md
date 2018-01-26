# CS50 2017/2018 Problem Sets & My project

Backup


## Pset 1: C
water.c : 
mario.c :
greedy.c : 

Very basic


## Pset2:  C Contiuned
caesar.c : a program to caesar cipher a text


vigenere.c : a program to vigenere cipher a text


## Pset 3: Game of Fifteen C continued
fifteen.c : a game of fifteen games


## Pset 4: Recover , C to manipulate files
whodunit.c : a program that  analyze an image and change it. Well designed image.

resize.c : resize a image

recover.c : a program that recovers a image which is still well designed.


## Pset 5: Speller using hash table to check the correctness of a text
Mainly about data structure learning.


## Pset 6: Python
1. python basic 
2. Create a simple web app(flask) to analyze the sentiment of twitter's users by twitter's API


Sentiments

smile.py : a program that categorizes a word as positive or negative

[![smile.png](https://s28.postimg.org/jzsjsjkod/smile.png)](https://postimg.org/image/907cgxu95/)

tweets.py categorizes a user’s recent 100 tweets as positive or negative (uses Twitter API)

[![tweets.png](https://s23.postimg.org/xjn5x6qm3/tweets.png)](https://postimg.org/image/4u0a0jmlz/)

Implement a website that generates a pie chart categorizing a user’s tweets
[![sentiments.png](https://s23.postimg.org/ortjkn7vf/sentiments.png)](https://postimg.org/image/o2ar8a7br/)

Usage: 
```bash
~/workspace/pset6/sentiments/ (master) $ export API_KEY= <insert your API_KEY from Twitter here>
~/workspace/pset6/sentiments/ (master) $ export API_SECRET= <insert your API_SECRET from Twitter here>
~/workspace/pset6/sentiments/ (master) $ export FLASK_APP=application.py
~/workspace/pset6/sentiments/ (master) $ export FLASK_DEBUG=1
~/workspace/pset6/sentiments/ (master) $ flask run
```
## Pset 7: Python & SQL, Flask, continued

C$50 Finance
Implement a website via which users can "buy" and "sell" stocks instantly., allowing to test your taste of real world finance stock. =.=


Requirements & Dependencies:
```bash
cd ~/workspace/pset7/finance/
pip3 install --user -r requirements.txt
```
Usage: 
```bash
~/workspace/pset7/finance/ (master) $ flask run
```
## Pset 8: Javascript, Flask continued
A website that combine Google Maps and Google News Feed.  You can look up a place's recent news by click on marksers in the map.

Requirements & Dependencies:
```bash
cd ~/workspace/pse8/mashup/
pip3 install --user -r requirements.txt
```
Usage: 
```bash
~/workspace/pset8/mashup/ (master) $ export API_KEY=<API_KEY from Google Maps API>
~/workspace/pset8/mashup/ (master) $ flask run
```


## Final Project - selfSpace

Usage: 
```bash
~/workspace/pset8/mashup/ (master) $ export API_KEY=<API_KEY from OMDb API>
~/workspace/pset8/mashup/ (master) $ flask run
```
TO-DO
- [ ] deploy the app on heroku

As a cinephile and a person who treasures feelings about fragments of life, I'd like to implement a simple but really handy website to record some information.  

1. In the "Movie" module, you can record a film by its release year and title,  then the film's poster and imdb link offered, allowing you to examine more specific infomation.  You can click "My films" to pick up some films to watch.
2. In the "Input" module, you can input some text, which could be something to do, some feelings about life, or even some sentences inspiring. Then click "Diary" to check the text you input as a form of timeline.
![selfSpace_Watchlist](https://i.imgur.com/KA4nJkh.jpg)

![Watchlist](https://imgur.com/d78kr0R.jpg)

![Watchlist2](https://i.imgur.com/EUFYwmX.png)

![board](https://imgur.com/FwFcebG.png)

![timeline](https://imgur.com/nFINQPD.png)
