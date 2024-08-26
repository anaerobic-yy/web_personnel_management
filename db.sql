-- Active: 1723796980678@@127.0.0.1@3306@d5ys
CREATE DATABASE d5ys;
USE d5ys;

CREATE TABLE 人员信息表 (
    序号 INT PRIMARY KEY AUTO_INCREMENT,
    姓名 VARCHAR(100),
    性别 VARCHAR(10),
    手机号码 VARCHAR(15),
    电子邮箱 VARCHAR(100)
);

CREATE TABLE 规则表 (
    序号 INT PRIMARY KEY AUTO_INCREMENT,
    字段名称 VARCHAR(50),
    规则表达式 VARCHAR(255)
);

CREATE TABLE 错误信息表 (
    序号 INT PRIMARY KEY AUTO_INCREMENT,
    人员信息表序号 INT,
    错误类别 VARCHAR(50),
    错误内容 VARCHAR(255),
    FOREIGN KEY (人员信息表序号) REFERENCES 人员信息表(序号)
);

INSERT INTO 人员信息表 (序号, 姓名, 性别, 手机号码, 电子邮箱) VALUES
(1, '张三', '男', '13800138000', 'zhangsan@example.com'),
(2, '李四', '女', '13800138001', 'lisi'),
(3, '王五', '男', '111', 'wangwu@example.com'),
(4, '赵六', '女', '13800138003', 'zhaoliu@example.com'),
(5, '孙七', '男', '13800138004', 'sunqi@example.com'),
(6, '周八', '女', '13800138005', 'zhouba@example.com'),
(7, '吴九', '不男不女', '13800138006', 'wujie@example.com'),
(8, '郑十', '女', '13800138007', 'zhengshi@example.com'),
(9, '钱十一', '男', '13800138008', 'qianshiyi@example.com'),
(10, '孙十二', '非男', '13800138009', 'sunshier'),
(11, '李十三', '男', 'xxx', 'lishisan@example.com'),
(12, '陈十四', '女', '13800138011', '@example.com'),
(13, '张十五', '男', '13800138012', 'zhang15@example.com'),
(14, '杨十六', '女', '222', 'yang16@example.com'),
(15, '刘十七', '男', '13800138014', 'liu17@example.com'),
(16, '黄十八', '女', '13800138015', 'huang18@example.com'),
(17, '冯十九', '男', '13800138016', 'feng19@example.com'),
(18, '蔡二十', '女', '13800138017', 'cai20@example.com'),
(19, '郭二十一', '男', '13800138018', ''),
(20, '朱二十二', '女', '13800138019', 'zhu22@example.com'),
(21, '秦二十三', '男', '13800138020', 'qin23@example.com'),
(22, '罗二十四', '女', '13800138021', 'luo24@example.com'),
(23, '邹二十五', '男', '13800138022', 'zou25@example.com'),
(24, '钟二十六', '女', '13800138023', 'zhong26@'),
(25, '潘二十七', '男', '13800138024', 'pan27@example.com'),
(26, '谭二十八', '女', '13800138025', 'tan28@example.com'),
(27, '杜二十九', '男', '13800138026', 'du29@example.com'),
(28, '沈三十', '女', '13800138027', 'shen30@example.com'),
(29, '曾三十一', '男', '13800138028', 'zeng31@example.com'),
(30, '梁三十二', '女', '13800138029', 'liang32@example.com')


-- 插入性别规则
INSERT INTO 规则表 (字段名称, 规则表达式)
VALUES ('性别', '^(男|女)$');

-- 插入手机号码规则（假设为中国大陆的11位手机号码）
INSERT INTO 规则表 (字段名称, 规则表达式)
VALUES ('手机号码', '^\d{11}$');

-- 插入电子邮箱规则
INSERT INTO 规则表 (字段名称, 规则表达式)
VALUES ('电子邮箱', '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$');



