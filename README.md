# web_personnel_management

简介：使用python的flask框架搭建小型web页面，使用html/CSS前端设计，连接mysql后台数据库，实现人员信息的数据筛查和增删改查。

## 功能

增加、编辑、删除、查询、检查数据

检查数据根据数据库中错误规则表操作，如需增加规则需要在表中增加正则表达式。

## 使用指南

安装python>=3.8, mysql数据库，添加必要的库

```
pip install -r requirements.txt
```
连接mysql数据库

创建数据库，运行db.sql文件

修改app.py文件中db_connection变量为自己的数据库连接信息

运行app.py文件


## 目录结构

```
web_personnel_management
├── app.py
├── db.sql
├── README.md
├── requirements.txt
└── templates
    ├── add.html
    ├── check.html
    ├── delete.html
    ├── edit.html
    ├── index.html
    ├── search.html
    └── style.css
```

