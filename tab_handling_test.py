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
   "urls":[
      {
         "url_link":"https://www.ais.th/consumers/package/postpaid/postpaid-plans",
         "operator_id":0,
         "pricing_type":1,
         "track_new_mega_row": false,
         "plans":[
            {
               "plan_name":"แพ็กเกจมหามงคล",
               "capture_mode":1,
               "has_extra_table":false,
               "has_term_and_condition":false
            },
            {
               "plan_name":"5G Serenade",
               "capture_mode":1,
               "has_extra_table":false,
               "has_term_and_condition":false
            },
            {
               "plan_name":"Online MAX",
               "capture_mode":1,
               "has_extra_table":false,
               "has_term_and_condition":false
            },
            {
               "plan_name":"Other",
               "capture_mode":1,
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

possible_fup_units = ['Gbps', 'Mbps', 'kbps']

#AIS --------------
def insertRowInfoForAISCards(new_row, capture_mode_id, list_item_icon_img, list_item_infos_head, list_item_infos_body, list_item_infos_footer = "") : #void function
	is_extra = True

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

	#WiFi boolean zone
	if re.search('WiFi', list_item_infos_head, re.IGNORECASE) :
		new_row["wifi"] = True

	#internet GB zone
	if ("เน็ต" in list_item_infos_head or re.search('internet', list_item_infos_head, re.IGNORECASE) or checkIsLikelyGSystemIcon(list_item_icon_img)) and new_row["internet_gbs"] == 0.0 :
		if checkIsInfiniteText(list_item_infos_body):
			new_row["internet_gbs"] = INFINITY
		elif 'GB' in list_item_infos_body and not ('Gbps' in list_item_infos_body) :
			new_row["internet_gbs"] = getNumberByUnit("GB", list_item_infos_body, 'Gbps')
		elif 'MB' in list_item_infos_body and not ('Mbps' in list_item_infos_body) :
			new_row["internet_gbs"] = getNumberByUnit("MB", list_item_infos_body, 'Mbps')/1000.0
		elif 'TB' in list_item_infos_body and not ('Tbps' in list_item_infos_body) :
			new_row["internet_gbs"] = getNumberByUnit("TB", list_item_infos_body, 'Tbps')*1000.0
		is_extra = False

	#call in minutes time zone
	if re.search('free-calls', list_item_icon_img, re.IGNORECASE) :
		#print("CALL TIME : "+list_item_infos_body)
		if checkIsInfiniteText(list_item_infos_body):
			new_row["call_minutes"] = INFINITY
			new_row["unlimited_call"] = True
		else :
			if "(นาที)" in list_item_infos_head :
				new_row["call_minutes"] = float(list_item_infos_body.replace('<b>', '').replace('</b>', '')) #predefined unit in header, here should be pure number
			else :
				new_row["call_minutes"] = getNumberByUnit("นาที", list_item_infos_body, 'ชม')
		is_extra = False

	#fair usage policy zone
	for fup_unit in possible_fup_units :
		target_str = ""
		if fup_unit in normalizeStringForNoneTypeToString(list_item_infos_footer) :
			target_str = list_item_infos_footer
		elif fup_unit in normalizeStringForNoneTypeToString(list_item_infos_body) :
			target_str = list_item_infos_body

		if target_str != "" :
			new_row["fair_usage_policy"] = getNumberByUnitAsUnittedString(fup_unit, target_str, "GB")
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
		new_row["entertainment_contract"] = getNumberByUnit("เดือน", list_item_infos_body)
		is_extra = False
	for i in range(len(entertainments)) :
		new_row["entertainment_package"] += entertainments[i].replace(comma_detection, comma_replacer)
		if i < len(entertainments) - 1 :
			new_row["entertainment_package"] += micro_delimeter

	#prilivedge zone
	if "เซเรเนด" in list_item_infos_head or re.search('Serenade', list_item_infos_head, re.IGNORECASE) :
		if list_item_infos_body != "-" :
			new_row["priviledge"] = True
			new_row["priviledge_exclusive"] = list_item_infos_body
		is_extra = False

	#extra zone
	if is_extra :
		trim_txt = list_item_infos_head.replace('<b>', '').replace('</b>', '')+" "+list_item_infos_body.replace('<b>', '').replace('</b>', '')
		if new_row["extra"] == None :
			new_row["extra"] = trim_txt.replace(comma_detection, comma_replacer)
		else :
			new_row["extra"] += micro_delimeter+trim_txt.replace(comma_detection, comma_replacer)

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
	"package": "",
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

OperatorUnsupportedException = Exception("Unsupported Operator.")
UntrackableException = Exception("Untrackable Page")
CaptureModeException = Exception("No such capture mode.")

def scrape_web(request, normalize_result = False):
	try :
		qr = json.loads(request)
		price_keywords = qr['price_keywords']
		urls = qr['urls']
		webdriver_timeout = qr['webdriver_timeout']

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
				if operator_id == 2 :
					mega_class_target = "//*[@class='x-dlrg8z']"

					root_web_contents = driver.find_elements(By.XPATH, f"{mega_class_target}")
					for root_web_content in root_web_contents :
						mega_root = root_web_content.find_element(By.XPATH, "..").find_element(By.XPATH, "..").find_element(By.XPATH, "..")
						title = mega_root.find_elements(By.XPATH, '*')[0].find_elements(By.XPATH, '*')[0].find_elements(By.XPATH, '*')[0].find_elements(By.XPATH, '*')[0].get_attribute('innerHTML').replace('<b>', '').replace('</b>', '').strip()
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
				#title_finder_lambda = lambda title_is_at_header : container_classes[operator] if title_is_at_header == True else operator_card_classes[operator]
				target_class = ""#plan["css_item_class_name"]
				requires_click = False
				target_click_class = ""
				menu_to_click_class = ""
				table_target_class = ""
				table_temp_arr = []
				disabled_mode = False #temp value
				clicked = False
				clickers = []

				#if-else structured like this on purpose for ease of re-readability
				if operator_id == 0 :
					if capture_mode_id == 0 :
						target_class = "//*[@class='package-card-generic']"
					elif capture_mode_id == 1 :
						requires_click = True
						target_click_class = "//*[contains(@class, 'search-tab-btn') and contains(@class, 'MuiTab-textColorPrimary') and contains(@class, 'MuiButtonBase-root')]"
						target_class = "//*[contains(@class, 'card-content') and contains(@class, 'MuiCardContent-root')]"
						need_to_scroll = True
					else :
						raise CaptureModeException
				else :
					raise OperatorUnsupportedException

				#init_web_contents_lambda = lambda title_is_at_header : driver.find_elements(By.CSS_SELECTOR, f".{target_class}")[0].find_elements(By.XPATH, f'./div[contains(@class, "{operator_card_classes[operator]}")]') if title_is_at_header == True else driver.find_elements(By.CSS_SELECTOR, f".{target_class}")
				if not disabled_mode :
					if plan["has_extra_table"] :
						tables = driver.find_elements(By.XPATH, f"{table_target_class}")

						if operator_id == 1 and capture_mode_id == 0 :
							table_body_target = None
							for i in range(len(tables)) :
								if "responsive" in tables[i].find_element(By.XPATH, "..").find_element(By.XPATH, "..").get_attribute('class') :
									table_body_target = tables[i]
									break
							#print(table_body_target.get_attribute('class'))
							hunt_keyword_1 = "คุ้มครอง"
							hunt_keyword_1_field = "ประกันชีวิตและอุบัติเหตุ"
							hunt_keyword_2 = "แอปดัง"
							hunt_keyword_2_field = "ความบันเทิง viu iQIYI WeTV"
							td_array = table_body_target.find_elements(By.XPATH, '*')
							row_span_1 = 0
							row_span_info_1 = ""
							row_span_2 = 0
							row_span_info_2 = ""
							for tr_i in range(len(td_array)) :
								trow = td_array[tr_i]
								trows_tds = trow.find_elements(By.XPATH, '*')
								table_temp_arr_sub_item = {
									"price": 0.0,
									"extra_raw_arr": [],
								}
								trow_price = 0.0
								for td_i in range(len(trows_tds)) :
									td_elem = trows_tds[td_i]
									td_elem_txt = td_elem.get_attribute('innerHTML').strip()
									if td_i == 0 : #price
										if "แนะนำ" in td_elem_txt :
											trow_price = float(td_elem.find_elements(By.XPATH, '*')[1].get_attribute('innerHTML').strip())
										else :
											trow_price = float(td_elem.find_elements(By.XPATH, '*')[0].get_attribute('innerHTML').strip())
										table_temp_arr_sub_item["price"] = trow_price

									elif hunt_keyword_1 in td_elem_txt :
										row_span_1 = td_elem.get_attribute('rowspan')
										if td_elem.get_attribute('rowspan') == None :
											row_span_1 = 1
										else :
											row_span_1 = int(row_span_1)
										#print("fetching info 1... maximum "+str(webdriver_timeout)+" seconds")
										row_span_info_1 = td_elem.find_elements(By.XPATH,"descendant::*[text()[contains(., '"+hunt_keyword_1+"')]]")
										if row_span_info_1 != None :
											if len(row_span_info_1) > 0 :
												row_span_info_1 = row_span_info_1[0].get_attribute('innerHTML').strip().split('<small>')[0].replace('<br>', '')
												table_temp_arr_sub_item["extra_raw_arr"].append(hunt_keyword_1_field+" "+row_span_info_1)
										
									elif hunt_keyword_2 in td_elem_txt :
										row_span_2 = td_elem.get_attribute('rowspan')
										if td_elem.get_attribute('rowspan') == None :
											row_span_2 = 1
										else :
											row_span_2 = int(row_span_2)
										#print("fetching info 2... maximum "+str(webdriver_timeout)+" seconds")
										row_span_info_2 = td_elem.find_elements(By.XPATH,"descendant::*[text()[contains(., '"+hunt_keyword_2+"')]]")
										if row_span_info_2 != None :
											if len(row_span_info_2) > 0 :
												row_span_info_2 = row_span_info_2[0].get_attribute('innerHTML').strip().split('<small>')[0].replace('<br>', '')
												table_temp_arr_sub_item["extra_raw_arr"].append(hunt_keyword_2_field+" "+row_span_info_2)

								if row_span_1 > 0 :
									#print(row_span_info_1)
									table_temp_arr_sub_item["extra_raw_arr"].append(hunt_keyword_1_field+" "+row_span_info_1)
									row_span_1 -= 1
								if row_span_2 > 0 :
									#print(row_span_info_2)
									if row_span_info_2 != None :
										table_temp_arr_sub_item["extra_raw_arr"].append(hunt_keyword_2_field+" "+row_span_info_2)
									row_span_2 -= 1
								table_temp_arr_sub_item["extra_raw_arr"] = list(set(table_temp_arr_sub_item["extra_raw_arr"]))
								table_temp_arr.append(table_temp_arr_sub_item)

						#print(table_temp_arr)	

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

							#new line
							original_window = driver.current_window_handle
							print(original_window)
							
							if operator_id == 0 : #start at "package-card-generic"
								if capture_mode_id == 0 :
									first_block = web_content.find_elements(By.XPATH, '*')[0].find_elements(By.XPATH, '*')[1]
									first_block__package_name = first_block.find_elements(By.XPATH, '*')[0].find_elements(By.XPATH, '*')[0].get_attribute('innerHTML').strip()
									first_block__price = numberCheckLambda(first_block.find_elements(By.XPATH, '*')[1].find_elements(By.XPATH, '*')[0].find_elements(By.XPATH, '*')[0].get_attribute('innerHTML').strip())
									#print(first_block__price)
									if first_block__package_name != "" :
										new_row["package"] = first_block__package_name
									else :
										new_row["package"] = plan_name
									new_row["price"] = first_block__price
									#first_block__system = checkSystemGetEnum(first_block.find_elements(By.XPATH, '*')[1].get_attribute('innerHTML').strip())

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
										#entertainment zone in case it is in footer
									if second_block_has_footer :
										for i in range(len(second_block_raw_list)) :
											target_item = second_block_raw_list[i]
											#print(target_item.get_attribute('class'))
											if i == 0 or "separator" in target_item.get_attribute('class') or "data-speed" in target_item.get_attribute('class') :
												continue
											
											raw_str_item = target_item.find_elements(By.XPATH, '*')[0].get_attribute('innerHTML')
											if re.search('viu', raw_str_item, re.IGNORECASE) :
												new_row["entertainment"] = True
												raw_str_item_title = raw_str_item.strip().split(" ฟรี")[0]
												raw_str_item_duration = getNumberByUnit("เดือน", raw_str_item)
												#print(raw_str_item_title, raw_str_item_duration)
												if new_row["entertainment_package"] == None :
													new_row["entertainment_package"] = raw_str_item_title.replace(comma_detection, comma_replacer)
												else :
													new_row["entertainment_package"] += micro_delimeter+raw_str_item_title.replace(comma_detection, comma_replacer)
												new_row["entertainment_contract"] = raw_str_item_duration

								elif capture_mode_id == 1 :
									first_block = web_content.find_elements(By.XPATH, '*')[1].find_elements(By.XPATH, '*')[0]
									first_block__package_name = first_block.find_elements(By.XPATH, '*')[0].find_elements(By.XPATH, '*')[0].get_attribute('innerHTML').strip()
									first_block__price = numberCheckLambda(first_block.find_elements(By.XPATH, '*')[1].find_elements(By.XPATH, '*')[0].get_attribute('innerHTML').strip())
									if first_block__package_name != "" :
										new_row["package"] = first_block__package_name
									else :
										new_row["package"] = plan_name
									new_row["price"] = first_block__price
									#print(first_block__price)

									second_block_list_items = web_content.find_elements(By.XPATH, '*')[2].find_elements(By.XPATH, '*')
									footer_item = None
									for list_item in second_block_list_items :
										if "line-panel" in list_item.get_attribute('class') :
											footer_item = list_item
											break
										list_item_icon_img = normalizeStringForNoneTypeToString(list_item.find_elements(By.XPATH, '*')[0].get_attribute('src')).strip()
										#print("MODE2 IMAGE: "+str(list_item_icon_img))
										list_item_infos = list_item.find_elements(By.XPATH, '*')[1].find_elements(By.XPATH, '*')
										list_item_infos_head = list_item_infos[0].get_attribute('innerHTML').strip()
										list_item_infos_body = list_item_infos[1].get_attribute('innerHTML').strip()
										#print(list_item_infos_head, list_item_infos_body)
										insertRowInfoForAISCards(new_row, capture_mode_id, list_item_icon_img, list_item_infos_head, list_item_infos_body, None)

									#new tab
									extra_button_block = web_content.find_elements(By.XPATH, '*')[3].find_elements(By.XPATH, '*')[1].find_elements(By.XPATH, '*')[0].find_elements(By.XPATH, '*')[0]
									clickers.append(extra_button_block)
									# Get all attributes of the element
									all_attributes = driver.execute_script(
										"var items = {}; "
										"for (index = 0; index < arguments[0].attributes.length; ++index) "
										"{ items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; "
										"return items;", extra_button_block)

									# Print all attributes
									for key, value in all_attributes.items():
										print(f"{key}: {value}")

							#for clicker in clickers :
							#	clicker.click()

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
		return result

	except Exception as e :
		e_type, e_object, e_traceback = sys.exc_info()

		e_filename = os.path.split(e_traceback.tb_frame.f_code.co_filename)[1]

		e_message = str(e)

		e_line_number = e_traceback.tb_lineno

		return json.dumps([{
				"error": e_message,
				"line_of_error": e_line_number,
				"file_that_errored": e_filename
			}])

print(scrape_web(mock_request, normalize_result=True))