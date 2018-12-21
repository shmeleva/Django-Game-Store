# wsd2018-project

Ten Points Project Plan
-----------------------

### 1. Team

* 728010 Sataponn Phutrakul
* 721130 Ekaterina Shmeleva
* 528621 Felipe Gonzalez Carceller


### 2. Goal

The goal is to develop a web application which allows developers to sell their games and allows players to buy them using online payment. Moreover, players are able to check the leaderboard for each game.


### 3. Plans

#### 3.1 Features

**Authentication**
* Use Django auth
* Email validation using Django's Console Backend

**Basic Player Functionalities**
* Buy games
* Play games
* Security restrictions
* Search games

**Basic Developer Functionalities**
* Manage list of games
* Sales statistics
* Security

**Game Interactions**
* Save high scores

#### 3.2 Extra Features

**3rd Party Login**
* Using Facebook

**RESTful API**
* For searching games
* High scores

**Social Media Sharing**
* Share high scores on Facebook and Twitter with a picture and a link to the service's webpage

**Mobile Friendly**
* Support use across many devices using bootstrap

**Facebook Comments**
* Using a 'Comments Plugin' feature provided by Facebook

### 4. Process and Time Schedule

We communicate using Telegram and we meet a couple of times a week to see how things are going. Most of the development will be done on our own time. We use Trello for project management.

* Week 1: Set up a database and build a simple layout.
* Week 2: Implement authentication.
* Weeks 3-4: Basic player and developer functionalities and CSS.
* Week 5: RESTful API.
* Week 6: Social media sharing and Facebook comments.

### 5. Models
* User
  * id
  * role
  * other parameters from Django


* Games
  * id
  * name
  * URL
  * description
  * imageURL
  * developerId
  * price
  * UserGame


* UserGame
  * id
  * userId
  * gameId
  * createdAt


* Result
  * id
  * userId
  * gameId
  * score
  * createdId


* Category
  * id
  * name


* GameCategory
  * gameId
  * categoryId

### 6. Layout Sketch

A very simple clickable prototype can be found at https://marvelapp.com/405c5bh

The games' thumbnail pictures are from https://www.miniclip.com/games/en/ and are only used for educational purposes.

![alt text](Screenshot1.jpg)

![alt text](Screenshot2.jpg)

![alt text](Screenshot3.jpg)
