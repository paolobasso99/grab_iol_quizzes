# Grab IOL Quizzes
This python app uses [Selenium Browser Automation](https://www.selenium.dev/) to grab all the quizzes in a Moodle course in order to export them as a csv.
I needed to have thos questions in a spreadsheet to build [this](https://quiz-elettronica.bassopaolo.com/) to practice.

## Why
My University uses Moodle and I wanted all the questions of one of my courses in a spreadsheet (so I could build [this](https://quiz-elettronica.bassopaolo.com/)).
Doing it mannually would not have been so fun then I decided to automate this process!

Selenium is a programmable chromium browser which I used to:
1. Log in into Moodle
2. Start a quiz
3. Grab all questions in that quiz and put them in an SQLite database
4. Repeat the quiz until no new question is found
5. Repeat for all quizzes

## Setup
I recomend to use python venv.
1. Install the pip requirements
2. Copy `.env.example` to `.env`
3. Edit your envirorment variables
4. Run `scrape.py` to start scraping
5. Run `to_csv.py` to export the database to a csv
