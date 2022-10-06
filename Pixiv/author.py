from pprint import pprint
import os,time
from aiohttp import ClientSession
from datetime import datetime as dt
import asyncio,aiohttp
from Pixiv.utility import headersss,download_result,get_artwork


class Pixiv():

    def __init__(self):
        
        self.id_begin = "0"

    def getAuthorName(self,to_json):
        """
        取得作者名稱
        :param to_json: json格式的資料
        """
        check_json = to_json["body"]["pickup"]
        # 如果pickup有資料，就取得作者名稱
        if check_json:
            # 如果作者名稱裡有 \u3000 則把它換成空白
            author_name = to_json["body"]["pickup"][0]["userName"].replace('\u3000','')
            return author_name
        else:
            # 如果pickup沒有資料，就用當下的日期取代作者名稱
            utc_time = dt.utcnow()
            author_name = utc_time.strftime('%Y%m%d')
            return author_name

    def checkfolder(self,response,author_id):
        """
        :param response: 給予response至 getAuthorName()後得到作者名稱
        :param author_id: 作者id
        """
        a_path ='../aoki'
        folder_name = self.getAuthorName(response)
        first_path = a_path+'/pixiv-artworks'
        if not os.path.exists(first_path):
            os.mkdir(first_path)

        self.path = a_path+'/pixiv-artworks/'+f"{folder_name}({author_id})"
        if not os.path.exists(self.path):
            try:
                os.mkdir(self.path)
            except:
                raise Exception("無法建立資料夾")


            
    async def main(self,var1, var2):

        author_id = var1
        check_start = var2

        # author_id = input("請輸入作者ID:\n")
        # check_start = input("是否要設定起始ID?(Y/N)\n").upper()

        if check_start == 'Y':
            while True:
                self.id_begin = input("請輸入起始ID:(ex:91234567)\n")
                id_list = [number for number in self.id_begin]
                # id要是8位數
                if self.id_begin.isdigit() and len(id_list) == 8:
                    break
                elif self.id_begin.isdigit() and len(id_list) == 9:
                    break

                else:
                    print("請輸入8或9位數字")
                    continue
                       
        headers = headersss(f"https://www.pixiv.net/users/{author_id}/artworks")

        # 利用作者ID 找到作者所有作品ID
        author_url = f"https://pixiv.net/ajax/user/{author_id}/profile/all?lang=zh-tw"

        timeout = aiohttp.ClientTimeout(total=600)
        connector = aiohttp.TCPConnector(limit=50, force_close=True)

        async with ClientSession(connector=connector, trust_env = True, timeout=timeout) as session:

            async with session.get(author_url,headers=headers) as response:
                
                # 確認連線問題
                if response.status == 200:
                    
                    to_json = await response.json()
                    #下載到目標位置
                    self.checkfolder(to_json,author_id)
                    #作者 所有作品ID list
                    art = list(to_json["body"]["illusts"].keys())
                    
                    # 如果有漫畫的作品
                    if to_json["body"]["manga"]:
                        print("=====作者有漫畫作品=====")
                        print("=====合併漫畫與作品ID List=====")

                        manga = list(to_json["body"]["manga"].keys())
                        # 合併(目前先合併，如非漫畫真的太多在另開資料夾存取)
                        art = art + manga

                    result,gif_result =  await get_artwork(art, session, self.path, id_begin=self.id_begin)
                    # 從執行緒的list中 抓出每個執行緒的成功與失敗次數
    
                    success_time,false_time = download_result(tuple=result)

                    print(f"成功下載IMG {success_time}張, 失敗{false_time}張")

                    if gif_result != []:
                        GIF_success,GIF_false = download_result(list=gif_result)

                        print(f"成功下載GIF {GIF_success}張, 失敗{GIF_false}張")


                else:
                    print("此作者不存在，或是連線有問題")
                    raise Exception("連線狀態",response.status)


if __name__ == "__main__":
    # 確認執行花費的時間
    start_time = time.time()
    
    # 使用windows執行asyncio會有錯誤，必須多加下面這行
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(Pixiv().main(6662895,'N'))

    end_time = time.time()
    #取小數點後兩位
    use_time = round(end_time-start_time,2) 
    print(f"總共花費{use_time}秒")

