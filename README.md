## Utility from parsing Chinese holiday from official website

[Chinese 中文](README_CN.md)

#### Install
pip install Chinese-holiday

#### Usage
> Check if one day is a holiday (including normal weekend, not including working weekend)

```is_holiday('2019-10-10')```

> Search url for notice of 2020 holiday

```search_notice_url（'2020')```

> Parse holiday info from url

```parse_holiday_info(url)```

> Return holiday data from cache

```get_holiday_data('2020')```

> Forcely return holiday data from website

```get_holiday_data('2020', True)```

> Get latest work day (default fome today)

```get_latest_workday()```

#### Cache
The utility will cache parsed result into holiday.json, you can use 
```is_holiday('2019-10-10', True)``` to forcely refresh it.