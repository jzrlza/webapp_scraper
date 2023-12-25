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
         "url_link":"https://www.true.th/trueonline/package-types/true-gigatex-pro-special-ssv/",
         "operator_id":2,
         "pricing_type":2,
         "track_new_mega_row": false,
         "collect_sub_urls": false,
         "urls_class_type_id": 0,
         "plans":[
            {
               "plan_name":"True Gigatex PRO Special",
               "capture_sub_names": false,
               "capture_mode":0,
               "has_extra_table":false,
               "has_term_and_condition":false
            }
         ],
         "special_case_plans": []
      },
      {
         "url_link":"https://www.true.th/trueonline/package-types/true-gigatex-pro",
         "operator_id":2,
         "pricing_type":2,
         "track_new_mega_row": false,
         "collect_sub_urls": false,
         "urls_class_type_id": 0,
         "plans":[
            {
               "plan_name":"True Gigatex PRO",
               "capture_sub_names": false,
               "capture_mode":0,
               "has_extra_table":false,
               "has_term_and_condition":false
            }
         ],
         "special_case_plans": []
      },
      {
         "url_link":"https://www.true.th/trueonline/package-types/true-gigatex-pro-security",
         "operator_id":2,
         "pricing_type":2,
         "track_new_mega_row": false,
         "collect_sub_urls": false,
         "urls_class_type_id": 0,
         "plans":[
            {
               "plan_name":"True Gigatex PRO Security",
               "capture_sub_names": false,
               "capture_mode":0,
               "has_extra_table":false,
               "has_term_and_condition":false
            }
         ],
         "special_case_plans": []
      },
      {
         "url_link":"https://www.true.th/trueonline/package-types/true-gigatex-pro-gold/",
         "operator_id":2,
         "pricing_type":2,
         "track_new_mega_row": false,
         "collect_sub_urls": false,
         "urls_class_type_id": 0,
         "plans":[
            {
               "plan_name":"True Gigatex PRO Gold",
               "capture_sub_names": false,
               "capture_mode":0,
               "has_extra_table":false,
               "has_term_and_condition":false
            }
         ],
         "special_case_plans": []
      },
      {
         "url_link":"https://www.true.th/trueonline/package-types/true-gigatex-pro-cyod/",
         "operator_id":2,
         "pricing_type":2,
         "track_new_mega_row": false,
         "collect_sub_urls": false,
         "urls_class_type_id": 0,
         "plans":[
            {
               "plan_name":"True Gigatex PRO CYOD",
               "capture_sub_names": false,
               "capture_mode":0,
               "has_extra_table":false,
               "has_term_and_condition":false
            }
         ],
         "special_case_plans": []
      },
      {
         "url_link":"https://www.true.th/trueonline/package-types/true-gigatex-pro-gamer/",
         "operator_id":2,
         "pricing_type":2,
         "track_new_mega_row": false,
         "collect_sub_urls": false,
         "urls_class_type_id": 0,
         "plans":[
            {
               "plan_name":"True Gigatex PRO Gamer",
               "capture_sub_names": false,
               "capture_mode":0,
               "has_extra_table":false,
               "has_term_and_condition":false
            }
         ],
         "special_case_plans": []
      },
      {
         "url_link":"https://www.true.th/en/trueonline/package-types/true-gigatex-pro-sme/",
         "operator_id":2,
         "pricing_type":2,
         "track_new_mega_row": false,
         "collect_sub_urls": false,
         "urls_class_type_id": 0,
         "plans":[
            {
               "plan_name":"True Gigatex PRO SME",
               "capture_sub_names": false,
               "capture_mode":0,
               "has_extra_table":false,
               "has_term_and_condition":false
            }
         ],
         "special_case_plans": []
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
         },
         "special_case_plans": []
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
         },
         "special_case_plans": [
	         {
	             "plan_name":"Smart AI Gamer",
	             "sub_url": "https://www.ais.th/consumers/fibre/package/smart-ai-gamer/",
	             "capture_sub_names": false,
	             "capture_mode":1,
	             "has_extra_table":true,
	             "has_term_and_condition":false
	         }
         ]
      },
      {
         "url_link":"https://www.true.th/trueonline/package-types/true-gigatex-pro-special-ssv/",
         "operator_id":2,
         "pricing_type":2,
         "track_new_mega_row": false,
         "collect_sub_urls": false,
         "urls_class_type_id": 0,
         "plans":[
            {
               "plan_name":"True Gigatex PRO Special",
               "capture_sub_names": false,
               "capture_mode":0,
               "has_extra_table":false,
               "has_term_and_condition":false
            }
         ],
         "special_case_plans": []
      },
      {
         "url_link":"https://www.true.th/trueonline/package-types/true-gigatex-pro",
         "operator_id":2,
         "pricing_type":2,
         "track_new_mega_row": false,
         "collect_sub_urls": false,
         "urls_class_type_id": 0,
         "plans":[
            {
               "plan_name":"True Gigatex PRO",
               "capture_sub_names": false,
               "capture_mode":0,
               "has_extra_table":false,
               "has_term_and_condition":false
            }
         ],
         "special_case_plans": []
      },
      {
         "url_link":"https://www.true.th/trueonline/package-types/true-gigatex-pro-security",
         "operator_id":2,
         "pricing_type":2,
         "track_new_mega_row": false,
         "collect_sub_urls": false,
         "urls_class_type_id": 0,
         "plans":[
            {
               "plan_name":"True Gigatex PRO Security",
               "capture_sub_names": false,
               "capture_mode":0,
               "has_extra_table":false,
               "has_term_and_condition":false
            }
         ],
         "special_case_plans": []
      },
      {
         "url_link":"https://www.true.th/trueonline/package-types/true-gigatex-pro-gold/",
         "operator_id":2,
         "pricing_type":2,
         "track_new_mega_row": false,
         "collect_sub_urls": false,
         "urls_class_type_id": 0,
         "plans":[
            {
               "plan_name":"True Gigatex PRO Gold",
               "capture_sub_names": false,
               "capture_mode":0,
               "has_extra_table":false,
               "has_term_and_condition":false
            }
         ],
         "special_case_plans": []
      },
      {
         "url_link":"https://www.true.th/trueonline/package-types/true-gigatex-pro-cyod/",
         "operator_id":2,
         "pricing_type":2,
         "track_new_mega_row": false,
         "collect_sub_urls": false,
         "urls_class_type_id": 0,
         "plans":[
            {
               "plan_name":"True Gigatex PRO CYOD",
               "capture_sub_names": false,
               "capture_mode":0,
               "has_extra_table":false,
               "has_term_and_condition":false
            }
         ],
         "special_case_plans": []
      },
      {
         "url_link":"https://www.true.th/trueonline/package-types/true-gigatex-pro-gamer/",
         "operator_id":2,
         "pricing_type":2,
         "track_new_mega_row": false,
         "collect_sub_urls": false,
         "urls_class_type_id": 0,
         "plans":[
            {
               "plan_name":"True Gigatex PRO Gamer",
               "capture_sub_names": false,
               "capture_mode":0,
               "has_extra_table":false,
               "has_term_and_condition":false
            }
         ],
         "special_case_plans": []
      },
      {
         "url_link":"https://www.true.th/en/trueonline/package-types/true-gigatex-pro-sme/",
         "operator_id":2,
         "pricing_type":2,
         "track_new_mega_row": false,
         "collect_sub_urls": false,
         "urls_class_type_id": 0,
         "plans":[
            {
               "plan_name":"True Gigatex PRO SME",
               "capture_sub_names": false,
               "capture_mode":0,
               "has_extra_table":false,
               "has_term_and_condition":false
            }
         ],
         "special_case_plans": []
      }
   ],
   "webdriver_timeout":5
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

def conversionMbpsDLUL(dl_or_ul_text) :
	if checkIsInfiniteText(dl_or_ul_text) :
		return INFINITY
	elif 'Mbps' in dl_or_ul_text :
		return getNumberByUnit("Mbps", dl_or_ul_text)
	elif 'kbps' in dl_or_ul_text :
		return getNumberByUnit("kbps", dl_or_ul_text)/1000.0
	elif 'Kbps' in dl_or_ul_text :
		return getNumberByUnit("Kbps", dl_or_ul_text)/1000.0
	elif 'Gbps' in dl_or_ul_text :
		return getNumberByUnit("Gbps", dl_or_ul_text)*1000.0

#AIS --------------
def insertRowInfoForAISCards(new_row, capture_mode_id, list_item_icon_img, list_item_infos_head, list_item_infos_body, list_item_infos_footer = "", price_keywords = ["บาท"], sub_price_keywords = ["สต."]) : #void function
	is_extra = True

	if "ระยะสัญญา" in list_item_infos_head :
		new_row["contract"] = int(getNumberByUnit("เดือน", list_item_infos_body))
		is_extra = False

	#WiFi boolean zone
	if re.search('WiFi', list_item_infos_head, re.IGNORECASE) or re.search('WiFi', list_item_infos_body, re.IGNORECASE) :
		new_row["wifi"] = True
		if re.search('router', list_item_infos_head, re.IGNORECASE) or re.search('router', list_item_infos_body, re.IGNORECASE):
			new_row["wifi_router"] = True
		if re.search('mesh', list_item_infos_head, re.IGNORECASE) or re.search('mesh', list_item_infos_body, re.IGNORECASE):
			new_row["wifi_mesh"] = True

	if "เน็ตมือถือ" in list_item_infos_head :
		if checkIsInfiniteText(list_item_infos_body):
			new_row["internet_gbs"] = INFINITY
		elif 'GB' in list_item_infos_body and not ('Gbps' in list_item_infos_body) :
			new_row["internet_gbs"] = getNumberByUnit("GB", list_item_infos_body, 'Gbps')
		elif 'MB' in list_item_infos_body and not ('Mbps' in list_item_infos_body) :
			new_row["internet_gbs"] = getNumberByUnit("MB", list_item_infos_body, 'Mbps')/1000.0
		elif 'TB' in list_item_infos_body and not ('Tbps' in list_item_infos_body) :
			new_row["internet_gbs"] = getNumberByUnit("TB", list_item_infos_body, 'Tbps')*1000.0
		is_extra = False

	#entertainment zone
	entertainments = []
	if re.search('netflix', list_item_icon_img, re.IGNORECASE) :
		new_row["entertainment"] = True
		new_row["entertainment_package"] = ""
		entertainments.append(list_item_infos_body)
		is_extra = False
	if re.search('PLAY Premium Plus', list_item_infos_head, re.IGNORECASE) :
		new_row["entertainment"] = True
		new_row["entertainment_package"] = ""
		entertainments.append(list_item_infos_head)
		new_row["entertainment_contract"] = int(getNumberByUnit("เดือน", list_item_infos_body))
		is_extra = False
	for i in range(len(entertainments)) :
		new_row["entertainment_package"] += entertainments[i].replace(comma_detection, comma_replacer)
		if i < len(entertainments) - 1 :
			new_row["entertainment_package"] += micro_delimeter

	#extra zone
	if is_extra :
		trim_txt = list_item_infos_head.replace('<b>', '').replace('</b>', '')+" "+list_item_infos_body.replace('<b>', '').replace('</b>', '')
		if new_row["extra"] == None :
			new_row["extra"] = trim_txt.replace(comma_detection, comma_replacer)
		else :
			new_row["extra"] += micro_delimeter+trim_txt.replace(comma_detection, comma_replacer)

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
   "internet_gbs": 0.0,
   "download_speed": None,
   "upload_speed": None,
   "fair_usage_policy": None,
   "g_no": None,
   "unlimited_internet_mode": 0,
   "wifi": False,
   "wifi_router": False,
   "wifi_mesh": False,
   "unlimited_call": False,
   "call_minutes": 0.0,
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
	"datetime": None,
	"has_extra_info_button": False
}

OperatorUnsupportedException = Exception("Unsupported Operator.")
UntrackableException = Exception("Untrackable Page")
CaptureModeException = Exception("No such capture mode.")

def scrape_web(request, normalize_result = False):
	try :
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

		hrefs = []

		driver = webdriver.Chrome()

		for url in urls :
			#print(url)
			
			driver.implicitly_wait(webdriver_timeout)
			action = ActionChains(driver)

			driver.get(url["url_link"])

			operator_id = url["operator_id"]
			operator_name = operators[url["operator_id"]]
			pricing_type_id = url["pricing_type"]
			track_new_mega_row = url["track_new_mega_row"]
			collect_sub_urls = url["collect_sub_urls"]
			urls_class_type_id = url["urls_class_type_id"]
			special_case_plans = url["special_case_plans"]
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
							if target_url in hrefs :
								plan["is_duplicate_url"] = True
							else :
								hrefs.append(target_url)
								plan["is_duplicate_url"] = False
							plan_arr.append(plan)
					elif urls_class_type_id == 1 :
						collect_sub_urls_class = "//*[contains(@class, 'cms-secondary-button') and contains(@class, 'cms-fullWidth-button')]"

						href_targets = driver.find_elements(By.XPATH, f"{collect_sub_urls_class}")
						for href_target in href_targets :
							#root_div = href_target.find_element(By.XPATH, "..").find_element(By.XPATH, "..")
							#title = root_div.find_elements(By.XPATH, '*')[0].find_elements(By.XPATH, '*')[0].get_attribute('innerHTML').replace('<b>', '').replace('</b>', '').strip()
							target_url = href_target.get_attribute('href').strip()
							is_special = False
							for special_plan in special_case_plans :
								if target_url in special_plan["sub_url"] :
									is_special = True
									new_plan = special_plan.copy()
									new_plan["is_duplicate_url"] = False
									plan_arr.append(new_plan)

							if not is_special :
								plan = plans_template.copy()
								#plan["plan_name"] = title
								plan["sub_url"] = target_url
								if target_url in hrefs :
									plan["is_duplicate_url"] = True
								else :
									hrefs.append(target_url)
									plan["is_duplicate_url"] = False
								plan_arr.append(plan)
					else :
						raise Exception("URL capture ID class invalid.")
				else :
					raise Exception("URL capture Operator ID invalid.")
				url["plans"] = plan_arr

			for plan in url["plans"] :
				#target_string_lambda = lambda plan_name_is_text : plan["plan_name"] if title_is_at_header == True else price_keywords[0]
				if collect_sub_urls :
					if plan["sub_url"] == None or plan["sub_url"] == "" :
						raise Exception("URL relation to plan name error.")
					if plan["is_duplicate_url"] :
						continue
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
				title_class = ""
				table_temp_arr = []
				disabled_mode = False #temp value
				clicked = False
				is_special_case = False

				#if-else structured like this on purpose for ease of re-readability
				if operator_id == 0 :
					if capture_mode_id == 0 :
						target_class = "//*[@class='package-card-generic']"
						title_class = "//*[contains(@class, 'cms-color-kellyGreen-500')]"
					elif capture_mode_id == 1 :
						target_class = "//*[@class='package-card-generic']"
						if plan["has_extra_table"] :
							table_target_class = "//table[@class='table-style']"
						else :
							raise Exception("this one needs table detection")
						is_special_case = True
					else :
						raise CaptureModeException
				elif operator_id == 2 :
					if capture_mode_id == 0 :
						target_class = "//*[@class='x-g2fj0g']"
						target_click_class = "//*[contains(@class, 'x-zvu66b') and contains(@class, 'btn-primary')]"
						requires_click = True
					else :
						raise CaptureModeException
				elif operator_id == 3 :
					if capture_mode_id == 0 :
						target_class = "//*[@class='x-1rtrt6h']"
					else :
						raise CaptureModeException
				else :
					raise OperatorUnsupportedException

				#init_web_contents_lambda = lambda title_is_at_header : driver.find_elements(By.CSS_SELECTOR, f".{target_class}")[0].find_elements(By.XPATH, f'./div[contains(@class, "{operator_card_classes[operator]}")]') if title_is_at_header == True else driver.find_elements(By.CSS_SELECTOR, f".{target_class}")
				if not disabled_mode :

					if requires_click :
						time.sleep(1)
						click_targets = driver.find_elements(By.XPATH, f"{target_click_class}")
						if len(click_targets) == 0 :
							clicked = True
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

					if is_special_case :
						time.sleep(2)
						table = driver.find_elements(By.XPATH, f"{table_target_class}")[0]

						elements = table.find_elements(By.XPATH, '*')[1].find_elements(By.XPATH, '*')
						#print(table.get_attribute('innerHTML'))

						dl_chunk_save = None
						ul_chunk_save = None
						wifi_router_save = None
						contract_int_save = None
						entertainment_save = None

						for row_i in range(len(elements)) :
							row = elements[row_i]
							columns = row.find_elements(By.XPATH, '*')
							#print("row")
							new_row = row_obj_template.copy()
							new_row["operator"] = operator_name
							new_row["plan"] = plan_name
							new_row["system"] = pricing_type_id
							for elem_i in range(len(columns)) :
								elem = columns[elem_i]

								if elem_i == 0 :
									new_row["price"] = numberCheckLambda(elem.find_elements(By.XPATH, '*')[0].get_attribute('innerHTML'))
								else :
									if elem.get_attribute('rowspan') != None :
										if int(elem.get_attribute('rowspan')) == len(elements) :
											if elem_i == 1 : #dl ul
												dl_ul_chunks = elem.find_elements(By.XPATH, '*')
												dl_chunk = conversionMbpsDLUL(dl_ul_chunks[0].get_attribute('innerHTML').replace('<span class="white">', ' ').replace('</span>', ''))
												ul_chunk = conversionMbpsDLUL(dl_ul_chunks[1].get_attribute('innerHTML').replace('<span class="white">', ' ').replace('</span>', ''))
												new_row["download_speed"] = dl_chunk
												new_row["upload_speed"] = ul_chunk
												dl_chunk_save = dl_chunk
												ul_chunk_save = ul_chunk
											elif elem_i == 2 :
												new_row["wifi_router"] = True
												wifi_router_save = "obj_exists"
											elif elem_i == 5 :
												contract_int = int(elem.find_elements(By.XPATH, '*')[0].get_attribute('innerHTML'))
												contract_int_save = contract_int
												new_row["contract"] = contract_int

										elif int(elem.get_attribute('rowspan')) == len(elements)-1 :
											if elem_i == 3 :
												new_row["entertainment"] = True
												new_row["entertainment_package"] = "Play S"
												new_row["entertainment_contract"] = contract_int_save
												entertainment_save = "Play S"
									else :
										if row_i == 2 and elem_i == 1 :
											raw_str = elem.find_elements(By.XPATH, '*')[0].get_attribute('innerHTML').replace('<span>', ' ').replace('</span>', '')
											if checkIsInfiniteText(raw_str, internet_specific=True) :
												new_row["internet_gbs"] = INFINITY
											elif 'GB' in raw_str :
												new_row["internet_gbs"] = getNumberByUnit("GB", raw_str, 'Gbps')
											elif 'MB' in raw_str :
												new_row["internet_gbs"] = getNumberByUnit("MB", raw_str, 'Mbps')/1000.0
											elif 'TB' in raw_str :
												new_row["internet_gbs"] = getNumberByUnit("TB", raw_str, 'Tbps')*1000.0

								if dl_chunk_save :
									new_row["download_speed"] = dl_chunk
								if ul_chunk_save :
									new_row["upload_speed"] = ul_chunk
								if wifi_router_save :
									new_row["wifi_router"] = True
								if contract_int_save :
									new_row["contract"] = contract_int_save
								if entertainment_save :
									new_row["entertainment"] = True
									new_row["entertainment_package"] = entertainment_save
									new_row["entertainment_contract"] = contract_int_save

							now = datetime.now()
							dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
							new_row["datetime"] = dt_string

							list_of_rows.append(new_row)
							
					elif clicked :
						#continue
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

									if plan_name == "" or plan_name == None :
										title_elem = driver.find_elements(By.XPATH, f"{title_class}")[0]
										new_row["plan"] = title_elem.get_attribute('innerHTML').replace('<b>', '').replace('</b>', '').strip()

									second_block = web_content.find_elements(By.XPATH, '*')[0].find_elements(By.XPATH, '*')[2].find_elements(By.XPATH, '*')[0]
									second_block_raw_list = second_block.find_elements(By.XPATH, '*')
									second_block_has_footer = len(second_block_raw_list) > 1
									second_block__list_items = second_block.find_elements(By.XPATH, '*')[0].find_elements(By.XPATH, '*')
									for list_item in second_block__list_items :
										list_item_icon_img = list_item.find_elements(By.XPATH, '*')[0].get_attribute('innerHTML').strip()
										list_item_infos = list_item.find_elements(By.XPATH, '*')[1].find_elements(By.XPATH, '*')
										list_item_infos_head = list_item_infos[0].get_attribute('innerHTML').strip()
										list_item_infos_body = list_item_infos[1].get_attribute('innerHTML').strip()
										list_item_infos_footer = list_item_infos[2].get_attribute('innerHTML').strip()
										#print(list_item_infos_head, list_item_infos_body, list_item_infos_footer)
										insertRowInfoForAISCards(new_row, capture_mode_id, list_item_icon_img, list_item_infos_head, list_item_infos_body, list_item_infos_footer)

									if second_block_has_footer :
										for i in range(len(second_block_raw_list)) :
											target_item = second_block_raw_list[i]
											#print(target_item.get_attribute('class'))
											if i == 0 or "separator" in target_item.get_attribute('class') or "data-speed" in target_item.get_attribute('class') :
												continue
											
											dl_ul_items = target_item.find_elements(By.XPATH, '*')[1].get_attribute('innerHTML').replace('<b>', '').replace('</b>', '').strip().split("/")
											if len(dl_ul_items) != 2 :
												continue
											else :
												dl_raw_str = dl_ul_items[0]
												ul_raw_str = dl_ul_items[1]
												#Mbps based
												new_row["download_speed"] = conversionMbpsDLUL(dl_raw_str)
												new_row["upload_speed"] = conversionMbpsDLUL(ul_raw_str)

							elif operator_id == 2 :
								if capture_mode_id == 0 :
									top_block = web_content.find_elements(By.XPATH, '*')[0]
									bottom_block = web_content.find_elements(By.XPATH, '*')[1]
									price_txt = bottom_block.find_elements(By.XPATH, '*')[0].find_elements(By.XPATH, '*')[0].find_elements(By.XPATH, '*')[0].get_attribute('innerHTML').replace('<b>', '').replace('</b>', '').strip()
									new_row["price"] = numberCheckLambda(price_txt)

									package_name_block = top_block.find_elements(By.XPATH, '*')[1]
									dl_ul_block = top_block.find_elements(By.XPATH, '*')[2]
									extra_block = top_block.find_elements(By.XPATH, '*')[3]
									bottom_button = bottom_block.find_elements(By.XPATH, '*')[1].find_elements(By.XPATH, '*')[0].find_elements(By.XPATH, '*')[0]
									if "ดูรายละเอียด" in bottom_button.get_attribute('innerHTML') :
										new_row["has_extra_info_button"] = True
							
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
							
							now = datetime.now()
							dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
							new_row["datetime"] = dt_string

							print(new_row)
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
		return result #list_of_rows

	except Exception as e :
		e_type, e_object, e_traceback = sys.exc_info()

		e_filename = os.path.split(e_traceback.tb_frame.f_code.co_filename)[1]

		e_message = str(e)

		e_line_number = e_traceback.tb_lineno

		#print(e)

		return json.dumps([{
				"error": e_message,
				"line_of_error": e_line_number,
				"file_that_errored": e_filename
			}])

print(scrape_web(mock_request, normalize_result=True))

"""
expected_result = scrape_web(mock_request, normalize_result=True)
for result in expected_result :
	print(result)
"""