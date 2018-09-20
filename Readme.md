# StackOverflow-lite

## Introduction

[![Build Status](https://travis-ci.org/ogol254/stackoverflow.svg?branch=master)](https://travis-ci.org/ogol254/stackoverflow) [![Maintainability](https://api.codeclimate.com/v1/badges/4754b5342d6a948f3f8f/maintainability)](https://codeclimate.com/github/ogol254/stackoverflow/maintainability)  [![Coverage Status](https://coveralls.io/repos/github/ogol254/stackoverflow/badge.svg?branch=master)](https://coveralls.io/github/ogol254/stackoverflow?branch=master)

## Run in Postman

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/ce5fa5121eb851f81114)

### Features

1. Users can create an account and log in.
2. Users can post questions.
3. Users can delete the questions they post.
4. Users can post answers.
5. Users can view the answers to questions.
6. Users can accept an answer out of all the answers to his/her question as the preferred answer.

### Installing

*Step 1*

Create directory
```$ mkdir stackoverflow```

```$ cd stackoverflow```

Create and activate virtual environment
```$ virtualenv env```

```$ source env/bin/activate```

Clone the repository [```here```](https://github.com/ogol254/stackoverflow) or 

``` git clone https://github.com/ogol254/stackoverflow ```

Install project dependencies 
```$ pip install -r requirements.txt```


*Step 2*

#### Set up database and virtual environment & Database 

Go to postgres terminal and create the following databases

``` # CREATE DATABASE database_name ; ```
``` # CREATE DATABASE test_database_name ; ```

*Step 3*

#### Storing environment variables 

```
export FLASK_APP="run.py"
export APP_SETTINGS="development"
export DATABASE_URL="dbname='database_name' host='localhost' port='5432' user='postgres' password='root'"
export DATABASE_TEST_URL="dbname='test_database_name' host='localhost' port='5432' user='postgress' password='root'"
```

*Step 4*

#### Running the application

```$ python run.py```

*Step 5*

#### Testing

```$ nosetests app/tests```

### API-Endpoints

#### Users Endpoints : /api/v1/

Method | Endpoint | Functionality
--- | --- | ---
POST | /auth/signup | Create a user account
POST | /auth/login | Sign in a user
POST | /auth/logout | Sign out a user

#### Questions Endpoints : /api/v1/

Method | Endpoint | Functionality
--- | --- | ---
POST | questions | Post a question
POST | /questions/int:ques_id/answers | post an answer to a question
GET | /questions | Get a List of all questions
GET | /questions/int:ques_id | Get a question using its id
GET | /questions/str:username | Get all questions posted by a particular user
GET | /questions/answers/most | Get the question with the most answers
PUT | /questions/int:ques_id | Edit a question
DELETE | /questions/int:ques_id | Delete a question using its id
POST | /questions/int:ques_id/answers | Post an answer to a question
PUT | /questions/int:ques_id/answers/int:ans_id | Edit an answer
PUT | /questions/int:ques_id/answers/int:ans_id | Mark an answer as preferred
PUT | /questions/int:ques_id/answers/int:ans_id/vote | Up/Downvote an answer
