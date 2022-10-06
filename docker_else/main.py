from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Flask Dockerized'


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8888)

#關閉docker -> docker stop <container_name>
#重啟docker -> docker start <container_name>