
import math, random
import zipfile
#import fake_useragent
import imageio.v2 as imageio
import configparser, os, asyncio
import json
from itertools import islice, takewhile, repeat
from tqdm import tqdm

# 製作假 useragent
# ua = fake_useragent.UserAgent()
# user_agent = ua.random

#讀取 config.ini
config = configparser.ConfigParser(interpolation=None)
config.read('Pixiv/config.ini', encoding="utf-8")
cookie = config['config']['cookie']
task_times = int(config['config']['task_times'])
check_times = int(config['config']['check_times'])
cool = int(config['cool_down']['cool'])



def loops_times(task_list,times):
    """
    :param task_list  => Task的list
    :param times      => 每次執行幾個task
    為了算準 tqdm 的total參數而用的函式
    """
    loops_times = len(task_list)/times
    if loops_times >= 1:

            if len(task_list)%times!=0:
                    loops_times = math.floor(loops_times) + 1
            else:
                    loops_times = math.floor(loops_times)
    else:
            loops_times = 1

    # if len(task_list)%times != 0:
    #         #math.floor 無條件捨去
    #         loops_times = math.floor(loops_times) + 1
    # elif loops_times < 1:
    #     loops_times = 1

    return loops_times

def split_every(n, iterable):
    """
    Slice an iterable into chunks of n elements
    :type n: int
    :type iterable: Iterable
    :rtype: Iterator
    我也不懂 總之就是給它 task list 和 次數 ，每次只會執行指定的次數TASK，直到list task清空 
    參考
    https://stackoverflow.com/questions/1915170/split-a-generator-iterable-every-n-items-in-python-splitevery
    """
    iterator = iter(iterable)
    #time.sleep(1)
    return takewhile(bool, (list(islice(iterator, n)) for _ in repeat(None)))

# def headerss(user_agent,referer,cookie):
#     """
#     廢棄，tag檔案要再更改成下面的用法
#     """
#     Aheaders = {'user-agent':user_agent,
#         'referer':referer ,
#         'cookie':cookie}
#     return Aheaders



def headersss(referer):
    """
    :param referer  => 參考的網址
    簡化多種樣式 header的用處
    """
    Aheaders = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.27',
        'referer':referer ,
        'cookie':cookie}
    return Aheaders

def download_result(tuple=False ,list=False):
    """
    :param tuple  => 參數來源內容包含tuple，[(1,2),(3,4)]
    :param list   => 參數蘭園內容僅有list，[1,2,3,4]
    
    解析來源list 產出 成功失敗次數
    """
    success_time = 0
    false_time = 0
    if tuple:
        for suc,fal,_ in tuple:
            success_time += suc
            false_time += fal
        
        return success_time,false_time
    
    elif list:
        for result in list:
            if result == True:
                success_time += 1
            elif result == False:
                false_time += 1
                
        return success_time,false_time

async def download_IMG(session, url,art_id,path,
                       rank=None,
                       fav_count=None):
        """
        :param session  => 登入要用的session
        :param url      => 作品的URL
        :param art_id   => 作品的ID
        :param path     => 作品要存放的路徑
        :param rank     => 爬取rank 要傳入rank排行參數
        :param fav_count=> 爬取tag 要傳入收藏數參數
        下載pixiv 作品原始圖像(original)
        """
        await asyncio.sleep(cool)

        headers = headersss(f'https://www.pixiv.net/artworks/{art_id}')
        async with session.get(url,headers=headers) as response:

            false_time = 0
            success_time = 0
            ugoira_id = []

            try:
                #if response.status == 200:
                result_json =  await response.json()
                body = result_json['body']
                # 下載該作品 original的圖片
                for datas in body:
                    download_url = datas['urls']['original']

                    name = download_url.split('/')[-1]
                    #print(download_url)
                    #如果有GIF則使用另外方式下載 
                    get_id = name.split('_')[0]

                    if rank:
                        name = f"{rank}_{name}"
                    elif fav_count:
                        name = f"({fav_count}){name}"

                    # if rank:
                    #     check_path_img = os.path.join(path, name)
                    # else:
                    check_path_img = os.path.join(path, name)

                    # 爬取作品遇到gif的話就把ID放進list
                    if rank and "ugoira" in name:
                        # 如果rank存在的前提下
                        ugoira_id.append((get_id,rank))
                    
                    elif fav_count and "ugoira" in name:
                        ugoira_id.append((get_id,fav_count))

                    elif "ugoira" in name:
                        
                        ugoira_id.append(get_id)

                        #await dowload_GIF(ugoira_id,session,path)
                    elif os.path.isfile(check_path_img):
                        #print(f"{name} 已經存在")
                        continue
                            
                    else:

                        async with session.get(download_url,headers=headers) as response:
                            
                            try:
                                #if response.status == 200:
                                # 取得content的內容，不知道為什麼是用read() 隨便試出來的
                                content = await response.read()

                                # if rank:
                                #     with open(path+'\\'+rank_name,mode='wb')as f:
                                #         f.write(content)

                                # else:
                                # 抓author的話 執行這段

                                with open(path+'/'+name,mode='wb')as f:
                                    f.write(content)

                                success_time += 1

                            except Exception as e:
                                print("下載失敗")
                                print("錯誤",e)
                                print("連線狀態",response.status)
                                false_time += 1

            except Exception as e:
                print("沒有找到作品，或是連線失敗")
                print("錯誤",e)
                print("連線狀態",response.status)
            return success_time, false_time, ugoira_id

async def dowload_GIF(ugoira_id, session, path, scrape_type,
                      fav = None):
        """
        :param ugoira_id   => GIF作品的ID
        :param session     => 登入要用的session
        :param path        => 作品要存放的路徑
        :param scrape_type => 爬取的種類(author、rank、tag)
        :param fav         => 爬取tag 要傳入收藏數參數
        下載pixiv 作品GIF原始圖像(original) 
        """
        await asyncio.sleep(cool)

        if scrape_type == 'rank':
            rank= ugoira_id[1]
            ugoira_id = ugoira_id[0]

        if scrape_type == 'rank':
            check_path = os.path.join(path, f"{rank}_{ugoira_id}.gif")

        elif scrape_type == 'tag':
            check_path = os.path.join(path, f"({fav}){ugoira_id}.gif")

        else:
            # type == author
            check_path = os.path.join(path, f"{ugoira_id}.gif")

        if os.path.isfile(check_path):
            print(f"{ugoira_id} 已經存在")
            return None
        
        else:

            url =f"https://www.pixiv.net/ajax/illust/{ugoira_id}/ugoira_meta"
            headers = headersss(f'https://www.pixiv.net/artworks/{ugoira_id}')

            try:
                async with session.get(url, headers=headers) as resp:
                    resp = await resp.json()
                    delay = [item["delay"] for item in resp["body"]["frames"]]
                    # print(delay)
                    delay = sum(delay) / len(delay)
                    zip_url = resp["body"]["originalSrc"]
            except Exception as e:
                print(e)
                print(f"{ugoira_id} is not found")
                return False
                
            
            await asyncio.sleep(3)
            try:
                async with session.get(zip_url, headers=headers) as zip_resp:
                    gif_data = await zip_resp.read()
            except Exception as e:
                print(e)
                print(f"{zip_url} 下載失敗")
                return False

            # 檔案路徑
            orignal_path = path
            if scrape_type == 'author':
                gif_path = os.path.join(path, f"{ugoira_id}")
            elif scrape_type == 'rank':
                gif_path = os.path.join(path, f"{rank}_{ugoira_id}")
            elif scrape_type == 'tag':
                gif_path = os.path.join(path, f"({fav}){ugoira_id}")

            if not os.path.exists(gif_path):
                os.mkdir(gif_path)

            zip_path = os.path.join(gif_path, "temp.zip")
            
            # wb+ 可以寫入和讀取
            with open(zip_path, "wb+") as fp:
                fp.write(gif_data)
            temp_file_list = []
            
            # r -> read
            zipo = zipfile.ZipFile(zip_path, "r")
            
            # namlist 返回按名稱排序的檔案名稱列表
            for file in zipo.namelist():
                temp_file_list.append(os.path.join(gif_path, file))
                # extract 將檔案拆解出來
                zipo.extract(file, gif_path)
            # 沒關掉的話就不會寫入
            zipo.close()

            
            image_data = []
            #print(f"=====正在組成{ugoira_id}.gif=====")
            for file in temp_file_list:
                image_data.append(imageio.imread(file))

            if scrape_type =='author':
                imageio.mimsave(os.path.join(orignal_path, f"{ugoira_id}" + ".gif"), image_data, "GIF", duration=delay / 1000)
            elif scrape_type =='rank':
                imageio.mimsave(os.path.join(orignal_path, f"{rank}_{ugoira_id}" + ".gif"), image_data, "GIF", duration=delay / 1000)
            elif scrape_type == 'tag':
                imageio.mimsave(os.path.join(orignal_path, f"({fav}){ugoira_id}" + ".gif"), image_data, "GIF", duration=delay / 1000)


            # 清除所有中間文件。

            for file in temp_file_list:
                os.remove(file)
            os.remove(zip_path)
            # 刪除站存資料夾
            os.rmdir(gif_path)
            #print(f"{ugoira_id}, 下載完成")
            return True



async def get_artwork(art, session, path, 
                      scrape_type='author', 
                      id_begin='0',
                      second=False,
                      favorites=None):
        """
        :param art: 作者的作品list
        :param cookie: 登入後的cookie
        :param path: 資料夾路徑
        """
        
        links = []
        img_result = []
        gif_id =[]
        gif_result = []
        comfirm_list = [] # for tag
        new_comfirm_list = [] #for tag
        error_id = [] #for tag
        exclude_id =[] #for tag

        for art_id in art:

            if scrape_type == 'author':
                # 如果起始ID大於 ard id 就略過此次迴圈
                if int(id_begin) >= int(art_id):
                    continue
            
            if scrape_type == 'tag':
                art_url = f'https://www.pixiv.net/ajax/illust/{art_id}?lang=zh-tw'
            else:
                art_url = f'https://www.pixiv.net/ajax/illust/{art_id}/pages?lang=zh'
            # 迴圈把所有作品的URL放進list
            links.append((art_url,art_id))
        
        if scrape_type == 'tag':

            print(f"總共有 {len(links)} 個作品")
            print("=====開始比較收藏數=====")
            await asyncio.sleep(3)
            #test_count = 13
            new_list= []
            try_times = 1
            # 神奇的global
            global check_times
            while True:

                if new_list != []:
                    print(f"第{try_times}次嘗試")
                    links = new_list
                    # 有變負數風險 日後修正
                    check_times = check_times - (try_times*3)

                check_tasks = [check_favorites(session, link, str(art_id), favorites) for link,art_id in links]
                loops_time = loops_times(check_tasks, check_times)



                # 重複爬取越多次 冷卻時間越久
                sleep_start = try_times * 10
                with tqdm(total=loops_time,desc="比較收藏數") as pbar:

                    pbar.set_postfix({"每次執行數量":check_times})

                    for tasks in split_every(check_times, check_tasks):

                        await asyncio.sleep(random.randint(sleep_start, sleep_start + 20))
                        confirm_url = await asyncio.gather(*tasks)
                        #comfirm_url => [(url,收藏數),(url,收藏數),(url,收藏數),(None,None)]
                        comfirm_list.extend(confirm_url)
                        
                        pbar.update()
                
                new_list= []
                try_times +=1
                # 最多爬取3次
                if try_times == 4:
                    print(f"已重複爬取循環{try_times}次，跳脫循環")
                    break

                for item in range(len(comfirm_list)-1,-1,-1):
                    if type(comfirm_list[item]) == tuple:
                        if len(comfirm_list[item]) == 2:
                            
                            new_list.append(comfirm_list[item])
                            comfirm_list.pop(item)
                
                # 如果沒有爬取失敗的 則跳脫迴圈
                if new_list == []:
                    print("沒有爬取失敗")
                    break
                print(f"有{len(new_list)}個爬取失敗")

                

            

            for item in range(len(comfirm_list)):
                if comfirm_list[item] ==None:
                    continue
                elif type(comfirm_list[item]) == tuple:
                    if len(comfirm_list[item]) == 2:
                        error_id.append(comfirm_list[item])

                    elif len(comfirm_list[item]) == 3:
                        new_comfirm_list.append(comfirm_list[item])
                else:
                    #bool
                    error_id.append(comfirm_list[item])

            

            # for item in range(len(comfirm_list)):
            #     if comfirm_list[item] ==None:
            #         continue
            #     elif type(comfirm_list[item]) != tuple:
            #         error_id.append(comfirm_list[item])
            #     else:
            #         new_comfirm_list.append(comfirm_list[item])

            #倒敘迴圈
            for item in range(len(error_id)-1,-1,-1):
                if type(error_id[item]) == bool:
                    exclude_id.append(error_id[item])
                    error_id.pop(item)
            
            exclude_count = sum(exclude_id)

        if scrape_type =='tag':
            print(f"總共有 {len(new_comfirm_list)} 個作品")
        else:
            print(f"總共有 {len(links)} 個作品")
        print("=====開始下載作品=====")
        await asyncio.sleep(3)

        # timeout = aiohttp.ClientTimeout(total=600)
        # connector = aiohttp.TCPConnector(limit=50,force_close=True)
        # async with ClientSession(connector=connector,trust_env = True) as session:
        if scrape_type =='rank':
            if second:
                print("=====開始下載rank 第2頁=====")
                img_tasks = [download_IMG(session, link[0], link[1], path, rank = str(rank)) for rank, link in enumerate(links, start=51)]
            else:
                img_tasks = [download_IMG(session, link[0], link[1], path, rank = str(rank)) for rank, link in enumerate(links, start=1)]
        
        elif scrape_type == 'tag':
            img_tasks = [download_IMG(session, url, str(art_id), path, fav_count=str(fav)) for url, fav, art_id in new_comfirm_list  if url != None]

        else:
            # scrape_type =='author'
            img_tasks = [download_IMG(session, link,str(art_id),path) for link,art_id in links]
        
        if img_tasks == []:
            print(f"=====沒有大於{favorites}收藏數的作品=====")

        else:

            loops_time = loops_times(img_tasks, task_times)
            with tqdm(total=loops_time,desc="IMG下載") as pbar:
                pbar.set_postfix({"每次執行數量":task_times})    
            
                for task in split_every(task_times, img_tasks):

                    result = await asyncio.gather(*task)

                    img_result.extend(result)
                    
                    #await asyncio.sleep(3)
                    pbar.update()
            
            gif_id = [getthird[0] for _,_,getthird in img_result if getthird]
            #print(gif_id)
            # for _,_,id in img_result:
            #     gif_id.extend(id)     

            if gif_id == []:
                print("=====沒有GIF=====")

            else:
                print(f"總共要下載 {len(gif_id)} 個GIF作品")
                print("=====開始下載GIF檔案=====")

                await asyncio.sleep(3)

                if scrape_type =='rank':
                    gif_tasks = [dowload_GIF(id_rank, session, path, scrape_type='rank') for id_rank in gif_id]
                
                elif scrape_type == 'tag':
                    gif_tasks = [dowload_GIF(id, session, path, scrape_type='tag', fav=fav) for id,fav in gif_id]

                else:
                    # scrape_type =='author'
                    gif_tasks = [dowload_GIF(id, session, path, scrape_type='author') for id in gif_id]

                # 使用tqdm讀取條 裡面的task不能有任何print
                loops_time = loops_times(gif_tasks,1)
                with tqdm(total=loops_time,desc="GIF下載") as pbar:

                    pbar.set_postfix({"每次執行數量":1})
                    # 每次最多下載一張GIF
                    for tasks in split_every(1, gif_tasks):
                        # 獲取執行任務後的結果
                        #await asyncio.sleep(1)
                        success =  await asyncio.gather(*tasks)
                        
                        gif_result.append(*success)
                        pbar.update()

            if scrape_type == "tag":
                print(f"錯誤總數: {(len(error_id))}")
                print("------------------------------")
                print(f"排除總數: {exclude_count}")

            
        # 回傳是為了讓主程式知道總共下載成功、失敗幾張圖片
        return img_result,gif_result

async def check_favorites(session, url, art_id, favorites):
        
       
        headers = headersss(f'https://www.pixiv.net/artworks/{art_id}')
        async with session.get(url,headers=headers) as response:
            try:
                #不知道為什麼有些網頁抓到是 500 錯誤 還有429
                
                # 當爬蟲時 出現連線失敗，回傳作品url&ID 
                if response.status != 200:
                    
                    # self.error_count += 1
                    # if self.error_count <= 10:
                    #     print("狀態: ",response.status)
                    #     print("網址: ",url)
                    return url, art_id

                result_json = await response.json()
                
                fav_count = result_json['body']['bookmarkCount']
                
                if fav_count >= int(favorites):
                    # print(f"這是這個作品的收藏數: {fav_count}")
                    # print(f"這是限制的收藏數: {int(self.favorites)}")
                    #art_id = result_json['body']['id']
                    new_url = f'https://www.pixiv.net/ajax/illust/{art_id}/pages?lang=zh'

                    # 去除包含再黑名單&TAG的作品
                    with open('config.json','r',encoding='utf8') as jfile:
                        jdata = json.load(jfile)
                    tag_list = result_json['body']['tags']['tags']
                    for tag_num in tag_list:
                        if tag_num['tag'] in jdata['badTag']:
                            
                            #self.exclude_count += 1
                            return True
                    if result_json['body']['userId'] in jdata['badUser']:
                        #self.exclude_count += 1
                        return True

                    return new_url, fav_count, art_id
                else:

                    return None
            except Exception as e:
                print(f"發生錯誤: {e}\n response.status: {response.status}")
                print("錯誤這邊啦 url : ",url)
                raise Exception("暫停")