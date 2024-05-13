from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
# import pywhatkit
from datetime import datetime, timedelta
import time 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from flask_cors import CORS
import os


app = Flask(__name__)
CORS(app)

options = Options() 
# options.add_experimental_option("debuggerAddress","localhost:9000")
# options.add_argument("log-level=INFO")
# options.add_argument("user-data-dir=C:/Users/CHARAN/AppData/Local/Google/Chrome/User Data") #)PATH is path to your chrome profile


def send_message(contact_person,message,driver):

    wait = WebDriverWait(driver, 72)
    waited=WebDriverWait(driver,40)
    print("hi")
    result="Failure"

    try:
        checkLaunch= wait.until(EC.element_to_be_clickable((By.XPATH,"//div[@class='_ai05']//div[@role='textbox']")))
    except Exception as e:
        print("whatsapp not found",e.message)
        driver.get('https://web.whatsapp.com')
        time.sleep(40)

    # contact_person='7674083953'
    try:
        searchBox= wait.until(EC.element_to_be_clickable((By.XPATH,"//div[@class='_ai05']//div[@role='textbox']")))
        print(searchBox)
        #search for the contact_person
        searchBox.send_keys(contact_person)
        print(searchBox)
        time.sleep(3) 
        searchBox.send_keys(Keys.RETURN)

        print(f"//span[@title={contact_person}]")
        print("//span[@title="+ contact_person +"]")
    except Exception as e:
        print(e)
    # if(contact_person.isdigit()):
    #     contactBox= wait.until(EC.element_to_be_clickable((By.XPATH,f"//span[@title='+91 {contact_person[:5]} {contact_person[5:]}']")))
    #     contactBox.click()
    #     print(contactBox)
    # else:
    #     contactBox= wait.until(EC.element_to_be_clickable((By.XPATH,f"//span[@title='{contact_person}']")))
    #     contactBox.click()
    #     print(contactBox)
    try:
        print("came test debug point")
        if(contact_person.isdigit()):
            check_contact_exist=waited.until(EC.presence_of_element_located((By.XPATH, f"//div[starts-with(@data-id,'true_91{contact_person[:]}')]")))
            # check_contact_exist= wait.until(EC.presence_of_element_located((By.XPATH, f"//div[@class='_aou8 _aj_h']//span[@title='+91 {contact_person[:5]} {contact_person[5:]}']")))
            print(check_contact_exist,"exist or not")
        # send the message
        title_box_selector = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@title='Type a message']")))
        # message="hello all alla lla"
        for i in range(1):
            title_box_selector.send_keys(message,Keys.ENTER)
            title_box_selector.send_keys(Keys.RETURN)
        result="Success"
        time.sleep(10)
    except Exception as e:
        print(str(e),"not found contact so cant send")
        result="Failure"
        print(result)
        #any data inseatch box xlear it 
        try:
            clearButton=waited.until(EC.element_to_be_clickable((By.XPATH,"//span[@data-icon='x-alt']")))
            clearButton.click()
        except Exception as e:
            print(e)

    return result

# send_message("8309370811",".")
# send_message("7674083953","hehe")
# send_message("8008717091","hmm")

def send_file_message(contact_person,message,file_path,driver):

    wait = WebDriverWait(driver, 72)
    waited=WebDriverWait(driver,40)
    print("hi")
    result="Failure"

    try:
        checkLaunch= wait.until(EC.element_to_be_clickable((By.XPATH,"//div[@class='_ai05']//div[@role='textbox']")))
    except Exception as e:
        print("whatsapp not found",e.message)
        driver.get('https://web.whatsapp.com')
        time.sleep(40)

    # contact_person='7674083953'
    try:
        searchBox= wait.until(EC.element_to_be_clickable((By.XPATH,"//div[@class='_ai05']//div[@role='textbox']")))
        print(searchBox)
        #search for the contact_person
        searchBox.send_keys(contact_person)
        print(searchBox)
        time.sleep(3) 
        searchBox.send_keys(Keys.RETURN)

        print(f"//span[@title={contact_person}]")
        print("//span[@title="+ contact_person +"]")
    except Exception as e:
        print(e)

    try:
        print("came test debug point")
        if(contact_person.isdigit()):
            check_contact_exist=waited.until(EC.presence_of_element_located((By.XPATH, f"//div[starts-with(@data-id,'true_91{contact_person[:]}')]")))
            # check_contact_exist= wait.until(EC.presence_of_element_located((By.XPATH, f"//div[@class='_aou8 _aj_h']//span[@title='+91 {contact_person[:5]} {contact_person[5:]}']")))
            print(check_contact_exist,"exist or not")
        
        #send the file
        attachment_box=wait.until(EC.element_to_be_clickable((By.XPATH,"//span[@data-icon='attach-menu-plus']")))
        attachment_box.click()
        time.sleep(1)
        
        file_box=wait.until(EC.element_to_be_clickable((By.XPATH,"//input[@accept='*']")))
        file_box.send_keys(file_path,Keys.ENTER)

        # send the message
        title_box_selector = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@title='Type a message']")))
        # message="hello all alla lla"
        
        title_box_selector.send_keys(message,Keys.ENTER)
        title_box_selector.send_keys(Keys.RETURN)

        result="Success"
        time.sleep(10)
    except Exception as e:
        print(str(e),"not found contact so cant send")
        result="Failure"
        print(result)
        #any data inseatch box xlear it 
        try:
            clearButton=waited.until(EC.element_to_be_clickable((By.XPATH,"//span[@data-icon='x-alt']")))
            clearButton.click()
        except Exception as e:
            print(e)

    return result

@app.route("/sendmsg", methods=["POST"])
def send_whatsapp_messages():
    data=request.json
    print(data)
    message=""
    if 'message' in data:
        message = data['message']
    if 'details' in data:
        resultsOfMessages = []   
        # chrome_driver_path="./chrome.exe"
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        time.sleep(10)
        # driver=webdriver.Chrome(service=Service())
        #intial connect to whatsapp
        driver.get('https://web.whatsapp.com')
        time.sleep(40)

        for detail in data['details']:
            phone=detail.get('number')
            isSent=send_message(phone,message,driver)
            resultsOfMessages.append({"phone": phone, "status": isSent})
    result={"msg":"messages sent successfully","isSent":resultsOfMessages}
    return jsonify(result)

# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
# driver.get('https://web.whatsapp.com')
# time.sleep(40)
# send_file_message("9989786348","hello welcome","./simple.pdf",driver)

@app.route("/sendfilemsg", methods=["POST"])
def send_whatsapp_file_messages():
    # file=request.files["file"]
    data=request.json
    message=""
    file_path="./simple.pdf"
    if 'message' in data:
        message = data['message']
        print(message)
    chrome_driver_path="chrome.exe"

    # Get the directory of the script
    # directory = os.path.dirname(os.path.realpath(__file__))
    
    # # Save the file in the same directory as the script
    # file_path = os.path.join(directory, file.filename)
    # file.save(file_path)

    if 'details' in data:
        resultsOfMessages = []        
        service = Service(executable_path=chrome_driver_path)

        # Start a new Chrome session using the service
        driver = webdriver.Chrome(service=Service(ChromeDriver))
        #intial connect to whatsapp
        driver.get('https://web.whatsapp.com')
        time.sleep(40)

        for detail in data['details']:
            phone=detail.get('number')
            isSent=send_file_message(phone,message,file_path,driver)
            resultsOfMessages.append({"phone": phone, "status": isSent})
    result={"msg":"messages sent successfully","isSent":resultsOfMessages}
    return jsonify(result)

@app.route("/",methods=["GET"])
def sayHI():
    return jsonify({"msg":"hello"})
@app.route("/hell",methods=["GET"])
def sayHell():
    return jsonify({"msg":"hell"})

# driver.close()

if __name__ == '__main__':
    app.run(debug=False)  # Set debug=False for production
    print("her poer 8081")
