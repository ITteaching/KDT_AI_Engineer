# 12. 파이썬과 MariaDB 연동

# [실습 1 : 6 ~ 7p]

* 데이타 입력 기본 예제

```SQL
-- 데이터 입력 예제
import pymysql

conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='1234', db='sqldb')
cur = conn.cursor()    
sql = "INSERT INTO userTBL(userID, name, birthYear, addr) VALUES('KIM', '김씨', 1991, '서울');"
cur.execute(sql)
conn.commit()
conn.close()
```



# [실습 2 : 8 ~ 9p]

* 데이타 조회 기본 예제

```SQL
-- 데이터 조회 예제
import pymysql

conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='1234', db='sqldb')
cur = conn.cursor()
sql = "SELECT userid, name, birthYear, addr FROM userTBL;"
cur.execute(sql)

while True:
	row = cur.fetchone()
	if row == None:
		break
    userid  = row[0]
    name    = row[1]
    birthYear = row[2]
    addr     = row[3]

	print(userid, name, birthYear, addr)

conn.close()
```

* JOIN 조회 기본 예제

```SQL
-- 구매 테이블(buytbl), 회원 테이블(usertbl)로부터 
-- 구매 이력이 있는이름/주소/연락처, 구매물품명/구매가격/구매수량 조회하기

import pymysql

conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='1234', db='sqldb')
cur = conn.cursor()

sql = """SELECT b.userid, b.name, b.addr, b.mobile1, b.mobile2, a.prodname, a.price, a.amount
		   FROM buytbl a
           	 INNER JOIN usertbl b
	         	ON a.userid = b.userid;"""
 
cur.execute(sql)

while True:
	row = cur.fetchone()
	if row == None:
		break
	userid  = row[0]
	name    = row[1]
	addr	= row[2]
	mobile1	= row[3]
	mobile2 = row[4]
	prodname = row[5]
	price	= row[6]
	amount	= row[7]

	print(userid, name, addr, mobile1, mobile2, prodname, price, amount)

conn.close()
```



# [실습 3 : 종합 실습]

### 1) input.py

* userid, name, birthYear, addr CMD 창에서 입력받음
* sqlDB의 userTBL에 입력받은 데이타 저장
* userid 입력값이 없는 경우 종료

```Python
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
    sql = "INSERT INTO userTBL(userID, name, birthYear, addr) VALUES('"+userid+"','"+name+"',"+birthYear+",'"+addr+"');"

    # 쿼리문 실행
    cur.execute(sql)

# commit 수행
conn.commit()

# DB 커넥션 close
conn.close()
```

### 2) list.py

* CMD 창에 userTBL 테이블의 userid, name, birthYear, addr 컬럼 데이타 모두 출력하기

```Python
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
```

### 3) gui.py

```python
from ctypes import addressof
import pymysql
from tkinter import *
import tkinter.messagebox

def insertData():
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='1234', db='sqldb')
    cur = conn.cursor()    

    # 에디터박스 데이타 가져오기
    userid  = edt1.get()
    name    = edt2.get()
    birthYear = edt3.get()
    addr    = edt4.get()

    try:
        sql = "INSERT INTO userTBL(userID, name, birthYear, addr) VALUES('" + userid + "','" + name + "','" + birthYear + "','" + addr + "');"
        cur.execute(sql)
    except:
        tkinter.messagebox.showerror("오류", "데이터 저장시 오류가 발생하였습니다.")
    else:
        tkinter.messagebox.showinfo("성공", "데이터가 정상적으로 저장되었습니다.")

    conn.commit()
    conn.close()

def selectData():
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='1234', db='sqldb')
    cur = conn.cursor()
    sql = "SELECT userid, name, birthYear, addr FROM userTBL;"
    cur.execute(sql)

    # 리스트박스 내용 삭제
    listBox1.delete(0,END)
    listBox2.delete(0,END)
    listBox3.delete(0,END)
    listBox4.delete(0,END)

    # 리스트박스 타이틀 추가
    listBox1.insert(END,"ID"); listBox1.insert(END,"----------");    
    listBox2.insert(END,"이름"); listBox2.insert(END,"----------");    
    listBox3.insert(END,"생년월일"); listBox3.insert(END,"----------");    
    listBox4.insert(END,"주소"); listBox4.insert(END,"----------");    

    # 데이타 출력
    while True:
        row = cur.fetchone()
        if row == None:
            break
        userid  = row[0]
        name    = row[1]
        birthYear = row[2]
        addr     = row[3]

        # 리스트박스에 데이타 추가
        listBox1.insert(END, userid)            
        listBox2.insert(END, name)            
        listBox3.insert(END, birthYear)            
        listBox4.insert(END, addr)            

    conn.close()

#################프로그램 시작##################################################

main = Tk()
main.title("GUI 입력/조회 프로그램")
main.geometry("700x300")

# 입력프레임, 조회프레임 생성
edtFrame = Frame(main)
edtFrame.pack()
listFrame = Frame(main)
# listFrame.pack()
listFrame.pack(side=BOTTOM, fill=BOTH, expand=1)

# label1 = Label(edtFrame, text="ID", width=5); label1.pack(side=LEFT, padx=5, pady=10)
# 4개 입력박스 생성
edt1 = Entry(edtFrame, width=10); edt1.pack(side=LEFT, padx=10, pady=10)
edt2 = Entry(edtFrame, width=10); edt2.pack(side=LEFT, padx=10, pady=10)
edt3 = Entry(edtFrame, width=10); edt3.pack(side=LEFT, padx=10, pady=10)
edt4 = Entry(edtFrame, width=10); edt4.pack(side=LEFT, padx=10, pady=10)

# 저장, 조회 버튼 생성
btnInsert = Button(edtFrame, text="저장", command=insertData); btnInsert.pack(side=LEFT, padx=10, pady=10)
btnSelect = Button(edtFrame, text="조회", command=selectData); btnSelect.pack(side=LEFT, padx=10, pady=10)

# 조회 리스트박스 4개 생성
listBox1 = Listbox(listFrame); listBox1.pack(side=LEFT, padx=10, pady=10)
listBox2 = Listbox(listFrame); listBox2.pack(side=LEFT, padx=10, pady=10)
listBox3 = Listbox(listFrame); listBox3.pack(side=LEFT, padx=10, pady=10)
listBox4 = Listbox(listFrame); listBox4.pack(side=LEFT, padx=10, pady=10)

main.mainloop()
```

