import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.header import Header

import time
from time import localtime ,strftime
from time import time as timetime
import datetime
from aiohttp import web , ClientSession
from jinja2 import PackageLoader,Environment
from sqlwarp import SQLhandler
import asyncio
import os
import pickle
from concurrent.futures import ThreadPoolExecutor
from functools import partial
import json
import random
from aiohttp import web
from aiohttp_basicauth import BasicAuthMiddleware
#######################################
#  SETTINGS
#######################################
DEBUG = False
routes = web.RouteTableDef()
sql = SQLhandler()
thread_pool = ThreadPoolExecutor()
if DEBUG:
    trade_time_utc8 = list(range(24))
else:
    trade_time_utc8 = [9,10,11,13,14,15]
auth_username = 'admin'
auth_password = 'password'
username_email = '60608080@qq.com'
password_email = 'gfdsalkjhgwkbgaj'
fetch_time_internal = 90
min_fetch_internal = 30
run_host = '127.0.0.1'
run_port = 7923
#######################################
#  
#######################################

# init target mail
def set_target_email(address = None):
    target_email = ''
    try:
        assert address == None
        assert os.path.exists('target_email.pickle')
        with open('target_email.pickle','rb') as f:
            target_email = pickle.load(f)
    except:
        if address != None:
            target_email = address
        else:
            target_email = '948566945@qq.com'
        with open('target_email.pickle','wb') as f:
            pickle.dump(target_email , f)
    return target_email

target_email = set_target_email()

# init jinja2 renderer
env_jinja2 = Environment(loader=PackageLoader('jinja2package','templates'))
def render_template(filename , **kwargs):

    def url_for(input ,filename):
        return f"/{input}/{filename}"
    
    template = env_jinja2.get_template(filename)
    kwargs['url_for'] = url_for
    return template.render(**kwargs)

# time module
def get_time_string_east8():
    last_time = strftime("%Y-%m-%d %H:%M:%S", localtime(timetime()))
    last_time = datetime.datetime.strptime(last_time, "%Y-%m-%d %H:%M:%S")
    last_time = last_time.astimezone(datetime.timezone(datetime.timedelta(hours=8)))
    return last_time

last_update_time = str(get_time_string_east8())

# aiohttp part
@routes.get('/')
async def hello(request):
    reslts = sql.show_recent_100('Tasks','taskid')

    ret = '''
    <HR align=center width=2000 color=#987cb9 SIZE=1>
    <table style="font-size:23px" border="1">
    <tr>
    <th>任务ID</th>
    <th>股票代码</th>
    <th>当前价格</th>
    <th>触发门槛</th>
    <th>目标价格</th>
    <th>最后更新时间</th>
    <th>完成状态</th>
    </tr>
''' 
    if reslts == False:
        ret = '<h1>database fetch error.</h1>'
    else:
        for stockitem in reslts:
            ret += f'<tr><td>{stockitem.taskid}</td><td>{stockitem.stocknum}</td><td>{stockitem.currentprice}</td><td>{"高于" if stockitem.incdesc == 0 else "低于"}</td><td>{stockitem.targetprice}</td><td>{stockitem.lastupdatetime}</td><td>{"完成" if stockitem.isover == 1 else "未完成"}</td></tr>'
        else:
            ret += '\n</table>'


    return web.Response(    text = render_template('index.html',full_list = ret),
                            content_type='text/html'
                        )
@routes.get('/add')
async def add(request):

    # async def async_insert_row(*args , **kwargs):
    #     loop = asyncio.get_running_loop()
    #     return await loop.run_in_executor(None, partial(sql.insert_row , *args , **kwargs))

    data = dict(request.rel_url.query)
    if 'stocknumber' in data and 'targetprice' in data and 'optionsvalue' in data:
        pass
    else:
        return web.Response(status=404)

    stocknumber = data['stocknumber']
    targetprice = data['targetprice']
    optionsvalue = data['optionsvalue']
    try:
        assert isinstance(stocknumber ,str)
        assert len(stocknumber) == 6
        assert float(targetprice) > 0
        targetprice = float(targetprice)
        assert int(optionsvalue) in [0,1]
        optionsvalue = int(optionsvalue)
        ret_v = sql.insert_row('Tasks' ,stocknum=stocknumber, targetprice=targetprice ,incdesc=optionsvalue)
        # ret_v = await async_insert_row('Tasks' ,stocknum=stocknumber, targetprice=targetprice ,incdesc=optionsvalue)
        assert ret_v == True
    except Exception as e:
        return web.Response(status=404)

    return web.Response(text = 'true')

@routes.get('/delete')
async def delete(request):

    data = dict(request.rel_url.query)
    if 'taskid' not in data:
        return web.Response(status=404)

    taskid_ = data['taskid']
    try:
        taskid_ = int(taskid_)
        ret_val = sql.query_and_delete('Tasks',SQLhandler.Tasks.taskid == taskid_)
    except Exception as e:
        return web.Response(status=404)

    return web.Response(text = 'true')

@routes.get('/gettargetmail')
async def gettargetmail(request):
    global target_email
    return web.Response(text = target_email)

@routes.get('/settargetmail')
async def settargetmail(request):
    global target_email

    data = dict(request.rel_url.query)

    try:
        assert 'emailaddr' in data
        emailaddr = data['emailaddr']
        assert isinstance(emailaddr , str)
        target_email = set_target_email(emailaddr)
    except Exception as e:
        return web.Response(status=404)
    
    return web.Response(text = 'true')

@routes.get('/lastupdatetime')
async def lastupdatetime(request):
    global last_update_time
    return web.Response(text = last_update_time)

@routes.get('/testmail')
async def testmail(request):
    loop = asyncio.get_running_loop()
    retv = await loop.run_in_executor(None, partial(send_mail_alert , 'testing' ,0,0,0, 0))
    if retv:
        return web.Response(text = '')
    else:
        return web.Response(status=404)

# @routes.get('/printlist')
# async def printlist(request):
#     sql.print_all('Tasks')
#     return web.Response(text = '')

# @routes.get('/flushall')
# async def flushall(request):
#     sql.flush_all('Tasks')
#     return web.Response(text = '')

def send_mail_alert(stockitem,stocknum,incdesc,targetprice,fetched_price):
    try:
        rcptlist = [target_email]
        receivers = ','.join(rcptlist)

        msg = MIMEMultipart('mixed')
        time_now = datetime.datetime.now()

        if stockitem == 'testing':
            msg['Subject'] = f'这是一封测试邮件 - {time_now.year}-{time_now.month}-{time_now.day}'
            msg['From'] = username_email
            msg['To'] = receivers
            alternative = MIMEMultipart('alternative')
            textplain = MIMEText(f'这是一封测试邮件，以测试您的发送和接收邮箱是否正常工作。当前服务器时间{time.asctime( time.localtime(time.time()) )}', _subtype='plain', _charset='UTF-8')
            alternative.attach(textplain)
            msg.attach(alternative)
        else:
            msg['Subject'] = f'您订阅的股票达到价格 - {time_now.year}-{time_now.month}-{time_now.day}'
            msg['From'] = username_email
            msg['To'] = receivers

            alternative = MIMEMultipart('alternative')
            text_ = f'您订阅的股票，号码"{stocknum}"已经达到目标价格，触发条件[{"超过" if incdesc == 0 else "低于"}] [{targetprice}] ，当前价格{fetched_price}，请及时确认。'
            hhhhh = '\n\n'
            textplain = MIMEText(f'{text_}{hhhhh}服务器时间{time.asctime( time.localtime(time.time()) )}', _subtype='plain', _charset='UTF-8')
            alternative.attach(textplain)
            msg.attach(alternative)

        client = smtplib.SMTP_SSL(host = 'smtp.qq.com')
        client.connect('smtp.qq.com')
        client.login(username_email, password_email)
        client.sendmail(username_email, rcptlist, msg.as_string())
        client.quit()
        return True
    except Exception as e:
        return False

async def single_fetch(url):
    try:
        async with ClientSession() as session:
            async with session.get(url) as response:
                html = await response.text()
        html = json.loads(html)
        return float(html['chart']['result'][0]['meta']['regularMarketPrice'])
    except:
        return None

async def fetch_once(stockitem , fetch_time_internal , min_fetch_internal):
    global last_update_time

    def get_url(stocknum):
        return f"https://query1.finance.yahoo.com/v8/finance/chart/{stocknum}.{'SS' if int(stocknum) >= 600000 else 'SZ'}?region=US&lang=en-US&includePrePost=false&interval=2m&range=1d&corsDomain=finance.yahoo.com&.tsrc=finance"

    def update_is_over(stockitem):
        sql.query_and_update('Tasks' , 'taskid' , stockitem.taskid , isover= 1)

    async def send_email_warp(stockitem,fetched_price):
        # return send_mail_alert(stockitem,fetched_price)
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(thread_pool, partial( send_mail_alert , 
                                                                None ,
                                                                stockitem.stocknum ,
                                                                stockitem.incdesc ,
                                                                stockitem.targetprice ,
                                                                fetched_price
                                                                ) )

    async def result_handler(stockitem , fetched_price):
        if DEBUG:
            print('###################')
            print(stockitem , fetched_price)
            print('###################')

        __last_update_time = str(get_time_string_east8())
        sql.query_and_update('Tasks' , 'taskid' , stockitem.taskid , currentprice=fetched_price , lastupdatetime = __last_update_time)
        if stockitem.incdesc == 0:
            if fetched_price >= stockitem.targetprice:
                update_is_over(stockitem)
                rv = await send_email_warp(stockitem,fetched_price)
                return True
            else:
                return False
        else:
            if fetched_price <= stockitem.targetprice:
                update_is_over(stockitem)
                rv = await send_email_warp(stockitem,fetched_price)
                return True
            else:
                return False

    fetch_times = fetch_time_internal // min_fetch_internal
    url = get_url(stockitem.stocknum)
    for fetch_time in range(fetch_times):
        if DEBUG:
            sleep_time = 0
        else:
            sleep_time = random.randint(0,min_fetch_internal)
        sleep_time_after = min_fetch_internal - sleep_time
        await asyncio.sleep(sleep_time)
        st_time = timetime()
        fetched_price = await single_fetch(url)
        if fetched_price == None:
            return 
        res = await result_handler(stockitem , fetched_price)
        if res == True:
            return
        fetch_cost_time = timetime() - st_time
        sleep_time_after = max(sleep_time_after - fetch_cost_time - 0.1 , 0)
        await asyncio.sleep(sleep_time_after)
        last_update_time = str(get_time_string_east8())

async def spider_core():
    loop = asyncio.get_running_loop()
    while True:
        current_time = get_time_string_east8()
        print(current_time ,"scaned list" ,end='')
        if current_time.hour in trade_time_utc8:
            print(',decide to work')
            scan_list = sql.get_all_monitor_target()
            for stockitem in scan_list:
                loop.create_task(fetch_once(stockitem ,fetch_time_internal ,min_fetch_internal))
            await asyncio.sleep(fetch_time_internal)
        else:
            print(',decide to sleep')
            await asyncio.sleep(10)

workingpath = os.path.dirname(os.path.abspath(__file__))
auth = BasicAuthMiddleware(username=auth_username, password=auth_password)
app = web.Application(middlewares=[auth])
app.add_routes(routes)
app.add_routes([web.static('/', os.path.join(workingpath ,'static'))])
loop = asyncio.get_event_loop()
loop.create_task(spider_core())
loop.run_until_complete(web._run_app(app, host = run_host , port = run_port ))
