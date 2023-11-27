import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
#from selenium.common.exceptions import NoSuchElementException
import re
import time
import json
from datetime import datetime
import sys
import os

throw_error_to_warn_new_row = False

mock_request = """{
   "price_keywords":[
      "บาท",
      ".-",
      "Baht",
      "THB",
      "฿"
   ],
   "sub_price_keywords":[
      "สต.",
      "สตางค์"
   ],
   "predefined_g_no": "5G",
   "predefined_g_no_if_free": "4G",
   "urls":[
      {
         "url_link":"https://www.ais.th/consumers/fibre/package",
         "operator_id":0,
         "pricing_type":2,
         "track_new_mega_row": false,
         "collect_sub_urls": true,
         "urls_class_type_id": 0,
         "plans":[],
         "plans_template": {
             "plan_name":"",
             "capture_sub_names": false,
             "capture_mode":0,
             "has_extra_table":false,
             "has_term_and_condition":false
         }
      }
   ],
   "webdriver_timeout":15
}"""

mock_request_temp = """{
   "price_keywords":[
      "บาท",
      ".-",
      "Baht",
      "THB",
      "฿"
   ],
   "sub_price_keywords":[
      "สต.",
      "สตางค์"
   ],
   "predefined_g_no": "5G",
   "predefined_g_no_if_free": "4G",
   "urls":[
      {
         "url_link":"https://www.ais.th/consumers/fibre/package",
         "operator_id":0,
         "pricing_type":2,
         "track_new_mega_row": false,
         "collect_sub_urls": true,
         "urls_class_type_id": 0,
         "plans":[],
         "plans_template": {
             "plan_name":"",
             "capture_sub_names": false,
             "capture_mode":0,
             "has_extra_table":false,
             "has_term_and_condition":false
         }
      },
      {
         "url_link":"https://www.ais.th/consumers/fibre",
         "operator_id":0,
         "pricing_type":2,
         "track_new_mega_row": false,
         "collect_sub_urls": true,
         "urls_class_type_id": 1,
         "plans":[],
         "plans_template": {
             "plan_name":"",
             "capture_sub_names": false,
             "capture_mode":0,
             "has_extra_table":false,
             "has_term_and_condition":false
         }
      },
      {
         "url_link":"https://www.true.th/trueonline/package-types/true-gigatex-pro-special-ssv/",
         "operator_id":2,
         "pricing_type":2,
         "track_new_mega_row": true,
         "collect_sub_urls": true,
         "urls_class_type_id": 0,
         "plans":[
            {
               "plan_name":"temp",
               "capture_sub_names": false,
               "capture_mode":0,
               "has_extra_table":false,
               "has_term_and_condition":false
            }
         ]
      }
   ],
   "webdriver_timeout":15
}"""

#ไม่รวมย้ายค่าย

INFINITY = "Unlimited"
micro_delimeter = ", "
comma_detection = '"' 
comma_replacer = "'" #in case of numbers like 100,000 : this maybe sensitive
quotation = ''

def normalizeStringForNoneTypeToString(raw_str) :
	if raw_str == None :
		return ""
	return raw_str

def normalizeStringEmptyToNoneType(raw_str) :
	if raw_str == "" :
		return None
	return raw_str

def distinctStringSet(list_string) : #returns str[]
	auxiliaryList = []
	for word in list_string:
		if word not in auxiliaryList:
			auxiliaryList.append(word)
	return auxiliaryList

def getNumbersWithCommaFromString(raw_txt) : #returns float[]
	pattern = r'\d{1,3}(?:,\d{3})*(?:\.\d+)?'

	matches = re.findall(pattern, raw_txt)

	numbers = [float(match.replace(',', '')) for match in matches]

	return numbers

def getNumbersWithNoCommaFromString(raw_txt) :
	pattern = r"[+-]?\d+(?:\.\d+)?"

	matches = re.findall(pattern, raw_txt)

	numbers = [float(match) for match in matches]

	return numbers

numberCheckLambda = (lambda raw_num_txt : getNumbersWithCommaFromString(raw_num_txt)[0] if "," in raw_num_txt else getNumbersWithNoCommaFromString(raw_num_txt)[0])

def getNumberByUnit(unit, raw_txt, unwanted_unit = "!@#$%^&") :
	raw_txt = " ".join(raw_txt.split())
	#print(raw_txt)

	split_spaces = raw_txt.replace('(', '').replace(')', '').replace('[', '').replace(']', '').replace('<', ' ').replace('>', ' ').split(" ")
	for split_i in range(len(split_spaces)) :
		splitted = split_spaces[split_i]
		if splitted == unit : #X GB
			return numberCheckLambda(split_spaces[split_i-1])
		elif unit in splitted and not (unwanted_unit in splitted) : #XGB
			return numberCheckLambda(splitted)

def getNumberByUnitAsUnittedString(unit, raw_txt, unwanted_unit = "!@#$%^&", have_space = False) :
	raw_txt = " ".join(raw_txt.split())
	#print(raw_txt)

	split_spaces = raw_txt.replace('(', '').replace(')', '').replace('[', '').replace(']', '').replace('<', ' ').replace('>', ' ').split(" ")
	space_str = ""
	if have_space :
		space_str = " "
	for split_i in range(len(split_spaces)) :
		splitted = split_spaces[split_i]
		if splitted == unit : #X GB
			float_num = numberCheckLambda(split_spaces[split_i-1])
			return f"{float_num:.0f}{space_str}{unit}"
		elif unit in splitted and not (unwanted_unit in splitted) : #XGB
			float_num = numberCheckLambda(splitted)
			return f"{float_num:.0f}{space_str}{unit}"

def checkSystemGetEnum(raw_txt) :
	if "ต่อเดือน" in raw_txt :
		return 1
	return 0

def checkIsLikelyGSystemIcon(txt) :
	return re.search('3g', txt, re.IGNORECASE) or re.search('4g', txt, re.IGNORECASE) or re.search('5g', txt, re.IGNORECASE)

def checkIsInfiniteText(txt, internet_specific = False) :
	if internet_specific :
		return "เน็ตไม่จำกัด" in txt or "เน็ตไม่อั้น" in txt or (re.search('internet', txt, re.IGNORECASE) and re.search('unlimited', txt, re.IGNORECASE))
	return "ไม่จำกัด" in txt or 'ไม่อั้น' in txt or re.search('unlimited', txt, re.IGNORECASE)

possible_fup_units = ['Gbps', 'Mbps', 'kbps', 'Kbps']
possible_time_limit_units = ['วัน', 'เดือน', 'สัปดาห์', 'ปี']

#AIS --------------
def insertRowInfoForAISCards(new_row, capture_mode_id, list_item_icon_img, list_item_infos_head, list_item_infos_body, list_item_infos_footer = "", price_keywords = ["บาท"], sub_price_keywords = ["สต."]) : #void function
	pass

#DTAC -----------
def insertRowInfoForDTACCards(new_row, capture_mode_id, full_raw_txt, icon_class = "", price_keywords = ["บาท"], sub_price_keywords = ["สต."]) :
	pass

#TRUE -----------
def insertRowInfoForTrueCards(new_row, capture_mode_id, html_blocks, price_keywords = ["บาท"], sub_price_keywords = ["สต."]) :
	pass

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
	"operator": "",
	"plan": "",
	"system": -1,
	"price": 0.0,
	"datetime": None
}

OperatorUnsupportedException = Exception("Unsupported Operator.")
UntrackableException = Exception("Untrackable Page")
CaptureModeException = Exception("No such capture mode.")

def scrape_web(request, normalize_result = False):
	#try :
		qr = json.loads(request)
		price_keywords = qr['price_keywords']
		sub_price_keywords = qr['sub_price_keywords']
		urls = qr['urls']
		webdriver_timeout = qr['webdriver_timeout']

		predefined_g_no = qr["predefined_g_no"]
		predefined_g_no_if_free = qr["predefined_g_no_if_free"]

		#print(qr)

		list_of_rows = []
		unknown_rows = []

		for url in urls :
			#print(url)

			driver = webdriver.Chrome()
			driver.implicitly_wait(webdriver_timeout)
			action = ActionChains(driver)

			driver.get(url["url_link"])

			operator_id = url["operator_id"]
			operator_name = operators[url["operator_id"]]
			pricing_type_id = url["pricing_type"]
			track_new_mega_row = url["track_new_mega_row"]
			collect_sub_urls = url["collect_sub_urls"]
			urls_class_type_id = url["urls_class_type_id"]
			mega_class_target = ""
			collect_sub_urls_class = ""

			need_to_scroll = False
			scrolled = False

			if track_new_mega_row and collect_sub_urls :
				raise Exception("track_new_mega_row and collect_sub_urls should never be both True")

			if track_new_mega_row and not collect_sub_urls :
				#raise error when there's new row but not match any members of the plans

				if operator_id == 0 :
					mega_class_target = "//*[contains(@class, 'cms-primary-button')]"

					root_web_contents = driver.find_elements(By.XPATH, f"{mega_class_target}")
					for root_web_content in root_web_contents :
						mega_root = root_web_content.find_element(By.XPATH, "..").find_element(By.XPATH, "..").find_element(By.XPATH, "..").find_element(By.XPATH, "..").find_element(By.XPATH, "..")
						title = mega_root.find_elements(By.XPATH, '*')[0].find_elements(By.XPATH, '*')[0].find_elements(By.XPATH, '*')[0].find_elements(By.XPATH, '*')[0].find_elements(By.XPATH, '*')[0].get_attribute('innerHTML').replace('<b>', '').replace('</b>', '').strip()
						this_title_is_in_planned_plan = False
						for plan in url["plans"] :
							plan_name = plan["plan_name"]
							if re.search(plan_name, title, re.IGNORECASE) :
								this_title_is_in_planned_plan = True
						if not this_title_is_in_planned_plan :
							if throw_error_to_warn_new_row :
								raise Exception("There exists a new plan name which has not yet been checked : "+url["url_link"])
							else :
								unknown_new_row = row_obj_template.copy()
								unknown_new_row["operator"] = operator_name
								unknown_new_row["plan"] = title+" ****"
								unknown_rows.append(unknown_new_row)
				else :
					raise UntrackableException


			if collect_sub_urls and not track_new_mega_row :
				plans_template = url["plans_template"]
				plan_arr = []
				if operator_id == 0 :
					if urls_class_type_id == 0 :
						collect_sub_urls_class = "//*[contains(@class, 'cms-primary-button')]"

						href_targets = driver.find_elements(By.XPATH, f"{collect_sub_urls_class}")
						for href_target in href_targets :
							root_div = href_target.find_element(By.XPATH, "..").find_element(By.XPATH, "..")
							title = root_div.find_elements(By.XPATH, '*')[0].find_elements(By.XPATH, '*')[0].get_attribute('innerHTML').replace('<b>', '').replace('</b>', '').strip()
							target_url = href_target.get_attribute('href').strip()
							plan = plans_template.copy()
							plan["plan_name"] = title
							plan["sub_url"] = target_url
							plan_arr.append(plan)
					elif urls_class_type_id == 1 :
						collect_sub_urls_class = "//*[contains(@class, 'cms-secondary-button') and contains(@class, 'cms-fullWidth-button')]"

						href_targets = driver.find_elements(By.XPATH, f"{collect_sub_urls_class}")
						for href_target in href_targets :
							root_div = href_target.find_element(By.XPATH, "..").find_element(By.XPATH, "..")
							title = root_div.find_elements(By.XPATH, '*')[0].find_elements(By.XPATH, '*')[0].get_attribute('innerHTML').replace('<b>', '').replace('</b>', '').strip()
							target_url = href_target.get_attribute('href').strip()
							plan = plans_template.copy()
							plan["plan_name"] = title
							plan["sub_url"] = target_url
							plan_arr.append(plan)
					else :
						raise Exception("URL capture ID class invalid.")
					url["plans"] = plan_arr

			for plan in url["plans"] :
				#target_string_lambda = lambda plan_name_is_text : plan["plan_name"] if title_is_at_header == True else price_keywords[0]
				if collect_sub_urls :
					if plan["sub_url"] == None or plan["sub_url"] == "" :
						raise Exception("URL relation to plan name error.")
					driver.get(plan["sub_url"]) 
					driver.implicitly_wait(2)

				target_string = price_keywords[0]
				plan_name = plan["plan_name"]
				capture_mode_id = plan["capture_mode"]
				capture_sub_names = plan["capture_sub_names"] #bool
				#title_finder_lambda = lambda title_is_at_header : container_classes[operator] if title_is_at_header == True else operator_card_classes[operator]
				target_class = ""#plan["css_item_class_name"]
				requires_click = False
				target_click_class = ""
				menu_to_click_class = ""
				table_target_class = ""
				table_temp_arr = []
				disabled_mode = False #temp value
				clicked = False

				#if-else structured like this on purpose for ease of re-readability
				if operator_id == 0 :
					if capture_mode_id == 0 :
						target_class = "//*[@class='package-card-generic']"
					else :
						raise CaptureModeException
				elif operator_id == 1 :
					if capture_mode_id == 0 :
						target_class = "//*[@class='lg-item-sim']"
					elif capture_mode_id == 1 :
						target_class = "//*[@class='item-sim']"
					else :
						raise CaptureModeException
				elif operator_id == 2 :
					if capture_mode_id == 0 :
						target_class = "//*[@class='x-1rtrt6h']"
					else :
						raise CaptureModeException
				else :
					raise OperatorUnsupportedException

				#init_web_contents_lambda = lambda title_is_at_header : driver.find_elements(By.CSS_SELECTOR, f".{target_class}")[0].find_elements(By.XPATH, f'./div[contains(@class, "{operator_card_classes[operator]}")]') if title_is_at_header == True else driver.find_elements(By.CSS_SELECTOR, f".{target_class}")
				if not disabled_mode :

					if plan["has_extra_table"] :
						pass

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
							#print(web_content.get_attribute('class'))
							new_row = row_obj_template.copy()
							new_row["operator"] = operator_name
							new_row["plan"] = plan_name
							new_row["system"] = pricing_type_id
							
							if operator_id == 0 : #start at "package-card-generic"
								if capture_mode_id == 0 :
									top_block = web_content.find_elements(By.XPATH, '*')[0].find_elements(By.XPATH, '*')[1]
									price_txt = top_block.find_elements(By.XPATH, '*')[1].find_elements(By.XPATH, '*')[0].find_elements(By.XPATH, '*')[0].get_attribute('innerHTML').replace('<b>', '').replace('</b>', '').strip()
									new_row["price"] = numberCheckLambda(price_txt)

							"""
							#LASTLY unlimited internet mode: 0 = no internet, 1 = unlimited, 2 = limited by speed, 3 = limited then stop
							if new_row["internet_gbs"] == INFINITY :
								new_row["unlimited_internet_mode"] = 1
								new_row["fair_usage_policy"] = None
							elif new_row["fair_usage_policy"] != None and new_row["internet_gbs"] > 0.0 :
								new_row["unlimited_internet_mode"] = 2
							elif new_row["fair_usage_policy"] == None and new_row["internet_gbs"] > 0.0 :
								new_row["unlimited_internet_mode"] = 3
							elif new_row["internet_gbs"] == 0.0 :
								new_row["unlimited_internet_mode"] = 0
							"""
							now = datetime.now()
							dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
							new_row["datetime"] = dt_string

							#print(new_row)
							list_of_rows.append(new_row)

			driver.close()

		if normalize_result :
			for row in list_of_rows :
				for row_key in row :
					if row[row_key] == None :
						row[row_key] = f'{quotation}-{quotation}'
					else :
						if row[row_key] == True :
							row[row_key] = f'{quotation}{1}{quotation}'
						elif row[row_key] == False :
							row[row_key] = f'{quotation}{0}{quotation}'
						elif isinstance(row[row_key], float) :
							if row[row_key].is_integer() :
								row[row_key] = f'{quotation}{row[row_key]:.0f}{quotation}'
							else :
								row[row_key] = f'{quotation}{row[row_key]:.3f}{quotation}'
						else :
							row[row_key] = f'{quotation}{row[row_key]}{quotation}'#.encode(encoding='UTF-8',errors='strict')

		if len(list_of_rows) <= 0 :
			raise Exception("No data can be found.")

		for unknown_new_row in unknown_rows :
			list_of_rows.append(unknown_new_row)

		result = json.dumps(list_of_rows)
		#print(result)
		return list_of_rows
"""
	except Exception as e :
		e_type, e_object, e_traceback = sys.exc_info()

		e_filename = os.path.split(e_traceback.tb_frame.f_code.co_filename)[1]

		e_message = str(e)

		e_line_number = e_traceback.tb_lineno

		print(e)

		return json.dumps([{
				"error": e_message,
				"line_of_error": e_line_number,
				"file_that_errored": e_filename
			}])
"""
#print(scrape_web(mock_request, normalize_result=True))


expected_result = scrape_web(mock_request, normalize_result=True)
for result in expected_result :
	print(result)
