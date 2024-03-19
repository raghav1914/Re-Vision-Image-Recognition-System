import backend,wolframalpha
import numpy as np
from leafdisease import *
from disease import *
import cv2,ctypes,os,webbrowser,pytesseract
from tkinter import *
from PIL import ImageTk, Image
from tkinter import scrolledtext
import tkinter.messagebox as tkMessageBox
from tkinter.filedialog import askopenfilename
from keras.models import load_model
import numpy as np
from keras.preprocessing import image
from keras.applications.vgg16 import preprocess_input

pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR/tesseract.exe'

def gui():
    global home
    home = Tk()
    home.title("Re-Vision")
    home.iconbitmap('./images/icon.ico')
    img = Image.open("images/home.png")
    img = ImageTk.PhotoImage(img)
    panel = Label(home, image=img)
    panel.pack(side="top", fill="both", expand="yes")
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    [w, h] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
    lt = [w, h]
    a = str(lt[0]//2-480)
    b= str(lt[1]//2-310)
    home.geometry("960x550+"+a+"+"+b)
    home.resizable(0,0)


    def ask(qu):
        question = qu

        app_id = "G8TEG4-653G35RUAQ"

        try:
            client = wolframalpha.Client(app_id)

            res = client.query(question)

            answer = next(res.results).text

            return f"Question : {qu}\n\nAnswer : {answer}"
        except:
            return f"No answer found for question:\n\n{qu}"


    def upload():
        fl = askopenfilename(initialdir=os.getcwd(), title="Select Image", filetypes=( ("image", ".png"),("image", ".jpg"),("image", ".jpeg")))
        d,de = backend.detectobj(fl)
  
        dircfolder=d.copy()
        imgobj = cv2.imread('temp.png')
        imgobj = cv2.resize(imgobj,(486,245))
        cv2.imwrite("temp2.png",imgobj)
        photo = Image.open("temp2.png")
        imgobj = ImageTk.PhotoImage(photo)
        def openfile():
            os.startfile("temp.png")
        OBJBTN= Button(home,image=imgobj, highlightthickness = 0, bd = 0,activebackground="#B1DBF3", command=openfile)
        OBJBTN.image = imgobj
        OBJBTN.place(x = 243,y = 85)
        text = scrolledtext.ScrolledText(home)
        text.configure(width=72,height=7,font=('',18,'bold'), highlightthickness = 0, bd = 0)
        text.place(x=0,y=370)
        

        dm = []
        f = []
        for i in d:
            if len(f)==3:
                dm.append(f)
                f = []
            f.append(i)
        f = []
        if len(d)%3!=0:
            x = len(d)%3
            for i in range(x,0,-1):
                i = i*-1
                print(i)
                f.append(d[i])
            dm.append(f)
        try:
            if dm!=[]:
                text.insert(INSERT,"Detected Objects Are :\n\n")
                def fileopem(f):
                    
                    webbrowser.open(f)

                for j in dm:
                    for i in j:
                        v = i
                        
                        i = i.replace("data","icons")+".png"
                   
                        photo = Image.open(i)
                        photo = photo.resize((100,100))
                        tempp = ImageTk.PhotoImage(photo)
                      
                        if './' in v:
                            v=v.replace('./',os.getcwd()+'/')
                       
                        
                        b = Button(home, image=tempp, highlightthickness = 0, bd = 0,bg="white",command=lambda vs = v: fileopem(vs))
                        b.image=tempp
                        
                        text.window_create("end", window=b)
                        text.insert("end", "        ")
                      
                     
            else:
                text.insert(INSERT,"No similar object detected in Database !!!\n\n")
        except:
            text.delete("1.0","end")
            text.insert(INSERT,"No similar object detected in Database !!!\n\n")

        def disease():
            pred = prediction(fl)
            text.delete("1.0","end")
            k = list(pred.keys())
            st = ''
            for i in k:
                st+=i.replace('_',' ')+ ': '+pred[i]+'\n\n\n'
            text.insert(INSERT,st)

        ocr = pytesseract.image_to_string(fl, lang = 'eng')
        print(ocr)
        flag = False

        def ans():
            a = ask(ocr)
            text.delete("1.0","end")
            text.insert(INSERT,a)

        def dpred():
            drp = predictdisease(ocr)
            if drp == "":
                text.delete("1.0","end")
                text.insert(INSERT,"Unable to recognize disease !!!")
            else:
                text.delete("1.0","end")
                text.insert(INSERT,f"Disease recognized is {drp}")   

        def yoga():
                    model = load_model('./dataset/yogamodel.h5')
                    img = image.load_img(fl, target_size=(224, 224))
                    x = image.img_to_array(img)
                    x = np.expand_dims(x, axis=0)
                    img_data = preprocess_input(x)
                    classes = model.predict(img_data)
                    clss = ["Adho Mukha Svanasana (downdog)","Utkat Kathosana (Goddess pose)","Falaksana (Plank)","Vrichasana (Tree)","Veerbhadrasana (warrior yoga)"]
                    text.delete("1.0","end")
                    data = {"Adho Mukha Svanasana (downdog)":['◉ Strengthens the upper body\n◉ Elongates the spine\n◉ Strengthens hands, wrists, and fingers\n◉ Opens up the backs of the legs\n◉ Improves circulation\n◉ Relieves tension and stress','◉ CHILD’S POSE\n◉ TABLETOP POSE\n◉ PUPPY POSE'],"Utkat Kathosana (Goddess pose)":["◉ Opens the hips, legs, and chest\n◉ Strengthens the legs, calves, abs, and knees\n◉ Stimulates the uro-genital system and pelvic floor.\n◉ Strengthens and stretches the shoulder joint.","◉ Goddess Pose.\n◉ Revolved Goddess Pose.\n◉ Goddess Pose Variation Namaste.\n◉ Standing Squat Pose On Tip Toes.\n◉ Goddess Pose Chair Side Stretch."],"Falaksana (Plank)":["◉ A Healthy Posture.\n◉ Balance and Coordination.\n◉ Improves Body Alignment and Helps Avoid Illness.\n◉ Build Core Strength.\n◉ Improves Flexibility.\n◉ Improves Metabolism. \n◉ Improves Overall Mental Health.","◉ Belly-Up Crunch\n◉ Diagonal Crunch\n◉ Crunch And Reach"],"Vrichasana (Tree)":["◉ Improves balance and stability in the legs.\n◉ On a metaphysical level, helps one to achieve balance in other aspects of life.Strengthens the ligaments and tendon of the feet.\n◉ Strengthens and tones the entire standing leg, up to the buttocks.\n◉ Assists the body in establishing pelvic stability.","◉ Bending Tree Pose (Vrksasana)\n◉ Half-Lotus Tree Pose (Ardha Padmasana in Vrksasana)\n◉ Side Plank Pose, Tree variation (Vrksasana in Vasisthasana)\n◉ Handstand, Tree variation (Vrksasana in Adho Mukha Vrksasana)"],"Veerbhadrasana (warrior yoga)":["◉ Strengthens your shoulders, arms, legs, ankles and back.\n◉ Opens yours hips, chest and lungs.\n◉ Improves focus, balance and stability.\n◉ Encourages good circulation and respiration.\n◉ Stretches your arms, legs, shoulders, neck, belly, groins and ankles.\n◉ Energizes the entire body.","◉ Knee down lunge\n◉ Low Lunge\n◉ Warrior 2\n◉ Crescent Lunge"]}
                    yg=clss[classes.argmax()]
                    text.insert(INSERT,f"Person in image is doing {yg}\n\nBenifits of this are : \n{data[yg][0]}\n\nSome similar excercises are: \n{data[yg][1]}")  

        for i in de:
    
            if "umbrella" in i or "leaf" in i or "plant" in i :
                flag = True
                Button(home,text="Detect Disease In Plant",bg="#D6ECF9",relief = SOLID,bd=2,font = ("",11),width=25,command=disease).place(x=365,y=333)

            if ocr!= '' and ("umbrella" in i or "leaf" in i or "plant" in i):
                flag = True
                Button(home,text="Find The Answer",bg="#D6ECF9",relief = SOLID,bd=2,font = ("",11),width=25,command=ans).place(x=30,y=333)
                Button(home,text="Analyze Report",bg="#D6ECF9",relief = SOLID,bd=2,font = ("",11),width=25,command=dpred).place(x=700,y=333)

            if "person" in i:
                print("uhwfbhd")
                Button(home,text="Yoga and similar excercise",bg="#D6ECF9",relief = SOLID,bd=2,font = ("",11),width=25,command=yoga).place(x=365,y=333)

        if ocr!='' and flag == False :

            Button(home,text="Find The Answer",bg="#D6ECF9",relief = SOLID,bd=2,font = ("",11),width=25,command=ans).place(x=150,y=333)
            Button(home,text="Analyze Medical Report",bg="#D6ECF9",relief = SOLID,bd=2,font = ("",11),width=25,command=dpred).place(x=600,y=333)


    photo = Image.open("images/reset.png")
    img2 = ImageTk.PhotoImage(photo)
    b1=Button(home, highlightthickness = 0, bd = 0,activebackground="#D6ECF9", image = img2,command=reset)
    b1.place(x=885,y=25)

    photo = Image.open("images/upload.png")
    img3 = ImageTk.PhotoImage(photo)
    b2=Button(home, highlightthickness = 0, bd = 0,activebackground="#B1DBF3", image = img3,command=upload)
    b2.place(x=394,y=246)
    

    home.mainloop()

def reset():
    global home
    try:
        os.remove("temp.png")
    except:
        pass 
    try:
        os.remove("temp2.png")
    except:
        pass 

    home.destroy()
    gui()


gui()