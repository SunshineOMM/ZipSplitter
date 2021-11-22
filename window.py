from tkinter import *
from tkinter import scrolledtext
from tkinter.filedialog import askopenfilename,askdirectory
import back

#-------------------BACKEND---------------------------


def clicked_start():
    global FILE_NAME_OLD_ARC
    global NAME_SEP_DIR
    global BATCH
    global START

    if FILE_NAME_OLD_ARC!=None and NAME_SEP_DIR!=None and check_enter_for_txt_batch() and check_enter_for_txt_start_pos():
        # Выбираем начиная со START файлов от начала, по BATCH файлов нужного расширения и формируем из них архивы zip
        bt = back.back_thread(add_text_to_log,FILE_NAME_OLD_ARC,NAME_SEP_DIR,BATCH,START)
        bt.start()

#-------------------END BACKEND---------------------------

#-------------------GUI---------------------------
def add_text_to_log(text):
    logs.insert(END,text+"\n\n")
    logs.see("end")

def clicked_choice_old_arc():
    global FILE_NAME_OLD_ARC
    FILE_NAME_OLD_ARC = askopenfilename()
    add_text_to_log(f"Архив, выбранный для разделения: {FILE_NAME_OLD_ARC} !")

def clicked_choice_separated_dir():
    global NAME_SEP_DIR
    NAME_SEP_DIR = askdirectory()
    NAME_SEP_DIR+="/"
    add_text_to_log(f"Выбран каталог для разделения: {NAME_SEP_DIR} !")

def check_enter_for_txt_batch():
    global BATCH
    enter=txt_batch.get()
    try:
        enter=int(enter)
        BATCH=enter
        add_text_to_log(f"Размер разбиения задан!")
        return True
    except:
        add_text_to_log(f"The wrong value is entered in the selection batch field!")
        return False

def check_enter_for_txt_start_pos():
    global START
    enter = txt_start_pos.get()
    try:
        enter = int(enter)
        START=enter-1
        add_text_to_log(f"Порядковый номер первого файла в разбиении задан!")
        return True
    except:
        add_text_to_log(f"The wrong value is entered in the selection start number field!")
        return False

def about_programm():
    new_window = Toplevel(window)
    new_window.geometry('450x400')
    label_how_use=Label(new_window,text="Как пользоваться ZipSplitter?\n"
                                        "1) Укажите архив, содержимое которого необходимо разделить;\n"
                                        "2) Укажите дирректорию, куда необходимо поместить разделённые и\n"
                                        " архивированные данные;\n"
                                        "3) Укажите по сколько элементов разбивать содержимое исходного архива;\n"
                                        "4) Укажите начиная с какого элемента необходимо начать разбиение.\n"
                                        "(если начинаем с начала, укажите 1)\n\n")
    label_how_use.grid(row=0, column=0)

    label_txt=Label(new_window,text="ZipSplitter делит содержимое архива (rar, zip)\n"
                                    " в соответствии с указанными параметрами и сохраняет некоторое\n "
                                    " количество получившихся архивов разделённых объектов в указанной папке.\n"
                                    " В данный момент для разделения используются\n"
                                    " только файлы с расширением xcf.\n\n")
    label_txt.grid(row=1, column=0)

    label_info = Label(new_window, text="ZipSplitter был разработан стажёром \n"
                                        "отдела исследований Александром Петровым, в интересах ГРИНАТОМ.\n\n")
    label_info.grid(row=2, column=0)

    label_contact_info = Label(new_window,
                       text="Исходный код программы размещён по адресу: https://github.com/SunshineOMM/ZipSplitter.git.")
    label_contact_info.grid(row=3, column=0)

#-------------------END GUI---------------------------

# global
FILE_NAME_OLD_ARC=None
NAME_SEP_DIR=None
START=None
BATCH=None

window = Tk()
window.title("ZipSplitter")
window.geometry('420x450')

menu = Menu(window)

menu.add_command(label="О программе",command=about_programm)
window.config(menu=menu)

lbl_att=Label(window,text="Внимание, работа данной программы может занять от 5 до 10 минут!",fg="orange")
lbl_att.grid(row=0,column=0,columnspan=2)

lbl_old_arc = Label(window,text="Выберите разбиваемый архив:")
lbl_old_arc.grid(row=1,column=0)
btn_choice_old_arc = Button(window, text="Обзор",command=clicked_choice_old_arc)
btn_choice_old_arc.grid(row=1,column=1)


lbl_separated_dir = Label(window, text="Выберите папку куда \nпоместить результат разбиения:")
lbl_separated_dir.grid(row=2,column=0)
btn_choice_separated_dir = Button(window, text="Обзор", command=clicked_choice_separated_dir)
btn_choice_separated_dir.grid(row=2,column=1)


lbl_batch = Label(window, text="Выберите по сколько файлов\n разбивать архив:")
lbl_batch.grid(row=3,column=0)
txt_batch = Entry(window,width=10)
txt_batch.grid(row=3,column=1)

lbl_start_pos = Label(window, text="Выберите с какого файла по счёту начать разбиение:\n(Если разбиение с начала, ввести 1)")
lbl_start_pos.grid(row=4,column=0)
txt_start_pos = Entry(window,width=10)
txt_start_pos.grid(row=4,column=1)

btn_choice_old_arc = Button(window, text="Поехали",command=clicked_start,width=50,bg="green")
btn_choice_old_arc.grid(row=5,column=0,columnspan=2)

logs = scrolledtext.ScrolledText(window, width=50, height=20)
logs.grid(row=6,columnspan=2)
window.mainloop()
