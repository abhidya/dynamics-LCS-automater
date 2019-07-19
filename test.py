import requests
from seleniumrequests import Chrome
from selenium.webdriver.common.keys import Keys
import seleniumrequests.request as mannyboi
import time
import datetime
import hashlib
import pandas


driver = Chrome(executable_path=r'\chromedriver.exe')
main_url = "https://lcs.dynamics.com/v2" #a redirect to a login page occurs
login_url = "https://lcs.dynamics.com/Logon/AdLogon"
email = ""

def build_request_session():
    requests_session = requests.Session()
    driver.get(main_url)
    driver.get(login_url)
    inputElement = driver.find_element_by_name("loginfmt")
    inputElement.send_keys(email)
    inputElement.send_keys(Keys.ENTER)
    while driver.current_url != "https://lcs.dynamics.com/v2":
        time.sleep(.5)
    requests_session.headers = mannyboi.get_webdriver_request_headers(driver)
    cookies = mannyboi.prepare_requests_cookies(driver.get_cookies())
    for cookie in cookies:
        requests_session.cookies.set(name=cookie, value=cookies[cookie])
    driver.close()
    return requests_session
    
def past24():
    data = "https://diag.lcs.dynamics.com/LogSearch/GetSlowQueries/"
    data += "?environmentId=&limit=50&"
    now = datetime.datetime.now().timestamp()
    yesterday = now - (24*60*60)
    startDate = "startDate="+str(int(yesterday)*1000) + "&"
    endDate = "endDate="+ str(int(now)*1000)+""
    data = data + startDate + endDate
    return data


session =  build_request_session()   
response = session.request("GET", past24())
df = pandas.read_json(response.text)
df["statement_id"] = df["statement"] + df["callStack"]
df["statement_id"] = df["statement_id"].apply(hash)
print(response.text)
