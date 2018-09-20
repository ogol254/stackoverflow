# StackOverflow-lite

## Introduction

[![Build Status](https://travis-ci.org/ogol254/stackoverflow.svg?branch=master)](https://travis-ci.org/ogol254/stackoverflow) [![Maintainability](https://api.codeclimate.com/v1/badges/4754b5342d6a948f3f8f/maintainability)](https://codeclimate.com/github/ogol254/stackoverflow/maintainability) [![codecov](https://codecov.io/gh/ogol254/stackoverflow/branch/master/graph/badge.svg)](https://codecov.io/gh/ogol254/stackoverflow) [![Coverage Status](https://coveralls.io/repos/github/ogol254/stackoverflow/badge.svg?branch=master)](https://coveralls.io/github/ogol254/stackoverflow?branch=master)

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

Clone the repository [```here```](https://github.com/ogol254/stackoverflow)

### Testing

*To test the UI:*
Navigate to the UI directory
On your preferred browser, open index.html
Alternatively, the site is [```hosted here```](blalal)


```$ pip install -r requirements.txt```

```$ nosetests app/tests```

```$ python run.py```

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
