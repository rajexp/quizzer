from portal.models import Question, Tag
from quizscrape import get_questions

def populate_quiz(url,tag):
    tag_list = []
    for t in tag.split(','):
        tag,created = Tag.objects.get_or_create(name=t.strip().title())
        tag_list.append(tag)
    questions = get_questions(url)
    for q in questions:
        _question,created = Question.objects.get_or_create(question=q['question'],option=q['opt'],answer=q['answer'],description=q['description'])
        for t in tag_list:
            _question.tag.add(t)
            _question.save()


