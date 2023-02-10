from fastapi import FastAPI
from selenium import webdriver
from fastapi.middleware.cors import CORSMiddleware
from selenium.webdriver.common.by import By
import time
from googletrans import Translator
from pydantic import BaseModel
from selenium.webdriver.support import expected_conditions as EC
import os
app = FastAPI()
 
@app.get("/")
def root():
    return {"message": "Hello__________"}
@app.get("/init")
def root():
    global driver
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)
    driver.get('https://www.drugs.com/drug_interactions.html')
    return {"message": "Hello__________"}

class drugs(BaseModel):
     drug1: str
     drug2: str
async def getinteraction():
    lnks = driver.find_elements(By.TAG_NAME, "a" )
    lnks[47].click()
    print('wait')
    
    interactions = driver.find_element(By.CLASS_NAME , 'interactions-reference-wrapper')
    return interactions.text
async def add_drug2():
    input_ =  driver.find_element(By.ID, "livesearch-interaction" )
    select =  driver.find_elements(By.CLASS_NAME, "ddc-btn" )
    input_.send_keys(drug_2)
    select[3].submit()
    return 'drug_2 added'
async def add_drug1():
    input_ =  driver.find_element(By.ID, "livesearch-interaction-basic" )
    select =  driver.find_elements(By.CLASS_NAME, "ddc-btn" )
    input_.send_keys(drug_1)
    select[3].submit()
    return 'drug_1 added'
@app.post('/add_drug1')
async def add_drug_1(drug1 : str) :
    global drug_1 
    drug_1 = drug1
    res =  await add_drug1()
    return res

@app.post('/add_drug2')
async def add_drug_2(drug2 : str) :
    global drug_2 
    drug_2 = drug2
    res =  await add_drug2()
    return res
@app.get('/getinteraction')
async def getinteraction_() :
    text =  await getinteraction()
    translator = Translator()
    print(text)
    new_text = translator.translate(text.split('\n')[3], dest = 'ar')
    return new_text.text

