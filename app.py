from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
import re
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# 连接数据库
def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='username',
        password='yourpassword',
        database='d5ys'
    )
    return connection

# 首页
@app.route('/')
def index():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM 人员信息表')
    records = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('index.html', records=records)

# 编辑
@app.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit(id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    if request.method == 'POST':
        # 存储表单数据
        name = request.form['name']
        gender = request.form['gender']
        phone = request.form['phone']
        email = request.form['email']
        prev_url = request.form.get('prev_url', url_for('index'))

        cursor.execute('''
            UPDATE 人员信息表
            SET 姓名 = %s, 性别 = %s, 手机号码 = %s, 电子邮箱 = %s
            WHERE 序号 = %s
        ''', (name, gender, phone, email, id))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(prev_url)

    cursor.execute('SELECT * FROM 人员信息表 WHERE 序号 = %s', (id,))
    record = cursor.fetchone()
    cursor.close()  
    connection.close()
    # 存储上一页的url
    session['prev_url'] = request.referrer or url_for('index')
    return render_template('edit.html', record=record)

# 插入错误信息到错误信息表
def insert_error(person_id, category, message):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO 错误信息表 (人员信息表序号, 错误类别, 错误内容)
        VALUES (%s, %s, %s)
    ''', (person_id, category, message))
    connection.commit()
    cursor.close()
    connection.close()  


# 错误规则验证
@app.route('/validate')
def validate():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # 清空错误信息表
    cursor.execute("TRUNCATE table 错误信息表")
    connection.commit()

    cursor.execute("SELECT * FROM 人员信息表")
    records = cursor.fetchall()

    cursor.execute("SELECT * FROM 规则表")
    rules = cursor.fetchall()

    # 进行规则匹配
    for rule in rules:
        rule_name, regex = rule['字段名称'], rule['规则表达式']
        
        for record in records:
            seq, name, gender, phone, email = record['序号'], record['姓名'], record['性别'], record['手机号码'], record['电子邮箱']

            # 判断错误类型
            if rule_name == '性别':
                if not gender:
                    insert_error(seq, '性别', '性别为空')
                elif not re.match(regex, gender):
                    insert_error(seq, '性别', '性别格式错误')
            if rule_name == '手机号码':
                if not phone:
                    insert_error(seq, '手机号码', '手机号码为空')
                elif not re.match(regex, phone):
                    insert_error(seq, '手机号码', '手机号码格式错误')
            if rule_name == '电子邮箱':
                if not email:
                    insert_error(seq, '电子邮箱', '电子邮箱为空')
                elif not re.match(regex, email):
                    insert_error(seq, '电子邮箱', '电子邮箱格式错误')
    
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # 计算各错误类别的数量
    cursor.execute("SELECT 错误类别, COUNT(*) as count FROM 错误信息表 GROUP BY 错误类别 ORDER BY 错误类别")
    error_summary = cursor.fetchall() # 错误信息汇总

    # 查询详细错误信息
    cursor.execute("SELECT * FROM 错误信息表 ORDER BY 错误类别")
    errors = cursor.fetchall()

    # 按错误类别分类
    error_categories = {}
    for error in errors:
        category = error['错误类别']
        if category not in error_categories:
            error_categories[category] = []
        error_categories[category].append(error)

    cursor.close()
    connection.close()

    return render_template('validate.html', error_categories=error_categories, error_summary=error_summary)


# 删除人员信息
@app.route('/delete/<int:id>')  
def delete(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM 错误信息表 WHERE 人员信息表序号 = %s", (id,))  
    cursor.execute("DELETE FROM 人员信息表 WHERE 序号 = %s", (id,))
    connection.commit()
    cursor.close()
    connection.close()
    flash("序号 %d 的人员信息删除成功" % id)
    return redirect(url_for('index'))


# 新增
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':

        name = request.form['name']
        gender = request.form['gender']
        phone = request.form['phone']
        email = request.form['email']

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO 人员信息表 (姓名, 性别, 手机号码, 电子邮箱)
            VALUES (%s, %s, %s, %s)
        ''', (name, gender, phone, email))
        connection.commit()
        cursor.close()
        connection.close()
        flash("人员信息添加成功，新增人员序号为 %d" % cursor.lastrowid)
        # return redirect(url_for('index'))

    return render_template('add.html')

# 查询
@app.route('/search', methods=['GET', 'POST'])
def search():
    person = None
    if request.method == 'POST':
        seq = request.form['seq']

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM 人员信息表 WHERE 序号 = %s', (seq,))
        person = cursor.fetchone()
        cursor.close()
        connection.close()

        if not person:
            flash('未找到匹配的人员信息')

    # 显示查询结果
    return render_template('search.html', person=person)

if __name__ == '__main__':
    app.run(debug=True)
