import os
import webbrowser
from typing import Union
from pandas.core.frame import DataFrame, Series
import regex
import pandas as pd
from tempfile import TemporaryDirectory
from a_pandas_ex_plode_tool import unstacked_df_back_to_multiindex, _unstack_df
from a_pandas_ex_df_to_string import ds_to_string

_tmp_dict_pd = TemporaryDirectory()


def series_to_dataframe(
    df: Union[pd.Series, pd.DataFrame]
) -> (Union[pd.Series, pd.DataFrame], bool):
    dataf = df.copy()
    isseries = False
    if isinstance(dataf, pd.Series):
        columnname = dataf.name
        dataf = dataf.to_frame()

        try:
            dataf.columns = [columnname]
        except Exception:
            dataf.index = [columnname]
            dataf = dataf.T
        isseries = True

    return dataf, isseries


def create_html_table_from_iterable(
    dframe: Union[pd.Series, pd.DataFrame],
    file_path: Union[None, str] = None,
    title: str = "Pandas DataFrame",
    sparsify: bool = True,
    returndf: bool = False,
):
    r"""
    Convert any nested iterable to an HTML table. Design is separated from data. You can use the preset, but if you want,
    you can easily create your own CSS style.



        Parameters:
            dframe: Union[pd.Series,pd.DataFrame]
                You can pass any iterable (list, dict, tuple …), json file path (str) or json URL (str)
            file_path: Union[None,str]
                File path for output, will be saved in your current working directory
                If None, no files will be written.
            title: str
                Title  for HTML
                (default =  'Pandas DataFrame')
            sparsify: bool
                Repeat/not repeat keys in every line
                (default = True)
            returndf:bool
                return input df
                for chaining
                (default = False)

        Returns:
            None or input DataFrame (for chaining)

    """

    html_string = f"""
    <html>
      <head><title>{title}</title></head>
      <link rel="stylesheet" type="text/css" href="df_style.css"/>
      <body>
        {{table}}
      </body>
    </html>.
    """
    styledatei = r"""
    body {
        color: #333;
        font: 140%/80px 'Helvetica Neue', helvetica, arial, sans-serif;
        text-shadow: 0 1px 0 #fff;
    }
    
    strong {
        font-weight: bold; 
    }
    
    em {
        font-style: italic; 
    }
    
    table {
        background: #f0f0f5;
        border-collapse: separate;
        box-shadow: inset 3 4px 3 #fff;
        font-size: 16px;
        line-height: 24px;
        margin: 30px auto;
        text-align: left;
        table-layout: fixed;
    }	
    
    
    
    th {
        background: linear-gradient(#777, #444);
        border-left: 0px solid #555;
        border-right: 0px solid #777;
        border-top: 0px solid #555;
        border-bottom: 0px solid #333;
        box-shadow: inset 0 1px 0 #999;
        color: #fff;
      font-weight: bold;
        padding: 10px 15px;
        position: relative;
        text-shadow: 0 1px 0 #000;	
    }
    
    th:after {
        background: linear-gradient(rgba(255,255,255,0), rgba(255,255,255,.08));
        content: '';
        display: block;
        height: 75%;
        left:10;
        margin: 0px 0 0 0;
        position: absolute;
        top: 55%;
        width: 100%;
    }
    
    th:nth-child(even) {
        border-left: 1px solid #111;	
        box-shadow: inset 2px 2px 0 #999;
            background: linear-gradient(rgba(0,0,20,.7), rgba(0,140,140,.99));
    
    }
    
    th:nth-child(odd) {
        border-left: 1px solid #111;	
        box-shadow: inset 2px 2px 0 #999;
            background: linear-gradient(rgba(0,0,70,.7), rgba(0,100,100,.99));
    
    }
    
    td {
        border-right: 1px solid #fff;
        border-left: 1px solid #e8e8e8;
        border-top: 1px solid #fff;
        border-bottom: 1px solid #e8e8e8;
        padding: 10px 15px;
        position: relative;
    }

    
    tr {
        background: linear-gradient(rgba(0,100,100,.7), rgba(0,255,255,.99));
    }
    
    tr:nth-child(odd) td {
        background: #f1f1f1;	
            font-size: 18px;
    }
    tr:nth-child(even) td {
        background: #a1f1f1;	
            font-size: 18px;
    
    }
    td:empty {background: green;}
    
    th:empty {
        background: #a1f1f1;	
            border-left: 0px solid #555;
        border-right: 0px solid #777;
        border-top: 0px solid #555;
        border-bottom: 0px solid #333;
        box-shadow: inset 0 0px 0 #999;
    
        }    
    tr:empty {background: green;}
    """

    filename = file_path
    pd.set_option("colheader_justify", "center")
    df, isseries = series_to_dataframe(dframe)

    df = _unstack_df(df)

    df = ds_to_string(df)

    for col in df.columns:
        df[col] = df[col].str.replace("<NA>", "", regex=False)

    if "aa_value" in df.columns:
        df = unstacked_df_back_to_multiindex(df)
        htm = html_string.format(
            table=df.drop(columns="aa_all_keys")
            .rename(columns={"aa_value": "values"})
            .to_html(classes="mystyle", sparsify=sparsify, justify="match-parent")
        )

    else:
        htm = html_string.format(
            table=df.fillna("").to_html(
                classes="mystyle", sparsify=sparsify, justify="match-parent"
            )
        )
    htm = regex.sub(r"(<th[^>]*>\d+)\.0+(</th>)", r"\g<1>\g<2>", htm)

    if filename is not None:
        dict_to_save = regex.sub(r"(^.*?[\\/])[^\\/]+(\.html?)?$", r"\g<1>", filename)
        purefile = filename.replace(dict_to_save, "")
        purefile = regex.sub(r"\.html?$", "", purefile)
        purefile += ".html"
        filepath = os.path.join(dict_to_save, purefile)
        styfile = os.path.join(dict_to_save, "df_style.css")
        if not os.path.exists(dict_to_save):
            os.makedirs(dict_to_save)

    else:
        filepath = os.path.join(_tmp_dict_pd.name, "tmpdf.html")
        styfile = os.path.join(_tmp_dict_pd.name, "df_style.css")

    with open(styfile, "w", encoding="utf-8") as f:
        f.write(styledatei)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(htm)

    if filename is None:
        webbrowser.open(os.path.join(_tmp_dict_pd.name, "tmpdf.html"))
    if returndf:
        return dframe


def pd_add_html_view():
    DataFrame.ds_html_view = create_html_table_from_iterable
    Series.ds_html_view = create_html_table_from_iterable


# from a_nested_dict_to_pdthtml import pd_add_html_view
# pd_add_html_view()
# df = pd.read_csv("https://github.com/pandas-dev/pandas/raw/main/doc/data/titanic.csv")
# pd_add_html_view()
# df.ds_html_view()
