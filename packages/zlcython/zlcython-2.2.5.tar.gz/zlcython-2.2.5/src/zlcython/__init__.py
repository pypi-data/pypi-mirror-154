import json
guicode = '''from tkinter import *
window=Tk()
def 图形化标题(title):
    window.title(title)
def 图形化窗口大小(width,height):
    window.geometry(str(width)+"x"+str(height))
def 显示窗口():
    window.mainloop()
def 显示文本(text,x=0,y=0):
    l=Label(window,text=text)
    l.place(x=x,y=y)
    return l
def 显示文本框(text,x=0,y=0,width=None,height=None):
    e=Entry(window,text=text,width=width,height=height)
    e.place(x=x,y=y)
    return e
def 显示按钮(text,command,x=0,y=0,width=None,height=None):
    b=Button(window,text=text,width=width,height=height,command=command)
    b.place(x=x,y=y)
    return b
def 当窗口关闭时(command):
    def func():
        command()
        try:
            window.destroy()
        except:pass
    window.protocol("WM_DELETE_WINDOW",func)
def 图形化窗口位置(x,y):
    window.geometry("+"+str(x)+"+"+str(y))
def 刷新窗口():
    window.update()
'''
with open('./trandic.json', 'r', encoding='utf-8') as f:
    trandic = json.load(f)
with open('./retrandic.json', 'r', encoding='utf-8') as f:
    replace_trandic = json.load(f)
with open('./keywords.json', 'r', encoding='utf-8') as f:
    custom_keywords = json.load(f)
keywords=[]
for item in custom_keywords:keywords.append(item[0])
def zlcytopy(line,linenum,libusedict):
    if line =='':return '',libusedict,'',False
    decodecode = ''
    out=''
    exit__=False
    code = []
    # out+=('开始处理第' + str(linenum + 1) + '行。内容为：' + line+ (''if line[-1] != '' else '') +'\n')
    lines = line.split()
    if lines==[]:return '',libusedict,'',False
    tab = ''
    if line.count(' ') == len(line):
        return " ",libusedict,'',False
    while True:
        if line.startswith("    "):
            tab += "    "
            line = line[4:]
            _ = line == line[:]
        else:
            break
    if lines[0] not in keywords:
        if len(lines) == 0:
            return '',libusedict,out,exit__
        if len(lines) == 1 and lines[0] == "导入图形化界面":
            usegui = True
            for guicodeline in guicode.split("\n"):
                decodecode += (tab+guicodeline+"\n")
            return decodecode,libusedict,out,exit__
        for i in range(len(lines)):
            if "请求网页" in lines[i]:
                libusedict["urllib_request"][0] = True
            if "随机数" in lines[i]:
                libusedict["random"][0] = True
            if "等待" in lines[i]:
                libusedict["time"][0] = True
            if lines[i] in trandic:
                lines[i] = trandic[lines[i]]
    else:
        for i in custom_keywords:
            if i[0] == lines[0]:
                input__ = lines[1:]
                if len(input__) != i[1]:
                    out+=(f"编译失败，请检查输入参数。\n行数：{linenum+1}\n错误代码内容：\n\n{tab+line}\n{tab}"+"^"*len(line)+f"\n错误信息：输入参数个数不符合要求。\n要求参数个数：{i[1]}\n实际参数个数：{len(input__)}")
                    exit__=True
                    return '',libusedict,out,exit__
                input__ = ' '.join(input__)
                for key, value in replace_trandic.items():
                    input__ = input__.replace(key, value)
                input__ = input__.split()
                for _a_b_ in input__:
                    _a_b_s = _a_b_.split(" ")
                    for _a_b_s_ in _a_b_s:
                        if _a_b_s_ in trandic:
                            _a_b_s_ = trandic[_a_b_s_]
                input__ = list(map(str, input__))
                libusedict[i[3]][0] = True
                decodecode += tab+(i[2] % tuple(input__))+"\n"
                # out+=(f"编译成功{linenum+1}行。输出：{tab+(i[2] % tuple(input__))}")
        return decodecode,libusedict,out,exit__
    replace_line = (' '.join(lines)+'\n')
    for key, value in replace_trandic.items():
        replace_line = replace_line.replace(key, value)
    decodecode += tab+replace_line
    # out+=('编译成功'+str(linenum+1)+'行。输出：'+tab+replace_line+'\n')
    return decodecode,libusedict,out,exit__