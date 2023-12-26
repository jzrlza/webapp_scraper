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
			"row_span": 3
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

final_rows = []
column_rowspan_states = {}
column_rowspan_value_states = {}
column_rowspan_bool_is_span_states = {}

for row_id in range(len(test_rows)) :
	columns = test_rows[row_id]
	values = []
	max_columns = 9999
	if row_id == 0 :
		max_columns = len(columns)
	column_id = 0
	id_offset = 0
	while column_id+id_offset < max_columns :
		if column_id < len(columns) :
			value_item = columns[column_id]
		else :
			print(column_id, id_offset, column_id+id_offset)
			if column_rowspan_states[column_id+id_offset] > 1 :
				print("leftover")
				values.append(column_rowspan_value_states[column_id+id_offset])
				column_rowspan_states[column_id+id_offset] -= 1
			id_offset = 0
			break
		if row_id == 0 :
			print(column_id, id_offset, column_id+id_offset)
			column_rowspan_states[column_id] = value_item['row_span']
			column_rowspan_value_states[column_id] = value_item["value"]
			if value_item['row_span'] > 1 :
				column_rowspan_bool_is_span_states[column_id] = True
			else :
				column_rowspan_bool_is_span_states[column_id] = False
			values.append(value_item["value"])
		else :
			#things get real
			searching_offset = True
			while searching_offset :
				print(column_id, id_offset, column_id+id_offset)
				if column_rowspan_states[column_id+id_offset] > 1 :
					print("offsetting")
					values.append(column_rowspan_value_states[column_id+id_offset])
					column_rowspan_states[column_id+id_offset] -= 1
					if column_id+id_offset < max_columns-1 :
						id_offset += 1
					else :
						searching_offset = False
						break
				else :
					print("lock on")
					column_rowspan_states[column_id+id_offset] = value_item['row_span']
					column_rowspan_value_states[column_id+id_offset] = value_item["value"]
					
					if column_rowspan_bool_is_span_states[column_id+id_offset] :
						values.append(column_rowspan_value_states[column_id+id_offset])
						if column_rowspan_states[column_id+id_offset] <= 1 :
							column_rowspan_bool_is_span_states[column_id+id_offset] = False
					else :
						values.append(value_item["value"])

					if value_item['row_span'] > 1 :
						column_rowspan_bool_is_span_states[column_id+id_offset] = True
					else :
						column_rowspan_bool_is_span_states[column_id+id_offset] = False
					
					searching_offset = False
					break
		column_id += 1

	print(column_rowspan_states)
	print(column_rowspan_value_states)
	print(column_rowspan_bool_is_span_states)
	print(values)
	print("----")
	final_rows.append(values)

for row_values in final_rows :
	print(row_values)