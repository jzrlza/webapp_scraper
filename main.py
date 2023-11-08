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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import re
import time

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
	"AIS" : ["package-card-generic", "MuiCardContent-root"],
	"DTAC" : ["innerWrap", None, "card-promotion"],
	"TRUE" : ["x-1iqxi85"]
}
operator_cards_header_title_classes = { 
	"AIS" : ["cmp-container", "search-tab-btn"],
	"DTAC" : ["tCaption", "txt-h-2", "title-card"], # *** title-card adds one layer
	"TRUE" : ["x-34ioum"] # now uses x-4ll1o9
}
operator_cards_container_classes = {
	"AIS" : ["cmp-container"],
	"DTAC" : ["cardPackages", None, "card-container"],
	"TRUE" : ["my-5"]
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
		action = ActionChains(driver)

		driver.get(url["url_link"])

		operator_id = url["operator_id"]
		operator_name = operators[url["operator_id"]]

		need_to_scroll = False
		scrolled = False

		for plan in url["plans"] :
			#target_string_lambda = lambda plan_name_is_text : plan["plan_name"] if title_is_at_header == True else price_keywords[0]
			target_string = price_keywords[0]
			plan_name = plan["plan_name"]
			capture_mode_id = plan["capture_mode"]
			#title_finder_lambda = lambda title_is_at_header : container_classes[operator] if title_is_at_header == True else operator_card_classes[operator]
			target_class = ""#plan["css_item_class_name"]
			requires_click = False
			target_click_class = ""
			menu_to_click_class = ""
			disabled_mode = False #temp value
			clicked = False

			#if-else structured like this on purpose for ease of re-readability
			if operator_id == 0 :
				if capture_mode_id == 0 :
					target_class = "//*[@class='package-card-generic']"
				elif capture_mode_id == 1 :
					requires_click = True
					target_click_class = "//*[contains(@class, 'search-tab-btn') and contains(@class, 'MuiTab-textColorPrimary') and contains(@class, 'MuiButtonBase-root')]"
					target_class = "//*[contains(@class, 'card-content') and contains(@class, 'MuiCardContent-root')]"
					need_to_scroll = True
			elif operator_id == 1 :
				if capture_mode_id == 0 :
					target_class = "//*[@class='innerWrap']"
				elif capture_mode_id == 1 :
					requires_click = True
					disabled_mode = True #temp
					#target_class = operator_cards_header_title_classes[operator_name][0]
				elif capture_mode_id == 2 :
					target_class = "//*[@class='card-promotion']"
			elif operator_id == 2 :
				if capture_mode_id == 0 :
					target_class = "//*[@class='x-1iqxi85']"

			#init_web_contents_lambda = lambda title_is_at_header : driver.find_elements(By.CSS_SELECTOR, f".{target_class}")[0].find_elements(By.XPATH, f'./div[contains(@class, "{operator_card_classes[operator]}")]') if title_is_at_header == True else driver.find_elements(By.CSS_SELECTOR, f".{target_class}")
			if not disabled_mode :
				if requires_click :
					time.sleep(1)
					click_targets = driver.find_elements(By.XPATH, f"{target_click_class}")
					for i in range(len(click_targets)):
						target = click_targets[i]
						menu_target = target.find_element(By.XPATH, "..")
						##print(target.get_attribute('class'), target.get_attribute('innerHTML'))
						if plan_name in target.get_attribute('innerHTML') :
							#print(target.get_attribute('class'), target.get_attribute('innerHTML'))
							if need_to_scroll and not scrolled :
								driver.execute_script("""
									window.scrollTo({
										top: arguments[0].getBoundingClientRect().top-50,
										behavior: "instant"
										});
									""", target)
								scrolled = True
							time.sleep(1)
							driver.execute_script("""
									let target = arguments[0]
									let menu_targets = arguments[1].children
									for (let i = 0; i <= menu_targets.length; i++) {
										if (target === menu_targets[i]) {
											target.click()
										}
									}
									""", target, menu_target)
							time.sleep(1)
							##print(target.get_attribute('class'))
							clicked = True
							break
				else :
					clicked = True

				if clicked :
					init_web_contents = driver.find_elements(By.XPATH, f"{target_class}")

					for i in range(len(init_web_contents)) :
						web_content = init_web_contents[i]
						#web_contents_ = driver.find_elements(By.XPATH,"//*[text()[contains(., '"+target_string+"')]]")
						print(web_content.get_attribute('class'))
						list_of_rows.append(web_content.get_attribute('class'))

		driver.close()

	return {"result" : list_of_rows}

app.mount("/", StaticFiles(directory="web"), name="web")
