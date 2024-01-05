import rowspan_handler

test_rows = [
	[
		{
			"value": "399",
			"row_span": 1
		},
		{
			"value": "20 GB",
			"row_span": 1
		},
		{
			"value": "100 นาที",
			"row_span": 1
		},
		{
			"value": "ไม่จำกัด",
			"row_span": 20
		},
		{
			"value": "ความคุ้มครองสูงสุด 220,000 บ.",
			"row_span": 2
		},
		{
			"value": "รับชมความบันเทิงซีรีย์ดัง",
			"row_span": 1
		},
		{
			"value": "Welcome Member",
			"row_span": 2
		}
	],
	[
		{
			"value": "499",
			"row_span": 1
		},
		{
			"value": "40 GB",
			"row_span": 1
		},
		{
			"value": "250 นาที",
			"row_span": 1
		},
		{
			"value": "ดูฟรี 3 แอปดัง + รับชมความบันเทิงซีรีย์ดัง",
			"row_span": 4
		}
	],
	[
		{
			"value": "599",
			"row_span": 1
		},
		{
			"value": "50 GB",
			"row_span": 1
		},
		{
			"value": "250 นาที",
			"row_span": 1
		},
		{
			"value": "ความคุ้มครองสูงสุด 320,000 บ.",
			"row_span": 8
		},
		{
			"value": "Silver Member",
			"row_span": 3
		}
	],
	[
		{
			"value": "699",
			"row_span": 1
		},
		{
			"value": "60 GB",
			"row_span": 1
		},
		{
			"value": "300 นาที",
			"row_span": 1
		}
	],
	[
		{
			"value": "899",
			"row_span": 1
		},
		{
			"value": "80 GB",
			"row_span": 1
		},
		{
			"value": "300 นาที",
			"row_span": 1
		}
	],
	[
		{
			"value": "1199",
			"row_span": 1
		},
		{
			"value": "ไม่จำกัด",
			"row_span": 5
		},
		{
			"value": "350 นาที",
			"row_span": 1
		},
		{
			"value": "รับชมบอลพรีเมียร์ลีก + ดูฟรี 3 แอปดัง + รับชมความบันเทิงซีรีย์ดัง",
			"row_span": 5
		},
		{
			"value": "Gold Member",
			"row_span": 2
		}
	],
	[
		{
			"value": "1499",
			"row_span": 1
		},
		{
			"value": "650 นาที",
			"row_span": 1
		}
	],
	[
		{
			"value": "1699",
			"row_span": 1
		},
		{
			"value": "1000 นาที",
			"row_span": 1
		},
		{
			"value": "Platinum Member",
			"row_span": 3
		}
	],
	[
		{
			"value": "1999",
			"row_span": 1
		},
		{
			"value": "1300 นาที",
			"row_span": 1
		}
	],
	[
		{
			"value": "2199",
			"row_span": 1
		},
		{
			"value": "1700 นาที",
			"row_span": 1
		}
	]
]

final_rows = rowspan_handler.rowspan_handle(test_rows)

for row_values in final_rows :
	print(row_values)
