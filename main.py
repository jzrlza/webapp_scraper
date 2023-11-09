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

def getNumbersWithCommaFromString(raw_txt) :
	pattern = r'\d{1,3}(?:,\d{3})*(?:\.\d+)?'

	matches = re.findall(pattern, raw_txt)

	numbers = [float(match.replace(',', '')) for match in matches]

	return numbers

def checkSystemGetEnum(raw_txt) :
	if "ต่อเดือน" in raw_txt :
		return 1
	return 0

def insertRowInfoForAISCards(new_row, list_item_infos_head, list_item_infos_body, list_item_infos_footer) : #void function
	#XG zone
	if "3G" in list_item_infos_head or "3G" in list_item_infos_body :
		new_row["g_no"] = "3G"
	if "4G" in list_item_infos_head or "4G" in list_item_infos_body :
		if new_row["g_no"] == None :
			new_row["g_no"] = "4G"
		else :
			new_row["g_no"] += "/4G"
	if "5G" in list_item_infos_head or "5G" in list_item_infos_body :
		if new_row["g_no"] == None :
			new_row["g_no"] = "5G"
		else :
			new_row["g_no"] += "/5G"

def modifyMainDictArrayByPrice(main_arr, price, field_edit, field_value) :
	for i in range(len(main_arr)) :
		dict_member = main_arr[i]
		#print(dict_member, field_edit, field_value)
		if dict_member["Price per Month"] == price :
			main_arr[i][field_edit] = field_value
			break

app = FastAPI()

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
row_obj_template = {
	"operator_id": -1,
	"plan": "",
	"price": 0.0,
	"system": -1,
	"unlimited_call": False,
	"call_minutes": 0.0,
	"capture_in_seconds": False,
	"unlimited_internet_mode": 0,
	"internet_gbs": 0.0,
	"fair_usage_policy": None,
	"wifi": False,
	"g_no": None,
	"sms": False,
	"mms": False,
	"entertainment": False,
	"entertainment_package": None,
	"entertainment_contract": 0,
	"priviledge": False,
	"priviledge_exclusive": None,
	"contract": 0,
	"extra": None,
	"notes": None
}

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
						new_row = row_obj_template.copy()
						new_row["operator_id"] = operator_id
						new_row["plan"] = plan_name
						
						if operator_id == 0 : #start at "package-card-generic"
							if capture_mode_id == 0 :
								first_block = web_content.find_elements(By.XPATH, '*')[0].find_elements(By.XPATH, '*')[1].find_elements(By.XPATH, '*')[1]
								first_block__price = getNumbersWithCommaFromString(first_block.find_elements(By.XPATH, '*')[0].find_elements(By.XPATH, '*')[0].get_attribute('innerHTML').strip())[0]
								print(first_block__price)
								new_row["price"] = first_block__price
								#first_block__system = checkSystemGetEnum(first_block.find_elements(By.XPATH, '*')[1].get_attribute('innerHTML').strip())
								new_row["system"] = 1

								second_block = web_content.find_elements(By.XPATH, '*')[0].find_elements(By.XPATH, '*')[2].find_elements(By.XPATH, '*')[0]
								second_block__list_items = second_block.find_elements(By.XPATH, '*')[0].find_elements(By.XPATH, '*')
								for list_item in second_block__list_items :
									list_item_infos = list_item.find_elements(By.XPATH, '*')[1].find_elements(By.XPATH, '*')
									list_item_infos_head = list_item_infos[0].get_attribute('innerHTML').strip()
									list_item_infos_body = list_item_infos[1].get_attribute('innerHTML').strip()
									list_item_infos_footer = list_item_infos[2].get_attribute('innerHTML').strip()
									print(list_item_infos_head, list_item_infos_body)
									insertRowInfoForAISCards(new_row, list_item_infos_head, list_item_infos_body, list_item_infos_footer)
							elif capture_mode_id == 1 :
								first_block = web_content.find_elements(By.XPATH, '*')[1].find_elements(By.XPATH, '*')[0]
								first_block__price = getNumbersWithCommaFromString(first_block.find_elements(By.XPATH, '*')[1].find_elements(By.XPATH, '*')[0].get_attribute('innerHTML').strip())[0]
								new_row["price"] = first_block__price
								print(first_block__price)
								new_row["system"] = 1

								second_block_list_items = web_content.find_elements(By.XPATH, '*')[2].find_elements(By.XPATH, '*')
								footer_item = None
								for list_item in second_block_list_items :
									if "line-panel" in list_item.get_attribute('class') :
										footer_item = list_item
										break
									list_item_infos = list_item.find_elements(By.XPATH, '*')[1].find_elements(By.XPATH, '*')
									list_item_infos_head = list_item_infos[0].get_attribute('innerHTML').strip()
									list_item_infos_body = list_item_infos[1].get_attribute('innerHTML').strip()
									print(list_item_infos_head, list_item_infos_body)
									insertRowInfoForAISCards(new_row, list_item_infos_head, list_item_infos_body, None)
						elif operator_id == 1 :
							if capture_mode_id == 0 :
								pass
							elif capture_mode_id == 1 :
								pass
							elif capture_mode_id == 2 :
								pass
						elif operator_id == 2 :
							if capture_mode_id == 0 :
								pass

						print(new_row)
						list_of_rows.append(new_row)

		driver.close()

	return {"result" : list_of_rows}

app.mount("/", StaticFiles(directory="web"), name="web")
