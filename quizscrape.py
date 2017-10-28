import requests
from bs4 import BeautifulSoup
import re
host = 'https://www.indiabix.com'

def sanitize_options(text):
    return text.replace(';',' ')

def sanitize_description(text):
    return "No description Avaliable" if text.startswith('No answer description available') else text
def process_answer(opt):
    if opt == 'A':
        return 1
    elif opt == 'B':
        return 2
    elif opt == 'C':
        return 3
    elif opt == 'D':
        return 4
def process(res):
    soup = BeautifulSoup(res.text,'lxml')
    que_div = soup.findAll("div",{"class":"bix-div-container"})
    print("Reached")
    question_bank = list()
    for i in que_div:
        question = dict()
        # print(i.find("td",{"class":"bix-td-qtxt"}).findAll("p"))
        question['question'] = ''.join([ p.get_text() for p in i.find("td",{"class":"bix-td-qtxt"}).findAll("p")])
        question['opt'] = [sanitize_options(o.get_text()) for o in i.findAll("td",{"id":re.compile('tdOptionDt_')})]
        question['answer'] = process_answer(i.find("span",{"class":"jq-hdnakqb"}).get_text())
        question['description'] = sanitize_description(i.find("div",{"class":"bix-ans-description"}).get_text().strip())
        question_bank.append(question)
    return question_bank
    # return get_links(news_div)

def get_pager_links(res):
    soup = BeautifulSoup(res.text,'lxml')
    pager = soup.findAll("span",{"class":"mx-pager-no"})
    links = []
    for i in pager:
        if i.parent.name == 'a':
            links.append(host+i.parent['href'])
    return links

# url = 'https://www.indiabix.com/general-knowledge/world-geography/'
def get_questions(url):
    questions = []
    try:
        res = requests.get(url)
    except:
        return []
    links = [url] +get_pager_links(res)
    for url in links:
        res = requests.get(url)
        print(res.status_code)
        questions += process(res)
    return questions
if  __name__ == "__main__":
    print(get_questions())
    