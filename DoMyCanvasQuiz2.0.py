from selenium import webdriver
import time,os

clickLastOne=0   # to click the last answer
answerList = []  # to store the right answers

def loginCanvasQuizPage():
    # 1. Login to canvas
    global clickLastOne
    browser = webdriver.Chrome('./chromedriver')
    browser.get("https://sjsu.instructure.com/courses/1358032/quizzes/1340792")
    name = browser.find_element_by_id("okta-signin-username")
    name.send_keys(os.environ.get('SJSU_ID'))
    passwd = browser.find_element_by_id("okta-signin-password")
    passwd.send_keys(os.environ.get('SJSU_Password'))
    login_button = browser.find_element_by_id("okta-signin-submit")
    login_button.click()
    time.sleep(2)

    # 2. Start the quiz
    startQuiz_button = browser.find_element_by_xpath("""//*[@id="take_quiz_link"]""")
    startQuiz_button.click()

    # 3. Go though all the questions and click the last one for now
    for Question in browser.find_elements_by_class_name("question_input"):
        if clickLastOne == 3:
            Question.click()
            clickLastOne = 0
        else:
            clickLastOne += 1

    # 4. Search in the answerList base one the local database.txt if the list is not empty, and then fix any wrong answers (second round)
    l = len(answerList)
    if l>0:
        for label in browser.find_elements_by_class_name("answer_label"):
            time.sleep(0.1)
            temp = (str(label.text))
            if temp in answerList:
                label.click()
                print ('Correcting the answer base on the local database...\nThe right answer is : \t', temp)

    # 5. Click submit button
    time.sleep(1)
    submitQuiz_button = browser.find_element_by_xpath("""//*[@id="submit_quiz_button"]""")
    submitQuiz_button.click()
    print('Done the quiz! Now start storing the correct answers into the database...')

    correctIncorrectList=[]
    clickedChoiceID = []
    labelList=[]

    # 1.loop though all the questions's label and store them into the label list for later use
    for label in browser.find_elements_by_class_name("answer_text"):
        temp = str(label.text)
        labelList.append(temp)

    # 2. loop though all the correct/incorrect msg from Canvas and store them into a list for later use
    for comment in browser.find_elements_by_class_name("quiz_comment"):
        time.sleep(0.1)
        temp = str(comment.text)
        if temp =='correct!':
            correctIncorrectList.append('correct')
        elif temp =="":
            temp=temp # do nothing , have to filter out ""
        else:
            correctIncorrectList.append("incorrect")

    # 3. loop though all the clicked choice's id and store them to a list for later use
    for aClass in browser.find_elements_by_class_name("question_input"):
        time.sleep(0.1)
        if aClass.get_property('checked') == 1: # if its checked
            temp=str(aClass.get_property('id')) # append its id to the list
            clickedChoiceID.append(temp)


    # Map the two lists to get a new list (the correct answer list)
    #
    # Ex.
    #   correctIncorrectList [] = correct , incorrect , correct ,  incorrect
    #   labelList            [] = str1 ,      str2 ,        str3 ,      str4
    # ----------------------------------------------------------------------
    #  correct answer list will be : [str1 , str3]

    for x in range(0,15):
        if correctIncorrectList[x]=='correct':
            answerList.append(labelList[x])
    print ("Done storing the correct answers into the local database.txt !")


def writeFile():
    file = open('database.txt', 'w')
    file.write("\n")
    for x in answerList:
        file.write(x)
        file.write('\n')
    file.close()

def readFile():
    file = open('database.txt','r').read().split('\n')
    for x in file:
        if x !='':
            answerList.append(x)



readFile()

for x in range(3):
    loginCanvasQuizPage()
    writeFile()


