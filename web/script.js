let input__keyword = document.getElementById("input__keyword")
//let input__url = document.getElementById("input__url")
//let input__csv_file = document.getElementById("input__csv_file")
//let input__mode = document.getElementById("input__mode")
let button__scrape = document.getElementById("button__scrape")

function CSV(array, delimeter=";") {
    // Use first element to choose the keys and the order
    let keys = Object.keys(array[0]);
    console.log(keys)
    // Build header
    let result = keys.join(delimeter) + "\n";

    // Add the rows
    array.forEach(function(obj){
        result += keys.map(k => obj[k]).join(delimeter) + "\n";
    });

    return result;
}

button__scrape.onclick = function() {
	//console.log(input__keyword.value)

	let urls = []

	let url_obj = {
		url_link: "", //str
		operator_id: 0, //enum, ais = 0, dtac = 1, true = 2
		pricing_type: 1,
		plans: [], // plan_obj[]
	}

	let plan_obj = {
		plan_name: "", //str
		capture_mode: 0, //enum, 0 = card, 1 = ul list, 2, numerical capture
		has_term_and_condition: false, //bool
	}

	let planned_inputs = [
		//AIS TEST ZONE
		/*
		{
			url_link: "https://www.ais.th/consumers/package/exclusive-plan/5g-max-professionals", //str
			operator_id: 0, //enum, ais = 0, dtac = 1, true = 2
			pricing_type: 1,
			plans: [
				{
					plan_name: "5G Max Professionals​", //str
					capture_mode: 0, //enum, 0 = card, 1 = ul list, 2, numerical capture
					has_term_and_condition: false, //bool
				},
			], // plan_obj[]
		},
		{
			url_link: "https://www.ais.th/consumers/package/exclusive-plan/5g-max-experience", //str
			operator_id: 0, //enum, ais = 0, dtac = 1, true = 2
			pricing_type: 1,
			plans: [
				{
					plan_name: "AIS 5G Max Experience", //str
					capture_mode: 0, //enum, 0 = card, 1 = ul list, 2, numerical capture
					has_term_and_condition: false, //bool
				},
			], // plan_obj[]
		},
		{
			url_link: "https://www.ais.th/consumers/package/postpaid/postpaid-plans", //str
			operator_id: 0, //enum, ais = 0, dtac = 1, true = 2
			pricing_type: 1,
			plans: [
				{
					plan_name: "แพ็กเกจมหามงคล", //str
					capture_mode: 1, //enum, 0 = card, 1 = ul list, 2, numerical capture
					has_term_and_condition: false, //bool
				},
				{
					plan_name: "5G Serenade", //str
					capture_mode: 1, //enum, 0 = card, 1 = ul list, 2, numerical capture
					has_term_and_condition: false, //bool
				},
				{
					plan_name: "Online MAX", //str
					capture_mode: 1, //enum, 0 = card, 1 = ul list, 2, numerical capture
					has_term_and_condition: false, //bool
				},
				{
					plan_name: "Other", //str
					capture_mode: 1, //enum, 0 = card, 1 = ul list, 2, numerical capture
					has_term_and_condition: false, //bool
				},
			], // plan_obj[]
		},
		{
			url_link: "https://www.ais.th/consumers/package/exclusive-plan/5g-netflix", //str
			operator_id: 0, //enum, ais = 0, dtac = 1, true = 2
			pricing_type: 1,
			plans: [
				{
					plan_name: "แพ็กเกจ 5G Netflix", //str
					capture_mode: 0, //enum, 0 = card, 1 = ul list, 2, numerical capture
					has_term_and_condition: false, //bool
				},
			], // plan_obj[]
		},
		{
			url_link: "https://www.ais.th/consumers/package/exclusive-plan/5g-smart-share", //str
			operator_id: 0, //enum, ais = 0, dtac = 1, true = 2
			pricing_type: 1,
			plans: [
				{
					plan_name: "แพ็กเกจ 5G SMART SHARE", //str
					capture_mode: 0, //enum, 0 = card, 1 = ul list, 2, numerical capture
					has_term_and_condition: false, //bool
				},
			], // plan_obj[]
		},
		{
			url_link: "https://www.ais.th/consumers/package/exclusive-plan/zeed-5g/5g-postpaid", //str
			operator_id: 0, //enum, ais = 0, dtac = 1, true = 2
			pricing_type: 1,
			plans: [
				{
					plan_name: "แพ็กเกจ AIS ZEED 5G รายเดือน", //str
					capture_mode: 0, //enum, 0 = card, 1 = ul list, 2, numerical capture
					has_term_and_condition: false, //bool
				},
			], // plan_obj[]
		},
		*/
		//DTAC TEST ZONE
		
		{
			url_link: "https://www.dtac.co.th/postpaid/products/package.html", //str
			operator_id: 1, //enum, ais = 0, dtac = 1, true = 2
			pricing_type: 1,
			plans: [
				{
					plan_name: "dtac 5G Better+", //str
					capture_mode: 0, //enum, 0 = card, 1 = ul list, 2, numerical capture
					has_term_and_condition: false, //bool
				},
			], // plan_obj[]
		},
		{
			url_link: "https://www.dtac.co.th/dtac-go-plus", //str
			operator_id: 1, //enum, ais = 0, dtac = 1, true = 2
			pricing_type: 1,
			plans: [
				{
					plan_name: "dtac GO+", //str
					capture_mode: 0, //enum, 0 = card, 1 = ul list, 2, numerical capture
					has_term_and_condition: false, //bool
				},
			], // plan_obj[]
		},
		{
			url_link: "https://www.dtac.co.th/postpaid/products/net.html", //str
			operator_id: 1, //enum, ais = 0, dtac = 1, true = 2
			pricing_type: 1,
			plans: [
				{
					plan_name: "Tablet Net Non-Stop", //str
					capture_mode: 1, //enum, 0 = card, 1 = ul list, 2, numerical capture
					has_term_and_condition: true, //bool
				},
				{
					plan_name: "SMP Entry 240", //str
					capture_mode: 2, //enum, 0 = card, 1 = ul list, 2, numerical capture
					has_term_and_condition: false, //bool
				},
			], // plan_obj[]
		},

		/*
		//TRUE TEST ZONE
		{
			url_link: "https://web.archive.org/web/20230322124658/https://www.true.th/truemoveh/postpaid/mass", //str
			operator_id: 2, //enum, ais = 0, dtac = 1, true = 2
			pricing_type: 1,
			plans: [
				{
					plan_name: "5G Together", //str
					capture_mode: 0, //enum, 0 = card, 1 = ul list, 2, numerical capture
					has_term_and_condition: false, //bool
				},
				{
					plan_name: "5G Net Ultra Max Speed", //str
					capture_mode: 0, //enum, 0 = card, 1 = ul list, 2, numerical capture
					has_term_and_condition: false, //bool
				},
			], // plan_obj[]
		},*/

	]

	let query = {
		price_keywords: ["บาท", ".-", "Baht", "THB", "฿"],
		urls: planned_inputs,
		webdriver_timeout: 5,
	}
	//'?&keyword='+input__keyword.value+'&input_url='+input__url.value+'&file_output_name='+input__csv_file.value+'&mode='+input__mode.value

	fetch('scrape_web',{
		  method: "POST",
		  headers: {
		      "Content-Type": "application/json",
		      // 'Content-Type': 'application/x-www-form-urlencoded',
		    },
		  body: JSON.stringify(query)
		})
   .then(response => response.json())
   .then(json => {
   	console.log(json.result)

   	let csvContent = CSV(json.result, ";")
   	console.log(csvContent)

   	//let encodedUri = encodeURI(csvContent);
   	//console.log(encodedUri)
   	//window.open(encodedUri, '_blank')
	//let link = document.getElementById("stealth_downloader");
	//link.setAttribute("href", encodedUri);
	//link.setAttribute("download", "my_data.csv");
	//document.body.appendChild(link); // Required for FF

	//link.click();
   }).catch(e => {
   	console.error(e)
   })
}