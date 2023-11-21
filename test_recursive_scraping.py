import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import re
import time
import json
from datetime import datetime

mock_request = """{
   "price_keywords":[
      "บาท",
      ".-",
      "Baht",
      "THB",
      "฿"
   ],
   "urls":[
      {
         "url_link":"https://www.true.th/truemoveh/postpaid/mass",
         "operator_id":2,
         "pricing_type":1,
         "plans":[
            {
               "plan_name":"5G Together",
               "capture_mode":0,
               "has_extra_table":false,
               "has_term_and_condition":false
            },
            {
               "plan_name":"5G Net Ultra Max Speed",
               "capture_mode":0,
               "has_extra_table":false,
               "has_term_and_condition":false
            }
         ]
      }
   ],
   "webdriver_timeout":15
}"""

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
	split_spaces = raw_txt.replace('(', '').replace(')', '').replace('[', '').replace(']', '').replace('<', ' ').replace('>', ' ').split(" ")
	for split_i in range(len(split_spaces)) :
		splitted = split_spaces[split_i]
		if splitted == unit : #X GB
			return numberCheckLambda(split_spaces[split_i-1])
		elif unit in splitted and not (unwanted_unit in splitted) : #XGB
			return numberCheckLambda(splitted)

def getNumberByUnitAsUnittedString(unit, raw_txt, unwanted_unit = "!@#$%^&") :
	split_spaces = raw_txt.replace('(', '').replace(')', '').replace('[', '').replace(']', '').replace('<', ' ').replace('>', ' ').split(" ")
	for split_i in range(len(split_spaces)) :
		splitted = split_spaces[split_i]
		if splitted == unit : #X GB
			float_num = numberCheckLambda(split_spaces[split_i-1])
			return f"{float_num:.0f}{unit}"
		elif unit in splitted and not (unwanted_unit in splitted) : #XGB
			float_num = numberCheckLambda(splitted)
			return f"{float_num:.0f}{unit}"

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

possible_fup_units = ['Gbps', 'Mbps', 'kbps']

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
	"sms": 0,
	"mms": 0,
	"entertainment": False,
	"entertainment_package": None,
	"entertainment_contract": 0,
	"priviledge": False,
	"priviledge_exclusive": None,
	"contract": 0,
	"extra": None,
	"notes": None,
	"datetime": None
}

def dom_classes(web_content, layer_no) :
	sub_elements = web_content.find_elements(By.XPATH, '*')
	class_names = web_content.get_attribute('class')
	print(layer_no, web_content.tag_name)
	total_classes = []
	if len(sub_elements) <= 0 :
		return class_names

	for sub_element in sub_elements :
		total_classes.append(dom_classes(sub_element, layer_no+1))

	return total_classes

def scrape_web(request, normalize_result = False):
	qr = json.loads(request)
	price_keywords = qr['price_keywords']
	urls = qr['urls']
	webdriver_timeout = qr['webdriver_timeout']

	#print(qr)

	list_of_rows = []

	for url in urls :
		#print(url)

		driver = webdriver.Chrome()
		driver.implicitly_wait(webdriver_timeout)
		action = ActionChains(driver)

		driver.get(url["url_link"])

		operator_id = url["operator_id"]
		operator_name = operators[url["operator_id"]]
		pricing_type_id = url["pricing_type"]

		target_class = "//body"
		init_web_content = driver.find_element(By.XPATH, f"{target_class}")

		dom_classes_arr = dom_classes(init_web_content, 0)
		print(dom_classes_arr)

		need_to_scroll = False
		scrolled = False

		for plan in url["plans"] :
			#target_string_lambda = lambda plan_name_is_text : plan["plan_name"] if title_is_at_header == True else price_keywords[0]
			target_string = price_keywords[0]
			plan_name = plan["plan_name"]
			capture_mode_id = plan["capture_mode"]
			#title_finder_lambda = lambda title_is_at_header : container_classes[operator] if title_is_at_header == True else operator_card_classes[operator]
			#plan["css_item_class_name"]
			requires_click = False
			target_click_class = ""
			menu_to_click_class = ""
			table_target_class = ""
			table_temp_arr = []
			disabled_mode = False #temp value
			clicked = False

			
			new_row = row_obj_template.copy()
			new_row["operator"] = operator_name
			new_row["plan"] = plan_name



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

	result = dom_classes_arr#json.dumps(list_of_rows)
	#print(result)
	return result

print(scrape_web(mock_request, normalize_result=False))