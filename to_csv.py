from components.Settings import Settings
from components.Question import Question
import pathlib


settings = Settings()

Question = Question(settings.get('QUESTIONS_DB_PATH'))

Question.to_csv(str(pathlib.Path(__file__).parent.absolute())+'\questions.csv')