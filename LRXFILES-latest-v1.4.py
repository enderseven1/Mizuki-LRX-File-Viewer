#-*- coding:utf-8 -*-
'''
    中文: 
    @ 作者：岛田水木
    @ 版本：1.4
    @ 创建日期：2023/5/28
    @ 最后更新：2023/6/1
    @ 更新日志：
        v1.0 2023/5/28: 初版发布。
        v1.1 2023/5/29: 1.添加英语语言。2.支持LRX文件3.0、3.1。3.修复bug。
        v1.2 2023/5/30: 1.修复bug。
        v1.3 2023/5/31: 1.修复bug。
        v1.4 2023/6/1: 1.修复bug。2.增强了对文件尾的修复能力。
        
    English:
    @ Author: Shimada Mizuki
    @ Version: 1.4
    @ Create Date: 2023/5/28
    @ Last Update: 2023/6/1
    @ Changelog: 
        v1.0 2023/5/28: First version. 
        v1.1 2023/5/29: (1)Add English language. (2)Add LRX 3.0,3.1 file. (3)Fix some bugs.
        v1.2 2023/5/30: (1)Fix some bugs.
        v1.3 2023/5/31: (1)Fix some bugs.
        v1.4 2023/6/1: (1)Fix some bugs.
'''

import os, easygui, random, sys, re
heads = {'1.0':'6025631696 5160966048 7622076112 5654449360 4936184512 6177212832 4576714240', 
         '2.0':'6025631696 5160966048 7622076112 5654449360 6584207056 4576714240', 
         '3.0':'xwauxioxnx uoxwnxxwra uxaawuxooa uxurrrnixw xuarawuwux ruuxuorarw',
         '3.1':'xwAUxIoxnx UoxwnxxwRa uxAAwuxooA UxURRRnIxw xUaRAwuwUx RUuxuoRARw'} #定义头 Heading
ends = {'3.0':'18694256 23424128 23649360 24550288 21847504 22523200 21847504 7207424 17342864 23649360 27478304 26352144 24099824 23649360',
        '3.1':'oaxnRAUx AIRARoAa AIxRnIxw ARUUwAaa AoaRuUwR AAUAIAww AoaRuUwR uAwuRAR ouIRAaxR AIxRnIxw AuRuaIwR AxIUAoRR ARwnnaAR AIxRnIxw'} #定义尾 Ending
allowapi = r'(1)|(2)|(3)|(4)|(5)|(6)|(7)|(8)|(9)|(0)'
allowapi31 = r'(w)|(o)|(A)|(I)|(R)|(U)|(x)|(u)|(a)|(n)'
banlistwords = r'(梁如萱我喜欢你)|(梁如萱我爱你)|(Liang Ruxuan I Love You)|(Liang Ruxuan I Like You)'
endingapi = ['E','d','i','g',':']

class LRXError(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return self.message
    __module__ = 'builtins'

if __name__ == '__main__':
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'] #随机生成用字母数字表 Alphabet for random filename
    lrxversion = 0
    threekey = ['w','o','A','I','R','U','x','u','a','n']
    bantext = ['"', '?', '>', '<', '\\', '|', '*', '/', ' ']
    strings = {#'':{'中文':'','English':''},
               '.LangList':{'中文':'',
                            'English':''},
               'BrokenEnding':{'中文':'错误编辑等原因破坏了尾信息，若读取的文本异常，可能该文件已损坏。从正规渠道取得lrx文件可以有效避免产生此问题。（修改并保存后自动修复尾信息）',
                               'English':'Bad editing or other reasons that corrupted the file ending. If the text read is abnormal, the file may be corrupted. Obtaining the LRX file from a regular source can avoid this problem to the greatest extent. (Automatically fix the end of the file after modifying and saving)'},
               'ContentRead':{'中文':'已成功打开文件，单击OK即可保存。',
                              'English':'The file was successfully opened. Click OK to save.'},
               'ContentWrited':{'中文':'内容已完整写入文件中，内容如下：',
                                'English':'Content written: '},
               'CopyrightTitle':{'中文':'感谢使用',
                                 'English':'Thanks for Using.'},
               'CreateFile1':{'中文':'是否要在当前位置（',
                              'English':'Do you want to create a new file at '},
               'CreateFile2':{'中文':'\\）创建文件？',
                              'English':'\\?'},
               'DelLang':{'中文':'切换语言',
                   'English':'Change Language'},
               'EnterFilename':{'中文':'请输入你的文件名（自动添加.lrx扩展名）',
                                'English':'Please enter your file name (without the extension)'},
               'EnterName':{'中文':'输入文件名',
                            'English':'Enter a filename'},
               'ErrorTip':{'中文':'错误提示',
                           'English':'Error'},
               'FileCreated':{'中文':'文件已创建：',
                              'English':'File created at '},
               'FileExists':{'中文':'文件已存在，请重新输入。',
                             'English':'The file already exists, please re-enter a filename.'},
               'FilenameSetWays':{'中文':'文件名要怎样设置？',
                                  'English':'How to set the filename?'},
               'InvalidFile':{'中文':'无效lrx文件（文件头无效）',
                              'English':'Invalid lrx file (Invalid heading).'},
               'LRXError1':{'中文':'梁如萱她不爱我...o(╥﹏╥)o',
                            'English':'Sharon (Ruxuan) Liang don\'t love me...o(╥﹏╥)o'},
               'NewFile':{'中文':'新建文件',
                          'English':'New File'},
               'NewSuccess':{'中文':'创建成功',
                             'English':'Created successfully.'},
               'No':{'中文':'否',
                     'English':'No'},
               'OpenFile1':{'中文':'打开文件',
                            'English':'Open a file'},
               'OpenFile2':{'中文':'打开文件',
                            'English':'Opening a file'},
               'PlsSelectAction':{'中文':'请选择你的操作',
                                  'English':'Please select your action.'},
               'Random':{'中文':'随机生成',
                         'English':'Random'},
               'Read':{'中文':'读取文件',
                       'English':'Read'},
               'ReadDoneLog':{'中文':'文件读取完毕',
                              'English':'Read completed.'},
               'SavingFile':{'中文':'正在保存...',
                              'English':'Saving file...'},
               'Select':{'中文':'选择文件',
                         'English':'Select a File'},
               'SelectAction':{'中文':'请选择文件操作',
                               'English':'Select an action'},
               'SelectFile':{'中文':'请选择你的LRX文件。',
                             'English':'Please select your LRX file.'},
               'Self':{'中文':'自己输入',
                       'English':'Self input'},
               'Selver':{'中文':'选择版本',
                         'English':'Version select'},
               'SetFilenameTitle':{'中文':'文件名',
                                   'English':'Set a filename'},
               'Tips':{'中文':'提示信息',
                       'English':'Message'},
               'Welcome':{'中文':'欢迎使用LRX文件查看器！\n本查看器可以新建、读取和写入各种版本的LRX文件！\n作者岛田水木，QQ：2068651347。\n',
                          'English':'Welcome to LRX File Viewer!\nThe viewer can create, read, and write various versions of LRX files!\nBy Shimada Mizuki, QQ: 2068651347.\n'},
               'WelcomeTitle':{'中文':'欢迎使用\n',
                               'English':'Welcome'},
               'Whichver':{'中文':'请选择文件版本',
                           'English':'Please select a version for new file.'},
               'WriteDoneLog':{'中文':'文件保存完毕',
                               'English':'Saved successfully.'},
               'Yes':{'中文':'是',
                      'English':'Yes'}
               } #语言信息对应 Language items

    def newFile(newfile1):
        '''
            新建文件。
            newfile1：文件路径。
        '''
        with open(newfile1,'w+', encoding='utf-8') as lrx:
            if whichver == '1.0':
                lrx.write('Heading: ' + heads[whichver] + '\n')
            elif whichver == '2.0':
                lrx.write('Heading: ' + heads[whichver] + '\n')
            elif whichver == '3.0':
                lrx.write('Heading: ' + heads[whichver] + '\n')
                lrx.write('Ending: ' + ends[whichver] + '\n')
            elif whichver == '3.1':
                lrx.write('Heading: ' + heads[whichver] + '\n')
                lrx.write('Ending: ' + ends[whichver] + '\n')
        print(strings['FileCreated'][language] + newfile)
        easygui.msgbox(strings['FileCreated'][language] + newfile, strings['NewSuccess'][language])

    def checkHead(lrxcontt1):
        '''
            检查头信息是否合法。
            lrxcontt1：文件内容。
        '''
        global lrxhead, lrxend, lrxversion
        lrxhead = lrxcontt1[0]
        if lrxhead == 'Heading: ' + heads['1.0'] or lrxhead == 'Heading: ' + heads['2.0'] or lrxhead == 'Heading: ' + heads['3.0'] or lrxhead == 'Heading: ' + heads['3.1']:
            if lrxhead == 'Heading: ' + heads['1.0']: #判断文件版本 File version
                print('=========================LRX 1.0 File=========================') 
                lrxversion = '1'
            elif lrxhead == 'Heading: ' + heads['2.0']:
                print('=========================LRX 2.0 File=========================')
                lrxversion = '2'
            elif lrxhead == 'Heading: ' + heads['3.0'] or lrxhead == 'Heading: ' + heads['3.1']:
                lrxend = lrxcontt1[-1]
                if lrxhead == 'Heading: ' + heads['3.0']:
                    print('=========================LRX 3.0 File=========================')
                    lrxversion = '3.0'
                elif lrxhead == 'Heading: ' + heads['3.1']:
                    print('=========================LRX 3.1 File=========================')
                    lrxversion = '3.1'
            return True

    def checkEnd(lrxend1):
        '''
            检查LRX3.0和LRX3.1的文件尾是否合法。
            lrxend1：文件尾。
        '''
        global lrxversion
        if lrxend1 != 'Ending: ' + ends[lrxversion]:
            print(strings['BrokenEnding'][language])
            easygui.msgbox(strings['BrokenEnding'][language],strings['ErrorTip'][language])
            if lrxend1 == '':
                return 'NoneEnd' #以E开头但是没有尾（可能是尾被破坏）
            elif lrxend1.startswith('E'):
                return 'FakeEnd' #以E开头但是尾不对（可能是尾被破坏）
            elif not lrxend1.startswith('E'):
                if (lrxversion == '3.0' and not re.match(allowapi,lrxend1.replace('n',''))) or (lrxversion == '3.1' and not re.match(allowapi31,lrxend1.replace('n',''))):
                    return 'FakeEnd'
                else:
                    return False #不是以E开头（可能是尾损坏）
        else:
            return True
            
    def readfile(filename):
        global heads, lrxversion, lrxend, threekeytemp, lrxhead
        with open(filename,'a+', encoding='utf-8') as lrx:
            lrxcontt = ''
            lrx.seek(0)
            for asd in lrx.readlines():
                lrxcontt += asd
            lrxcontt = lrxcontt.strip('\n').split('\n')
            if checkHead(lrxcontt):
                if lrxversion == '3.0' or lrxversion == '3.1':
                    endsget = checkEnd(lrxend)
                    if not endsget or endsget == 'FakeEnd':
                        if not endsget: #不是以E开头（可能是尾缺失）
                            lrx.seek(0,2)
                            lrx.write('\nEnding: ' + ends[lrxversion])
                        elif endsget == 'NoneEnd': #直接添加尾
                            lrx.seek(0,2)
                            lrx.write('Ending: ' + ends[lrxversion])
                        elif endsget == 'FakeEnd': #以E开头但是尾不对（可能是尾被破坏），删除此行换新尾
                            lrx.seek(0)
                            fix = lrx.readlines()[:-1]
                            lrx.seek(0)
                            lrx.truncate(0)
                            lrx.write(''.join(fix)[:-1] + '\nEnding: ' + ends[lrxversion])
                        lrx.flush()
                        lrxend = 'Ending: ' + ends[lrxversion]
                lrx.seek(0)
                lrxcontect = lrx.readlines()
                del lrxcontect[0]
                if lrxversion == '3.0' or lrxversion == '3.1':
                    del lrxcontect[-1]
                    if lrxcontect != []:
                        lrxcontect[-1] = lrxcontect[-1][:-1]
                print(lrxcontect)
                for index,iiie in enumerate(lrxcontect):
                    for inde in endingapi:
                        if inde in iiie:
                            #print(iiie)
                            if iiie.endswith('\n'): # 删除不能转换的字符
                                lrxcontect[index] = iiie = iiie[:iiie.index(inde)] + '\n'
                            else:
                                lrxcontect[index] = iiie = iiie[:iiie.index(inde)]
                            #print(lrxcontect[index])
                        print(lrxcontect)
                lrxcont = []
                contents= []
                print(lrxcontect)
                lrxccccc = ''
                lrxcontect = ''.join(lrxcontect)
                for i in lrxcontect:
                    if lrxversion == '3.1':
                        threekeytemp = ''
                        if i == ' ':
                            threekeytemp += ' '
                        elif i == '\n':
                            threekeytemp += '\n'
                        else:
                            try:
                                threekeytemp += str(threekey.index(i)) #挨个将字母转换成数字
                            except IndexError:
                                threekeytemp += ''
                        ccccccc = threekeytemp
                        print(ccccccc)
                    else:
                        ccccccc = i
                    lrxccccc += ccccccc
                lrxccccc = lrxccccc.split('\n')
                for csdf in lrxccccc:
                    lrxcont.append(csdf.split(' '))
                for c in lrxcont:
                    if c == ['']:
                        contents.append('')
                    else:
                        aaaaaaa = ''
                        for b in c:
                            if int(b)//14//8//2011 > sys.maxunicode: #挨个将数字转换成文字
                                aaaaaaa += chr(sys.maxunicode)
                            else:
                                aaaaaaa += chr(int(b)//14//8//2011)
                        contents.append(aaaaaaa)
                contents = '\n'.join(contents)
                #contents = contents[:-1]
                print(contents + '\n——————————————————————————\n' + strings['ReadDoneLog'][language] + '\n——————————————————————————\n') #输出读取完成日志，并输出文件内容
                editend = easygui.textbox(msg=strings['ContentRead'][language], title=filename, text=contents) #弹出文件窗口
                if editend == contents or editend == None:
                    pass
                else:
                    print(strings['SavingFile'][language])
                    lrx.seek(0)
                    lrx.truncate(0)
                    lrx.write(lrxhead + '\n')
                    #print(editend)
                    error = False
                    subed = re.sub(banlistwords,'',editend,0,re.I)
                    if subed != editend:
                        error = 1
                        editend = subed
                    del subed
                    #print(editend)
                    editeee = editend.split('\n')
                    #print(editeee)
                    list2 = []
                    for aaaa in editeee:
                        list1 = []
                        for ais in aaaa:
                            if lrxversion == '3.1':
                                tempssss = ''
                                for bgh in str(ord(ais)*2011*8*14):
                                    tempssss += threekey[int(bgh)]
                                list1.append(tempssss)
                            else:
                                list1.append(str(ord(ais)*2011*8*14))
                        list2.append(' '.join(list1))
                    lrx.write('\n'.join(list2))
                    if lrxversion == '3.0' or lrxversion == '3.1':
                        lrx.write('\n' + lrxend)
                    if error:
                        raise LRXError(strings['LRXError1'][language]) #我无法面对残酷的现实，救命啊
                    print(contents + '\n——————————————————————————\n' + strings['WriteDoneLog'][language] + '\n——————————————————————————\n')
                    easygui.msgbox(strings['WriteDoneLog'][language], strings['Tips'][language])
            else:
                print(strings['InvalidFile'][language])
                easygui.msgbox(strings['InvalidFile'][language], strings['ErrorTip'][language])
    while True:
            notlang = True
            logfile = os.getcwd() + '\\lrx.cfg'
            if os.path.exists(logfile):
                with open(logfile, 'r', encoding='utf-8') as log:
                    kkk = log.read()
                    if kkk in strings['.LangList']:
                        language = kkk
                        notlang = False
            if notlang:
                language = easygui.buttonbox(msg='请选择软件语言。\nPlease select the language of interface.\n\n软件的语言会被保存在lrx.cfg中，如需修改请删除该文件或清除其内容或单击切换语言。\nThe language of the software will be saved in the lrx .cfg file. Delete the file or click the "Change Language" button if you need to modify it.', title='设置语言/Set language', choices=('中文', 'English'))
                with open(logfile, 'w+', encoding='utf-8') as log:
                    if language != None:
                        log.write(str(language))

            if language != None:
                print(strings['Welcome'][language])
                while True:
                    syss = easygui.buttonbox(msg=strings['Welcome'][language] + '\n\n' +strings['PlsSelectAction'][language], title=strings['WelcomeTitle'][language], choices=(strings['Select'][language], strings['NewFile'][language], strings['DelLang'][language])) #syss is selection of this window to select an action. *syss 是用户在此窗口选择的项，用于获取用户的操作。
                    if syss == strings['Select'][language]: #If "Select a file" is selected. *如果选择“选择文件”。
                        filename1 = easygui.fileopenbox(msg=strings['SelectFile'][language], title=strings['Select'][language], default='*.lrx')
                        if filename1 != None: #Open it if a file is selected. *打开选择的文件。
                            readfile(filename1)
                    elif syss == strings['NewFile'][language]: #If "New File" is selected. *如果选择“新建文件”。
                        isnew = easygui.buttonbox(msg=strings['CreateFile1'][language] + os.getcwd() + strings['CreateFile2'][language], title=strings['NewFile'][language], choices=(strings['Yes'][language], strings['No'][language])) #isnew is selection of this window to confirm whether a new file is created in the current location. *isnew 是用户在此窗口选择的项，用于确认是否在当前位置新建文件。
                        if isnew == strings['Yes'][language]: #Yes *选是
                            while True:
                                whichver = easygui.buttonbox(msg=strings['Whichver'][language], title=strings['Selver'][language], choices=('1.0', '2.0', '3.0', '3.1')) #whichver is version is selected of file. *whichver是选择的文件版本
                                if whichver != None:
                                    while True:
                                        isname = easygui.buttonbox(msg=strings['FilenameSetWays'][language], title=strings['SetFilenameTitle'][language], choices=(strings['Self'][language], strings['Random'][language]))
                                        if isname != None:
                                            if isname == strings['Self'][language]:
                                                while True:
                                                    newf = easygui.enterbox(msg=strings['EnterFilename'][language], title=strings['EnterName'][language])
                                                    if newf != None:
                                                        newf += '.lrx'
                                                        for texti in bantext:
                                                            newf = newf.replace(texti,'') #替换文件名中不能使用的字符
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
                                                    n = random.randint(8,15)
                                                    for a in range(n): #生成n个字符长度的文件名
                                                        newf += alphabet[random.randint(0,35)]
                                                    newfile = os.getcwd() + '\\' + newf + '.lrx'
                                                    if not os.path.isfile(newfile):
                                                        break
                                            if newf != None:
                                                newFile(newfile)
                                                break
                                        else:
                                            break
                                else:
                                    break
                                break
                    elif syss == strings['DelLang'][language]:
                        with open(logfile, 'w+', encoding='utf-8') as log:
                            break
                    else:
                        break
                if syss == strings['DelLang'][language]:
                    continue
            print(strings['CopyrightTitle'][language] + '\nCopyright © 2023 Shimada Mizuki. All Rights Reserved.') #结尾版权信息 Copyright
            break
