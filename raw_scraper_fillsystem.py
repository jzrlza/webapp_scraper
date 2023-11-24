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
               "capture_mode":1,
               "has_extra_table":false,
               "has_term_and_condition":false
            }
         ]
      },
      {
         "url_link":"https://www.ais.th/consumers/package/prepaid/plan/call",
         "operator_id":0,
         "pricing_type":0,
         "track_new_mega_row": true,
         "plans":[
            {
               "plan_name":"โปรแนะนำ",
               "capture_sub_names": false,
               "capture_mode":0,
               "has_extra_table":false,
               "has_term_and_condition":false
            },
         ]
      },
      {
         "url_link":"https://www.ais.th/consumers/package/prepaid/plan/call-internet",
         "operator_id":0,
         "pricing_type":0,
         "track_new_mega_row": true,
         "plans":[
            {
               "plan_name":"โปรแนะนำ",
               "capture_sub_names": false,
               "capture_mode":0,
               "has_extra_table":false,
               "has_term_and_condition":false
            },
         ]
      },
      {
         "url_link":"https://www.ais.th/consumers/package/prepaid/plan/special",
         "operator_id":0,
         "pricing_type":0,
         "track_new_mega_row": true,
         "plans":[
            {
               "plan_name":"โปรแนะนำ",
               "capture_sub_names": false,
               "capture_mode":0,
               "has_extra_table":false,
               "has_term_and_condition":false
            },
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
	split_spaces = raw_txt.replace('(', '').replace(')', '').replace('[', '').replace(']', '').replace('<', ' ').replace('>', ' ').split(" ")
	for split_i in range(len(split_spaces)) :
		splitted = split_spaces[split_i]
		if splitted == unit : #X GB
			return numberCheckLambda(split_spaces[split_i-1])
		elif unit in splitted and not (unwanted_unit in splitted) : #XGB
			return numberCheckLambda(splitted)

def getNumberByUnitAsUnittedString(unit, raw_txt, unwanted_unit = "!@#$%^&", have_space = False) :
	raw_txt = " ".join(raw_txt.split())
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

	print(list_item_icon_img)
	print(list_item_infos_head, list_item_infos_body)

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

	print(list_item_infos_footer)
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
			print(chunk, price_keywords)
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
def insertRowInfoForDTACCards(new_row, capture_mode_id, list_item_full_text) :
	pass
	"""
	is_extra = True

	#internet, g, fup, and gb zone
	if 'เน็ต' in list_item_full_text :
		if checkIsInfiniteText(list_item_full_text) :
			new_row["internet_gbs"] = INFINITY
		elif 'GB' in list_item_full_text :
			new_row["internet_gbs"] = getNumberByUnit("GB", list_item_full_text, 'Gbps')
		elif 'MB' in list_item_full_text :
			new_row["internet_gbs"] = getNumberByUnit("MB", list_item_full_text, 'Mbps')/1000.0
		elif 'TB' in list_item_full_text :
			new_row["internet_gbs"] = getNumberByUnit("TB", list_item_full_text, 'Tbps')*1000.0

		if "3G" in list_item_full_text :
			if new_row["g_no"] == None :
				new_row["g_no"] = "3G"
			elif not "3G" in new_row["g_no"] :
				new_row["g_no"] += "/3G"
		if "4G" in list_item_full_text :
			if new_row["g_no"] == None :
				new_row["g_no"] = "4G"
			elif not "4G" in new_row["g_no"] :
				new_row["g_no"] += "/4G"
		if "5G" in list_item_full_text :
			if new_row["g_no"] == None :
				new_row["g_no"] = "5G"
			elif not "5G" in new_row["g_no"] :
				new_row["g_no"] += "/5G"

		for fup_unit in possible_fup_units :
			if fup_unit in list_item_full_text :
				new_row["fair_usage_policy"] = getNumberByUnitAsUnittedString(fup_unit, list_item_full_text, "GB")
				break

		is_extra = False

	#call zone
	if 'โทรฟรีทุกเครือข่าย' in list_item_full_text :
		#print(list_item_full_text)
		if checkIsInfiniteText(list_item_full_text.strip().split(">")[1].split("<")[0]) :
			new_row["call_minutes"] = INFINITY
			new_row["unlimited_call"] = True
		else :
			new_row["call_minutes"] = getNumberByUnit("นาที", list_item_full_text, 'ชม')
		is_extra = False

	if "เบอร์ดีแทค" in list_item_full_text and "โทรฟรี" in list_item_full_text :
		new_row["unlimited_call"] = True
		is_extra = False

	#priviledge zone
	if re.search('member', list_item_full_text, re.IGNORECASE) :
		priv_str = None
		priv_str_chunks = list_item_full_text.replace('<br>', ' ').strip().split(">")[1].split("<")[0].split(" ")
		for priv_str_chunk in priv_str_chunks :
			if "สิทธิ์" in priv_str_chunk or re.search('member', priv_str_chunk, re.IGNORECASE) :
				continue
			else :
				if priv_str == None :
					priv_str = priv_str_chunk
				else :
					priv_str += " "+priv_str_chunk
		new_row["priviledge"] = True
		new_row["priviledge_exclusive"] = priv_str
		is_extra = False

	#wifi zone
	if re.search('WiFi', list_item_full_text, re.IGNORECASE) :
		new_row["wifi"] = True
		is_extra = False

	#entertainment zone
	if 'ชมฟรี' in list_item_full_text or "ความบันเทิง" in list_item_full_text :
		new_row["entertainment"] = True
		entertainment_str = list_item_full_text.replace('<br>', ' ').replace('\n                                ', '').strip().split(">")[1].split("<")[0]
		if new_row["entertainment_package"] == None :
			new_row["entertainment_package"] = entertainment_str.replace('<b>', '').replace('</b>', '').replace(comma_detection, comma_replacer)
		else :
			new_row["entertainment_package"] += micro_delimeter+entertainment_str.replace('<b>', '').replace('</b>', '').replace(comma_detection, comma_replacer)
		is_extra = False

	#extra zone : this one isb too evil
	if is_extra :
		pass
	"""

def insertRowInfoForTrueCards(new_row, capture_mode_id, list_item_full_text) :
	pass
	"""
	if "สิทธิ์" in list_item_full_text and re.search('card', list_item_full_text, re.IGNORECASE) and re.search('true', list_item_full_text, re.IGNORECASE) :
		
		priv_str = None
		priv_str_chunks = list_item_full_text.split(" ")
		for priv_str_chunk_i in range(len(priv_str_chunks)) :
			priv_str_chunk = priv_str_chunks[priv_str_chunk_i]
			if priv_str_chunk_i == 0 :
				continue
			else :
				if re.search('true', priv_str_chunks[priv_str_chunk_i-1], re.IGNORECASE) and re.search('card', priv_str_chunks[priv_str_chunk_i+1], re.IGNORECASE) :
					priv_str = priv_str_chunk
					break

		new_row["priviledge"] = True
		new_row["priviledge_exclusive"] = priv_str

		if "เดือน" in list_item_full_text :
			new_row["contract"] = getNumberByUnit("เดือน", list_item_full_text)

	elif "ความบันเทิง" in list_item_full_text or "รับชม" in list_item_full_text or "ดูหนัง" in list_item_full_text or "ฟังเพลง" in list_item_full_text :
		new_row["entertainment"] = True
		if new_row["entertainment_package"] == None :
			new_row["entertainment_package"] = list_item_full_text.replace('<b>', '').replace('</b>', '').replace(comma_detection, comma_replacer)
		else :
			new_row["entertainment_package"] += micro_delimeter+list_item_full_text.replace('<b>', '').replace('</b>', '').replace(comma_detection, comma_replacer)
		if "เดือน" in list_item_full_text :
			new_row["entertainment_contract"] = getNumberByUnit("เดือน", list_item_full_text.replace('<b>', '').replace('</b>', ''))
	else :
		if new_row["extra"] == None :
			new_row["extra"] = list_item_full_text.replace('<b>', '').replace('</b>', '').replace(comma_detection, comma_replacer)
		else :
			new_row["extra"] += micro_delimeter+list_item_full_text.replace('<b>', '').replace('</b>', '').replace(comma_detection, comma_replacer)
	"""

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
			mega_class_target = ""

			need_to_scroll = False
			scrolled = False

			if track_new_mega_row :
				pass
				#raise error when there's new row but not match any members of the plans
				if operator_id == 0 :
					mega_class_target = "//*[@class='carousel-inner-content']"

					root_web_contents = driver.find_elements(By.XPATH, f"{mega_class_target}")
					for root_web_content in root_web_contents :
						mega_root = root_web_content.find_element(By.XPATH, "..").find_element(By.XPATH, "..").find_element(By.XPATH, "..").find_element(By.XPATH, "..").find_element(By.XPATH, "..")
						title = mega_root.find_elements(By.XPATH, '*')[0].find_elements(By.XPATH, '*')[0].find_elements(By.XPATH, '*')[0].find_elements(By.XPATH, '*')[0].find_elements(By.XPATH, '*')[0].get_attribute('innerHTML').strip()
						this_title_is_in_planned_plan = False
						for plan in url["plans"] :
							plan_name = plan["plan_name"]
							if re.search(plan_name, title, re.IGNORECASE) :
								this_title_is_in_planned_plan = True
						if not this_title_is_in_planned_plan :
							raise Exception("There exists a new plan name which has not yet been checked.")

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
					elif capture_mode_id == 1 :
						target_class = "//*[@class='package-card-generic']"#"//*[contains(@class, 'card-content') and contains(@class, 'MuiCardContent-root')]"
				elif operator_id == 1 :
					if capture_mode_id == 0 :
						target_class = "//*[@class='lg-item-sim']"
					elif capture_mode_id == 1 :
						target_class = "//*[@class='item-sim']"
				elif operator_id == 2 :
					if capture_mode_id == 0 :
						target_class = "//*[@class='x-1iqxi85']"
					elif capture_mode_id == 1 :
						target_class = "//*[@class='x-1iqxi85']"

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

									first_blocks = root_block.find_elements(By.XPATH, '*')[1].find_elements(By.XPATH, '*')[0].find_elements(By.XPATH, '*')
									price_bloock = first_blocks[2]
									details_block = first_blocks[3]

								elif capture_mode_id == 1 :
									root_block = web_content.find_element(By.XPATH, "..")
									title = root_block.find_elements(By.XPATH, '*')[0].find_elements(By.XPATH, '*')[0].get_attribute('innerHTML').strip()
									if not re.search(plan_name, title, re.IGNORECASE) :
										continue
									real_blocks = web_content.find_elements(By.XPATH, '*')[0].find_elements(By.XPATH, '*')
									top_details = real_block[1]
									bottom_details = real_block[3]
									
							elif operator_id == 2 :
								if capture_mode_id == 0 :
									pass
									"""
									new_row["system"] = pricing_type_id
									mega_root = web_content.find_element(By.XPATH, "..").find_element(By.XPATH, "..").find_element(By.XPATH, "..").find_element(By.XPATH, "..").find_element(By.XPATH, "..").find_element(By.XPATH, "..").find_element(By.XPATH, "..").find_element(By.XPATH, "..")
									title = mega_root.find_elements(By.XPATH, '*')[0].find_elements(By.XPATH, '*')[0].find_elements(By.XPATH, '*')[0].find_elements(By.XPATH, '*')[0].get_attribute('innerHTML').strip()
									if not re.search(plan_name, title, re.IGNORECASE) :
										continue
									price_block = web_content.find_elements(By.XPATH, '*')[0]
									basic_info_block_infos = web_content.find_elements(By.XPATH, '*')[1].find_elements(By.XPATH, '*')
									wifi_content = web_content.find_elements(By.XPATH, '*')[3].find_elements(By.XPATH, '*')[1].get_attribute('innerHTML').strip()
									g_block = web_content.find_elements(By.XPATH, '*')[4]
									misc_blocks = web_content.find_elements(By.XPATH, '*')[5].find_elements(By.XPATH, '*')[1].find_elements(By.XPATH, '*')

									new_row["price"] = numberCheckLambda(price_block.find_elements(By.XPATH, '*')[0].find_elements(By.XPATH, '*')[0].get_attribute('innerHTML').strip())

									for basic_info_block in basic_info_block_infos :
										top_sub_block_content = basic_info_block.find_elements(By.XPATH, '*')[0].get_attribute('innerHTML').strip()
										bottom_sub_block_divs = basic_info_block.find_elements(By.XPATH, '*')[1].find_elements(By.XPATH, '*')
										if "เน็ต" in top_sub_block_content :
											if re.search('true-3g', top_sub_block_content, re.IGNORECASE) :
												if new_row["g_no"] == None :
													new_row["g_no"] = "3G"
												elif not "3G" in new_row["g_no"] :
													new_row["g_no"] += "/3G"
											if re.search('true-4g', top_sub_block_content, re.IGNORECASE) :
												if new_row["g_no"] == None :
													new_row["g_no"] = "4G"
												elif not "4G" in new_row["g_no"] :
													new_row["g_no"] += "/4G"
											if re.search('true-5g', top_sub_block_content, re.IGNORECASE) :
												if new_row["g_no"] == None :
													new_row["g_no"] = "5G"
												elif not "5G" in new_row["g_no"] :
													new_row["g_no"] += "/5G"
											unit = bottom_sub_block_divs[1].get_attribute('innerHTML').strip()
											if checkIsInfiniteText(unit):
												new_row["internet_gbs"] = INFINITY
											else :
												value_num = numberCheckLambda(bottom_sub_block_divs[0].get_attribute('innerHTML').strip())
												if 'GB' in unit and not ('Gbps' in unit) :
													new_row["internet_gbs"] = value_num
												elif 'MB' in unit and not ('Mbps' in unit) :
													new_row["internet_gbs"] = value_num/1000.0
												elif 'TB' in unit and not ('Tbps' in list_item_infos_body) :
													new_row["internet_gbs"] = value_num*1000.0

										elif "โทร" in top_sub_block_content :
											unit = bottom_sub_block_divs[1].get_attribute('innerHTML').strip()
											if checkIsInfiniteText(unit):
												new_row["call_minutes"] = INFINITY
												new_row["unlimited_call"] = True
											else :
												value_num = numberCheckLambda(bottom_sub_block_divs[0].get_attribute('innerHTML').strip())
												new_row["call_minutes"] = value_num

									if re.search('wifi', wifi_content, re.IGNORECASE) :
										new_row["wifi"] = True

									for misc_block in misc_blocks :
										for sub_misc_block in misc_block.find_elements(By.XPATH, '*') :
											if "<img" in sub_misc_block.get_attribute('innerHTML').strip() :
												continue
											misc_block_raw_text = sub_misc_block.get_attribute('innerHTML').strip()
											insertRowInfoForTrueCards(new_row, capture_mode_id, misc_block_raw_text)
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

		result = json.dumps(list_of_rows)
		#print(result)
		return list_of_rows

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

expected_result = scrape_web(mock_request, normalize_result=True)
for result in expected_result :
	print(result)