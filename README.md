## Utility from parsing Chinese holiday from official website

[Chinese 中文](README_CN.md)

#### Install
pip install Chinese-holiday

#### Usage
```is_holiday('2019-10-10')    # Check if one day is a holiday (including normal weekend, not including working weekend)```

```search_notice_url（'2020')		# Search url for notice of 2020 holiday```

```parse_holiday_info(url)			# Parse holiday info from url```

```get_holiday_data('2020')    # Return holiday data from cache```

```get_holiday_data('2020', True)    # Forcely return holiday data from website```

#### Cache
The utility will cache parsed result into holiday.json, you can use 
```is_holiday('2019-10-10', True)``` to forcely refresh it.