from components.Settings import Settings
from components.Scraper import Scraper
import json
import os

settings = Settings()

# Get old questions from file
questions = {}
json_file_name = settings.get('QUESTIONS_JSON_FILE')
if(os.path.exists(json_file_name)):
    with open(json_file_name, 'r') as json_file:
        questions = json.loads(json_file)

scraper = Scraper(
    iol_course_url=settings.get('IOL_COURSE_URL'),
    unibo_username=settings.get('UNIBO_USERNAME'),
    unibo_password=settings.get('UNIBO_PASSWORD'),
    chromedriver_path=settings.get('CHROMEDRIVER_PATH'),
    questions=questions
)

scraper.load_quizzes()

scraper.start_quiz('Domande Circuiti Digitali', 2)
questions = scraper.get_questions()

# Write questions to json file
with open(json_file_name, 'w') as json_file:
    json.dump(questions, json_file)

# Quit
scraper.quit_driver()
quit()