import tkinter as tk
from tkinter import ttk
import pymysql
from tkinter import messagebox

class hospital():
    def __init__(self,root):
        self.root = root
        self.root.title("Hospital Management ")
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        self.root.geometry(f"{self.width}x{self.height}+0+0")

        title =tk.Label(self.root,bg=self.clr(220,180,190),text="Hospital Management Sysytem ",bd=3,relief="groove",font=("Arial",50,"bold"))
        title.pack(side="top",fill="x")
        inframe =tk.Frame(self.root,bd=4,relief="groove",bg=self.clr(190,180,220)) 
        inframe.place(width=self.width/3,height=self.height-180,x=30,y=100)

        idLbl = tk.Label(inframe,text="Id ",bg=self.clr(190,180,220) ,font=("Arial",15,"bold"))
        idLbl.grid(row=0,column=0,padx=20,pady=15)
        self.idIn = tk.Entry(inframe,width=20,bd=2,font=("Arial",15))
        self.idIn.grid(row=0,column=1,padx=10,pady=15)

        nameLbl = tk.Label(inframe,text="Full Name",bg=self.clr(190,180,220) ,font=("Arial",15,"bold"))
        nameLbl.grid(row=1,column=0,padx=20,pady=15)
        self.nameIn =tk.Entry(inframe,width=20,bd=2,font=("Arial",15))
        self.nameIn.grid(row=1,column=1,padx=10,pady=20)

        bgLbl=tk.Label(inframe,text="Blood Group ",bg=self.clr(190,180,220) ,font=("Arial",15,"bold"))
        bgLbl.grid(row=2,column=0,padx=20,pady=15)
        self.bgIn=tk.Entry(inframe,width=20,bd=2,font=("Arial",15))
        self.bgIn.grid(row=2,column=1,padx=10,pady=15)

        desLbl =tk.Label(inframe,text="Desease ",bg=self.clr(190,180,220) ,font=("Arial",15,"bold"))
        desLbl.grid(row=3,column=0,padx=20,pady=15)
        self.desIn=tk.Entry(inframe,width=20,bd=2,font=("Arial",15))
        self.desIn.grid(row=3,column=1,padx=10,pady=15)

        hpLbl =tk.Label(inframe,text="Health Point",bg=self.clr(190,180,220) ,font=("Arial",15,"bold"))
        hpLbl.grid(row=4,column=0,padx=20,pady=15)
        self.hpIn=tk.Entry(inframe,width=20,bd=2,font=("Arial",15))
        self.hpIn.grid(row=4,column=1,padx=10,pady=15)

        madicationLbl =tk.Label(inframe,text="Madicine ",bg=self.clr(190,180,220) ,font=("Arial",15,"bold"))
        madicationLbl.grid(row=5,column=0,padx=20,pady=15)
        self.madicationIn=tk.Entry(inframe,width=20,bd=2,font=("Arial",15))
        self.madicationIn.grid(row=5,column=1,padx=10,pady=15)

        addressLbl =tk.Label(inframe,text="Address ",bg=self.clr(190,180,220) ,font=("Arial",15,"bold"))
        addressLbl.grid(row=6,column=0,padx=20,pady=15)
        self.addressIn=tk.Entry(inframe,width=20,bd=2,font=("Arial",15))
        self.addressIn.grid(row=6,column=1,padx=10,pady=15)

        okbtn = tk.Button(inframe,text="Admit",command=self.insertFunc,bd=2,relief="raised",bg="gray",font=("Arial",20,"bold"),width=20)
        okbtn.grid(padx=30,pady=60,columnspan=2)

        #detail frame
        self.detframe = tk.Frame(self.root,bd=4,relief="groove",bg=self.clr(190,220,180))
        self.detframe.place(width=self.width/2+110,height=self.height-180,x=self.width/3+60,y=100)

        pidLbl =tk.Label(self.detframe,text="Patient Id:",bg=self.clr(190,220,180),font=("Arial",15,))
        pidLbl.grid(row=0,column=0,padx=10,pady=15)
        self.pidin=tk.Entry(self.detframe,bd=1,width=12,font=("Arial",15))
        self.pidin.grid(row=0,column=1,padx=7,pady=15)

        medicbtn=tk.Button(self.detframe,command=self.madicsFun,text="Medication",width=10,bd=2,relief="raised",font=("Arial",15,"bold"))
        medicbtn.grid(row=0,column=2,padx=8,pady=15) 

        hpBtn = tk.Button(self.detframe,command=self.hPointFunc,text="Health Point",width=10,font=("Arial",15,"bold"))
        hpBtn.grid(row=0,column=3,padx=8,pady=15)

        disBtn = tk.Button(self.detframe,command=self.disFun,text="Discharge",width=10,font=("Arial",15,"bold"))
        disBtn.grid(row=0,column=4,padx=8,pady=15)
        self.tabFun()
        self.table.pack(fill="both",expand=1)

    def tabFun(self):
        self.tabFrame = tk.Frame(self.detframe,bd=3,relief="raised",bg="cyan")
        self.tabFrame.place(width=self.width/2+80,height=self.height-280,x=15,y=80)
        x_scroll =tk.Scrollbar(self.tabFrame,orient="horizontal")
        x_scroll.pack(side="bottom",fill="x")

        y_scroll =tk.Scrollbar(self.tabFrame,orient="vertical")
        y_scroll.pack(side="right",fill="y")

        self.table = ttk.Treeview(self.tabFrame,columns=("id","Name","b_group","desease","hpoint","madication","addr"),xscrollcommand=x_scroll.set,yscrollcommand=y_scroll.set)

        x_scroll.config(command=self.table.xview)
        y_scroll.config(command=self.table.yview)

        self.table.heading("id",text="Id")
        self.table.heading("Name",text="Name")
        self.table.heading("b_group",text="B_group")
        self.table.heading("desease",text="desease")
        self.table.heading("hpoint",text="h_point")
        self.table.heading("madication",text="madication")
        self.table.heading("addr",text="Address")

        self.table["show"]="headings"

        self.table.column("id",width=40)
        self.table.column("Name",width=100)
        self.table.column("b_group",width=40)
        self.table.column("desease",width=130)
        self.table.column("hpoint",width=40)
        self.table.column("madication",width=150)
        self.table.column("addr",width=180)

        self.table.pack(fill="both",expand=1)

    def clr(self,r,g,b):
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def insertFunc(self):
        id =int(self.idIn.get())
        name =(self.nameIn.get())
        bGroup =(self.bgIn.get())
        desease =(self.desIn.get())
        hp =(self.hpIn.get())
        madicin =(self.madicationIn.get())
        adr =(self.addressIn.get())
        if id and name and bGroup and desease and hp and madicin and adr:

            try:
                self.dbFun()
                query = f"insert into hospital (id,name,b_group,desease,h_point,madicin,addr) values(%s,%s,%s,%s,%s,%s,%s)"
                self.cur.execute(query,(id,name,bGroup,desease,hp,madicin,adr))
                self.con.commit()
                self.tabFun()
                self.table.delete(*self.table.get_children())
                self.cur.execute("select * from hospital where id = %s",id)
                data =self.cur.fetchone()
                self.table.insert('',tk.END,values=data)
                tk.messagebox.showinfo("Sucess",f"Patient {name} is admitted !")
                self.con.close()
                self.clearFun()
            except Exception as e:
                tk.messagebox.showerror("Error",f"Error {e}")
        else :
            tk.messagebox.showerror("Error","Fill all input Fields !")

    
    def dbFun(self):
        self.con =pymysql.connect(host="localhost",user="root",passwd="192009",database="hospital")
        self.cur = self.con.cursor()

    def clearFun(self):
        self.idIn.delete(0,tk.END)
        self.nameIn.delete(0,tk.END)
        self.bgIn.delete(0,tk.END)
        self.desIn.delete(0,tk.END)
        self.hpIn.delete(0,tk.END)
        self.madicationIn.delete(0,tk.END)
        self.addressIn.delete(0,tk.END)

    def madicsFun(self):
        pid =int(self.pidin.get())
        if pid:
            try:
                self.dbFun()
                query = f"select * from hospital where id = %s"
                self.cur.execute(query,pid)
                data = self.cur.fetchone()
                self.tabFun()
                self.table.delete(*self.table.get_children())
                self.table.insert('',tk.END,values=data)


            except Exception as e:
                tk.messagebox.showerror("Error",f"Error {e}")

        else :
            tk.messagebox.showerror("Error","Must Enter Patient ID")

    def hPointFunc(self):
        self.pointframe = tk.Frame(self.root,bg="light gray",bd=3,relief="ridge")
        self.pointframe.place(width=400,height=200,x=500,y=200)

        lbl = tk.Label(self.pointframe,text="Enter Point : ",bg="light gray",font=("Arial",15,"bold"))
        lbl.grid(row=0,column=0,padx=20,pady=30)
        self.pointIn = tk.Entry(self.pointframe,width=17,bd=2,font=("Arial",15,"bold"))
        self.pointIn.grid(row=0,column=1,padx=10,pady=30)

        okbtn =tk.Button(self.pointframe,command=self.addPoint,text="Add Point",bd=3,relief="raised",font=("Arial",20,"bold"),width=15)
        okbtn.grid(row=1,column=0,padx=2,pady=10,columnspan=2) 

    def addPoint(self):
        pId =int(self.pidin.get())
        point = int(self.pointIn.get())
        if pId:
            try:
                self.dbFun()
                query = f"select h_point from hospital  where id =%s"
                self.cur.execute(query,(pId))
                val = self.cur.fetchone()[0]

                newPoint = val + point
                query2 = f"update hospital set h_point = %s where id=%s "
                self.cur.execute(query2,(newPoint,pId))
                self.con.commit()
                self.tabFun()
                self.table.delete(*self.table.get_children())
                self.cur.execute("select * from hospital where id =%s",pId)
                row = self.cur.fetchone()
                self.table.insert('',tk.END,values=row)
                tk.messagebox.showinfo("Sucess",f"Health Position is update for patient {pId}")
                self.con.close()
                self.pointframe.destroy()

            except Exception as e:
                tk.messagebox.showerror("Error",f"Error: {e}")

        else:
            tk.messagebox.showerror("Error","Must Enter Patient Id")
    def disFun(self):
        pId =int(self.pidin.get())
        try:
            self.dbFun()
            query = f"delete from hospital where id =%s"
            self.cur.execute(query,pId)
            self.con.commit()
            tk.messagebox.showinfo("Sucessfully",f"Patient {pId} is discharges from the hospital .")
        except Exception as e:
            tk.messagebox.showerror("Error",f"Error{e}")
        
root = tk.Tk()
obj = hospital(root)
root.mainloop()