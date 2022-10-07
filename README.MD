### DataFrame / Series in your browser

```python
#Based on pypi.org/project/any-iter-to-html-table/
from a_pandas_ex_html_view import pd_add_html_view
import pandas as pd
pd_add_html_view() #this adds to new methods to pandas
df = pd.read_csv("https://github.com/pandas-dev/pandas/raw/main/doc/data/titanic.csv")
df.ds_html_view() #for whole DataFrame
df.Name.ds_html_view() #for Series
```

![](https://github.com/hansalemaos/screenshots/raw/main/screenshotpandastable.png)

![](https://github.com/hansalemaos/screenshots/raw/main/screenshotpandasseries.png)

### For DataFrames with MultiIndex

If you create your MultiIndexed DataFrame using [a-pandas-ex-plode-tool · PyPI](https://pypi.org/project/a-pandas-ex-plode-tool/)

a_pandas_ex_html_view will format the DataFrame in the prettiest way possible :)

![](https://github.com/hansalemaos/screenshots/raw/main/pandsnesteddicthtml.png)

```python
from a_pandas_ex_plode_tool import pd_add_explode_tools
pd_add_explode_tools()
data = {
    "glossary": {
        "title": "example glossary",
        "GlossDiv": {
            "title": "S",
            "GlossList": {
                "GlossEntry": {
                    "ID": "SGML",
                    "SortAs": "SGML",
                    "GlossTerm": "Standard Generalized Markup Language",
                    "Acronym": "SGML",
                    "Abbrev": "ISO 8879:1986",
                    "GlossDef": {
                        "para": "A meta-markup language, used to create markup languages such as DocBook.",
                        "GlossSeeAlso": ["GML", "XML"],
                    },
                    "GlossSee": "markup",
                }
            },
        },
    }
}
df = pd.Q_AnyNestedIterable_2df(data)
df.ds_html_view()   
#if you don't want to open it in browser, just save it to your HDD:
df.ds_html_view('f:\\testhtml.html') 
```
