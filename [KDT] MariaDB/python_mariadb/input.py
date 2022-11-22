import pymysql

# DB 커넥션 객체 생성
conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='1234', db='sqldb')

# 커서 객체 생성
cur = conn.cursor()

while True:
    userid  = input("사용자 ID : ")
    if userid == "":
        break
        
    name    = input("사용자 이름 : ")
    birthYear = input("사용자 출생연도 : ")
    addr    = input("주소 : ")

    # 쿼리문 작성
    sql = "INSERT INTO userTBL(userID, name, birthYear, addr) VALUES('" + userid + "','" + name + "'," + birthYear + ",'" + addr + "');"

    # 쿼리문 실행
    cur.execute(sql)

# commit 수행
conn.commit()

# DB 커넥션 close
conn.close()