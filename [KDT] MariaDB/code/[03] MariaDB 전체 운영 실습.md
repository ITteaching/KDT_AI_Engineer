

# 3. MariaDB 전체 운영 실습

### 3.1.1 employees 데이타베이스 다운받기

* mysql -> document -> more -> install -> github(code -> download zip)

* 압축푼 폴더에서 shell 실행 후 커맨드창에서 "source employees.sql" 수행

### 3.1.2 db 서버 start/stop

* 관리자권한 cmd 창 실행

* net start/stop mariadb 또는 mysql

  

# [실습 1 : 5 ~ 7p]

### 3.1.3 데이타베이스 생성

```SQL
create database shopDB;
show databases;
USE shopDB;
```

### 3.1.4 테이블 생성

* HeidiSQL 활용하여 작업 수행
* meberTBL 테이블 생성

```SQL
CREATE TABLE memberTBL
(	memberID      CHAR(8)  PRIMARY KEY,
 	memberName    CHAR(5)  NOT NULL,
 	memberAddress CHAR(20) NULL
);
```

| 열 이름(한글)       | 영문 이름     | 데이터 형식 | 길이         | NULL 허용 |
| ------------------- | ------------- | ----------- | ------------ | --------- |
| 아이디(Pirmary Key) | memberID      | 문자(CHAR)  | 8글자(영문)  | X         |
| 회원 이름           | memberName    | 문자(CHAR)  | 5글자(한글)  | X         |
| 주소                | memberAddress | 문자(CHAR)  | 20글자(한글) | O         |

* productTBL 테이블 생성

```SQL
CREATE TABLE productTBL
(	productName  CHAR(4)  PRIMARY KEY,
 	cost         INT      NOT NULL,
 	makeDate     DATE     NULL,
 	company      CHAR(10)  NULL,
 	amount       INT      NOT NULL
);
```

| 열 이름(한글)          | 영문 이름   | 데이터 형식 | 길이         | NULL 허용 |
| ---------------------- | ----------- | ----------- | ------------ | --------- |
| 제품 이름(Primary Key) | productName | 문자(CHAR)  | 4글자(한글)  | X         |
| 가격                   | cost        | 숫자(INT)   | 정수         | X         |
| 제조일자               | makeDate    | 날짜(DATE)  | 날짜형       | O         |
| 제조회사               | company     | 문자(CHAR)  | 10글자(한글) | O         |
| 남은수량               | amount      | 숫자(INT)   | 정수         | X         |



# [실습 2 : 8p]

### 3.1.5 데이타 활용

* 데이타 입력 (memberTBL, productTBL)

```SQL
INSERT INTO memberTBL VALUES('10001', 'Kim', '서울 강남구');
INSERT INTO memberTBL VALUES('10002', 'Lee', '인천 남동구');
INSERT INTO memberTBL VALUES('10003', 'Park','경기 성남구');
INSERT INTO memberTBL VALUES('10004', 'Han', '경기 부천시');
```

| memberID | memberName | memberAddress |
| -------- | ---------- | ------------- |
| 10001    | Kim        | 서울 강남구   |
| 10002    | Lee        | 인천 남동구   |
| 10003    | Park       | 경기 성남구   |
| 10004    | Han        | 경기 부천시   |

```sql
INSERT INTO productTBL VALUES('컴퓨터', 20, '2017-12-03', 'Samsung', 20);
INSERT INTO productTBL VALUES('세탁기', 15, '2020-05-11', 'LG', 10);
INSERT INTO productTBL VALUES('냉장고', 25, '2022-07-05', 'GE', 5);
```

| productName | cost | makeDate   | company | amount |
| ----------- | ---- | ---------- | ------- | ------ |
| 컴퓨터      | 20   | 2017-12-03 | Samsung | 20     |
| 세탁기      | 15   | 2020-05-11 | LG      | 10     |
| 냉장고      | 25   | 2022-07-05 | GE      | 5      |



# [실습 3 : 9p]

* 데이타 조회

```SQL
SELECT * FROM memberTBL;

SELECT memberName, memberAddress FROM memberTBL;

SELECT * FROM memberTBL WHERE memberName='Park';
```

* 데이타 입력/수정/삭제

```sql
INSERT INTO membertbl 
     VALUES ('10005', 'Hong', '경기도 군포시');

UPDATE membertbl
   SET memberAddress = '서울 마포구' 
 WHERE memberName = 'Hong';

DELETE FROM membertbl
      WHERE memberName = 'Hong';

SELECT *
  FROM membertbl
   WHERE memberName = 'Hong';
```



# [실습 4 : 10p]

### 3.1.6 INDEX / VIEW 생성

```SQL
-- indexTBL 테이블 SQL로 작성
CREATE TABLE indextbl 
      (first_name VARCHAR(14),
       last_name VARCHAR(16),
       hire_date DATE);
       
-- 데이타 생성 : employees.employees 테이블에서 500건 insert
INSERT INTO indextbl
SELECT first_name, last_name, hire_date
 FROM employees.employees
  LIMIT 500;

-- 데이타 확인
SELECT * FROM indexTBL; 	 

-- 실행경로 확인(인덱스 생성전)
explain SELECT * FROM indextbl WHERE first_name = 'Mary';

-- INDEX 생성
CREATE INDEX idx_indextbl_firstname ON indextbl(first_name);

-- 실행경로 확인(인덱스 생성후)
explain SELECT * FROM indextbl WHERE first_name = 'Mary';

-- VIEW 생성
CREATE VIEW uv_memberTBL
AS
SELECT memberID, memberAddress 
  FROM membertbl;

-- 데이타 확인
SELECT * FROM uv_membertbl;
```



# [실습 5 : 11p]

### 3.1.7 STORED PROCEDURE 생성

```SQL
-- PROCEDURE 생성
DELIMITER //
CREATE PROCEDURE myproc()
BEGIN
    SELECT * FROM membertbl WHERE membername = '당탕이';
    SELECT * FROM producttbl WHERE productname = '냉장고';
END //
DELIMITER ;

-- PROCEDURE 실행
CALL myproc();
```

### 3.1.8 TRIGGER	

* 백업 테이블 생성

```sql
CREATE TABLE deletedMemberTBL
(memberID CHAR(8),
  memberName CHAR(5),
  memberAddress CHAR(20),
  deleteDate date
  );
```

* TRIGGER 생성 / 실행

```SQL
-- TRIGGER 생성
DELIMITER //
CREATE TRIGGER trg_deletedMemberTBL		-- 트리거 이름
AFTER DELETE							-- 삭제 후에 작동하게 지정
ON memberTBL							-- 트리거를 부착할 테이블
FOR EACH ROW							-- 각 행마다 적용
   BEGIN
INSERT INTO deletedMemberTBL
	  -- OLD 테이블의 내용을 백업테이블에 삽입
      VALUES (OLD.memberID, OLD.memberName, OLD.memberAddress, CURDATE() );
   END //
   DELIMITER ;

-- TRIGGER 실행
SELECT * FROM membertbl;		
DELETE FROM membertbl WHERE memberName = 'Lee';		  
SELECT * FROM membertbl;		
SELECT * FROM deletedMemberTBL;
```
