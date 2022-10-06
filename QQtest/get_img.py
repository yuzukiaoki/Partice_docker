from datetime import datetime as dt
import requests,re

def time_list(what_value,req_address,req_id,*args,): #將json裡的某個值放進list
    response = requests.get(req_address,{"id":req_id})
    data = response.json()
    
    print(type(data))
    print(data)
    time=[]
    if args[0] == 0 :
        for i in range(0,len(data)):
            time.append(data[i][what_value])
    elif args[0] == 1 :
        data = data[0][f"{args[1]}"]
        #dataKey = [k for k,v in kwargs.items()]
        
        for i in range(0,len(data)):
            print(i)
            time.append(data[i][what_value])

    return time,data

url_list = time_list("url","https://api.jsonstorage.net/v1/json/cc3a38bc-d03a-43bd-b2dc-0d4127034cf1/9c265be9-ce5f-45f8-bcd4-d55f378c3c29?apiKey=123",
"9c265be9-ce5f-45f8-bcd4-d55f378c3c29?apiKey=123",1,"download_url")[0]
count = 0
print(url_list)

for url in range(0,len(url_list)): #timestamp 有小數點 可以當名稱?
    pic = requests.get(url_list[url])

    file_name = re.findall(r"(?<=\/)[^\/\?#]+(?=[^\/]*$)", url_list[url])[0] # 神奇功能
    print(file_name)
    with open(f'D:\\YuzukiAoki\\測試用文件夾\\{dt.now().timestamp()}{file_name}','wb') as f:
        
        f.write(pic.content)
        count += 1
        print(f"write {count} url")