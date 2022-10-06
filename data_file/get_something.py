import requests ,random
import sys,traceback,json,asyncio
from datetime import datetime as dt
from datetime import timedelta
from imgurpython import ImgurClient


async def time_task(bot):
    await bot.wait_until_ready()  # 等待bot 啟動完畢
    while not bot.is_closed():  # 如果bot沒有關閉的話 就一直loop

        now_time = set_timeznoe(8).strftime('%H:%M')  # 原為datetime.datetime.now()
        # with open('mumi_setting.json', 'r', encoding='utf8') as jfile:
        #     jdata = json.load(jfile)
        dragon_channel = bot.get_channel(743370434048950272)#396383026533105685 主要聊天室
        #print("(39)恐龍報時頻道: ",self.channel)
        await dragon_channel.send("hehe")
        await asyncio.sleep(30)


"""
將byte轉成MB
"""
def transfer_MB(byte_thing):
    divisor = 1024 #divisor 除數
    transferKB = byte_thing/divisor
    transferMB = transferKB/divisor
    return transferMB

"""
混合的reaction 不只案表情也可以延遲指定時間並發送言論
可以只要隨機發送json的value或是指定的文字，或是除了前面再加上表情符號，可以全功能都要
"""
async def mix_reaction(msg,*args): #[random1, random2, sleeptime, msg or json, react or msg content, reaction]
            if random.randint(1,100) < random.randint(args[0],args[1]): #應該是 "<" 才對 右邊機率大於左邊
                if args[4] == "react":
                    await msg.add_reaction(args[5])#"<:wet:811109729727545364>"
                else:
                    pass
                await asyncio.sleep(args[2])
                if args[3] == "msg":
                    await msg.channel.send(args[4])
                    pass
                elif args[3]:
                    await random_react(args[3],msg)
                else:
                    pass
            else:
                pass

"""
根據函數帶入的參數(args)數量，bot會增加幾個reaction，最多5個，
"""
async def add_all_reaction(msg,*args): #[random1, random2]
    if random.randint(1,100) < random.randint(args[0],args[1]):
        if len(args)>2 :  #如果args這個list長度大於2 就推第2個表情 下面以此類推
            await msg.add_reaction(args[2])
        if len(args)>3 :
            await msg.add_reaction(args[3])
        if len(args)>4 :
            await msg.add_reaction(args[4])
        if len(args)>5 :
            await msg.add_reaction(args[5])
    else:
        pass
"""
原本在event.py頂端就有 with open，但這裡沒有，所以搬過來看看是否正常
此功能主要 隨機選擇 json檔案裡 指定key裡隨機value
"""
def random_react(json_document,msg): #random choice json 統整成funtion
    with open('mumi_setting.json','r',encoding='utf8') as jfile:
        jdata = json.load(jfile)
    
    #if random.randint(1,100) > random.randint(40,50):
    react_rand = random.choice(jdata[json_document])
    return msg.channel.send(react_rand)


"""
避免fb scraper抓到的圖檔死去，先上傳至imgur 再由mumibot傳送該imgur網址
"""
def upload_photo(image_url,what_album):
    client_id = ''
    client_secret = ''
    access_token = ''
    refresh_token = ''
    client = ImgurClient(client_id, client_secret, access_token, refresh_token)
    album = what_album # You can also enter an album ID here
    config = {
  'album': album,
 }

    print("Uploading image... ")
    image = client.upload_from_url(image_url, config=config, anon=False)
    print("Done")    
    return image['link']

"""
獲取指定server的所有資訊 (根據帶入的資料)，我這邊用意是抓取特定伺服器 所有channel id
"""
def get_server(req_address,req_id,server_info,server_value): #server_value 這邊抓channel_id  #抓server避免重複頻道ID一直上傳
            response = requests.get(req_address,{"id":req_id})
            data = response.json()
            server_id = []
            for server in range(0,len(data[0][server_info])):
                server_id.append(data[0][server_info][server][server_value])
            return server_id


"""
增加使用權限的 channel 或是 user
"""
def discord_append(address,ad_id,num,n_key,**kwargs):#channel_info追加用
            response = requests.get(address,{"id":ad_id}) 

            data = response.json()
            #回傳給json如個是字串 要用f"{}"包起來
            
            try_get_channel = kwargs.get('channel_guild',[])
            try_get_user = kwargs.get('bot_user_id',[])
            try_get_url = kwargs.get('url',[])
            try_get_n_url = kwargs.get('n_url',[])
            # 改天來測試一下這裡變數在幹嘛
            if type(try_get_channel) != list:
                content = {"channel_guild":kwargs.get('channel_guild',[]),
                "channel_name":kwargs.get('channel_name',[]),
                "channel_id":kwargs.get('channel_id',[])}

            elif type(try_get_user) != list:
                content = {"bot_user_name":kwargs.get('bot_user_name',[]),
                "bot_user_id":kwargs.get('bot_user_id',[])}
            
            elif type(try_get_url) != list: #h_img_download JSON專用格式
                content = {"url":kwargs.get('url',[]),
                "datetime":kwargs.get('datetime',[]),
                "unicode":kwargs.get('unicode',[]),
                "type":kwargs.get('type',[])} # 追加
            
            elif type(try_get_n_url) != list: # normal_img_download JSON專用格式
                content = {"n_url":kwargs.get('n_url',[]),
                "n_datetime":kwargs.get('n_datetime',[]),
                "n_unicode":kwargs.get('n_unicode',[]),
                "n_type":kwargs.get('n_type',[])} 
                
            else:
                pass
            
            data[num][n_key].append(content)

            return data


"""
去除使用權限的 channel 或是 user
"""
def discord_pop(address,ad_id,num,n_key,*arg):#channel_info追加用
            response = requests.get(address,{"id":ad_id}) 
            data = response.json()
            dict_len =   len(data[num][n_key])
            for key in arg:
                if key == 'channel_id':
                    for number in range(0,dict_len):
                        if data[num][n_key][number]['channel_id'] == arg[1] :
                            data[num][n_key].pop(number)
                            break
                elif key =='bot_user_id':
                    for number in range(0,dict_len):
                        if data[num][n_key][number]['bot_user_id'] == arg[1] :
                            data[num][n_key].pop(number)
                            break
            return data      

            #                           ID 可能為 使用者 或 頻道
            #arg目前暫定順序 (新增/刪除 , ID ,  哪個key )


"""
將資料上傳至 雲端json
"""
def discord_upd(address,ad_id,num,n_key,*arg,**kwargs):    #上傳至雲端json #channel_info上傳用
            if arg[0] == 0 : # 0 增加資料  #arg[0] 用來觀看是要增加還是刪除 
                update = requests.put(address,  #arg[1] 放 ID
                params =   {"id":ad_id},
                json = discord_append(address,ad_id,num,n_key,**kwargs)
                )
            elif arg[0] == 1 : # 1 刪除資料
                update = requests.put(address,
                params =   {"id":ad_id},
                json = discord_pop(address,ad_id,num,n_key,*arg)
                )

'''
↓ 上傳到雲端json，根據傳來的參數(azure、honkai、wflipper、maple)，來帶入各個排版，最後回傳整理好的資料(data)
'''
def res_append(scrap_id,scrap_datetime,address,ad_id,scrap_fb):
    response = requests.get(address,{"id":ad_id}) #新增value(疊加

    data = response.json()
    if scrap_fb == "azure":
        content = {"azure_id":scrap_id,"azure_datetime":scrap_datetime}
    elif scrap_fb == "honkai":
        content = {"honkai_id":scrap_id,"honkai_datetime":scrap_datetime}
    elif scrap_fb == "wflipper":
        content = {"wflipper_id":scrap_id,"wflipper_datetime":scrap_datetime}
    elif scrap_fb == "maple":
        content = {"maple_id":scrap_id,"maple_datetime":scrap_datetime}
    else:
        pass
    data.append(content)
    return data

'''
↓ 取得該json每一個指定value(這邊抓時間的value)，將每一個key值得value抓出來放到一個list，最後回傳該list
  arg[0] 使用的json有 : honkai_json、楓之谷_json、Azure_json
  arg[1] 使用的json有 : mix_json、img_download
'''
def some_list(what_value,req_address,req_id,*arg): #將json裡的某個值放進list
    response = requests.get(req_address,{"id":req_id})
    data = response.json()
    someList=[]
    if arg[0] == 0 :
        for i in range(0,len(data)):
            someList.append(data[i][what_value])
    elif arg[0] == 1 : 
        data = data[0][arg[1]]  # data賦予新值，避免下面又要下太長
        for i in range(0,len(data)): # 抓取data指定資料的range 總共要讓for迴圈跑幾次
            someList.append(data[i][what_value]) # 最後將抓到的資料全部放到LIst裡
    else:
        print("值帶錯了吧，87")
        pass
    return someList     # 回傳值
'''
↓ 將資料上傳(更新)至指定的json資料庫
'''
def upd(up_id,up_datetime,address,ad_id,scrap_fb):    #上傳至雲端json
    update = requests.put(address,
    params =   {"id":ad_id},
    json = res_append(up_id,up_datetime,address,ad_id,scrap_fb)
    )

'''
↓   能夠抓到報錯的資料
    取得該發生錯誤的行數和什麼error
'''
def printError(e,taskString): 
            error_class = e.__class__.__name__ #取得錯誤類型
            detail = e.args[0] #取得詳細內容
            cl, exc, tb = sys.exc_info() #取得Call Stack
            lastCallStack = traceback.extract_tb(tb)[-1] #取得Call Stack的最後一筆資料
            fileName = lastCallStack[0] #取得發生的檔案名稱
            lineNum = lastCallStack[1] #取得發生的行號
            funcName = lastCallStack[2] #取得發生的函數名稱
            #  print("_______________________This is Error____________________")
            errMsg = "________File \"{}\", line {}, in {}: [{}] {}".format(fileName, lineNum, funcName, error_class, detail)
            print(taskString,errMsg)
        #print("This is Azure errorMsg: ",errMsg)


'''
↓   如果 被FB Ban，每發生一次 temporarily banned ，就睡10分鐘 第二次就 20分鐘，直到解除被ban
'''
def BannedError(count,BannedWarning):  

            count +=1
            sleep_secs = 600 * count
            print(f"{BannedWarning} {sleep_secs / 60} m ({sleep_secs} secs)")
            return  sleep_secs
#print(f"Temporarily banned, sleeping for {sleep_secs / 60} m ({sleep_secs} secs)")
# def is_owner(ctx):
#     return ctx.message.author.id == "557103501256163348"

'''
↓   隨機冷卻時間應用
'''
def random_sleep(first,second):
    result = random.randint(first,second)
    return result

'''
↓   抓時間
'''
def set_timeznoe(timezone):
    utc_time = dt.utcnow()
    local_time = utc_time + timedelta(hours=timezone)
    return local_time







# def channel_append(channel_guild,channel_name,channel_id,address,ad_id,num,n_key):#channel_info追加用
#             response = requests.get(address,{"id":ad_id}) 

#             data = response.json()
#             #回傳給json如個是字串 要用f"{}"包起來 
#             content = {"channel_guild":f"{channel_guild}","channel_name":f"{channel_name}","channel_id":channel_id}
#             #if channel_id not in server_info(num,n_key,channel_id,address,ad_id):
#             data[num][n_key].append(content)
#             # else:
#             #     pass
#             return data

# def upd_server(up_guild,up_name,up_id,address,ad_id,num,n_key):    #上傳至雲端json #channel_info上傳用
#             update = requests.put(address,
#             params =   {"id":ad_id},
#             json = channel_append(up_guild,up_name,up_id,address,ad_id,num,n_key)
#             )



# def server_info(n,n_value,what_value,req_address,req_id): #將json裡的某個值放進list
#             response = requests.get(req_address,{"id":req_id})
#             data = response.json()
#             server=[]
#             for i in range(0,len(data[n][n_value])):
#                 server.append(data[n][n_value][i][what_value])
#             return server



# def get_server(req_address,req_id,server_info,server_value): #server_value 這邊抓channel_id  #抓server避免重複頻道ID一直上傳
#     response = requests.get(req_address,{"id":req_id})
#     data = response.json()
#     server_id = []
#     for server in range(0,len(data[0][server_info])):
#         server_id.append(data[0][server_info][server][server_value])
#     return server_id