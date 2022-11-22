import pymysql

# DB 커넥션 객체 생성
conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='1234', db='sqldb')

# 커서 객체 생성
cur = conn.cursor()

# 쿼리문 작성
sql = "SELECT userid, name, birthYear, addr FROM userTBL;"

# 쿼리문 실행
cur.execute(sql)

print("ID\t이름\t출생연도 주소")
print("-" * 30)
# 데이타 출력
while True:
    row = cur.fetchone()
    if row == None:
        break
    userid  = row[0]
    name    = row[1]
    birthYear = row[2]
    addr     = row[3]

    print(f'{userid}\t{name}\t{birthYear}\t{addr}')
    # print(row)

# DB 커넥션 close
conn.close()