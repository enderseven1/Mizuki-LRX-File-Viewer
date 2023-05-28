#-*- coding:utf-8 -*-
import os, easygui, random
heads = {'1.0':'Heading: 6025631696 5160966048 7622076112 5654449360 4936184512 6177212832 4576714240', '2.0':'Heading: 6025631696 5160966048 7622076112 5654449360 6584207056 4576714240'} #定义头信息
lastfile = False
last = ''
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
def readfile(filename):
    global lastfile, last, filename1, heads, abe1r
    lrx = open(filename1,'r')
    lrxhead = lrx.readline().strip('\n')
    if lrxhead == heads['1.0'] or lrxhead == heads['2.0']:
        if lrxhead == heads['1.0']: #判断文件版本
            print('=========================LRX 1.0 File=========================') 
        elif lrxhead == heads['2.0']:
            print('=========================LRX 2.0 File=========================')
        lrx.close()
        abc = easygui.buttonbox(msg='请选择文件操作', title='打开文件', choices=('写入', '读取'))
        if abc == '写入':
            with open(filename1,'w+') as lrx:
                print('已清除所有内容')
                lrx.write(lrxhead + '\n')
                lrx.flush()
                while True:
                    erter = input('请输入要写入的内容（仅支持单行输入，输入[exit]结束）')
                    if erter != '[exit]':
                        list1 = []
                        for ais in erter:
                            list1.append(str(ord(ais)*2011*8*14))
                        lrx.write(' '.join(list1) + '\n')
                    else:
                        break
            print('写入完毕')
        elif abc == '读取':
            with open(filename1,'r') as lrx:
                lrxcontect = lrx.readlines()
                #print(lrxcontect)
                del lrxcontect[0]
                lrxcont = []
                contents=''
                for i in lrxcontect:
                    lrxcont.append(i.strip('\n').split(' '))
                for c in lrxcont:
                    for b in c:
                        contents += chr(int(b)//14//8//2011)
                    contents += '\n'
                easygui.textbox(msg='读取完毕，内容如下：', title='文件内容', text=contents)
            print('读取完毕')
        lastfile = True
        last = ''
    else:
        print('不是有效的lrx文件')
while True:
    if lastfile:
        last = easygui.buttonbox(msg='是否打开上一个文件', title='打开文件', choices=('是', '否'))
        if last == '是':
            readfile(filename1)
        else:
            lastfile = False
            last = ''
    if not lastfile and last != '是':
        syss = easygui.buttonbox(msg='请选择你的操作', title='操作文件', choices=('选择', '新建'))
        if syss == '选择':
            filename1 = easygui.fileopenbox(msg='请选择你的LRX文件。', title='选择文件', default='*.lrx')
            if filename1 != None:
                readfile(filename1)
            else:
                break
        elif syss == '新建':
            newf = ''
            for a in range(8):
                newf += alphabet[random.randint(0,35)]
            newfile = os.getcwd() + '\\' + newf + '.lrx'
            with open(newfile,'w+') as lrx:
                lrx.write(heads['2.0'])
                lrx.close()
            print('文件已创建：' + newfile)
        else:
            break
print('copyright©2023 Shimadamizuki')
