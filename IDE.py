#Для окна
from tkinter import *
from tkinter.filedialog import asksaveasfilename,askopenfilename
import tkinter.scrolledtext
import tkinter.messagebox as msg
#Для консоли
import platform
import subprocess
#Для подсветки синтаксиса
import idlelib.colorizer as ic
import idlelib.percolator as ip
import re

compiler = Tk()
compiler.geometry('700x600')
name = 'VisualCharm'
compiler.title(f"*untitled* - {name}")
file_path = ''
compiler.wm_iconbitmap(default='assets/img/favicon.ico')
win_width = int(compiler.winfo_reqheight())
win_height = int(compiler.winfo_reqwidth())

#theme_bg = "#1E1E1E"
theme_bg = "#fff"

def set_file_path(path):
    global file_path
    file_path = path

def open_file(*args):
    path = askopenfilename(filetypes=[('Python Files','*.py')])
    try:
        with open(path,'r') as file:
            code = file.read()
            editor.delete('1.0',END)
            editor.insert('1.0',code)
            set_file_path(path)
            compiler.title(f"{path} - {name}")
    except:
        pass

def save_as(*args):
    if file_path == '':
        path = asksaveasfilename(filetypes=[('Python Files','*.py')])
    else:
        path = file_path
    with open(path,'w') as file:
        code = editor.get('1.0',END)
        file.write(code)
        set_file_path(path)
        compiler.title(f"{path} - {name}")

def run(*args):
    if file_path == '':
        msg.showinfo('Please save your code','Please save your code')
    else:
        command = f'python {file_path}'
        save_as()
        process = subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
        output,error = process.communicate()
        code_output.config(state='normal')
        code_output.insert('1.0',output)
        code_output.insert('1.0',error)
        code_output.insert('1.0',f'==== {file_path} ====\n')
        code_output.config(state='disabled')

def update_label():
    row, col = editor.index('insert').split('.')
    label.config(text=f'Python {platform.python_version()}   Line {row}, Column {col}')
    compiler.after(100, update_label)

def get_text_coord(s: str, i: int):
    for row_number, line in enumerate(s.splitlines(keepends=True), 1):
        if i < len(line):
            return f'{row_number}.{i}'
        
        i -= len(line)

editor = tkinter.scrolledtext.ScrolledText(undo=True,font="DejaVu 11",width=win_width,bg=theme_bg)
editor.pack()

#Подсветка синтаксиса
cdg = ic.ColorDelegator()
cdg.prog = re.compile(r'\b(?P<MYGROUP>tkinter)\b|' + ic.make_pat(), re.S)
cdg.idprog = re.compile(r'\s+(\w+)', re.S)

'''
cdg.tagdefs['MYGROUP'] = {'foreground': '#4EC9B0', 'background': theme_bg}
cdg.tagdefs['COMMENT'] = {'foreground': '#6A9955', 'background': theme_bg}
cdg.tagdefs['KEYWORD'] = {'foreground': '#C586C0', 'background': theme_bg}
cdg.tagdefs['BUILTIN'] = {'foreground': '#DCDC8B', 'background': theme_bg}
cdg.tagdefs['STRING'] = {'foreground': '#7F3F00', 'background': theme_bg}
cdg.tagdefs['DEFINITION'] = {'foreground': '#007F7F', 'background': theme_bg}
cdg.tagdefs['ERROR'] = {'foreground': '#000000', 'background': theme_bg}
cdg.tagdefs['hit'] = {'foreground': '#ffffff', 'background': theme_bg}
'''

ip.Percolator(editor).insertfilter(cdg)

#Добавляем меню бары
menu_bar = Menu(compiler)

file_menu = Menu(menu_bar,tearoff=0)
file_menu.add_command(label='Open    |  Ctrl+O',command=open_file)
file_menu.add_command(label='Save      |  Ctrl+S',command=save_as)
file_menu.add_command(label='Save as |  Ctrl+S',command=save_as)
file_menu.add_command(label='Exit        |  Alt+F4',command=exit)
menu_bar.add_cascade(label='File',menu=file_menu)

run_bar = Menu(menu_bar,tearoff=0)
run_bar.add_command(label='Run  |  Ctrl+F5',command=run)
menu_bar.add_cascade(label="Run",menu=run_bar)

edit_bar = Menu(menu_bar,tearoff=0)
edit_bar.add_command(label='Undo | Ctrl+Z',command=editor.edit_undo)
edit_bar.add_command(label='Redo  | Ctrl+Shift+Z',command=editor.edit_redo)
menu_bar.add_cascade(label="Edit",menu=edit_bar)

compiler.config(menu=menu_bar)

code_output = tkinter.scrolledtext.ScrolledText(height=10,state='disabled',width=win_width)
code_output.pack()

#Добавляем сатусбар
label = Label(compiler, anchor='e')
label.pack(fill='x')

#Добавляем хоткеи
compiler.bind("<Control-o>", open_file)
compiler.bind("<Control-s>", save_as)
compiler.bind("<F5>", run)

#Запуск
update_label()
compiler.mainloop()
