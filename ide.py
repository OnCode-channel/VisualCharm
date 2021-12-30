from tkinter import *
from tkinter.filedialog import asksaveasfilename,askopenfilename
import tkinter.scrolledtext
import tkinter.messagebox as msg
from tkinter import ttk
#Для консоли
import platform,subprocess,os,json
#Для подсветки синтаксиса
import idlelib.colorizer as ic
import idlelib.percolator as ip
import re

compiler = Tk()
compiler.minsize(width=600,height=700)
name = 'VisualCharm'
compiler.title(f"*untitled* - {name}")
file_path = ''
compiler.wm_iconbitmap(default='assets/img/favicon.ico')

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
            compiler.title(f"{os.path.split(path)[1]} - {name}")
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
        compiler.title(f"{os.path.split(path)[1]} - {name}")

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

def create_file(*args):
    try:
        editor.delete('1.0',END)
        save_as()
    except:
        pass

def update_label():
    row, col = editor.index('insert').split('.')
    label.config(text=f'Python {platform.python_version()}   Line {row}, Column {col}')
    compiler.after(100, update_label)

def get_text_coord(s: str, i: int):
    for row_number, line in enumerate(s.splitlines(keepends=True), 1):
        if i < len(line):
            return f'{row_number}.{i}'
        
        i -= len(line)

numbers = Text(compiler, width=4, bg='lightgray', state=DISABLED, relief=FLAT)
numbers.grid(row=0, column=0, sticky='NS')

scroll_y = ttk.Scrollbar(compiler)
scroll_y.grid(row=0, column=3, sticky='NS')

def on_yscrollcommand(*args):
    scroll_y.set(*args)
    numbers.yview_moveto(args[0])

editor = Text(compiler, yscrollcommand=on_yscrollcommand, wrap=NONE,undo=True,bg=theme_bg)
editor.grid(row=0, column=1,columnspan=2, sticky='NSWE')

scroll_x = ttk.Scrollbar(compiler,orient='horizontal',command=editor.xview)
scroll_x.grid(row=1,column=0,columnspan=3,sticky="WE")

editor.configure(xscrollcommand=scroll_x.set)

def scroll_command(*args):
    editor.yview(*args)
    numbers.yview(*args)

scroll_y.config(command=scroll_command)

def insert_numbers():
    count_of_lines = editor.get(1.0, END).count('\n') + 1
    numbers.config(state=NORMAL)
    numbers.delete(1.0, END)
    numbers.insert(1.0, '\n'.join(map(str, range(1, count_of_lines))))
    numbers.config(state=DISABLED)

insert_numbers()

def on_edit(event):
    insert_numbers()
    editor.edit_modified(0)

cdg = ic.ColorDelegator()
cdg.prog = re.compile(r'\b(?P<MYGROUP>tkinter)\b|' + ic.make_pat(), re.S)
cdg.idprog = re.compile(r'\s+(\w+)', re.S)

try:
    with open('assets/theme.jso') as json_file:
        data = json.load(json_file)
        cdg.tagdefs['MYGROUP'] = {'foreground': f'{data["MYGROUP"]}', 'background': f'{theme_bg}'}
        cdg.tagdefs['COMMENT'] = {'foreground': f'{data["COMMENT"]}', 'background': f'{theme_bg}'}
        cdg.tagdefs['KEYWORD'] = {'foreground': f'{data["KEYWORD"]}', 'background': f'{theme_bg}'}
        cdg.tagdefs['BUILTIN'] = {'foreground': f'{data["BUILTIN"]}', 'background': f'{theme_bg}'}
        cdg.tagdefs['DEFINITION'] = {'foreground': f'{data["DEFINITION"]}', 'background': f'{theme_bg}'}
except:
    pass

ip.Percolator(editor).insertfilter(cdg)

#Добавляем меню бары
menu_bar = Menu(compiler)

file_menu = Menu(menu_bar,tearoff=0)
file_menu.add_command(label='New (Ctrl+N)',command=create_file)
file_menu.add_command(label='Open (Ctrl+O)',command=open_file)
file_menu.add_command(label='Save (Ctrl+S)',command=save_as)
file_menu.add_command(label='Save as (Ctrl+S)',command=save_as)
file_menu.add_command(label='Exit (Alt+F4)',command=exit)
menu_bar.add_cascade(label='File',menu=file_menu)

run_bar = Menu(menu_bar,tearoff=0)
run_bar.add_command(label='Run (Ctrl+F5)',command=run)
menu_bar.add_cascade(label="Run",menu=run_bar)

edit_bar = Menu(menu_bar,tearoff=0)
edit_bar.add_command(label='Undo (Ctrl+Z)',command=editor.edit_undo)
edit_bar.add_command(label='Redo (Ctrl+Shift+Z)',command=editor.edit_redo)
menu_bar.add_cascade(label="Edit",menu=edit_bar)

compiler.config(menu=menu_bar)

code_output = tkinter.scrolledtext.ScrolledText(height=10,state='disabled')
code_output.grid(row=2,column=0,columnspan=4,sticky="nsew")

#Добавляем сатусбар
label = Label(compiler, anchor='e')
label.grid(row=3,column=2,sticky="nsew")

#Добавляем хоткеи
compiler.bind("<Control-o>", open_file)
compiler.bind("<Control-s>", save_as)
compiler.bind("<F5>", run)

editor.bind('<<Modified>>', on_edit)

compiler.grid_columnconfigure(1, weight=1)
compiler.grid_rowconfigure(0, weight=1)

update_label()
compiler.mainloop()
