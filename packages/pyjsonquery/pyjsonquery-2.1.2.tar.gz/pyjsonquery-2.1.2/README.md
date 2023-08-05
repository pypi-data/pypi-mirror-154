# PyJsonQuery *(pyjsonq)*

PyJsonQ is an easy to use and package to query json data.
It is a rewrite of the Go package "GoJSONQ" which you can find here:
[GoJSONQ Github Repository][gojsonq]

I decided to rewrite this package in Python because I love it's
simple API and is just a beauty to work with.

## Future

Over time I will potentially update this package and add more fun and
useful stuff to it, but for now the only thing I added are two
operators for the `Where` method: `holds`, `notHolds`

## Installation

```bash
pip install pyjsonquery
```

## Usage

First import the `JsonQuery` class into your project

```python
from pyjsonq import JsonQuery
``` 

Next create a new JsonQuery instance and load the data into the query
using either **File / file**, **String / string**,
**TOMLFile / toml_file**, **TOMLString / toml_string** or
**Raw / raw**.

```python
jq: JsonQuery = JsonQuery().String(
  """
  {
    "city": "dhaka",
    "type": "weekly",
    "temperatures": [
      30,
      39.9,
      35.4,
      33.5,
      31.6,
      33.2,
      30.7
    ]
  }
  """
)

# OR

jq: JsonQuery = JsonQuery().File("./file.json")
```

Once you created your query object you can then query over it using
a variety of methods. Here is a quick example:

```python
avg_temp: float = jq.At("temperatures").Avg()
print(avg_temp)  # 33.471428571428575

city_name: str = jq.Find("city")
print(city_name)  # dhaka
```

You can query over the json using various methods such as
[**Find**][find],
[**First**][first],
[**Nth**][nth],
[**Pluck**][pluck],
[**Where**][where],
[**OrWhere**][orWhere],
[**WhereIn**][whereIn],
[**Sort**][sort],
[**SortBy**][sortBy],
[**Drop**][drop],
etc.

You can also aggregate your data after a query using
[**Avg**][avg],
[**Count**][count],
[**Max**][max],
[**Min**][min],
etc.

An overview over all query functions can be found in the
[wiki page][wiki]


[gojsonq]: https://github.com/thedevsaddam/gojsonq
[wiki]: wiki

[find]: find
[first]: first
[nth]: nth
[pluck]: pluck
[where]: where
[orWhere]: orWhere
[whereIn]: whereIn
[sort]: sort
[sortBy]: sortBy
[drop]: drop

[avg]: avg
[count]: count
[max]: max
[min]: min
