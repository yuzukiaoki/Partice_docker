# pratice docker

![](https://img.shields.io/badge/python-3.9.3-green) ![](https://img.shields.io/badge/latest%20update-2022%2F10%2F6-green)



## 簡易說明


- 試著將pixiv爬蟲設置再disocrd Bot
- 將discord bot 放置在docker
- 達成當pixiv作者更新作品時，能自動推播至discord，同時將檔案下載至指定volume
- 使用docker讓Code不受不同電腦環境限制，保持同一環境(docker)

## 使用code

`QQbot.py`: discord Bot主程式

`./Pixiv/author.py` : Pixiv爬蟲主程式

`docker-compose.yml` : 架設docker容器

