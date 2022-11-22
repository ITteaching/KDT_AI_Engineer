## [8장] 테이블과 뷰

* 기준테이블명으로 외래 키 테이블 조회

```SQL
SELECT *
  FROM information_schema.check_constraints 
 WHERE constraint_schema = 데이타베이스명 AND table_name = 테이블명;
```



## [09장] 인덱스

* 인덱스 생성

```SQL
ALTER TABLE 테이블명
	CREATE INDEX 인덱스명(컬럼명);
	
CREATE INDEX 인덱스명 ON 테이블명(컬럼명);
```

* 인덱스 삭제

```SQL
ALTER TABLE 테이블명
	DROP INDEX 인덱스명
	
DROP INDEX 인덱스명 ON 테이블명	
```

DROP INDEX 인덱스명 ON 테이블명	



### [11장] 전체 텍스트 검색과 파티션

* 전체 텍스트 인덱스 생성

```SQL
CREATE FULLTEXT INDEX idx_description ON FulltextTbl(description);
```

* 전체 텍스트 인덱스로 만들어진 단어 확인

```SQL
SELECT word, doc_count, doc_id, position
  FROM INFORMATION_SCHEMA.INNODB_FT_INDEX_TABLE;
```

* 전체 텍스트 검색을 위한 쿼리

```SQL
MATCH (col1, col2, ...) AGAINST (expr [search_modifier])

search_modifier:
{
	IN NATURAL LANGUAGE MODE
	| IN BOOLEAN MODE
	| WITH QUERY EXPNASION  -- 검색완료 후 검색된 텍스트와 관련있는 내용을 추가로 검색한 결과 제공함
}
```

* 중지(제외) 단어 설정

```sql
-- 중지(제외) 단어 테이블 생성 (컬럼명은 반드시 소문자 'value'이어야만 함)
CREATE TABLE user_stopword (value VARCHAR(30));

-- 중지(제외) 단어 테이블 입력
INSERT INTO user_stopword VALUES('그는'), ('그리고'), ('극에');

-- innodb GLOBAL 변수 설정 및 확인
SET GLOBAL innodb_ft_server_stopword_table = 'fulltextdb/user_stopword';
SHOW GLOBAL VARIABLES LIKE 'innodb_ft_server_stopword_table';
```

