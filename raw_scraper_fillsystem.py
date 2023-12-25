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
         "url_link":"https://www.true.th/truemoveh/prepaid/",
         "operator_id":2,
         "pricing_type":0,
         "track_new_mega_row": false,
         "plans":[
            {
               "plan_name":"ซิมเติมเงิน",
               "capture_sub_names": true,
               "capture_mode":0,
               "has_extra_table":false,
               "has_term_and_condition":false
            }
         ]
      }
   ],
   "webdriver_timeout":15
}"""

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
         "url_link":"https://www.ais.th/consumers/package/prepaid/plan/new",
         "operator_id":0,
         "pricing_type":0,
         "track_new_mega_row": true,
         "plans":[
            {
               "plan_name":"โปรแนะนำ",
               "capture_sub_names": true,
               "capture_mode":0,
               "has_extra_table":false,
               "has_term_and_condition":false
            },
            {
               "plan_name":"โปร NET SIM",
               "capture_sub_names": false,
               "capture_mode":0,
               "has_extra_table":false,
               "has_term_and_condition":false
            }
         ]
      },
      {
         "url_link":"https://www.ais.th/consumers/package/prepaid/plan/call",
         "operator_id":0,
         "pricing_type":0,
         "track_new_mega_row": false,
         "plans":[
            {
               "plan_name":"โปรแนะนำ",
               "capture_sub_names": false,
               "capture_mode":0,
               "has_extra_table":false,
               "has_term_and_condition":false
            }
         ]
      },
      {
         "url_link":"https://www.ais.th/consumers/package/prepaid/plan/call-internet",
         "operator_id":0,
         "pricing_type":0,
         "track_new_mega_row": false,
         "plans":[
            {
               "plan_name":"โปรแนะนำ",
               "capture_sub_names": false,
               "capture_mode":0,
               "has_extra_table":false,
               "has_term_and_condition":false
            }
         ]
      },
      {
         "url_link":"https://www.ais.th/consumers/package/prepaid/plan/special",
         "operator_id":0,
         "pricing_type":0,
         "track_new_mega_row": false,
         "plans":[
            {
               "plan_name":"โปรแนะนำ",
               "capture_sub_names": false,
               "capture_mode":0,
               "has_extra_table":false,
               "has_term_and_condition":false
            }
         ]
      },
      {
         "url_link":"https://www.dtac.co.th/prepaid/simdtac.html",
         "operator_id":1,
         "pricing_type":0,
         "track_new_mega_row": false,
         "plans":[
            {
               "plan_name":"ซิมเติมเงินดีแทค",
               "capture_sub_names": true,
               "capture_mode":0,
               "has_extra_table":false,
               "has_term_and_condition":false
            },
            {
               "plan_name":"ซิมดีแทคเติมเงินอื่น",
               "capture_sub_names": true,
               "capture_mode":1,
               "has_extra_table":false,
               "has_term_and_condition":false
            }
         ]
      },
      {
         "url_link":"https://www.true.th/truemoveh/prepaid/",
         "operator_id":2,
         "pricing_type":0,
         "track_new_mega_row": false,
         "plans":[
            {
               "plan_name":"ซิมเติมเงิน",
               "capture_sub_names": true,
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
	is_extra = True

	#print(list_item_icon_img)
	#print(list_item_infos_head, list_item_infos_body)

	#XG zone
	if "3G" in list_item_infos_head or "3G" in list_item_infos_body or re.search('3g', list_item_icon_img, re.IGNORECASE) :
		if new_row["g_no"] == None :
			new_row["g_no"] = "3G"
			is_extra = False
		elif not "3G" in new_row["g_no"] :
			new_row["g_no"] += "/3G"
			is_extra = False
	if "4G" in list_item_infos_head or "4G" in list_item_infos_body or re.search('4g', list_item_icon_img, re.IGNORECASE) :
		if new_row["g_no"] == None :
			new_row["g_no"] = "4G"
			is_extra = False
		elif not "4G" in new_row["g_no"] :
			new_row["g_no"] += "/4G"
			is_extra = False
	if "5G" in list_item_infos_head or "5G" in list_item_infos_body or re.search('5g', list_item_icon_img, re.IGNORECASE) :
		if new_row["g_no"] == None :
			new_row["g_no"] = "5G"
			is_extra = False
		elif not "5G" in new_row["g_no"] :
			new_row["g_no"] += "/5G"
			is_extra = False

	#internet GB zone
	if (not "ฟรี" in list_item_infos_head) and (not "/" in list_item_infos_body) and ("เน็ต" in list_item_infos_head or re.search('internet', list_item_infos_head, re.IGNORECASE) or re.search('social', list_item_infos_head, re.IGNORECASE) or checkIsLikelyGSystemIcon(list_item_icon_img) or "โซเชียล" in list_item_infos_body) and new_row["internet_gbs"] == 0.0 :
		if checkIsInfiniteText(list_item_infos_body) or checkIsInfiniteText(list_item_infos_head):
			new_row["internet_gbs"] = INFINITY
			#if so, there's also speed
			for fup_unit in possible_fup_units :
				target_str = ""
				if fup_unit in normalizeStringForNoneTypeToString(list_item_infos_footer) :
					target_str = list_item_infos_footer.replace('.', '')
				elif fup_unit in normalizeStringForNoneTypeToString(list_item_infos_body) :
					target_str = list_item_infos_body.replace('.', '')
				elif fup_unit in normalizeStringForNoneTypeToString(list_item_infos_head) :
					target_str = list_item_infos_body.replace('.', '')

				if target_str != "" :
					new_row["speed"] = getNumberByUnitAsUnittedString(fup_unit, target_str, "GB")

		elif 'GB' in list_item_infos_body and not ('Gbps' in list_item_infos_body) :
			new_row["internet_gbs"] = getNumberByUnit("GB", list_item_infos_body, 'Gbps')
		elif 'MB' in list_item_infos_body and not ('Mbps' in list_item_infos_body) :
			new_row["internet_gbs"] = getNumberByUnit("MB", list_item_infos_body, 'Mbps')/1000.0
		elif 'TB' in list_item_infos_body and not ('Tbps' in list_item_infos_body) :
			new_row["internet_gbs"] = getNumberByUnit("TB", list_item_infos_body, 'Tbps')*1000.0
		is_extra = False

	#print(list_item_infos_footer)
	#time limit zone
	if "นาน" in list_item_infos_head or "นาน" in list_item_infos_body or "นาน" in list_item_infos_footer :
		for time_limit_unit in possible_time_limit_units :
			target_str = ""
			if "นาน" in list_item_infos_head :
				target_str = list_item_infos_head.replace(time_limit_unit+'ละ', '')
			elif "นาน" in list_item_infos_body :
				target_str = list_item_infos_body.replace(time_limit_unit+'ละ', '')
			elif "นาน" in list_item_infos_footer :
				target_str = list_item_infos_footer.replace(time_limit_unit+'ละ', '')

			#print(target_str)

			if target_str != "" :
				new_value = getNumberByUnitAsUnittedString(time_limit_unit, target_str, "GB", have_space=True)
				if new_value == None :
					continue
				else :
					new_row["limited_time"] = new_value
		is_extra = False

	#WiFi boolean zone
	if re.search('WiFi', list_item_infos_head, re.IGNORECASE) :
		new_row["wifi"] = True

	#internet cost per byte zone
	if (price_keywords[0]+"/" in list_item_infos_body) and ("เน็ต" in list_item_infos_head or re.search('internet', list_item_infos_head, re.IGNORECASE)) :
		new_row["internet_fee_baht_per_mb"]
		if price_keywords[0]+'/GB' in list_item_infos_body and not ('Gbps' in list_item_infos_body) :
			new_row["internet_fee_baht_per_mb"] = getNumberByUnit(price_keywords[0]+"/GB", list_item_infos_body, 'Gbps')*1000
		elif price_keywords[0]+'/MB' in list_item_infos_body and not ('Mbps' in list_item_infos_body) :
			new_row["internet_fee_baht_per_mb"] = getNumberByUnit(price_keywords[0]+"/MB", list_item_infos_body, 'Mbps')
		elif price_keywords[0]+'/TB' in list_item_infos_body and not ('Tbps' in list_item_infos_body) :
			new_row["internet_fee_baht_per_mb"] = getNumberByUnit(price_keywords[0]+"/TB", list_item_infos_body, 'Tbps')*1000000.0
		is_extra = False

	#cost per minute zone
	if re.search('free-calls', list_item_icon_img, re.IGNORECASE) and "โทร" in list_item_infos_head :
		if "แรก" in list_item_infos_footer :
			raw_number = 0.0
			if sub_price_keywords[0] in list_item_infos_footer :
				raw_number = getNumberByUnit(sub_price_keywords[0], list_item_infos_footer)/100.0
			else :
				raw_number = getNumberByUnit(price_keywords[0], list_item_infos_footer)

			if "วินาที" in list_item_infos_footer :
				raw_number = raw_number/60.0
			new_row["call_first_minute_fee_baht_per_minute"] = raw_number

		price_per_freq = 0.0
		if sub_price_keywords[0] in list_item_infos_body :
			price_per_freq = getNumberByUnit(sub_price_keywords[0], list_item_infos_body)/100.0
		else :
			price_per_freq = getNumberByUnit(price_keywords[0], list_item_infos_body)

		freq_time_multi = 1.0
		freq_time_unit = "นาที"
		freq_time_for_round = 1.0
		if "วินาที" in list_item_infos_body :
			freq_time_multi = 1.0/60.0
			freq_time_unit = "วินาที"

		if "ทุก" in list_item_infos_body :
			freq_time_for_round = getNumberByUnit(freq_time_unit, list_item_infos_body)*freq_time_multi
		else :
			freq_time_for_round = freq_time_multi

		new_row["call_next_minutes_fee_baht_per_minute"] = price_per_freq/freq_time_for_round

		is_extra = False

	#vid call
	if re.search('Video call', list_item_infos_head, re.IGNORECASE) :
		new_row["video_call_fee_per_minute"] = getNumberByUnit(price_keywords[0]+"/นาที", list_item_infos_body)
		is_extra = False

	#sms mms
	if re.search('SMS/MMS', list_item_infos_head, re.IGNORECASE) :
		chunks = list_item_infos_body.strip().split(",")
		for chunk in chunks :
			#print(chunk, price_keywords)
			if re.search('SMS', chunk, re.IGNORECASE) :
				new_row["sms_fee_per_msg"] = getNumberByUnit(price_keywords[0], chunk.strip())
			elif re.search('MMS', chunk, re.IGNORECASE) :
				new_row["mms_fee_per_msg"] = getNumberByUnit(price_keywords[0], chunk.strip())
		is_extra = False

	"""
	#extra zone
	if is_extra :
		trim_txt = list_item_infos_head.replace('<b>', '').replace('</b>', '')+" "+list_item_infos_body.replace('<b>', '').replace('</b>', '')
		if new_row["extra"] == None :
			new_row["extra"] = trim_txt.replace(comma_detection, comma_replacer)
		else :
			new_row["extra"] += micro_delimeter+trim_txt.replace(comma_detection, comma_replacer)
	"""

#DTAC -----------
def insertRowInfoForDTACCards(new_row, capture_mode_id, full_raw_txt, icon_class = "", price_keywords = ["บาท"], sub_price_keywords = ["สต."]) :
	#print(full_raw_txt)
	#print(icon_class)

	if icon_class == "ico-call-all" :
		new_row["call_first_minute_fee_baht_per_minute"] = numberCheckLambda(full_raw_txt)
		new_row["call_next_minutes_fee_baht_per_minute"] = numberCheckLambda(full_raw_txt)
	elif icon_class == "ico-sms" :
		new_row["sms_fee_per_msg"] = numberCheckLambda(full_raw_txt)
	elif icon_class == "ico-net" :
		new_row["internet_fee_baht_per_mb"] = numberCheckLambda(full_raw_txt)
	else :
		trim_txt = full_raw_txt.replace('<br>', ' ')
		#print(trim_txt)

#TRUE -----------
def insertRowInfoForTrueCards(new_row, capture_mode_id, html_blocks, price_keywords = ["บาท"], sub_price_keywords = ["สต."]) :
	head_str = html_blocks[0].get_attribute('innerHTML').strip()
	price_blocks = html_blocks[1].find_elements(By.XPATH, '*')
	footer_str = html_blocks[2].get_attribute('innerHTML').strip()

	price_str = price_blocks[0].get_attribute('innerHTML').strip()
	price_unit_str_1 = price_blocks[1].get_attribute('innerHTML').split('<span')[0].strip()
	price_unit_str_2 = price_blocks[1].find_elements(By.XPATH, '*')[0].get_attribute('innerHTML').strip()

	#print(head_str, price_str, price_unit_str_1, price_unit_str_2, footer_str)

	if "เน็ต" in head_str :
		new_row["price"] = numberCheckLambda(price_str)
		for fup_unit in possible_fup_units :
			target_str = ""
			if fup_unit in normalizeStringForNoneTypeToString(footer_str) :
				target_str = footer_str.replace('.', '')

			if target_str != "" :
				new_row["speed"] = getNumberByUnitAsUnittedString(fup_unit, target_str, "GB")
	elif "โทร" in head_str :
		init_price = numberCheckLambda(price_str)
		if "/วินาที" in price_unit_str_2 :
			minutes = 1/60.0
			new_row["call_next_minutes_fee_baht_per_minute"] = init_price/minutes
		elif "วินาที" in price_unit_str_2 :
			minutes = numberCheckLambda(price_unit_str_2)/60.0
			new_row["call_next_minutes_fee_baht_per_minute"] = init_price/minutes
		else :
			new_row["call_next_minutes_fee_baht_per_minute"] = init_price
		if footer_str != "" :
			if "นาทีแรก" in footer_str :
				new_row["call_first_minute_fee_baht_per_minute"] = getNumberByUnit(price_keywords[0], footer_str.strip())

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
	"g_no": None,
	"unlimited_internet_mode": 0,
	"wifi": False,
	"internet_gbs": 0.0,
	"fair_usage_policy": None,
	"speed": None,
	"limited_time": None,
	"internet_fee_baht_per_mb": 0.0,
	"call_first_minute_fee_baht_per_minute": 0.0,
	"call_next_minutes_fee_baht_per_minute": 0.0,
	"video_call_fee_per_minute": None,
	"sms_fee_per_msg": None,
	"mms_fee_per_msg": None,
	"promotion_switch_fee": 0.0,
	"datetime": None
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
			mega_class_target = ""

			need_to_scroll = False
			scrolled = False

			if track_new_mega_row :
				#raise error when there's new row but not match any members of the plans

				if operator_id == 0 :
					mega_class_target = "//*[@class='carousel-inner-content']"

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

			for plan in url["plans"] :
				#target_string_lambda = lambda plan_name_is_text : plan["plan_name"] if title_is_at_header == True else price_keywords[0]
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
									root_block = web_content.find_element(By.XPATH, "..").find_element(By.XPATH, "..").find_element(By.XPATH, "..").find_element(By.XPATH, "..").find_element(By.XPATH, "..").find_element(By.XPATH, "..").find_element(By.XPATH, "..").find_element(By.XPATH, "..").find_element(By.XPATH, "..")
									title = root_block.find_elements(By.XPATH, '*')[0].find_elements(By.XPATH, '*')[0].find_elements(By.XPATH, '*')[0].find_elements(By.XPATH, '*')[0].find_elements(By.XPATH, '*')[0].get_attribute('innerHTML').strip()
									if not re.search(plan_name, title, re.IGNORECASE) :
										continue

									first_block = web_content.find_elements(By.XPATH, '*')[0].find_elements(By.XPATH, '*')[1]
									if capture_sub_names :
										actual_plan_name = first_block.find_elements(By.XPATH, '*')[0].find_elements(By.XPATH, '*')[0].get_attribute('innerHTML').strip()
										new_row["plan"] = actual_plan_name
									if re.search(price_keywords[0], first_block.get_attribute('innerHTML').strip(), re.IGNORECASE) :
										raw_txt_thb = first_block.find_elements(By.XPATH, '*')[1].find_elements(By.XPATH, '*')[0].find_elements(By.XPATH, '*')[0].get_attribute('innerHTML').strip()
										new_row["price"] = getNumberByUnit(price_keywords[0], raw_txt_thb.replace('<b>', ' ').replace('</b>', ' '))

									second_block = web_content.find_elements(By.XPATH, '*')[0].find_elements(By.XPATH, '*')[2].find_elements(By.XPATH, '*')[0]
									second_block__info_block_1 = second_block.find_elements(By.XPATH, '*')[0]
									second_block__info_block_2 = second_block.find_elements(By.XPATH, '*')[1]
									second_block__info_block_1__items = second_block__info_block_1.find_elements(By.XPATH, '*')
									for list_item in second_block__info_block_1__items :
										list_item_icon_img = list_item.find_elements(By.XPATH, '*')[0].get_attribute('innerHTML').strip()
										list_item_infos = list_item.find_elements(By.XPATH, '*')[1].find_elements(By.XPATH, '*')
										list_item_infos_head = list_item_infos[0].get_attribute('innerHTML').strip()
										list_item_infos_body = list_item_infos[1].get_attribute('innerHTML').strip()
										list_item_infos_footer = list_item_infos[2].get_attribute('innerHTML').strip()
										insertRowInfoForAISCards(new_row, capture_mode_id, list_item_icon_img, list_item_infos_head, list_item_infos_body, list_item_infos_footer, price_keywords, sub_price_keywords)
									if "ค่าเปลี่ยน" in second_block__info_block_2.get_attribute('innerHTML').strip() :
										raw_txt = second_block__info_block_2.find_elements(By.XPATH, '*')[0].find_elements(By.XPATH, '*')[0].find_elements(By.XPATH, '*')[0].get_attribute('innerHTML').strip()
										new_row["promotion_switch_fee"] = getNumberByUnit(price_keywords[0], raw_txt)

							elif operator_id == 1 :
								if capture_mode_id == 0 :
									root_block = web_content.find_element(By.XPATH, "..").find_element(By.XPATH, "..")
									title = root_block.find_elements(By.XPATH, '*')[2].get_attribute('innerHTML').strip()
									if not re.search(plan_name, title, re.IGNORECASE) :
										continue

									first_blocks = web_content.find_elements(By.XPATH, '*')[0].find_elements(By.XPATH, '*')[1].find_elements(By.XPATH, '*')[0].find_elements(By.XPATH, '*')
									price_block = first_blocks[2]
									details_blocks = first_blocks[3].find_elements(By.XPATH, '*')

									price_block_txt = price_block.find_elements(By.XPATH, '*')[1].get_attribute('innerHTML').replace('</span>', '').replace('/', ' ').replace('<span>', '').strip()
									#print(price_block_txt)
									new_row["price"] = getNumberByUnit(price_keywords[0], price_block_txt)

									details_block__top_elements = details_blocks[0].find_elements(By.XPATH, '*')[0].find_elements(By.XPATH, '*')
									for top_elem in details_block__top_elements :
										insertRowInfoForDTACCards(new_row, capture_mode_id, top_elem.get_attribute('innerHTML').strip(), "", price_keywords, sub_price_keywords)
									details_block__bottom_elements = details_blocks[1].find_elements(By.XPATH, '*')[0].find_elements(By.XPATH, '*')
									for bottom_elem in details_block__bottom_elements :
										sub_elems = bottom_elem.find_elements(By.XPATH, '*')
										insertRowInfoForDTACCards(new_row, capture_mode_id, sub_elems[1].get_attribute('innerHTML').strip(), sub_elems[0].get_attribute('class'), price_keywords, sub_price_keywords)

								elif capture_mode_id == 1 :
									root_block = web_content.find_element(By.XPATH, "..").find_element(By.XPATH, "..")
									title = root_block.find_elements(By.XPATH, '*')[0].find_elements(By.XPATH, '*')[0].get_attribute('innerHTML').strip()
									if not re.search(plan_name, title, re.IGNORECASE) :
										continue

									real_blocks = web_content.find_elements(By.XPATH, '*')[0].find_elements(By.XPATH, '*')
									top_detail = real_blocks[len(real_blocks)-3]
									bottom_details = real_blocks[len(real_blocks)-1].find_elements(By.XPATH, '*')

									new_row["plan"] = bottom_details[0].get_attribute('innerHTML').strip()
									price_block_txt = bottom_details[1].get_attribute('innerHTML').replace('</span>', '').replace('/', ' ').replace('<span>', '').strip()
									new_row["price"] = getNumberByUnit(price_keywords[0], price_block_txt.replace('ฟรี', '0'))

							elif operator_id == 2 :
								if capture_mode_id == 0 :
									mega_root = web_content.find_element(By.XPATH, "..").find_element(By.XPATH, "..").find_element(By.XPATH, "..").find_element(By.XPATH, "..").find_element(By.XPATH, "..").find_element(By.XPATH, "..").find_element(By.XPATH, "..")
									title = mega_root.find_elements(By.XPATH, '*')[0].find_elements(By.XPATH, '*')[0].find_elements(By.XPATH, '*')[0].find_elements(By.XPATH, '*')[0].get_attribute('innerHTML').strip()
									if not re.search(plan_name, title, re.IGNORECASE) :
										continue

									real_items = web_content.find_elements(By.XPATH, '*')[0].find_elements(By.XPATH, '*')
									top_head = real_items[0]
									second_head = real_items[1]
									head_txt = second_head.get_attribute('innerHTML').strip()
									if "ย้ายค่าย" in head_txt :
										continue
									new_row["plan"] = head_txt
									basic_details_blocks = real_items[len(real_items)-3].find_elements(By.XPATH, '*')
									basic_details__left_blocks = basic_details_blocks[0].find_elements(By.XPATH, '*')
									basic_details__right_blocks = basic_details_blocks[1].find_elements(By.XPATH, '*')
									price_details_blocks = real_items[len(real_items)-2].find_elements(By.XPATH, '*')[0].find_elements(By.XPATH, '*')
									new_row["price"] = numberCheckLambda(price_details_blocks[1].get_attribute('innerHTML').strip())
									insertRowInfoForTrueCards(new_row, capture_mode_id, basic_details__left_blocks, price_keywords, sub_price_keywords)
									insertRowInfoForTrueCards(new_row, capture_mode_id, basic_details__right_blocks, price_keywords, sub_price_keywords)
									

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
							row[row_key] = f'{quotation}{"Yes"}{quotation}'
						elif row[row_key] == False :
							row[row_key] = f'{quotation}{"No"}{quotation}'
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