from sqlalchemy.orm import Session
from database import SessionLocal
from models import Question,Test
data = [
    {
        "question": "What is the output of the following Python code: print(2 ** 3)?",
        "answer": "8"
    },
    {
        "question": "In Java, which keyword is used to define a subclass?",
        "answer": "extends"
    },
    {
        "question": "What does SQL stand for?",
        "answer": "Structured Query Language"
    },
    {
        "question": "Which HTML tag is used to define an unordered list?",
        "answer": "<ul>"
    },
    {
        "question": "In JavaScript, how do you create a function named 'myFunction'?",
        "answer": "function myFunction() {}"
    },
    {
        "question": "What is the purpose of CSS in web development?",
        "answer": "To style HTML elements"
    },
    
    {
        "question": "What is the name of the process that converts source code into machine code?",
        "answer": "Compilation"
    }
]

def create_test_data(db:Session):
    data=Test(title="dummy test",description="This test is generated using Script..")
    db.add(data)
    db.commit()

def create_quiz_data(db: Session, data):
    test=db.query(Test).filter(Test.title=="dummy test").first()
    for item in data:
        new_quiz=Question(test_id=test.id,question_text=item.get("question"),correct_ans=item.get("answer"))
        db.add(new_quiz)
    db.commit()

def main():
    db = SessionLocal()

    create_test_data(db)
    create_quiz_data(db, data)
    db.close()
    print("QUIZ CREATED...")

if __name__ == "__main__":
    main()
