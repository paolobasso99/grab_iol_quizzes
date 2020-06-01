from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import urllib.parse as urlparse
from urllib.parse import parse_qs
from components.Question import Question

class Scraper:
    def __init__(self, iol_course_url: str, unibo_username: str, unibo_password: str, chromedriver_path: str, Question: object) -> None:
        self.iol_course_url = iol_course_url
        self.unibo_username = unibo_username
        self.unibo_password = unibo_password
        self.chromedriver_path = chromedriver_path
        self.Question = Question

        self.quizzes = {}

        # Init webdriver
        self.driver = webdriver.Chrome(self.chromedriver_path)

        # Login
        self.driver.get(self.iol_course_url)
        self.login()

    def quit_driver(self):
        self.driver.quit()    

    def login(self):
        usarname_input = self.driver.find_element_by_id('userNameInput')
        password_input = self.driver.find_element_by_id('passwordInput')
        submit_button = self.driver.find_element_by_id('submitButton')

        usarname_input.send_keys(self.unibo_username)
        password_input.send_keys(self.unibo_password)
        submit_button.click()

    @staticmethod
    def get_id_from_url(url: str) -> str:
        parsed = urlparse.urlparse(url)
        return parse_qs(parsed.query)['id'][0]

    # Get list with the name of the quiz and the ID
    def load_quizzes(self):
        self.driver.get(self.iol_course_url)

        quiz_anchors = self.driver.find_elements_by_css_selector(
            'li.quiz .activityinstance a')

        self.quizzes = {}
        for a in quiz_anchors:
            name = a.text.split('\n', 1)[0]
            url = a.get_attribute('href')

            self.quizzes[name] = Scraper.get_id_from_url(url)

    def start_quizzes(self, min_times_after_not_new: int = 2):
        for quiz in self.quizzes:
            self.start_quiz(quiz, min_times_after_not_new)

    def start_quiz(self, name: str, min_times_after_not_new: int = 2):
        # Check if name in quizzes
        if name in self.quizzes:
            has_new = True
            times_after_not_new = 0

            while(has_new or times_after_not_new < min_times_after_not_new):
                if not(has_new):
                    times_after_not_new += 1
                else:
                    times_after_not_new = 0

                summary_html = self.get_summary_html(name)
                has_new = self.process_summary(summary_html, quiz=name)

        else:
            raise Exception(
                'No quiz with the name {} is present, did you use load_quizzes()'.format(name))

    def get_summary_html(self, name: str):
        self.driver.get(
            'https://iol.unibo.it/mod/quiz/view.php?id={}'.format(self.quizzes[name]))

        # Start quiz
        self.driver.find_element_by_css_selector(
            '.quizstartbuttondiv button').click()

        # Go to first question
        self.driver.find_element_by_css_selector(
            '.qn_buttons .qnbutton[data-quiz-page="0"]').click()

        ended = False
        while(not(ended)):
            try:
                # Select first answer for each question
                first_answers = self.driver.find_elements_by_css_selector(
                    '.answer input[value="0"]')

                for a in first_answers:
                    a.click()

                # Next page
                self.driver.find_element_by_css_selector(
                    '.submitbtns input[name="next"]').click()

            except NoSuchElementException:
                ended = True

        # End quiz
        self.driver.find_element_by_css_selector(
            '.submitbtns form[action="https://iol.unibo.it/mod/quiz/processattempt.php"] button[type="submit"]').click()

        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, ".confirmation-buttons .btn-primary"))).click()

        # Process summary
        return self.driver.page_source


    def process_summary(self, html, quiz = "") -> bool:
        soup = BeautifulSoup(html, 'html.parser')
        has_new = False

        question_containers = soup.find_all("div", {"class": "que"})
        for question_container in question_containers:
                # Get text
                question_text = question_container.find(
                    'div', {"class": "qtext"}).text

                # Get answers
                answer_elements = question_container.select('.answer label')
                answers = []
                for answer_element in answer_elements:
                    answers.append(answer_element.find(text=True, recursive=False))

                # Add to questions if needed
                if(self.Question.add(question_text, answers, quiz)):
                    print(question_text)
                    has_new = True

        return has_new
