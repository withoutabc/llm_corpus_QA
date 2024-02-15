FROM python:3.9

# 设置工作目录
WORKDIR /app

# 将当前目录中的所有文件复制到容器的工作目录中
COPY . /app

#RUN apt-get update
#RUN apt-get install sqlite3

# 安装依赖项
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

EXPOSE 5000

# 启动应用程序
CMD ["python", "app.py"]