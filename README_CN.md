## 从国务院网站解析节假日信息的小工具

#### 安装
pip install Chinese-holiday

#### 使用
> 判断某一天是否为节假日（含周末与法定节假日，不含规定上班的日期）

```is_holiday('2019-10-10')```

> 查找发布2020节假日公告的网址

```search_notice_url（'2020')```

> 从url的页面中解析出节假日信息（与search_notice_url配合使用）

```parse_holiday_info(url)```

> 返回缓存文件中的假日信息

```get_holiday_data('2020')```

> 强制重新解析并返回假日信息

```get_holiday_data('2020', True)```

#### 缓存
工具会默认将解析的结果保存在holiday.json文件中，避免重复解析，可以使用
```is_holiday('2019-10-10', True)```来强制解析