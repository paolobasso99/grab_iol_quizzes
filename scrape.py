from components.Settings import Settings
from components.Scraper import Scraper

settings = Settings()
Question = Question(settings.get('QUESTIONS_DB_PATH'))
scraper = Scraper(
    iol_course_url=settings.get('IOL_COURSE_URL'),
    unibo_username=settings.get('UNIBO_USERNAME'),
    unibo_password=settings.get('UNIBO_PASSWORD'),
    chromedriver_path=settings.get('CHROMEDRIVER_PATH'),
    Question=Question
)

scraper.load_quizzes()

scraper.start_quizzes(5)

# Quit
scraper.quit_driver()
quit()