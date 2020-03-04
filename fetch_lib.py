import json

def return_method_tonghuashun(html_text):
    ind_ = html_text.index('(')
    ind_2 = len(html_text) - html_text[::-1].index(')')
    html_json = json.loads(html_text[ind_+1:ind_2-1])
    return float(html_json['items']['24'])

def fetch_agent_tonghuashun(stocknum):
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Host': 'd.10jqka.com.cn',
        'Referer': 'http://stockpage.10jqka.com.cn/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'
    }
    return f'http://d.10jqka.com.cn/v2/fiverange/hs_{stocknum}/last.js' , {'headers':headers} ,return_method_tonghuashun

def return_method_yahoo(html_text):
    html_json = json.loads(html_text)
    return float(html_json['chart']['result'][0]['meta']['regularMarketPrice'])

def fetch_agent_yahoo(stocknum):
    
    return f"https://query1.finance.yahoo.com/v8/finance/chart/{stocknum}.{'SS' if int(stocknum) >= 600000 else 'SZ'}?region=HK&lang=en-US&includePrePost=false&interval=2m&range=1d&corsDomain=finance.yahoo.com&.tsrc=finance" , {} , return_method_yahoo
