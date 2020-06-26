import tkinter as tk
import tkinter.filedialog as tkf
import tkinter.messagebox as msg
import os
import re
import shutil
import win32con
import win32clipboard
#from googletrans import Translator
from subprocess import Popen, PIPE

#配置
#box.geometry("500x300")

static_path='C:/Users/Kylin/Desktop/Blog/source/_posts/'
os.chdir(static_path)

run_path='C:/Users/Kylin/Desktop/快速博客/'

win = tk.Tk()
win.title("博客小助手")
win.iconbitmap(run_path + "box.ico")
#translator = Translator()
main_title = ""
#title_tran = ""

#Function
def hexo_new(get_title):
    global main_title
    #global title_tran
    if get_title.replace(" ", "") != "":
        #os_command_origin="powershell -command "
        #poweshell部分文字输入不进去好像有“”等
        os_command_origin = "cmd /c "
        hexo_new_posts = 'hexo new '+get_title
        #os.system(os_command_origin+hexo_new_posts)
        #print(os_command_origin+hexo_new_posts)
        #changed_title=os.popen(os_command_origin+hexo_new_posts).read().decode('utf-8')
        changed_title = Popen(os_command_origin+hexo_new_posts, shell=True,stdout=PIPE, stderr=PIPE).stdout.read().decode('utf-8')
        get_true_title_re = re.compile(r'INFO  Created: ~\\Desktop\\Blog\\source\\_posts\\(.*?)\.md')
        true_title = get_true_title_re.findall(changed_title)[0]
        #赋值
        main_title = true_title #实际文件名
        #title_tran = translator.translate(get_title).text #翻译名
        #写入翻译，弃用tran插件
        #f_t = open(true_title+".md")
        #f_data = f_t.read().replace("translate_title:", "translate_title: " + title_tran)
        #f_t.close()
        #with open(true_title+".md", "w") as f_tt:
        #    f_tt.write(f_data)
    else:
        msg.showinfo("提示", "请输入标题！")

def s_files(def_filenames, def_string_filename):
    global static_path
    global main_title
    cho_msg = ""
    get_the_last = ""
    #应该不会把md文档当作附件用的。。。
    if len(def_filenames) != 0:
        g_main_t = def_filenames[0].replace(static_path, "")
        get_main_title_re = re.compile(r'(.*?)\.md')
        gmtre = get_main_title_re.findall(g_main_t)
        if len(gmtre) != 0:
            main_title = gmtre[0].replace(" ", "")
            msg.showinfo("提示", main_title)
            get_the_last = g_main_t.replace(main_title, "")

        if get_the_last != ".md":
            if main_title != "":
                cho_msg = msg.askokcancel('提示', '需要移动文件到文章附件目录吗？')
                if cho_msg:
                    for i in range(0,len(def_filenames)):
                        def_string_filename.append(def_filenames[i])
                        #get_data["text"]=str(def_string_filename)
                        shutil.move(def_filenames[i], static_path + main_title)
                        get_fujian_re = re.compile(r'[^\\\?\/\*\|<>:"]+?\..*')
                        get_fj = get_fujian_re.findall(def_filenames[i])[0]
                        get_clip_re = re.compile(r'\..*')
                        get_clip = get_clip_re.findall(get_fj)[0]
                        final_clip = "<img src=\""+get_fj+"\" width=\"100%\" alt=\""+get_fj.replace(get_clip,"")+"\">"
                        win32clipboard.OpenClipboard()
                        win32clipboard.EmptyClipboard()
                        win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, final_clip)
                        win32clipboard.CloseClipboard()
                    #if main_title == "" and msg.askokcancel('提示', '是否需要选择目录？'):
            else:
                #if main_title == "" and len(def_filenames) != 0:
                #    msg.showinfo("提示", "请新建文章！")
                #elif main_title != "" and len(def_filenames) == 0 or main_title == "" and len(def_filenames) == 0:
                    #msg.showinfo("提示", "请选择文件！")
                #elif main_title != "" and cho_msg != True:
                #    msg.showinfo("提示", "请同意！")
                pass

        elif get_the_last == ".md":
            pass

def shell_files():
    #global main_title
    filenames = tkf.askopenfilenames()
    string_filename = []
    s_files(filenames, string_filename)

def select_o():
    #win.destroy()

    box = tk.Tk()
    box.title("新建文章")
    box.iconbitmap(run_path + "box.ico")

    title = tk.Entry(box, text='文章标题', width=20)
    title.grid(row=1, column=2, padx=10, pady=10)

    post_title = tk.Button(box, text='生成文章', width=7, height=1, command=lambda:hexo_new(title.get()))
    post_title.grid(row=1, column=6, padx=10, pady=10)

    select_files = tk.Button(box, text='选择...', width=7, height=1, command=shell_files)
    select_files.grid(row=2, column=6, padx=10, pady=10)

    get_data = tk.Label(box)
    get_data.grid(row=2, column=2)

    box.mainloop()

def select_t():
    box = tk.Tk()
    box.title("修改图片")
    box.iconbitmap(run_path + "box.ico")

    select_filemd = tk.Button(box, text="选择Markdown文件", command=shell_files)
    select_filemd.grid(row=1, column=1, padx=15, pady=10)

    select_filemd_fujian = tk.Button(box, text="选择附件", command=shell_files)
    select_filemd_fujian.grid(row=2, column=1, padx=10, pady=10)

    box.mainloop()

def get_main_d():
    global main_title
    msg.showinfo("提示", main_title)

#Main

select_one = tk.Button(win, text="新建文章", width=7, height=1, command=select_o)
select_one.grid(row=1, column=1, padx=10, pady=10)

select_l = tk.Label(win, text="OR", width=2, height=1)
select_l.grid(row=1, column=2, padx=5, pady=5)

select_two = tk.Button(win, text="修改图片", width=7, height=1, command=select_t)
select_two.grid(row=1, column=3, padx=10, pady=10)

get_main_t = tk.Button(win, text="Main Title", width=10, height=1, command=get_main_d)
get_main_t.grid(row=2, column=2, padx=0, pady=5)

#v = tk.IntVar()
#r1 = tk.Radiobutton(win, text="one", value=1, variable=v)
#r1.grid(row=3, column=2, padx=0, pady=10)
#if v.get() == 1:
#    clip()

win.mainloop()