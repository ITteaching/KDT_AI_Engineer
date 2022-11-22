```sql
-- 데이타베이스 생성
create database shopDB;
show databases;
USE shopDB;

-- memberTBL 생성
CREATE TABLE memberTBL 
(	memberID		CHAR(8) PRIMARY KEY,
 	memberName		CHAR(5) NOT NULL,
 	memberAddress	CHAR(20) NULL
);

-- productTBL 생성
CREATE TABLE productTBL
(	productName		CHAR(4) PRIMARY KEY,
 	cost			INT		NOT NULL,
 	makeDate		DATE	NULL,
 	company			CHAR(5)	NULL,
 	amount			INT		NOT NULL
);

-- DATA INSERT
INSERT INTO memberTBL VALUES('10001', 'Kim', '서울 강남구');
INSERT INTO memberTBL VALUES('10002', 'Lee', '인천 남동구');
INSERT INTO memberTBL VALUES('10003', 'Park','경기 성남구');
INSERT INTO memberTBL VALUES('10004', 'Han', '경기 부천시');

INSERT INTO productTBL VALUES('컴퓨터', 20, '2017-12-03', 'Samsung', 20);
INSERT INTO productTBL VALUES('세탁기', 15, '2020-05-11', 'LG', 10);
INSERT INTO productTBL VALUES('냉장고', 25, '2022-07-05', 'GE', 5);
```
