import json
import sqlite3

class Question:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path

        # Create DB table if needed
        db = sqlite3.connect(self.db_path)
        c = db.cursor()
        c.execute(
            ''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='questions' ''')

        if not(c.fetchone()[0] == 1):
            c.execute('''CREATE TABLE questions (text text, answers text, quiz text)''')
        
        db.commit()
        db.close()

    def add(self, text: str, answers: list, quiz: str = "") -> bool:
        # Load db
        db = sqlite3.connect(self.db_path)
        c = db.cursor()

        # Get questions with same text
        c.execute('SELECT * FROM questions WHERE text=?', (text,))
        questions = c.fetchall()

        # Determinate if question needs to be added
        addable = True
        for q_text, q_answers, q_quiz in questions:
            q_answers = json.loads(q_answers)
            if(set(q_answers) == set(answers)):
                addable = False
        
        if(addable):
            c.execute("INSERT INTO questions VALUES (?,?,?)",(text, json.dumps(answers), quiz))

        # Close
        db.commit()
        db.close()

        return addable