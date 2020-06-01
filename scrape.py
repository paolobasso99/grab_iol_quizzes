from components.Settings import Settings
from components.Scraper import Scraper

import os

settings = Settings()

scraper = Scraper(
    iol_course_url=settings.get('IOL_COURSE_URL'),
    unibo_username=settings.get('UNIBO_USERNAME'),
    unibo_password=settings.get('UNIBO_PASSWORD'),
    chromedriver_path=settings.get('CHROMEDRIVER_PATH'),
    questions_db_path=settings.get('QUESTIONS_DB_PATH')
)

scraper.load_quizzes()

scraper.start_quizzes()

# Quit
scraper.quit_driver()
quit()