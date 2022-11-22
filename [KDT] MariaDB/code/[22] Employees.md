# 22. Employees

## 1. Dataset Download

* https://dev.mysql.com/doc/employee/en : 소개 사이트

* https://github.com/datacharmer/test_db : 다운로드 사이트



## 2. Employees DB 생성

* create database employees
* 압축풀기 : employees.zip
* CMD에서 source employees.sql 실행



## 3. 실습 순서

* ERD 설명 (10분)
* Table layout 작성 (20분)
* Table별 데이타 확인 (10분)
* Table간 Relation 확인 (10분)
* Join 기본 실습 (100분)
* 집계 실습 (50분)



### [실습1] ERD 설명 (10분)



### [실습2] TABLE Layout 작성 (20분)

* Table ID / name : employees / 직원정보

| Column Name | Column ID  |   Data Type   | Length |   Null   | Key  |
| :---------: | :--------: | :-----------: | :----: | :------: | :--: |
|  사원번호   |   emp_no   |      INT      |        | NOT NULL |  PK  |
|  생년월일   | birty_date |     DATE      |        | NOT NULL |      |
|    이름     | first_name |    VARCHAR    |   14   | NOT NULL |      |
|     성      | last_name  |    VARCHAR    |   16   | NOT NULL |      |
|  남녀구분   |   gender   | ENUM('M','F') |        | NOT NULL |      |
|   입사일    | hire_date  |     DATE      |        | NOT NULL |      |

* Table ID / name : title / 직무정보

| Column Name | Column ID | Data Type | Length |   Null   |  Key   |
| :---------: | :-------: | :-------: | :----: | :------: | :----: |
|  사원번호   |  emp_no   |    INT    |        | NOT NULL | PK, FK |
|    직무     |   title   |  VARCHAR  |   50   | NOT NULL |   PK   |
| 직무시작일  | from_date |   DATE    |        | NOT NULL |   PK   |
| 직무종료일  |  to_date  |   DATE    |        |   NULL   |        |

* Table ID / name : salaries / 연봉정보

|  Column Name   | Column ID | Data Type | Length |   Null   |  Key   |
| :------------: | :-------: | :-------: | :----: | :------: | :----: |
|    사원번호    |  emp_no   |    INT    |        | NOT NULL | PK, FK |
|      연봉      |  salary   |    INT    |        | NOT NULL |        |
| 연봉계약시작일 | from_date |   DATE    |        | NOT NULL |   PK   |
| 연봉계약종료일 |  to_date  |   DATE    |        | NOT NULL |        |

* Table ID / name : dept_emp / 부서정보

|  Column Name   | Column ID | Data Type | Length |   Null   |  Key   |
| :------------: | :-------: | :-------: | :----: | :------: | :----: |
|    사원번호    |  emp_no   |    INT    |        | NOT NULL | PK, FK |
|    부서번호    |  dept_no  |   CHAR    |   4    | NOT NULL | PK, FK |
| 부서근무시작일 | from_date |   DATE    |        | NOT NULL |        |
| 부서근무종료일 |  to_date  |   DATE    |        | NOT NULL |        |

* Table ID / name : departments / 부서코드

| Column Name | Column ID | Data Type | Length |   Null   | Key  |
| :---------: | :-------: | :-------: | :----: | :------: | :--: |
|  부서번호   |  dept_no  |   CHAR    |   4    | NOT NULL |  PK  |
|   부서명    | dept_name |  VARCHAR  |   40   | NOT NULL |      |

* Table ID / name : dept_manager / 부서장정보

|   Column Name    | Column ID | Data Type | Length |   Null   |  Key   |
| :--------------: | :-------: | :-------: | :----: | :------: | :----: |
|     부서번호     |  dept_no  |   CHAR    |   4    | NOT NULL | PK, FK |
|     사번번호     |  emp_no   |    INT    |        | NOT NULL | PK, FK |
| 부서장근무시작일 | from_date |   DATE    |        | NOT NULL |        |
| 부서장근무종료일 |  to_date  |   DATE    |        | NOT NULL |        |



### [실습3] Table별 데이타 확인 (10분)

```SQL
SELECT * FROM employees;
SELECT * FROM salaries;
SELECT * FROM titles;
SELECT * FROM dept_emp;
SELECT * FROM departments;
SELECT * FROM dept_manager;
```



### [실습4] Table간 Relation 확인 (10분)



### [실습5]  Join 기본 SQL (50분)

* 예제 1) 직원 기본정보

```SQL
-- 조회내용 : 사번, 이름(first_name, last_name), 성별, 입사일 조회
-- 조건 : 사번이 10000번에서 100100번까지 직원
SELECT emp_no, first_name, last_name, gender, hire_date
  FROM employees
 WHERE emp_no between 100000 and 100010;
```

* 예제 2) 직원 직무정보

```SQL
-- 조회내용 : 사번, 이름(first_name, last_name), 성별, 입사일, 직무, 직무시작일, 직무종료일 조회
-- 조건 : 사번이 10000번에서 100100번까지 직원
SELECT	a.emp_no, a.first_name, a.last_name, a.gender, a.hire_date,
		b.title, b.from_date, b.to_date
  FROM employees a
  	INNER JOIN titles b
  		ON a.emp_no = b.emp_no
 WHERE a.emp_no between 100000 and 100010;
```

* 예제 3) 직원 현재 직무정보

```SQL
-- 조회내용 : 사번, 이름(first_name, last_name), 성별, 입사일, 직무, 직무시작일, 직무종료일 조회
-- 조건1 : 사번이 10000번에서 100100번까지 직원
-- 조건2 : 현재 직무인 데이타만 조회
SELECT	qa.emp_no, a.first_name, a.last_name, a.gender, a.hire_date,
		b.title, b.from_date, b.to_date
  FROM employees a
  	INNER JOIN titles b
  		ON a.emp_no = b.emp_no
 WHERE a.emp_no between 100000 and 100010
   AND b.to_date >= current_date();
-- AND to_date = '9999-01-01';  
```

* 예제 4) 직원 연봉정보

```SQL
-- 조회내용 : 사번, 이름(first_name, last_name), 성별, 입사일, 연봉, 연봉계약시작일, 연봉계약종료일 조회
-- 조건 : 사번이 10000번에서 100100번까지 직원
SELECT	a.emp_no, a.first_name, a.last_name, a.gender, a.hire_date,
		b.salary, b.from_date, b.to_date
  FROM employees a
  	INNER JOIN salaries b
  		ON a.emp_no = b.emp_no
 WHERE a.emp_no between 100000 and 100010;
```

* 예제 5) 직원 현재 연봉정보

```sql
-- 조회내용 : 사번, 이름(first_name, last_name), 성별, 입사일, 연봉, 연봉계약시작일, 연봉계약종료일 조회
-- 조건1 : 사번이 10000번에서 100100번까지 직원
-- 조건2 : 현재 계약중인 연봉 데이타만 조회
SELECT	a.emp_no, a.first_name, a.last_name, a.gender, a.hire_date,
		b.salary, b.from_date, b.to_date
  FROM employees a
  	INNER JOIN salaries b
  		ON a.emp_no = b.emp_no
 WHERE a.emp_no between 100000 and 100010
   AND b.to_date >= current_date();
```

* 예제 6) 직원 부서정보

```sql
-- 조회내용 : 사번, 이름(first_name, last_name), 성별, 입사일, 부서번호, 부서근무시작일, 부서근무종료일 조회
-- 조건 : 사번이 10000번에서 100100번까지 직원
SELECT	a.emp_no, a.first_name, a.last_name, a.gender, a.hire_date,
		b.dept_no, b.from_date, b.to_date
  FROM employees a
  	INNER JOIN dept_emp b
  		ON a.emp_no = b.emp_no
 WHERE a.emp_no between 100000 and 100010;
```

* 예제 7) 직원 현재 부서정보

```sql
-- 조회내용 : 사번, 이름(first_name, last_name), 성별, 입사일, 부서번호, 부서근무시작일, 부서근무종료일 조회
-- 조건1 : 사번이 10000번에서 100100번까지 직원
-- 조건2 : 현재 근무중인 부서 데이타만 조회
SELECT	a.emp_no, a.first_name, a.last_name, a.gender, a.hire_date,
		b.dept_no, b.from_date, b.to_date
  FROM employees a
  	INNER JOIN dept_emp b
  		ON a.emp_no = b.emp_no
 WHERE a.emp_no between 100000 and 100010
    AND b.to_date >= current_date();
```

* 예제 8) 직원 현재 부서정보 : 부서명 포함

```SQL
-- 조회내용 : 사번, 이름(first_name, last_name), 성별, 입사일, 부서번호, 부서근무시작일, 부서근무종료일, 부서명 조회
-- 조건1 : 사번이 10000번에서 100100번까지 직원
-- 조건2 : 현재 근무중인 부서 데이타만 조회
SELECT	a.emp_no, a.first_name, a.last_name, a.gender, a.hire_date,
		b.dept_no, b.from_date, b.to_date,
		c.dept_name
  FROM employees a
  	INNER JOIN dept_emp b
  		ON a.emp_no = b.emp_no
	INNER JOIN departments c  
    	ON b.dept_no = c.dept_no
 WHERE a.emp_no between 100000 and 100010
    AND b.to_date >= current_date();
```

* 예제 9) 직원 현재 부서정보 : 부서명, 부서장사번 포함

```sql
-- 조회내용 : 사번, 이름(first_name, last_name), 성별, 입사일, 부서번호, 부서근무시작일, 부서근무종료일, 부서명, 부서장사번 조회
-- 조건1 : 사번이 10000번에서 100100번까지 직원
-- 조건2 : 현재 근무중인 부서 데이타만 조회
-- 조건3 : 현재 근무중인 부서의 현재 부서장 사번만 조회
SELECT	a.emp_no, a.first_name, a.last_name, a.gender, a.hire_date,
		b.dept_no, b.from_date, b.to_date,
		c.dept_name,
		d.emp_no
  FROM employees a
  	INNER JOIN dept_emp b
  		ON a.emp_no = b.emp_no
	INNER JOIN departments c  
    	ON b.dept_no = c.dept_no
	INNER JOIN dept_manager d 
		ON c.dept_no=d.dept_no    	
 WHERE a.emp_no between 100000 and 100010
    AND b.to_date >= current_date()
    AND d.to_date >= current_date();
```

* 예제 10) 직원 현재 부서정보 : 부서명, 부서장사번, 부서장명 포함

```SQL
SELECT	a.emp_no, a.first_name, a.last_name, a.gender, a.hire_date,
		b.dept_no, b.from_date, b.to_date,
		c.dept_name,
		d.emp_no,
		CONCAT(f.first_name, f.last_name)
  FROM employees a
  	INNER JOIN dept_emp b
  		ON a.emp_no = b.emp_no
	INNER JOIN departments c  
    	ON b.dept_no = c.dept_no
	INNER JOIN dept_manager d 
		ON c.dept_no=d.dept_no    
	INNER JOIN employees f
    	ON d.emp_no = f.emp_no
 WHERE a.emp_no between 100000 and 100010
    AND b.to_date >= current_date()
    AND d.to_date >= current_date();
```

* 예제 11) 직원 직무, 연봉정보

```SQL
-- 조회내용 : 사번, 이름(first_name, last_name), 성별, 입사일, 직무, 직무시작일, 직무종료일, 연봉, 연봉계약시작일, 연봉계약종료일
-- 조건1 : 사번이 10000번에서 100100번까지 직원
-- 조건2 : 현재 직무인 데이타만 조회
-- 조건3 : 현재 계약 연봉만 조회  
SELECT a.emp_no, a.first_name, a.last_name, gender, a.hire_date, b.title, b.from_date, b.to_date, c.salary, c.from_date, c.to_date
  FROM employees a
  	INNER JOIN titles b
  		ON a.emp_no = b.emp_no
  	INNER JOIN salaries c
  		ON a.emp_no = c.emp_no
 WHERE a.emp_no between 100000 and 100010
   AND b.to_date >= current_date()
   AND c.to_date >= current_date();
```

* 예제 12) 직원 직무, 연봉, 부서정보

```SQL
-- 조회내용 : 사번, 이름(first_name, last_name), 성별, 입사일, 직무, 직무시작일, 직무종료일, 연봉, 연봉계약시작일, 연봉계약종료일, 부서번호, 부서명
-- 조건1 : 사번이 10000번에서 100100번까지 직원
-- 조건2 : 현재 직무인 데이타만 조회
-- 조건3 : 현재 계약 연봉만 조회  
-- 조건4 : 현재 소속 부서만 조회  
SELECT	a.emp_no, a.first_name, a.last_name, a.gender, a.hire_date, 
		b.title, b.from_date, b.to_date,
		c.salary, c.from_date, c.to_date,
		d.dept_no,
		e.dept_name
  FROM employees a
  	INNER JOIN titles b
  		ON a.emp_no = b.emp_no
  	INNER JOIN salaries c
  		ON a.emp_no = c.emp_no
	INNER JOIN dept_emp d 
		ON a.emp_no = d.emp_no
	INNER JOIN departments e 
		ON d.dept_no=e.dept_no
 WHERE a.emp_no between 100000 and 100010
   AND b.to_date >= current_date()
   AND c.to_date >= current_date()
   AND d.to_date >= current_date();
```

* 예제 13) 직원 직무, 연봉, 부서, 부서장 정보

```SQL
-- 조회내용 : 사번, 이름(first_name, ' ', last_name), 성별, 입사일, 직무, 직무시작일, 직무종료일, 연봉, 연봉계약시작일, 연봉계약종료일, 부서번호, 부서명, 부서장사번, 부서장이름(first_name, ' ', last_name)
-- 조건1 : 사번이 10000번에서 100100번까지 직원
-- 조건2 : 현재 직무인 데이타만 조회
-- 조건3 : 현재 계약 연봉만 조회  
-- 조건4 : 현재 소속 부서만 조회  
```

* 예제 13-1) 기본 SQL 활용

```SQL
SELECT	a.emp_no, a.first_name, a.last_name, a.gender, a.hire_date, 
		b.title, b.from_date, b.to_date,
		c.salary, c.from_date, c.to_date,
		d.dept_no,
		e.dept_name,
		concat(g.first_name,' ', g.last_name) manager_name 
  FROM employees a
  	INNER JOIN titles b
  		ON a.emp_no = b.emp_no
  	INNER JOIN salaries c
  		ON a.emp_no = c.emp_no
	INNER JOIN dept_emp d 
		ON a.emp_no = d.emp_no
	INNER JOIN departments e 
		ON d.dept_no=e.dept_no
	INNER JOIN dept_manager f 
		ON e.dept_no = f.dept_no
	INNER JOIN employees g
    	ON f.emp_no = g.emp_no
 WHERE a.emp_no between 100000 and 100010
   AND b.to_date >= current_date()
   AND c.to_date >= current_date()
   AND d.to_date >= current_date()
   AND f.to_date >= current_date();
```

* 예제 13-2) 서브 쿼리 사용

```SQL
SELECT	a.emp_no, a.first_name, a.last_name, a.gender, a.hire_date, 
		b.title, b.from_date, b.to_date,
		c.salary, c.from_date, c.to_date,
		d.dept_no,
		e.dept_name,
		(SELECT concat(first_name,' ', last_name) name 
           FROM employees
          WHERE emp_no=f.emp_no) manager_name
  FROM employees a
  	INNER JOIN titles b
  		ON a.emp_no = b.emp_no
  	INNER JOIN salaries c
  		ON a.emp_no = c.emp_no
	INNER JOIN dept_emp d 
		ON a.emp_no = d.emp_no
	INNER JOIN departments e 
		ON d.dept_no=e.dept_no
	INNER JOIN dept_manager f 
		ON e.dept_no = f.dept_no
 WHERE a.emp_no between 100000 and 100010
   AND b.to_date >= current_date()
   AND c.to_date >= current_date()
   AND d.to_date >= current_date()
   AND f.to_date >= current_date();
```

* 예제 13-3) INLINE VIEW 활용

```SQL
SELECT x.*, concat(y.first_name,' ', y.last_name) manager_name
 FROM 
 	(
	 SELECT	a.emp_no, a.first_name, a.last_name, gender, a.hire_date, 
			b.title, b.from_date title_fd, b.to_date title_td,
			c.salary, c.from_date salary_fd, c.to_date salary_td,
			d.dept_no, e.dept_name, f.emp_no manager_no
	  FROM employees a
  		INNER JOIN titles b
  			ON a.emp_no = b.emp_no
	  	INNER JOIN salaries c
  			ON a.emp_no = c.emp_no
		INNER JOIN dept_emp d 
			ON a.emp_no = d.emp_no
		INNER JOIN departments e 
			ON d.dept_no=e.dept_no
		INNER JOIN dept_manager f 
			ON e.dept_no = f.dept_no
	 WHERE a.emp_no between 100000 and 100010
	   AND b.to_date >= current_date()
	   AND c.to_date >= current_date()
	   AND d.to_date >= current_date()
	   AND f.to_date >= current_date()
	 ) x
	INNER JOIN employees y 
		ON x.manager_no = y.emp_no;
```

* 예제 13-4) VIEW TABLE 활용

```SQL
-- VIEW TABLE 생성
CREATE VIEW v_employee_all AS
	 SELECT	a.emp_no, a.first_name, a.last_name, gender, a.hire_date, 
			b.title, b.from_date title_fd, b.to_date title_td,
			c.salary, c.from_date salary_fd, c.to_date salary_td,
			d.dept_no, e.dept_name, f.emp_no manager_no
	  FROM employees a
  		INNER JOIN titles b
  			ON a.emp_no = b.emp_no
	  	INNER JOIN salaries c
  			ON a.emp_no = c.emp_no
		INNER JOIN dept_emp d 
			ON a.emp_no = d.emp_no
		INNER JOIN departments e 
			ON d.dept_no=e.dept_no
		INNER JOIN dept_manager f 
			ON e.dept_no = f.dept_no
	 WHERE a.emp_no between 100000 and 100010
	   AND b.to_date >= current_date()
	   AND c.to_date >= current_date()
	   AND d.to_date >= current_date()
	   AND f.to_date >= current_date()

-- VIEW TABLE 조회
SELECT * FROM v_employee_all;	  

-- VIEW TABLE 활용 SQL
SELECT x.*, concat(y.first_name,' ', y.last_name) manager_name
 FROM v_employee_all x
	INNER JOIN employees y 
		ON x.manager_no = y.emp_no;
```



### [실습 6] 집계 실습

### 1) 현재기준

* 남녀별 최고, 최저, 평균 연봉

```sql
SELECT a.gender, avg(b.salary), max(b.salary), min(b.salary), count(*)
  FROM employees a
  	INNER JOIN salaries b 
  		ON a.emp_no = b.emp_no 
 WHERE b.to_date >= curdate()
GROUP BY a.gender; 
```

* 직무별 최고, 최저, 평균 연봉

```sql
SELECT c.title, avg(b.salary), max(b.salary), min(b.salary), count(*)
  FROM employees a
  	INNER JOIN salaries b 
  		ON a.emp_no = b.emp_no 
  	INNER JOIN titles c 
  		ON a.emp_no = c.emp_no
 WHERE b.to_date >= curdate()
   AND c.to_date >= curdate()
GROUP BY c.title;
```

* 부서별 최고, 최저, 평균 연봉

```sql
SELECT c.dept_no,d.dept_name, avg(b.salary), max(b.salary), min(b.salary), count(*)
  FROM employees a
  	INNER JOIN salaries b 
  		ON a.emp_no = b.emp_no 
  	INNER JOIN dept_emp c 
  		ON a.emp_no = c.emp_no
	INNER JOIN departments d 
		ON c.dept_no = d.dept_no
 WHERE b.to_date >= curdate()
   AND c.to_date >= curdate()
GROUP BY c.dept_no, d.dept_name;
```

* 부서별/직무별 최고, 최저, 평균 연봉

```sql
SELECT c.dept_no,d.dept_name, e.title, avg(b.salary), max(b.salary), min(b.salary), count(*)
  FROM employees a
  	INNER JOIN salaries b 
  		ON a.emp_no = b.emp_no 
  	INNER JOIN dept_emp c 
  		ON a.emp_no = c.emp_no
	INNER JOIN departments d 
		ON c.dept_no = d.dept_no
	INNER JOIN titles e
    	ON a.emp_no = e.emp_no
 WHERE b.to_date >= curdate()
   AND c.to_date >= curdate()
   AND e.to_date >= curdate()
GROUP BY c.dept_no, d.dept_name, e.title;
```



### 2) 시작연도 기준

* 남녀별 연도별 최고, 최저, 평균 연봉

```sql
SELECT a.gender, year(from_date), avg(b.salary), max(b.salary), min(b.salary), count(*)
  FROM employees a
  	INNER JOIN salaries b 
  		ON a.emp_no = b.emp_no 
GROUP BY a.gender, year(from_date); 
```

* 현재 직무 기준 연도별 최고, 최저, 평균 연봉

```sql
SELECT c.title, year(b.from_date), avg(b.salary), max(b.salary), min(b.salary), count(*)
  FROM employees a
  	INNER JOIN salaries b 
  		ON a.emp_no = b.emp_no 
  	INNER JOIN titles c 
  		ON a.emp_no = c.emp_no
 WHERE c.to_date >= curdate()
GROUP BY c.title, year(b.from_date);
```

* 현재 부서 기준 연도별 최고, 최저, 평균 연봉

```sql
SELECT c.dept_no,d.dept_name, year(b.from_date), avg(b.salary), max(b.salary), min(b.salary), count(*)
  FROM employees a
  	INNER JOIN salaries b 
  		ON a.emp_no = b.emp_no 
  	INNER JOIN dept_emp c 
  		ON a.emp_no = c.emp_no
	INNER JOIN departments d 
		ON c.dept_no = d.dept_no
 WHERE c.to_date >= curdate()
GROUP BY c.dept_no, d.dept_name, year(b.from_date);
```

* 현재 부서, 현재 직무 기준 연도별 최고, 최저, 평균 연봉

```sql
SELECT c.dept_no,d.dept_name, e.title, year(b.from_date), avg(b.salary), max(b.salary), min(b.salary), count(*)
  FROM employees a
  	INNER JOIN salaries b 
  		ON a.emp_no = b.emp_no 
  	INNER JOIN dept_emp c 
  		ON a.emp_no = c.emp_no
	INNER JOIN departments d 
		ON c.dept_no = d.dept_no
	INNER JOIN titles e
    	ON a.emp_no = e.emp_no
 WHERE c.to_date >= curdate()
   AND e.to_date >= curdate()
GROUP BY c.dept_no, d.dept_name, e.title, year(b.from_date);
```

* 현재 부서장인 사람의 연도별 최고, 최저, 평균 연봉

```sql
SELECT year(b.from_date), avg(b.salary),max(b.salary), min(b.salary), count(*)
  FROM dept_manager a
  	INNER JOIN salaries b
  		ON a.emp_no=b.emp_no
 WHERE a.to_date >= current_date()	  		
GROUP BY year(b.from_date) ;
```

