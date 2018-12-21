# wsd2018-project

### 1. Team

* 728010 Sataponn Phutrakul
* 721130 Ekaterina Shmeleva
* 528621 Felipe Gonzalez Carceller


### 2. Goal

The goal is to develop an online game store where *(1)* developers can publish and sell games and view statistics for games and *(2)* players can search for games, purchase games via an online payment system, launch and play games, leave public comments for developers and other players, and view leaderboards for individual games.

### 3. Plans

#### 3.1 Basic Features

**Authentication**
* User registration and logging in and out will be implemented using the [Django authentication system](https://docs.djangoproject.com/en/2.1/topics/auth/);
* User registration with email verification will be implemented by configuring our Django web application to use the [console backend](https://docs.djangoproject.com/en/2.1/topics/email/#console-backend) for sending emails.

**Player Functionalities**
* Search games and filter games by genre, price, and ownership;
* Purchase games via an online payment system;
* Launch and play games;
* View leaderboards for individual games;
* Leave public Facebook comments and share games on social media (*see 3.2*).

**Developer Functionalities**
* Publish and manage games, including setting and making changes to its URL, description, and price;
* View sales statistics.

**Game Interactions**
* Recording player high-scores.

**Security**
* Players should only be able to play games they have purchased;
* Developers should only be able to modify and access statistics of their own games and should not be able to impersonate other developers;
* Developers should not be able to play games, players should not be able to publish games;
* Etc.

#### 3.2 Extra Features

**Social Login**
* We will implement Facebook Login to provide an alternative to the standard email registration using either [`django-allauth`](https://github.com/pennersr/django-allauth) or [`django-facebook`](https://github.com/tschellenbach/Django-facebook) library.

**RESTful API**
* We will implement an API for retrieving publicly available information:
  * A `GET` method for searching games with pagination;
  * A `GET` method for retrieving high scores for individual games.

**Social Media Sharing**
* We will add [Facebook](https://developers.facebook.com/docs/plugins/share-button/) and [Twitter](https://developer.twitter.com/en/docs/twitter-for-websites/tweet-button/overview.html) share buttons so that users can share a game (including its image, description, and URL) and their high scores.

**Mobile Friendly**
* We will build our application using [Bootstrap](https://getbootstrap.com/docs/3.3/) to support a variety of devices, including smartphones, tablets, and desktops.

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
