#import yaml
import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi_utils.session import FastAPISessionMaker
from fastapi_utils.tasks import repeat_every
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
import re

def distinctStringSet(list_string) :
	auxiliaryList = []
	for word in list_string:
		if word not in auxiliaryList:
			auxiliaryList.append(word)
	return auxiliaryList

def modifyMainDictArrayByPrice(main_arr, price, field_edit, field_value) :
	for i in range(len(main_arr)) :
		dict_member = main_arr[i]
		#print(dict_member, field_edit, field_value)
		if dict_member["Price per Month"] == price :
			main_arr[i][field_edit] = field_value
			break

app = FastAPI()

field_names = [
	"operator_id",
	"plan",
	"price",
	"system",
	"unlimited_call",
	"call_minutes",
	"capture_in_seconds",
	"unlimited_internet_mode",
	"internet_gbs",
	"fair_usage_policy",
	"wifi",
	"g_no",
	"sms",
	"mms",
	"entertainment",
	"entertainment_package",
	"entertainment_contract",
	"priviledge",
	"priviledge_exclusive",
	"contract",
	"extra",
	"notes"
]

#config_file = "config.yaml"
#sql_file = "test.sqlite"

#if os.path.exists(config_file):
#    with open(config_file, "r", encoding="utf-8") as f:
        #config = yaml.safe_load(f)
#else:
#    print("Configuration file not found; using default configuration")
#    config = {}
#app.include_router(info.router)
#app.include_router(form.router)

@app.on_event("startup")
def on_startup():
	print("App is starting up.")


    #initialize_databases(sql_file, config)

operators = ["AIS", "DTAC", "TRUE"]
operator_card_classes = { #where the title is inside each cards
	"AIS" : "package-card-generic",
	"DTAC" : "wrapPackages",
	"TRUE" : "x-1iqxi85"
}
container_classes = { #where it has title as header
	"AIS" : "cmp-container",
	"DTAC" : "cardPackages",
	"TRUE" : "my-5"
}


@app.post("/scrape_web")
#@repeat_every(seconds=30) #works
async def scrape_web(request: Request):
	qr = await request.json()
	price_keywords = qr['price_keywords']
	urls = qr['urls']
	webdriver_timeout = qr['webdriver_timeout']

	print(price_keywords)

	list_of_rows = []

	for url in urls :
		#print(url)

		driver = webdriver.Chrome()
		driver.implicitly_wait(webdriver_timeout)

		driver.get(url["url_link"])

		operator = operators[url["operator_id"]]

		for plan in url["plans"] :
			#target_string_lambda = lambda plan_name_is_text : plan["plan_name"] if title_is_at_header == True else price_keywords[0]
			target_string = price_keywords[0]

			#title_finder_lambda = lambda title_is_at_header : container_classes[operator] if title_is_at_header == True else operator_card_classes[operator]
			target_class = plan["css_item_class_name"]

			#init_web_contents_lambda = lambda title_is_at_header : driver.find_elements(By.CSS_SELECTOR, f".{target_class}")[0].find_elements(By.XPATH, f'./div[contains(@class, "{operator_card_classes[operator]}")]') if title_is_at_header == True else driver.find_elements(By.CSS_SELECTOR, f".{target_class}")
			init_web_contents = driver.find_elements(By.CSS_SELECTOR, f".{target_class}")

			for i in range(len(init_web_contents)) :
				web_content = init_web_contents[i]
				#web_contents_ = driver.find_elements(By.XPATH,"//*[text()[contains(., '"+target_string+"')]]")
				list_of_rows.append(web_content.get_attribute('class'))

		driver.close()

	return {"result" : list_of_rows}

app.mount("/", StaticFiles(directory="web"), name="web")
