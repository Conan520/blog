# blog python服务端


使用了poetry(https://python-poetry.org/)管理依赖,未安装poetry，可以使用`pip install poetry`进行安装

```
poetry install
```

数据库使用的是mysql，settings.py中的DATABASES字段中的内容需要修改成自己想要的

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mytest',      # 数据库名
        'USER': 'root',          # 用户名（如root）
        'PASSWORD': 'root123',  # 密码
        'HOST': 'localhost',       # 或MySQL服务器IP（远程时使用）
        'PORT': '3306',            # 默认端口
        'OPTIONS': {
            'charset': 'utf8mb4',  # 支持Emoji等特殊字符
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
```

配置好数据库之后，可以使用如下命令，把model映射到mysql中的表

```
python manage.py makemigrations

python manage.py migrate
```

运行server

```
python manage.py runserver
```