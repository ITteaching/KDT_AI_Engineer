# 24. Mydata

### 1. Dataset Download

* https://www.kaggle.com/nicapotato/womens-ecommerce-clothing-reviews : 다운로드 사이트




## 2. mydata DB 생성

* 압축풀기 : archive.zip
* Table -> 데이타 가져오기 : source Womens Clothing E-Commerce Reviews.csv 실행



## 3. 실습 순서

* Table layout 작성 (20분) 
* Division별 평점 계산 (30분)
* 상품, 연령, SIZE별 집계 (50분)



### [실습1] TABLE Layout 작성 (10분)

* Table ID / name : ProdReview / 상품 리뷰정보

|      Column Name       |        Column ID        | Data Type | Length | Null | Key  |
| :--------------------: | :---------------------: | :-------: | :----: | :--: | :--: |
|       상품 번호        |      Clothing  ID       |    INT    |        | NULL |  UK  |
|          연령          |           Age           |    INT    |        | NULL |      |
|       리뷰 제목        |          Title          |  VARCHAR  |  512   | NULL |      |
|       리뷰 내용        |       Review Text       |  VARCHAR  |  512   | NULL |      |
|          평점          |         Rating          |    INT    |        | NULL |      |
| 리뷰어 상품 추천 여부  |     Recommended IND     |    INT    |        | NULL |      |
|    긍정적 피드백 수    | Positive Feedback Count |    INT    |        | NULL |      |
|  상품이 속한 Division  |      Division Name      |  VARCHAR  |   50   | NULL |      |
| 상품이 속한 Department |     Department Name     |  VARCHAR  |   50   | NULL |      |
|      상품의 타입       |       Class Name        |  VARCHAR  |   50   | NULL |      |



### [실습2]  (30분)

### 1) Division별 평점 분포 계산

* Division별 평균 평점

```sql
SELECT	`Division Name`,
		AVG(Rating)
  FROM ProdReview
GROUP BY 1;  
```

* Department별 평균 평점

```sql
SELECT	`Department Name`,
		AVG(Rating)
  FROM ProdReview
GROUP BY 1;  
```

* 평점이 낮은 Trend의 평점이 3점 이하인 데이타

```sql
SELECT *
  FROM ProdReview
 WHERE `Department Name` = 'Trend'
   AND Rating <=3; 
```

* 평점이 낮은 Trend의 평점이 3점 이하인 데이타
* 연령대별 그룹핑 : case when

```sql
SELECT age,
		CASE WHEN age BETWEEN 10 AND 19 THEN '1019'
			 WHEN age BETWEEN 20 AND 29 THEN '2019'
			 WHEN age BETWEEN 30 AND 39 THEN '3019'
			 WHEN age BETWEEN 40 AND 49 THEN '4019'
			 WHEN age BETWEEN 50 AND 59 THEN '5019'
			 WHEN age BETWEEN 60 AND 69 THEN '6019'
			 WHEN age BETWEEN 70 AND 79 THEN '7019'
			 WHEN age BETWEEN 80 AND 89 THEN '8019'
			 WHEN age BETWEEN 90 AND 99 THEN '9019' END AS ageband
  FROM ProdReview
 WHERE `Department Name` = 'Trend'
   AND Rating <=3;
```

* 연령대별 그룹핑 : FLOOR

```SQL
SELECT	age,
		FLOOR(age/10) * 10 AS ageband
  FROM ProdReview
 WHERE `Department Name` = 'Trend'
   AND Rating <=3;
```

* Trend 평점3 점 이하 리뷰 연령 분포

```sql
SELECT	FLOOR(age/10) * 10 AS ageband,
		count(*)
  FROM ProdReview
 WHERE `Department Name` = 'Trend'
   AND Rating <=3
GROUP BY 1
ORDER BY 2 DESC;
```

* Trend Department별 연령별 리뷰 수

```sql
SELECT	FLOOR(age/10) * 10 AS ageband,
		count(*)
  FROM 	ProdReview		
 WHERE `Department Name` = 'Trend'
GROUP BY 1
ORDER BY 2 DESC;
```

* Trend 50대 3점 이하 리뷰 수

```sql
SELECT	*
  FROM 	ProdReview		
 WHERE `Department Name` = 'Trend'
   AND FLOOR(age/10) * 10 = 50
   AND Rating <= 3
GROUP BY 1
ORDER BY 2 DESC;
```



### 2) 상품의 주요 Complain

* Department별 평점이 낮은 10개 상품 조회

```SQL
SELECT	`Department Name`,
		`Clothing ID`,
		avg(rating)
  FROM	ProdReview
GROUP BY 1,2;
```

* Department별 순위생성

```sql
SELECT	*,
		ROW_NUMBER() OVER(PARTITION BY `Department Name` ORDER BY avg_rating) RATING
  FROM	(SELECT	`Department Name`,
				`Clothing ID`,
				avg(rating) avg_rating
	 	  FROM	ProdReview
		GROUP BY 1,2
	     ) A;
```

* Department별 1~10위까지 조회

```sql
SELECT *
  FROM
	(SELECT	*,
			ROW_NUMBER() OVER(PARTITION BY `Department Name` ORDER BY avg_rating) RATING
	   FROM	(SELECT	`Department Name`,
					`Clothing ID`,
					avg(rating) avg_rating
		 	  FROM	ProdReview
			GROUP BY 1,2
	         ) A
	) B
WHERE B.RATING <= 10;
```

* Department 1~10위까지의 리뷰 내용 조회

```sql
-- temp_ration temp table 생성
CREATE TEMPORARY TABLE TEMP_RATING AS
SELECT *
  FROM
	(SELECT	*,
			ROW_NUMBER() OVER(PARTITION BY `Department Name` ORDER BY avg_rating) RATING
	   FROM	(SELECT	`Department Name`,
					`Clothing ID`,
					avg(rating) avg_rating
		 	  FROM	ProdReview
			GROUP BY 1,2
	         ) A
	) B
WHERE B.RATING <= 10;

-- temp_ration, prodreview join 수행
SELECT b.*
  FROM temp_rating A
  	INNER JOIN prodreview B 
  		ON A.`Clothing ID` = B.`Clothing ID`
  	WHERE a.`Department Name`='Bottoms';
```



### 3) 연령별 Worst Department

* 연령, Department별 가장 낮은 점수

```SQL
SELECT	`Department Name`,
		floor(age/10)*10 ageband,
		avg(rating) avg_rating
  FROM	ProdReview
GROUP BY 1,2;
```

* rank 생성

```sql
SELECT	*,
		ROW_NUMBER() OVER(PARTITION BY `ageband` ORDER BY avg_rating) RATING
  FROM	(SELECT	`Department Name`,
				floor(age/10)*10 ageband,
				avg(rating) avg_rating
	 	  FROM	ProdReview
		GROUP BY 1,2
	     ) A;
```

* rank가 1인 데이터 조회

```SQL
SELECT *
  FROM (      
SELECT	*,
		ROW_NUMBER() OVER(PARTITION BY `ageband` ORDER BY avg_rating) RATING
  FROM	(SELECT	`Department Name`,
				floor(age/10)*10 ageband,
				avg(rating) avg_rating
	 	  FROM	ProdReview
		GROUP BY 1,2
	     ) A
) B
WHERE B.RATING = 1;
```



### 4) Size Complain

* 리뷰 내용(REVIEW TEXT)에 SIZE 단어 포함 시 case when 구문 사용하여 1, 0으로 구분

```SQL
SELECT	`REVIEW TEXT`,
		CASE WHEN `REVIEW TEXT` LIKE '%SIZE%' THEN 1 ELSE 0 END SIZE_YN		
  FROM prodreview;
```

* 리뷰 내용(REVIEW TEXT)에 SIZE, LARGE, LOOSE, SMALL, TIGHT 단어 포함 건수 계산

  : 전체

```sql
SELECT	SUM(CASE WHEN `REVIEW TEXT` LIKE '%SIZE%' THEN 1 ELSE 0 END) NUM_SIZE,
		SUM(CASE WHEN `REVIEW TEXT` LIKE '%LARGE%' THEN 1 ELSE 0 END) NUM_LARGE,
		SUM(CASE WHEN `REVIEW TEXT` LIKE '%LOOSE%' THEN 1 ELSE 0 END) NUM_LOOSE,
		SUM(CASE WHEN `REVIEW TEXT` LIKE '%SMALL%' THEN 1 ELSE 0 END) NUM_SMALL,
		SUM(CASE WHEN `REVIEW TEXT` LIKE '%TIGHT%' THEN 1 ELSE 0 END) NUM_TIGHT,        
		COUNT(*) NUM_TOTAL
  FROM prodreview;
```

* 리뷰 내용(REVIEW TEXT)에 SIZE, LARGE, LOOSE, SMALL, TIGHT 단어 포함 건수 계산

  : Department별 

```sql
SELECT	`Department Name`,
		SUM(CASE WHEN `REVIEW TEXT` LIKE '%SIZE%' THEN 1 ELSE 0 END) NUM_SIZE,
		SUM(CASE WHEN `REVIEW TEXT` LIKE '%LARGE%' THEN 1 ELSE 0 END) NUM_LARGE,
		SUM(CASE WHEN `REVIEW TEXT` LIKE '%LOOSE%' THEN 1 ELSE 0 END) NUM_LOOSE,
		SUM(CASE WHEN `REVIEW TEXT` LIKE '%SMALL%' THEN 1 ELSE 0 END) NUM_SMALL,
		SUM(CASE WHEN `REVIEW TEXT` LIKE '%TIGHT%' THEN 1 ELSE 0 END) NUM_TIGHT,        
		COUNT(*) NUM_TOTAL
  FROM prodreview
GROUP BY 1;
```

* 리뷰 내용(REVIEW TEXT)에 SIZE, LARGE, LOOSE, SMALL, TIGHT 단어 포함 건수 계산

  : 연령대별, Department별 

```sql
SELECT	floor(age/10)*10,
		`Department Name`,
		SUM(CASE WHEN `REVIEW TEXT` LIKE '%SIZE%' THEN 1 ELSE 0 END) NUM_SIZE,
		SUM(CASE WHEN `REVIEW TEXT` LIKE '%LARGE%' THEN 1 ELSE 0 END) NUM_LARGE,
		SUM(CASE WHEN `REVIEW TEXT` LIKE '%LOOSE%' THEN 1 ELSE 0 END) NUM_LOOSE,
		SUM(CASE WHEN `REVIEW TEXT` LIKE '%SMALL%' THEN 1 ELSE 0 END) NUM_SMALL,
		SUM(CASE WHEN `REVIEW TEXT` LIKE '%TIGHT%' THEN 1 ELSE 0 END) NUM_TIGHT,        
		COUNT(*) NUM_TOTAL
  FROM prodreview
GROUP BY 1,2
ORDER BY 1,2;
```

* 리뷰 내용(REVIEW TEXT)에 SIZE, LARGE, LOOSE, SMALL, TIGHT 단어 포함 건수 계산

  : 연령대별, Department별 비중 계산

```SQL
SELECT	floor(age/10)*10,
		`Department Name`,
		SUM(CASE WHEN `REVIEW TEXT` LIKE '%SIZE%' THEN 1 ELSE 0 END) / COUNT(*) NUM_SIZE,
		SUM(CASE WHEN `REVIEW TEXT` LIKE '%LARGE%' THEN 1 ELSE 0 END) / COUNT(*) NUM_LARGE,
		SUM(CASE WHEN `REVIEW TEXT` LIKE '%LOOSE%' THEN 1 ELSE 0 END) / COUNT(*) NUM_LOOSE,
		SUM(CASE WHEN `REVIEW TEXT` LIKE '%SMALL%' THEN 1 ELSE 0 END) / COUNT(*) NUM_SMALL,
		SUM(CASE WHEN `REVIEW TEXT` LIKE '%TIGHT%' THEN 1 ELSE 0 END) / COUNT(*) NUM_TIGHT,        
		COUNT(*) NUM_TOTAL
  FROM prodreview
GROUP BY 1,2
ORDER BY 1,2;
```
