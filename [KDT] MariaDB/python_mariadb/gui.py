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