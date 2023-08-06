import re
import json

with open('./tranlist.json', 'r', encoding='utf-8') as f:
    tranlist = json.load(f)

def tran(err:str)->str:

    for v in tranlist:
        isre,re_,tran_=v["se"],v["re"],v["t"]
        if re_ == err:
            return tran_
    for v in tranlist:
        isre,re_,tran_=v["se"],v["re"],v["t"]
        if isre=="re":
            eee=re.findall(re_,err)
            if len(eee)==1:
                return tran_ % eee[0]
        elif isre=="startwithreplace":
            if err.startswith(re_):
                return tran_
    return err

def main():
    i=input("请输入错误代码：")
    print(tran(i))

if __name__ == '__main__':
    main()