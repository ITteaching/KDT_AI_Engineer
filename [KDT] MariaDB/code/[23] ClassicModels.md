# 23. ClassicModels

## 1. Dataset Download

* https://www.mysqltutorial.org/mysql-sample-database.aspx : 다운로드 사이트




## 2. classicmodels DB 생성

* 압축풀기 : mysqlsampledatabase.zip
* CMD에서 source mysqlsampledatabase.sql 실행



## 3. 실습 순서

* ERD 설명 (10분)
* Table layout 작성 (20분) : orders, orderdetails, customers, products
* Table별 데이타 확인 (10분)
* Table간 Relation 확인 (10분)
* 구매 지표 (30분)
* 그룹 구매 지표 (50분)



### [실습1] ERD 설명 (10분)



### [실습2] TABLE Layout 작성 (20분)

* Table ID / name : orders / 주문정보

| Column Name  |   Column ID    | Data Type | Length |   Null   | Key  |
| :----------: | :------------: | :-------: | :----: | :------: | :--: |
|   주문번호   |  orderNumber   |    INT    |        | NOT NULL |  PK  |
|   주문일자   |   orderDate    |   DATE    |        | NOT NULL |      |
| 배송요청일자 |  requireDate   |   DATE    |        | NOT NULL |      |
|   발송일자   |  shippedDate   |   DATE    |        |   NULL   |      |
|   상태구분   |     status     |  VARCHAR  |   15   | NOT NULL |      |
|     비고     |    comments    |   TEXT    |        |   NULL   |      |
|   고객번호   | customerNumber |    INT    |        | NOT NULL |  FK  |

* Table ID / name : orderdetails / 주문상세정보

| Column Name  |    Column ID    | Data Type | Length |   Null   |  Key   |
| :----------: | :-------------: | :-------: | :----: | :------: | :----: |
|   주문번호   |   orderNumber   |    INT    |        | NOT NULL | PK, FK |
|   상품코드   |   productCode   |  VARCHAR  |   15   | NOT NULL | PK, FK |
|     수량     | quantityOrdered |    INT    |        | NOT NULL |        |
|     단가     |    priceEach    |  DECIMAL  |  10,2  | NOT NULL |        |
| 주문번호순서 | orderLineNumber | SMALLINT  |        | NOT NULL |        |

* Table ID / name : products / 제품정보

| Column Name  |     Column ID      | Data Type | Length |   Null   | Key  |
| :----------: | :----------------: | :-------: | :----: | :------: | :--: |
|   제품코드   |    productCode     |  VARCHAR  |        | NOT NULL |  PK  |
|    제품명    |    productName     |  VARCHAR  |        | NOT NULL |      |
|   제품라인   |    productLine     |  VARCHAR  |        | NOT NULL |  FK  |
|   제품규모   |    productScale    |  VARCHAR  |        | NOT NULL |      |
|    제조사    |   productVendor    |  VARCHAR  |        | NOT NULL |      |
|   제품설명   | productDescription |   TEXT    |        | NOT NULL |      |
| 제품제고수량 |  quantityInStock   | SMALLINT  |        | NOT NULL |      |
|    판매가    |      buyPrice      |  DECIMAL  |  10,2  | NOT NULL |      |
| 권장소비자가 |        MSRP        |  DECIMAL  |  10,2  | NOT NULL |      |

* Table ID / name : customers / 고객정보

| Column Name  |       Column ID        | Data Type | Length |   Null   | Key  |
| :----------: | :--------------------: | :-------: | :----: | :------: | :--: |
|   고객번호   |     customerNumber     |    INT    |        | NOT NULL |  PK  |
|    고객명    |      customerName      |  VARCHAR  |   50   | NOT NULL |      |
|  접촉자이름  |    contactLastName     |  VARCHAR  |   50   | NOT NULL |      |
|   접촉자성   |    contactFirstName    |  VARCHAR  |   50   | NOT NULL |      |
|   전화번호   |         phone          |  VARCHAR  |   50   | NOT NULL |      |
|    주소1     |      addressLine1      |  VARCHAR  |   50   | NOT NULL |      |
|    주소2     |      addressLine2      |  VARCHAR  |   50   |   NULL   |      |
|     도시     |          city          |  VARCHAR  |   50   | NOT NULL |      |
|      주      |         state          |  VARCHAR  |   50   |   NULL   |      |
|   우편번호   |       postalCode       |  VARCHAR  |   15   |   NULL   |      |
|     국가     |        country         |  VARCHAR  |   50   | NOT NULL |      |
|   직원번호   | salesRepEmployeeNumber |    INT    |        |   NULL   |  FK  |
| 카드제한금액 |      creditLimit       |  DECIMAL  |  10,2  |   NULL   |      |



### [실습3] Table별 데이타 확인 (10분)

```SQL
SELECT * FROM orders;
SELECT * FROM orderdetails;
SELECT * FROM products;
SELECT * FROM customers;
```



### [실습4] Table간 Relation 확인 (10분)



### [실습5]  구매 지표 (30분)

### 1) 매출액

* 예제 5-1) 일별 매출액

```sql
-- 기본 데이타 조회
SELECT	a.orderDate, 
		b.quantityOrdered, b.priceEach,
		b.quantityOrdered * b.priceEach   
  FROM orders a
 	INNER JOIN orderdetails b 
 		ON a.orderNumber = b.orderNumber;

-- GROUP BY 적용
SELECT	a.orderDate, 
		sum(b.quantityOrdered), sum(b.priceEach),
		sum(b.quantityOrdered * b.priceEach)   
  FROM orders a
 	INNER JOIN orderdetails b 
 		ON a.orderNumber = b.orderNumber
GROUP BY a.orderDate;
```

* 예제 5-2) 월별 매출액

```sql
SELECT	substr(a.orderDate,1,7), 
		sum(b.quantityOrdered), sum(b.priceEach),
		sum(b.quantityOrdered * b.priceEach)   
  FROM orders a
 	INNER JOIN orderdetails b 
 		ON a.orderNumber = b.orderNumber
GROUP BY substr(a.orderDate,1,7);
```

* 예제 5-3) 연별 매출액

```sql
SELECT	substr(a.orderDate,1,4), 
		sum(b.quantityOrdered), sum(b.priceEach),
		sum(b.quantityOrdered * b.priceEach)   
  FROM orders a
 	INNER JOIN orderdetails b 
 		ON a.orderNumber = b.orderNumber
GROUP BY substr(a.orderDate,1,4);
```



### 2) 구매자 수, 구매 건수

* 일자별 구매자 수와 구매 건수

   : 일자별로 동일한 구매자가 2건 이상 구매한 데이타 존재함

```sql
select	orderDate,
		count(*),
		count(distinct customerNumber)
  from orders
group by orderDate;
```



### 3) 연도별 인당 매출액

* 연도별 매출액 / 고객 수

```sql
SELECT	substr(a.orderDate,1,4), 
		count(distinct customerNumber),
		sum(b.quantityOrdered), sum(b.priceEach),
		sum(b.quantityOrdered * b.priceEach) / count(distinct customerNumber)  
  FROM orders a
 	INNER JOIN orderdetails b 
 		ON a.orderNumber = b.orderNumber
GROUP BY substr(a.orderDate,1,4);
```



### 4) 건당 구매 금액

* 연도별 매출액 / 주문 건수

```sql
SELECT	substr(a.orderDate,1,4), 
		count(distinct a.orderNumber),
		sum(b.quantityOrdered), sum(b.priceEach),
		sum(b.quantityOrdered * b.priceEach) / count(distinct a.orderNumber)  
  FROM orders a
 	INNER JOIN orderdetails b 
 		ON a.orderNumber = b.orderNumber
GROUP BY substr(a.orderDate,1,4);
```



### [실습6]  그룹 구매 지표 (50분)

### 1) 국가별, 도시별 매출액

* customers 테이블의 country, city 컬럼 필요

```sql
SELECT	c.country, c.city, SUM(b.quantityOrdered * b.priceEach) sales
  FROM orders a
 	INNER JOIN orderdetails b 
 		ON a.orderNumber = b.orderNumber
 	INNER JOIN customers c
 		ON a.customerNumber = c.customerNumber
GROUP BY c.country, c.city
ORDER BY c.country, c.city;
```



### 2) 북미 vs 비북미 매출액

* CASE WHEN 문장 사용 : 북미 - 'USA', 'Canada'

```sql
SELECT	CASE WHEN c.country in ('USA', 'Canada') THEN 'NA'
		ELSE 'Others' END,
        (b.quantityOrdered * b.priceEach) sales
  FROM orders a
 	INNER JOIN orderdetails b 
 		ON a.orderNumber = b.orderNumber
 	INNER JOIN customers c
 		ON a.customerNumber = c.customerNumber
GROUP BY 1
ORDER BY 1;
```



### 3) 매출 TOP 5 국가 및 매출

* 국가별 매출순으로 소팅

```sql
SELECT  c.country,
		SUM(b.quantityOrdered * b.priceEach) sales,
		DENSE_RANK() OVER(ORDER BY SALES DESC) RNK
  FROM orders a
  	INNER JOIN orderdetails b
    	ON a.orderNumber = b.orderNumber
    INNER JOIN customers c
    	ON a.customerNumber = c.customerNumber
GROUP BY c.country
ORDER BY RNK;
```

* 매출 TOP 5  국가만 조회

```SQL
SELECT *
  FROM (
		SELECT  c.country,
				SUM(b.quantityOrdered * b.priceEach) sales,
				DENSE_RANK() OVER(ORDER BY SALES DESC) RNK
		  FROM orders a
		  	INNER JOIN orderdetails b
		    	ON a.orderNumber = b.orderNumber
		    INNER JOIN customers c
    			ON a.customerNumber = c.customerNumber
		GROUP BY c.country
		ORDER BY RNK
		) RNK
WHERE RNK <= 5;
```



### 4) 미국 TOP 5 차량 모델

* 미국 차량 모델 판매량

```sql
SELECT	productname, sum(b.quantityOrdered * b.priceEach)   
  FROM orders a
 	INNER JOIN orderdetails b 
 		ON a.orderNumber = b.orderNumber
	INNER JOIN products c
    	ON b.productCode = c.productCode
	INNER JOIN customers d
    	ON a.customerNumber = d.customerNumber
 WHERE d.country = 'USA'
GROUP BY productname
ORDER BY 2 DESC;
```

* 미국 차량 모델 판매량 TOP 5 : LIMIT 이용

```SQL
SELECT *
  FROM (
		SELECT	productname, sum(b.quantityOrdered * b.priceEach)   
		  FROM orders a
		 	INNER JOIN orderdetails b 
		 		ON a.orderNumber = b.orderNumber
			INNER JOIN products c
		    	ON b.productCode = c.productCode
			INNER JOIN customers d
		    	ON a.customerNumber = d.customerNumber
		 WHERE d.country = 'USA'
		GROUP BY productname
		ORDER BY 2 DESC
		) RNK
LIMIT 5;
```

* 미국 차량 모델 판매량 TOP 5 : OVER() 이용

```SQL
SELECT *
  FROM (
		SELECT	productname,
    			sum(b.quantityOrdered * b.priceEach) sales,
	    		ROW_NUMBER() OVER(ORDER BY SALES DESC) RNK
  		  FROM orders a
 			INNER JOIN orderdetails b 
 				ON a.orderNumber = b.orderNumber
			INNER JOIN products c
    			ON b.productCode = c.productCode
			INNER JOIN customers d
    			ON a.customerNumber = d.customerNumber
 		WHERE d.country = 'USA'
		GROUP BY productname
		) RNK
WHERE RNK <=5;
```

