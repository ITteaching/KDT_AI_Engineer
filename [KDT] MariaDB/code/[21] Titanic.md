# 21. Titanic

## 1. Dataset Download

* https://www.kaggle.com/datasets/pavlofesenko/titanic-extended/download

* full.csv 압축해제



## 2. titanicDB 생성

* create database titanicDB
* full.csv upload



## 3. titanic TABLE

|     Column Name     |  Column ID  | Data Type | Length |   Null   | Key  |
| :-----------------: | :---------: | :-------: | :----: | :------: | :--: |
|       승객ID        | passengerid |    INT    |        | NOT NULL |  PK  |
|      생존 여부      |  survived   |  DOUBLE   |        |          |      |
|     티켓 클래스     |   pclass    |    INT    |        |          |      |
|        성별         |     sex     |  VARCHAR  |   10   |          |      |
| 탑승 형제/배우자 수 |    sibsp    |    INT    |        |          |      |
|  탑승 부모/자녀 수  |    parch    |    INT    |        |          |      |
|      티켓 번호      |   ticket    |  VARCHAR  |   50   |          |      |
|      티켓 비용      |    fare     |  DOUBLE   |        |          |      |
|      객실 번호      |    cabin    |  VARCHAR  |   50   |          |      |
|      승선 항구      |  embarked   |  VARCHAR  |   50   |          |      |
|       위키 ID       |   wikiid    |    INT    |        |          |      |
|        이름         |  name_wiki  |  VARCHAR  |  255   |          |      |
|        연령         |  age_wiki   |  VARCHAR  |  255   |          |      |
|        고향         |  hometown   |  VARCHAR  |  255   |          |      |
|       출발지        |   boarded   |  VARCHAR  |  255   |          |      |
|       목적지        | destination |  VARCHAR  |  255   |          |      |
|      생존 보트      |  lifeboat   |  VARCHAR  |  255   |          |      |
|        body         |    body     |  VARCHAR  |  255   |          |      |
|        class        |    class    |    INT    |        |          |      |



## 4. 요인별 생존 여부 관계

### 1) 성별

* 타이타닉 데이타 구조 파악

```sql
USE titanicDB;
SELECT * 
  FROM titanic
 LIMIT 10;
```

* 성별에 따른 생존자 수 확인

   : 탑승은 남자가 많으나, 여성의 생존자 수가 많음

```sql
SELECT sex, count(passengerid), sum(survived)
  FROM titanic
 GROUP BY sex;
```

* 성별 탑승자 수와 생존자 수의 비율 확인

   : 여성의 생존 비율이 높음

```sql
SELECT	sex,
		count(passengerid),
		sum(survived),
		sum(survived) / count(passengerid)
  FROM titanic
 GROUP BY sex;
```



### 2) 연령, 성별

* 연령을 연령대로 변경

```sql
SELECT floor(age/10)*10, age
  FROM titanic;
```

* 연령대별 탑승자수, 생존자수, 생존비율 확인

   : 20대 수가 가장 많았고, 70대를 제외하면 60대 생존율이 가장 낮았음

   : 0세에서 9세까지 가장 높음

```sql
SELECT	floor(age/10)*10,
		count(passengerid),
		sum(survived),
		sum(survived) / count(passengerid)
  FROM titanic
 GROUP BY floor(age/10)*10; 
```

* 연령에 성별 추가하여 확인

   : 50대 여성의 생존비율이 가장 높고, 10대 남성의 생존비율이 가장 낮음

```sql
SELECT	floor(age/10)*10,
		sex,
		count(passengerid),
		sum(survived),
		sum(survived) / count(passengerid)
  FROM titanic
 GROUP BY floor(age/10)*10, sex; 
```

* 남성, 여성의 동일 연령대별 생존율 차이 구하기

```sql
-- 남성과 여성의 데이타 셋을 분리하기
SELECT	floor(age/10)*10 ageband,
		sex,
		count(passengerid) pinwon,
		sum(survived) sinwon,
		sum(survived) / count(passengerid) sratio
  FROM titanic
 GROUP BY floor(age/10)*10, sex
 HAVING sex = 'male'; 
 
SELECT	floor(age/10)*10 ageband,
		sex,
		count(passengerid) pinwon,
		sum(survived) sinwon,
		sum(survived) / count(passengerid) sratio
  FROM titanic
 GROUP BY floor(age/10)*10, sex
 HAVING sex = 'female'; 
 
-- 분리한 두 개에 데이타셋을 join으로 하나의 데이타셋으로 만들기 
 SELECT a.ageband, a.sratio male_sratio, b.sratio femail_sratio, b.sratio-a.sratio sratio_diff
   FROM (SELECT	floor(age/10)*10 ageband,
				sex,
				count(passengerid) pinwon,
				sum(survived) sinwon,
				sum(survived) / count(passengerid) sratio
		  FROM titanic
		 GROUP BY floor(age/10)*10, sex
		 HAVING sex = 'male' ) A
		 LEFT JOIN 
		 (
         SELECT	floor(age/10)*10 ageband,
				sex,
				count(passengerid) pinwon,
				sum(survived) sinwon,
				sum(survived) / count(passengerid) sratio
		  FROM titanic
		GROUP BY floor(age/10)*10, sex
		HAVING sex = 'female' ) B
        ON a.ageband = b.ageband;
```



### 3) 객실 등급(pclass)

* 객실 등급별 승객 수와 생존자 수, 생존율 계산

   : 1등급  > 2등급 > 3등급 생존율 보임

```sql
SELECT	pclass,
		count(passengerid),
		sum(survived),
		sum(survived) / count(passengerid)
  FROM titanic
 GROUP BY pclass;
```

* 객실 등급별 남여별 생존율

```sql
SELECT	pclass,
		sex,
		count(passengerid),
		sum(survived),
		sum(survived) / count(passengerid)
  FROM titanic
 GROUP BY pclass, sex;
```

* 객실 등급별 남여별 연령별 생존율

```sql
SELECT	pclass,
		sex,
		floor(age/10)*10 ageband,
		count(passengerid),
		sum(survived),
		sum(survived) / count(passengerid)
  FROM titanic
 GROUP BY pclass, sex, floor(age/10)*10
 ORDER BY sex, pclass;
```



### 4) 승선 항구(embarked)

* 승선 항구별 승객 수

```sql
SELECT embarked, count(*)
  FROM titanic
GROUP BY embarked;
```

* 승선 항구별, 성별 승객 수

```sql
SELECT embarked, sex, count(*)
  FROM titanic
GROUP BY embarked, sex;
```

* 승선 항구별, 성별 승객 비중(%)

  : 위 두개의 데이타셋을 결합하여 쿼리 작성

```sql
SELECT b.embarked, b.sex, b.n_count, a.t_count, b.n_count / a.t_count
  FROM
  	(	
      SELECT embarked, count(*) t_count
		FROM titanic
	  GROUP BY embarked
	) A
	INNER JOIN
		(
    	  SELECT embarked, sex, count(*) n_count
			FROM titanic
		  GROUP BY embarked, sex
	    ) B
		ON A.embarked = B.embarked;
```



### 5) 탑승객 분석

* 출발지, 도착지별 승객 수

```sql
SELECT boarded, destination, count(*)
  FROM titanic
GROUP BY boarded, destination
ORDER BY 3 DESC;
```

* 상위 경로 5개 조회

```SQL
SELECT *
  FROM (
		SELECT boarded, destination, count(*) t_count
		  FROM titanic
		GROUP BY boarded, destination
		ORDER BY t_count DESC
      ) base
LIMIT 5;
```

* 상위 경로 5개에 해당하는 승객들의 이름 조회

```SQL
SELECT a.name_wiki, a.boarded, a.destination
  FROM titanic a
  	INNER JOIN (
        		SELECT *
				  FROM (
						SELECT boarded, destination, count(*) t_count
						  FROM titanic
						GROUP BY boarded, destination
						ORDER BY t_count DESC
				      ) route
				LIMIT 5
    			) b
		ON a.boarded = b.boarded
           AND a.destination = b.destination;
```

* 참고) OVER 함수 이용

```sql
SELECT	*,
		ROW_NUMBER() OVER(ORDER BY n_count DESC) rank
  FROM (
		SELECT boarded, destination, count(*) n_count
		  FROM titanic
		GROUP BY boarded, destination
      ) route;
      
SELECT a.name_wiki, a.boarded, a.destination
  FROM titanic a
  	INNER JOIN (
        		SELECT	*,
						ROW_NUMBER() OVER(ORDER BY n_count DESC) rank
  				  FROM (
						SELECT boarded, destination, count(*) n_count
						  FROM titanic
						GROUP BY boarded, destination
				      ) route
				LIMIT 5
    			) b
		ON a.boarded = b.boarded
           AND a.destination = b.destination;      
```

* Hometown별 탑승객 수 및 생존율

```SQL
SELECT hometown, count(*), sum(survived), sum(survived) / count(*) 
  FROM titanic
GROUP BY hometown
ORDER BY 2 DESC;
```

* 탑승객 수가 10명 이상이면서 생존율이 50% 이상인 hometown 정보

```sql
SELECT hometown, count(*), sum(survived), sum(survived) / count(*) 
  FROM titanic
GROUP BY hometown
HAVING count(*) >= 10
  AND sum(survived) / count(*) >= 0.5;
```
