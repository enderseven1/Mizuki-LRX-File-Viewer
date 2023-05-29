#-*- coding:utf-8 -*-
'''
    中文: 
    @作者：岛田水木
    @版本：1.1
    @创建日期：2023/5/28
    @最后更新：2023/5/29
    @更新日志：
        v1.0 2023/5/28: 初版发布。
        v1.1 2023/5/29: 1.添加英语语言。2.支持LRX文件3.0。3.修复bug。

    English:
    @Author: Shimada Mizuki
    @Version: 1.1
    @Create Date: 2023/5/28
    @Last Update: 2023/5/29
    @Changelog: 
        v1.0 2023/5/28: First version. 
        v1.1 2023/5/29: (1)Add English language. (2)Add LRX 3.0 file. (3)Fix some bugs.
'''

import os, easygui, random
heads = {'1.0':'6025631696 5160966048 7622076112 5654449360 4936184512 6177212832 4576714240', 
         '2.0':'6025631696 5160966048 7622076112 5654449360 6584207056 4576714240', 
         '3.0':'xwauxioxnx uoxwnxxwra uxaawuxooa uxurrrnixw xuarawuwux ruuxuorarw'} #定义头 Heading
ends = {'3.0':'18694256 23424128 23649360 24550288 21847504 22523200 21847504 7207424 17342864 23649360 27478304 26352144 24099824 23649360'} #定义尾 Ending

if __name__ == '__main__':
    lastfile = False
    last = ''
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'] #随机生成用字母数字表 Alphabet for random filename
    lrxversion = 0
    strings = {#'':{'中文':'','English':''},
               'Action':{'中文':'操作文件','English':'Action a file'},
               'BrokenEnding':{'中文':'错误编辑或其他原因导致尾信息失效，若读取的文本异常，可能该文件已损坏。','English':'Bad editing or other reasons that cause the end of the file to become corrupted. If the text read is abnormal, the file may be corrupted.'},
               'ClearContent':{'中文':'已清除所有内容','English':'All content cleard.'},
               'ContentRead':{'中文':'读取完毕，内容如下：','English':'Read complete:'},
               'ContentWrited':{'中文':'内容已完整写入文件中，内容如下：','English':'Content written: '},
               'CreateFile1':{'中文':'是否要在','English':'Do you want to create a new file at '},
               'CreateFile2':{'中文':'\\位置创建文件？','English':'\\?'},
               'EnterFilename':{'中文':'请输入你的文件名（自动添加.lrx扩展名）','English':'Please enter your file name (without the extension)'},
               'EnterName':{'中文':'输入文件名','English':'Enter a filename'},
               'ErrorTip':{'中文':'错误提示','English':'Error'},
               'FileContent':{'中文':'文件内容','English':'File content'},
               'FileCreated':{'中文':'文件已创建：','English':'File created at '},
               'FileExists':{'中文':'文件已存在，请重新输入。','English':'The file already exists, please re-enter a filename.'},
               'FilenameSetWays':{'中文':'文件名要怎样设置？','English':'How to set the filename?'},
               'InvalidFile':{'中文':'无效lrx文件','English':'Invalid lrx file.'},
               'LastFile':{'中文':'是否打开上一个文件？','English':'Do you want to open the file you just opened?'},
               'NewFile':{'中文':'新建文件','English':'New file'},
               'NewSuccess':{'中文':'创建成功','English':'Created successfully.'},
               'No':{'中文':'否','English':'No'},
               'OpenFile1':{'中文':'打开文件','English':'Open a file'},
               'OpenFile2':{'中文':'打开文件','English':'Opening a file'},
               'PlsSelectAction':{'中文':'请选择你的操作','English':'Please select your action.'},
               'Random':{'中文':'随机生成','English':'Random'},
               'Read':{'中文':'读取文件','English':'Read'},
               'ReadDoneLog':{'中文':'读取完毕','English':'Read completed.'},
               'Select':{'中文':'选择文件','English':'Select a file'},
               'SelectAction':{'中文':'请选择文件操作','English':'Select an action'},
               'SelectFile':{'中文':'请选择你的LRX文件。','English':'Please select your LRX file.'},
               'Self':{'中文':'自己输入','English':'Self input'},
               'SetFilenameTitle':{'中文':'文件名','English':'Set a filename'},
               'Write':{'中文':'写入文件','English':'Write'},
               'WriteDoneLog':{'中文':'写入完毕','English':'Write completed.'},
               'WriteLineTip':{'中文':'请输入要写入的内容（仅支持单行输入，或使用\\n进行多行输入，输入[exit]结束操作并保存）','English':'Enter what you want to write (one line at a time or multiple lines using "\\n".Enter [exit] to end writing and save it. ）'},
               'Yes':{'中文':'是','English':'Yes'}
               } #语言信息对应 Language items
    language = easygui.buttonbox(msg='请选择软件语言。\nPlease select the language of interface.', title='设置语言/Set language', choices=('中文', 'English'))

    def readfile(filename):
        global lastfile, last, filename1, heads, lrxversion ,contenttttt
        lrx = open(filename1,'r')
        lrxcontt = ''
        for asd in lrx.readlines():
            lrxcontt += asd
        lrxcontt = lrxcontt.strip('\n').split('\n')
        lrxhead = lrxcontt[0]
        lrxend = lrxcontt[-1]
        if lrxhead == 'Heading: ' + heads['1.0'] or lrxhead == 'Heading: ' + heads['2.0'] or lrxhead == 'Heading: ' + heads['3.0']:
            if lrxhead == 'Heading: ' + heads['1.0']: #判断文件版本 File version
                print('=========================LRX 1.0 File=========================') 
                lrxversion = 1
            elif lrxhead == 'Heading: ' + heads['2.0']:
                print('=========================LRX 2.0 File=========================')
                lrxversion = 2
            elif lrxhead == 'Heading: ' + heads['3.0']:
                print('=========================LRX 3.0 File=========================')
                if lrxend != 'Ending: ' + ends['3.0']:
                    print(strings['BrokenEnding'][language])
                    easygui.msgbox(strings['BrokenEnding'][language],strings['ErrorTip'][language])
                    lrxend = 'Ending: ' + ends['3.0']
                lrxversion = 3
            lrx.close()
            abc = easygui.buttonbox(msg=strings['SelectAction'][language], title=strings['OpenFile2'][language], choices=(strings['Write'][language], strings['Read'][language]))
            if abc == strings['Write'][language]:
                with open(filename1,'w+') as lrx:
                    print(strings['ClearContent'][language])
                    lrx.write(lrxhead + '\n')
                    lrx.flush()
                    contenttttt = ''
                    while True:
                        erter = input(strings['WriteLineTip'][language])
                        if erter != '[exit]':
                            contenttttt += erter + '\n'
                            list1 = []
                            for ais in erter:
                                list1.append(str(ord(ais)*2011*8*14))
                            lrx.write(' '.join(list1) + '\n')
                            lrx.flush()
                        else:
                            if lrxversion == 3:
                                lrx.write(lrxend + '\n')
                            break
                print(strings['WriteDoneLog'][language])
                easygui.textbox(msg=strings['ContentWrited'][language], title=strings['FileContent'][language], text=contenttttt)
            elif abc == strings['Read'][language]:
                with open(filename1,'r') as lrx:
                    lrxcontect = lrx.readlines()
                    #print(lrxcontect)
                    del lrxcontect[0]
                    if lrxversion == 3:
                        del lrxcontect[-1]
                    lrxcont = []
                    contents=''
                    for i in lrxcontect:
                        lrxcont.append(i.strip('\n').split(' '))
                    for c in lrxcont:
                        for b in c:
                            if b == '':
                                contents += ''
                            else:
                                contents += chr(int(b)//14//8//2011)
                        contents += '\n'
                    print(strings['ReadDoneLog'][language])
                    easygui.textbox(msg=strings['ContentRead'][language], title=strings['FileContent'][language], text=contents)
            lastfile = True
            last = ''
            lrxversion = 0
        else:
            print(strings['InvalidFile'][language])
            easygui.msgbox(strings['InvalidFile'][language], strings['ErrorTip'][language])
            lrx.close()

    if language != None:
        while True:
            if lastfile:
                last = easygui.buttonbox(msg=strings['LastFile'][language], title=strings['OpenFile2'][language], choices=(strings['Yes'][language], strings['No'][language]))
                if last == strings['Yes'][language]:
                    readfile(filename1)
                else:
                    lastfile = False
                    last = ''
            if not lastfile and last != strings['Yes'][language]:
                syss = easygui.buttonbox(msg=strings['PlsSelectAction'][language], title=strings['Action'][language], choices=(strings['Select'][language], strings['NewFile'][language]))
                if syss == strings['Select'][language]:
                    filename1 = easygui.fileopenbox(msg=strings['SelectFile'][language], title=strings['Select'][language], default='*.lrx')
                    if filename1 != None:
                        readfile(filename1)
                    else:
                        break
                elif syss == strings['NewFile'][language]:
                    isnew = easygui.buttonbox(msg=strings['CreateFile1'][language] + os.getcwd() + strings['CreateFile2'][language], title=strings['NewFile'][language], choices=(strings['Yes'][language], strings['No'][language]))
                    if isnew == strings['Yes'][language]:
                        isname = easygui.buttonbox(msg=strings['FilenameSetWays'][language], title=strings['SetFilenameTitle'][language], choices=(strings['Self'][language], strings['Random'][language]))
                        if isname != None:
                            if isname == strings['Self'][language]:
                                while True:
                                    newf = easygui.enterbox(msg=strings['EnterFilename'][language], title=strings['EnterName'][language])
                                    if newf != None:
                                        newf += '.lrx'
                                        newf = newf.replace(' ','') #替换文件名中不能使用的字符
                                        newf = newf.replace('\\','')
                                        newf = newf.replace('/','')
                                        newf = newf.replace('*','')
                                        newf = newf.replace('"','')
                                        newf = newf.replace('|','')
                                        newf = newf.replace('?','')
                                        newf = newf.replace('<','')
                                        newf = newf.replace('>','')
                                        newfile = os.getcwd() + '\\' + newf
                                        if os.path.isfile(newfile):
                                            print(strings['FileExists'][language])
                                            easygui.msgbox(strings['FileExists'][language], strings['ErrorTip'][language])
                                        else:
                                            break
                                    else:
                                        break
                            elif isname == strings['Random'][language]:
                                while True:
                                    newf = ''
                                    for a in range(8):
                                        newf += alphabet[random.randint(0,35)]
                                    newfile = os.getcwd() + '\\' + newf + '.lrx'
                                    if not os.path.isfile(newfile):
                                        break
                            if newf != None:
                                with open(newfile,'w+') as lrx:
                                    lrx.write('Heading: ' + heads['3.0'] + '\n')
                                    lrx.write('Ending: ' + ends['3.0'] + '\n')
                                    lrx.close()
                                print(strings['FileCreated'][language] + newfile)
                                easygui.msgbox(strings['FileCreated'][language] + newfile, strings['NewSuccess'][language])
                else:
                    break
    print('\nThanks for using.\ncopyright©2023 Shimadamizuki') #结尾版权信息 Copyright
