import tkinter
from tkinter import messagebox
from tkinter import StringVar
import pymssql
import datetime
import tkinter.font
def drawGUI():
    global user
    global pas
    global win
    username=None
    user=None
    pas=None
    win=None
    win=tkinter.Tk()
    win.title('小小日记登陆系统')
    win.geometry("300x220")
    #win.iconbitmap('cat.png')
    usernameLab=tkinter.Label(win,text='用户名：',width=10).place(x=20,y=60)
    user=tkinter.StringVar()
    usernameEn=tkinter.Entry(win,width=20,textvariable=user,bg='#FFE1FF').place(x=75,y=60)
    passwordLab=tkinter.Label(win,text='密码：',width=10).place(x=20,y=90)
    pas=tkinter.StringVar()
    passwordEn=tkinter.Entry(win,width=20,textvariable=pas,show='*',bg='#FFE1FF').place(x=75,y=90)
    loginBut=tkinter.Button(win,text='登陆',width=8,bg='#00ffff',command=loginEvent) 
    loginBut.place(x=75,y=120)
    loginBut.bind('<Button-1>',loginEvent)
    registBut=tkinter.Button(win,text='注册',width=8,bg='#00ffff',command=registEvent).place(x=150,y=120)
    win.bind("<KeyPress-Return>",loginEvent)
    win.mainloop()
def loginEvent(event):
    global username
    username=str(user.get())
    password=str(pas.get())
    if username=="" or password=="":
        print("用户名或密码不能为空")
    conn=connectSql()
    selectPass=selectUser(conn,username)
    closeConn(conn)
    if selectPass==1:
        messagebox.showinfo("info","该用户未注册")
        return 
    if password==selectPass:
        #messagebox.showinfo("info","登陆成功")##数据库链接判断用户名密码是否正确
        win.destroy()
        indexGUI()
    else:
        messagebox.showinfo("info","密码错误")
def connectSql():
    conn=pymssql.connect(server='127.0.0.1',user='sa',password='266289',database='person')
    print(datetime.datetime.now().strftime('%Y-%m-%d')+"数据库链接成功")
    return conn
def closeConn(conn):
    print(datetime.datetime.now().strftime('%Y-%m-%d')+"数据库已经关闭链接")
    conn.close()
def selectUser(conn,username):
    row=[]
    cursor=conn.cursor()
    cursor.execute('select *from logonTable where username=%s',username)
    row = cursor.fetchone()
    if row==None:
        return 1
    else:
        print(datetime.datetime.now().strftime('%Y-%m-%d')+"数据库查询成功")
        return row[1]
def insertUser(conn,username,password):
    cursor=conn.cursor()
    cursor.executemany("insert into logonTable values (%s, %s)",[(username,password)])
    conn.commit()
    print(username+"插入成功")

def registEvent():
    name=str(user.get())
    word=str(pas.get())
    conn=connectSql()
    sign=varselectUser(conn,name)
    if sign==1:
        messagebox.showinfo("info","该用户已经注册")
        return
    if name==" " or word==" ":
        print("用户名或密码不能为空")
        return
    if len(word)<=6:
        messagebox.showinfo("info","密码的长度必须大于6哦")
        return
    if word.isdigit():
        messagebox.showinfo("info","密码不能只含有数字")
        return
    if word.isalpha():
        messagebox.showinfo("info","密码不能只含有字母")
        return
    
    print("name:"+name+"word:"+word)
    insertUser(conn,name,word)
    closeConn(conn)
    messagebox.showinfo("info","注册成功")
def varselectUser(conn,name):
    row=[]
    cursor=conn.cursor()
    cursor.execute('select *from logonTable where username=%s',name)
    row = cursor.fetchone()
    if row==None:
        return 0
    else:
        return 1

def indexGUI():
    global exitInsert
    exitInsert=0
    index=tkinter.Tk()
    index.title("小小日记")
    f1=tkinter.Frame(index,bg='#00ffff')
    f1.pack()
    index.geometry("500x500")
    menu1=tkinter.Menu(index)
    fileMenu=tkinter.Menu(menu1)
    editMenu=tkinter.Menu(menu1)
    fileMenu.add_command(label='查看历史日记',command=findTextGUI)
    fileMenu.add_command(label='保存(Ctr+s)',command=insertTest)
    fileMenu.add_command(label='退出',command=exitEvent)
    editMenu.add_command(label='关于',command=aboutGUI)
    #editMenu.add_command(label="退出",command=test)
    #editMenu.add_command(label="退出",command=test)
    menu1.add_cascade(label='文件',menu=fileMenu)
    menu1.add_cascade(label='编辑',menu=editMenu)
    index['menu']=menu1
    global diaryText
    font1=tkinter.font.Font(family='Fixdsys',size=14)
    font2=tkinter.font.Font(family='Fixdsys',size=14)
    helloLab=tkinter.Label(index,text=username+"你好！！请在下面记录你的日记(记得保存哦)",font=font2,bg="#FFDEAD")
    helloLab.pack()

    day=str('今天是:'+datetime.datetime.now().strftime('%Y-%m-%d'))
    print(day)
    dayLab=tkinter.Label(index,text=day,font=font2,bg='#CD9B9B')
    dayLab.pack()

    diaryText=tkinter.Text(index,width="500",height="500",bg='#F8F8FF',font=font1)
    diaryText.pack()
    diaryText.focus()
    index.bind('<Control-KeyPress-s>',insertTest)          #光标默认位置
    index.mainloop
def exitEvent():
    exit()
def insertTest(event):
    conn=connectSql()
    indexText=str(diaryText.get(0.0,tkinter.END))
    time=str(datetime.datetime.now().strftime('%Y-%m-%d'))
    cursor=conn.cursor()
    cursor.executemany("insert into testTable values (%s,%s, %s)",[(username,time,indexText)])
    conn.commit()
    closeConn(conn)
    messagebox.showinfo('info','日记保存成功')
    exitInsert==1
def test():
    print('测试')
def findTextGUI():
    global getText
    findGui=tkinter.Tk()
    findGui.title('查看历史日记')
    findGui.geometry("500x400")
    font1=tkinter.font.Font(family='Fixdsys',size=28,weight='bold')
    timeLab=tkinter.Label(findGui,text='请输入日期(2018-11-26):',width=30,font=font1).place(x=75,y=15)
    global time
    time=tkinter.Text(findGui,width="30",height="1",bg='#C1FFC1',font=font1)
    time.place(x=75,y=40)
    findBut=tkinter.Button(findGui,text='查询',width=8,bg='#8B6969',height='1',command=selectTime).place(x=400,y=40)
    getText=tkinter.Text(findGui,width="45",height="15",font=font1,bg='#F8F8FF')
    getText.place(x=2,y=80)
    findGui.mainloop()
def selectTime():
    getText.delete('1.0','end')
    getTime=str(time.get(0.0,tkinter.END))
    conn=connectSql()
    row=[]
    cursor=conn.cursor()
    Time=getTime.strip()
    cursor.execute('select *from testTable where username=%s and time=%s',(username,Time))
    print('username'+username)
    row = cursor.fetchone()
    if row==None:
        messagebox.showinfo("info","你在这天没有写过日记或忘记保存了哦！！")
        return
    print(row)
    closeConn(conn)
    font1=tkinter.font.Font(family='Fixdsys',size=10)
    getText.insert(0.0,(row[1]+'    :'+row[2]))
def aboutGUI():
    aboutGui=tkinter.Tk()
    abouGui.title('关于我们')
    abouGui.geometry('500x500')
    abouGui.mainloop()
    print("test")
drawGUI() #144