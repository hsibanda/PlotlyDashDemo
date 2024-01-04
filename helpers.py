def flattern_list(input_list):
	output = [item.strip() if isinstance(item, str) else item for sublist in input_list for item in sublist]

	return output
