#-*- coding:utf-8 -*-
'''
    中文: 
    @ 作者：岛田水木
    @ 版本：1.5.1
    @ 创建日期：2023/5/28
    @ 最后更新：2023/6/3
    @ 更新日志：
        v1.0 2023/5/28: 初版发布。
        v1.1 2023/5/29: 1.添加英语语言。2.支持LRX文件3.0、3.1。3.修复bug。
        v1.2 2023/5/30: 1.修复bug。
        v1.3 2023/5/31: 1.修复bug。
        v1.4 2023/6/1: 1.修复bug。2.增强了对文件尾的修复能力。
        v1.5 2023/6/2: 1.简化了代码结构。2.文件尾损坏时可以选择不打开。
        v1.5.1 2023/6/3: 1.合并窗口。2.简洁代码，去掉很多if语句及循环结构，以递归函数替换。
        
    English:
    @ Author: Shimada Mizuki
    @ Version: 1.5.1
    @ Create Date: 2023/5/28
    @ Last Update: 2023/6/3
    @ Changelog: 
        v1.0 2023/5/28: First version. 
        v1.1 2023/5/29: (1)Add English language. (2)Add LRX 3.0,3.1 file. (3)Fix some bugs.
        v1.2 2023/5/30: (1)Fix some bugs.
        v1.3 2023/5/31: (1)Fix some bugs.
        v1.4 2023/6/1: (1)Fix some bugs.
        v1.5 2023/6/2: (1)Fix some bugs. (2)You can choose not to open the end of the file if it is damaged.
        v1.5.1 2023/6/3: (1)Consolidated some windows. (2)The code is concise, removing a lot of if statements and loop structures.

    LRX文件版本概述：
        LRX 1.0/2.0/3.0 一样，只是文件头不同。
        LRX 3.1 在 3.0 的基础上将文件头的字母区分大小写，并将内容也从数字改为字母。

    LRX file version description:
        LRX 1.0/2.0/3.0 is the same, except that the file header is different.
        LRX 3.1 builds on 3.0 to make the letters of the file header case-sensitive and change the content from numbers to letters.
'''

import os
import easygui
import random
import sys
import re #导入模块

lrxversion = 0 #文件版本
heads = {'1.0':'6025631696 5160966048 7622076112 5654449360 4936184512 6177212832 4576714240', 
         '2.0':'6025631696 5160966048 7622076112 5654449360 6584207056 4576714240', 
         '3.0':'xwauxioxnx uoxwnxxwra uxaawuxooa uxurrrnixw xuarawuwux ruuxuorarw',
         '3.1':'xwAUxIoxnx UoxwnxxwRa uxAAwuxooA UxURRRnIxw xUaRAwuwUx RUuxuoRARw'} #定义头 Heading
ends = {'3.0':'18694256 23424128 23649360 24550288 21847504 22523200 21847504 7207424 17342864 23649360 27478304 26352144 24099824 23649360',
        '3.1':'oaxnRAUx AIRARoAa AIxRnIxw ARUUwAaa AoaRuUwR AAUAIAww AoaRuUwR uAwuRAR ouIRAaxR AIxRnIxw AuRuaIwR AxIUAoRR ARwnnaAR AIxRnIxw'} #定义尾 Ending
allowapi = r'(1)|(2)|(3)|(4)|(5)|(6)|(7)|(8)|(9)|(0)'
allowapi31 = r'(w)|(o)|(A)|(I)|(R)|(U)|(x)|(u)|(a)|(n)'
banlistwords = r'(梁如萱我喜欢你)|(梁如萱我爱你)|(Liang Ruxuan I Love You)|(Liang Ruxuan I Like You)' #违禁词表
endingapi = ('E','d','i','g',':') # 可能会出现的不能转换的字母
alphabet = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0') #随机生成用字母数字表 Alphabet for random filename
threekey = ('w','o','A','I','R','U','x','u','a','n') #3.1解码器
bantext = ('"', '?', '>', '<', '\\', '|', '*', '/', ' ') #不能出现在文件名中的字符
strings = {'中文': {'BrokenEnding': ('错误编辑等原因破坏了尾信息，若读取的文本异常，可能该文件已损坏。' #定义语言
                                    '从正规渠道取得lrx文件可以有效避免产生此问题。若要强制打开请点击继续。（修改并保存后自动修复尾信息）'), 
                    'Cancel': '取消',
                    'ContentRead': '已成功打开文件，单击OK即可保存。', 
                    'ContentWrited': '内容已完整写入文件中：', 
                    'Continue': '继续',
                    'CopyrightTitle': '\n感谢使用', 
                    'CreateFile1': '将在当前位置（', 
                    'CreateFile2': '\\）创建文件。', 
                    'DelLang': '切换语言', 
                    'ErrorTip': '错误提示', 
                    'FileCreated': '文件已创建：', 
                    'FileExists': '文件已存在，请重新输入。', 
                    'FilenameSetWays': '请在输入框中输入文件名，若留空则为你随机生成。', 
                    'InvalidFile': '无效lrx文件（文件头或文件尾无效）', 
                    'LRXError1': '梁如萱她不爱我...o(╥﹏╥)o', 
                    'NewFile': '新建文件', 
                    'NewSuccess': '创建成功', 
                    'No': '否', 
                    'OpenFile1': '打开文件', 
                    'OpenFile2': '打开文件', 
                    'PlsSelectAction': '请选择你的操作', 
                    'Read': '读取文件', 
                    'ReadingLog': '读取中...', 
                    'ReadDoneLog': '读取完毕', 
                    'SavingFile': '正在保存...', 
                    'Select': '选择文件', 
                    'SelectAction': '请选择文件操作', 
                    'SelectFile': '请选择你的LRX文件。', 
                    'SetFilenameTitle': '文件名', 
                    'Tips': '提示信息', 
                    'Welcome': ('欢迎使用LRX文件查看器！\n本查看器可以新建、读取和写入各种版本的LRX文件！\n'
                                '作者岛田水木，QQ：2068651347。\n'), 
                    'WelcomeTitle': '欢迎使用\n', 
                    'Whichver': '请选择文件版本', 
                    'WriteDoneLog': '文件保存完毕', 
                    'Yes': '是'}, 
            'English': {'BrokenEnding': ('Bad editing or other reasons that corrupted the file ending. '
                                        'If the text read is abnormal, the file may be corrupted. '
                                        'Obtaining the LRX file from a regular source can avoid this problem to the greatest extent. '
                                        'To force it on, click Continue.'
                                        '(Automatically fix the end of the file after modifying and saving)'), 
                    'Cancel': 'Cancel',
                    'ContentRead': 'The file was successfully opened. Click OK to save.', 
                    'ContentWrited': 'Content written: ', 
                    'Continue': 'Continue',
                    'CopyrightTitle': '\nThanks for Using.', 
                    'CreateFile1': 'A new file will be created at ', 
                    'CreateFile2': '\\.', 
                    'DelLang': 'Change Language', 
                    'ErrorTip': 'Error', 
                    'FileCreated': 'File created at ', 
                    'FileExists': 'The file already exists, please re-enter a filename.', 
                    'FilenameSetWays': 'Please enter a file name in the input box. If left blank, a random file name is generated for you.', 
                    'InvalidFile': 'Invalid lrx file (Invalid heading or ending).', 
                    'LRXError1': "Sharon (Ruxuan) Liang don't love me...o(╥﹏╥)o", 
                    'NewFile': 'New File', 
                    'NewSuccess': 'Created successfully.', 
                    'No': 'No', 
                    'OpenFile1': 'Open a file', 
                    'OpenFile2': 'Opening a file', 
                    'PlsSelectAction': 'Please select your action.', 
                    'Read': 'Read', 
                    'ReadingLog': 'Reading...', 
                    'ReadDoneLog': 'Read completed.', 
                    'SavingFile': 'Saving file...', 
                    'Select': 'Select a File', 
                    'SelectAction': 'Select an action', 
                    'SelectFile': 'Please select your LRX file.', 
                    'SetFilenameTitle': 'Set a filename', 
                    'Tips': 'Message', 
                    'Welcome': ('Welcome to LRX File Viewer!\nThe viewer can create, read, and write various versions of LRX files!\n'
                                'By Shimada Mizuki, QQ: 2068651347.\n'), 
                    'WelcomeTitle': 'Welcome', 
                    'Whichver': 'Please select a version for new file.', 
                    'WriteDoneLog': 'Saved successfully.', 
                    'Yes': 'Yes'}}

class LRXError(Exception): #自定义异常
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return self.message
    __module__ = 'builtins'

def checkEnd(lrxfileend):
    '''
        检查LRX3.0和LRX3.1的文件尾是否合法。
        lrxfileend：文件尾
    '''
    global lrxversion
    if lrxfileend != 'Ending: ' + ends[lrxversion]:
        print(strings[language]['BrokenEnding'])
        endingset = easygui.buttonbox(msg=strings[language]['BrokenEnding'], title=strings[language]['ErrorTip'], choices=(strings[language]['Continue'], strings[language]['Cancel']))
        if endingset == strings[language]['Continue']:
            pass
        else:
            return 'Cencelled'
        if lrxfileend == '':
            return 'NoneEnd' #没有尾（可能是尾被破坏）
        elif lrxfileend.startswith('E'):
            return 'FakeEnd' #以E开头但是尾不对（可能是尾被破坏）
        elif not lrxfileend.startswith('E'):
            if (lrxversion == '3.0' and not re.match(allowapi,lrxfileend.replace('n',''))) or (lrxversion == '3.1' and not re.match(allowapi31,lrxfileend.replace('n',''))):
                return 'FakeEnd'
            else:
                return False #不是以E开头（可能是尾损坏）
    else:
        return True

def checkHead(lrxfilecontect):
    '''
        检查头信息是否合法。
        lrxfilecontect：文件内容
    '''
    global lrxhead, lrxend, lrxversion
    lrxhead = lrxfilecontect[0]
    if lrxhead == 'Heading: ' + heads['1.0']: #以文件头判断文件版本 File version
        lrxversion = '1.0'
    elif lrxhead == 'Heading: ' + heads['2.0']:
        lrxversion = '2.0'
    elif lrxhead == 'Heading: ' + heads['3.0'] or lrxhead == 'Heading: ' + heads['3.1']:
        lrxend = lrxfilecontect[-1]
        if lrxhead == 'Heading: ' + heads['3.0']:
            lrxversion = '3.0'
        elif lrxhead == 'Heading: ' + heads['3.1']:
            lrxversion = '3.1'
    else:
        return False
    print('=========================LRX ' + lrxversion + ' File=========================')
    return True

def checkLangConfig():
    '''
        检查语言配置。
    '''
    global logfile, language
    logfile = os.getcwd() + '\\lrx.cfg'
    with open(logfile, 'a+', encoding='utf-8') as log:
        log.seek(0)
        loged = log.readlines()
        for lines in loged:
            if lines.startswith('Language: ') and lines.replace('Language: ','') in strings:
                language = lines.replace('Language: ','')
                return True
        return False

def convert(lrxccccc1):
    '''
        将字符转换为文字。
        lrxccccc1：需要转换的内容列表
    '''
    contents = []
    lrxcont = []
    for csdf in lrxccccc1: #用空格分隔每个数字
        lrxcont.append(csdf.split(' '))
    for c in lrxcont:
        if c == ['']:
            contents.append('')
        else:
            aaaaaaa = []
            for b in c:
                if b == '':
                    pass
                elif int(b)//14//8//2011 > sys.maxunicode: #挨个将数字转换成文字，如果超过能解码的范围，就取最大值
                    aaaaaaa.append(chr(sys.maxunicode))
                else:
                    aaaaaaa.append(chr(int(b)//14//8//2011))
            contents.append(''.join(aaaaaaa))
    return '\n'.join(contents)

def firstSel():
    global whichver, language, logfile
    syss = easygui.buttonbox(msg=strings[language]['Welcome'] + '\n\n' +strings[language]['PlsSelectAction'], 
                             title=strings[language]['WelcomeTitle'], choices=(strings[language]['Select'], strings[language]['NewFile'], strings[language]['DelLang'])) #syss is selection of this window to select an action. *syss 是用户在此窗口选择的项，用于获取用户的操作。
    if syss == strings[language]['Select']: #If "Select a file" is selected. *如果选择“选择文件”。
        filename1 = easygui.fileopenbox(msg=strings[language]['SelectFile'], title=strings[language]['Select'], default='*.lrx')
        if filename1 != None: #Open it if a file is selected. *打开选择的文件。
            readfile(filename1)
        firstSel()
    elif syss == strings[language]['NewFile']: #If "New File" is selected. *如果选择“新建文件”。
        whichver = easygui.buttonbox(msg=strings[language]['CreateFile1'] + os.getcwd() + strings[language]['CreateFile2'] + '\n\n' + strings[language]['Whichver'], 
                                        title=strings[language]['NewFile'], choices=('1.0', '2.0', '3.0', '3.1')) #whichver is version is selected of file. *whichver是选择的文件版本
        if whichver != None:
            if setFilename():
                newFile(newfile) #新建文件
        firstSel()
    elif syss == strings[language]['DelLang']:
        with open(logfile, 'w+', encoding='utf-8') as log:
            del language
        return True

def newFile(newfile1):
    '''
        新建文件。
        New File.
        newfile1：文件路径 *File path.
    '''
    with open(newfile1,'w+', encoding='utf-8') as lrx:
        if whichver == '1.0' or whichver == '2.0':
            lrx.write('Heading: ' + heads[whichver] + '\n')
        elif whichver == '3.0' or whichver == '3.1':
            lrx.write('Heading: ' + heads[whichver] + '\n')
            lrx.write('Ending: ' + ends[whichver])
    print(strings[language]['FileCreated'] + newfile)
    easygui.msgbox(strings[language]['FileCreated'] + newfile, strings[language]['NewSuccess'])

def randomFilename():
    '''
        随机生成文件名。
        Generate a filename randomly.
    '''
    newfilename = [alphabet[random.randint(0,35)] for a in range(random.randint(8,15))]
    newfilename = ''.join(newfilename)
    newfile = os.getcwd() + '\\' + newfilename + '.lrx'
    if os.path.isfile(newfile):
        randomFilename()
    return newfile

def readfile(filename):
    '''
        读取文件。
    '''
    global heads, lrxversion, lrxend, lrxhead
    with open(filename,'a+', encoding='utf-8') as lrx:
        editend = reads(filename,lrx)
        if editend == contents or editend == 'None':
            pass
        elif editend:
            writes(editend, lrx)
        else:
            print(strings[language]['InvalidFile'])
            easygui.msgbox(strings[language]['InvalidFile'], strings[language]['ErrorTip'])

def reads(lrxfilename,fileobj):
    '''
        读取文件内容。
        lrxfilename：文件路径
        fileobj：已打开的文件对象
    '''
    global contents, lrxend
    lrxcontt = []
    fileobj.seek(0)
    for asd in fileobj.readlines():
        lrxcontt.append(asd)
    lrxcontt = ''.join(lrxcontt).strip('\n').split('\n')
    if checkHead(lrxcontt):
        if lrxversion == '3.0' or lrxversion == '3.1':
            endsget = checkEnd(lrxend)
            if endsget == 'Cencelled':
                return False
            elif not endsget or endsget == 'FakeEnd' or endsget == 'NoneEnd':
                if not endsget: #不是以E开头（可能是尾缺失）
                    fileobj.seek(0,2)
                    fileobj.write('\nEnding: ' + ends[lrxversion])
                elif endsget == 'NoneEnd': #直接添加尾
                    fileobj.seek(0,2)
                    fileobj.write('Ending: ' + ends[lrxversion])
                elif endsget == 'FakeEnd': #以E开头但是尾不对（可能是尾被破坏），删除此行换新尾
                    fileobj.seek(0)
                    fix = fileobj.readlines()[:-1]
                    fileobj.seek(0)
                    fileobj.truncate(0)
                    fileobj.write(''.join(fix)[:-1] + '\nEnding: ' + ends[lrxversion])
                fileobj.flush()
                lrxend = 'Ending: ' + ends[lrxversion]
        print(strings[language]['ReadingLog'] + '\n——————————————————————————')
        fileobj.seek(0)
        lrxcontect = fileobj.readlines()
        del lrxcontect[0]
        if lrxversion == '3.0' or lrxversion == '3.1':
            del lrxcontect[-1]
            if lrxcontect != []:
                lrxcontect[-1] = lrxcontect[-1][:-1]
        if lrxcontect != replaceCantConvert(lrxcontect):
            lrxcontect = replaceCantConvert(lrxcontect)
            fileobj.seek(0)
            fileobj.truncate(0)
            fileobj.write('\n'.join(lrxcontect))
            fileobj.flush
        lrxccccc = []
        for i in ''.join(lrxcontect):
            if lrxversion == '3.1':
                threekeytemp = []
                if i == ' ':
                    threekeytemp.append(' ')
                elif i == '\n':
                    threekeytemp.append('\n')
                else:
                    try:
                        threekeytemp.append(str(threekey.index(i))) #挨个将字母转换成数字
                    except IndexError:
                        threekeytemp.append('')
                ccccccc = ''.join(threekeytemp)
            else:
                ccccccc = i
            lrxccccc.append(ccccccc)
        contents = convert(''.join(lrxccccc).split('\n'))
        print(contents + '\n——————————————————————————\n' + strings[language]['ReadDoneLog'] + '\n——————————————————————————\n') #输出读取完成日志，并输出文件内容
        editend = easygui.textbox(msg=strings[language]['ContentRead'], title=lrxfilename, text=contents) #弹出文件窗口
        if editend == None or editend == '':
            return 'None'
        return editend
    else:
        return False

def replaceCantConvert(contectoflrxfile):
    '''
        替换掉不可转换的字母。
        contectoflrxfile：要替换的内容列表
    '''
    for indexofline,lineoffile in enumerate(contectoflrxfile): #读取每行
        for word in endingapi: #读取每行中的每个字
            if word in lineoffile: #若检测到不能转换的字符
                if lineoffile.endswith('\n'): # 删除不能转换的字符，有换行符则补回
                    contectoflrxfile[indexofline] = lineoffile = lineoffile[:lineoffile.index(word)] + '\n'
                else:
                    contectoflrxfile[indexofline] = lineoffile = lineoffile[:lineoffile.index(word)]
    return contectoflrxfile

def setFilename():
    global newfile
    newf = easygui.enterbox(msg=strings[language]['FilenameSetWays'], title=strings[language]['SetFilenameTitle'])
    if newf: #自己输入文件名
        newf = ''.join([newf,'.lrx'])
        for texti in bantext:
            newf = newf.replace(texti,'') #替换文件名中不能使用的字符
        newfile = os.getcwd() + '\\' + newf
        if os.path.isfile(newfile):
            print(strings[language]['FileExists'])
            easygui.msgbox(strings[language]['FileExists'], strings[language]['ErrorTip'])
            setFilename()
    elif newf == '': #随机生成文件名
        newf = newfile = randomFilename()
    return newf
    
def writes(edited, fileobj):
    print(strings[language]['SavingFile'])
    fileobj.seek(0)
    fileobj.truncate(0)
    fileobj.write(lrxhead + '\n')
    error = False
    subed = re.sub(banlistwords,'',edited,0,re.I) #将违禁词替换
    if subed != edited: #如果有违禁词被替换掉了
        error = 1
        edited = subed #把违禁词从写入的内容里替换掉
    del subed
    editeee = edited.split('\n')
    list2 = []
    for aaaa in editeee:
        list1 = []
        for ais in aaaa:
            if lrxversion == '3.1':
                tempssss = []
                for bgh in str(ord(ais)*2011*8*14):
                    tempssss.append(threekey[int(bgh)])
                list1.append(''.join(tempssss))
            else:
                list1.append(str(ord(ais)*2011*8*14))
        list2.append(' '.join(list1))
    fileobj.write('\n'.join(list2))
    if lrxversion == '3.0' or lrxversion == '3.1':
        fileobj.write('\n' + lrxend)
    if error:
        raise LRXError(strings[language]['LRXError1']) #我无法面对残酷的现实，救命啊
    print(contents + '\n——————————————————————————\n' + strings[language]['WriteDoneLog'] + '\n——————————————————————————\n')
    easygui.msgbox(strings[language]['WriteDoneLog'], strings[language]['Tips'])

if __name__ == '__main__':
    while True:
        langed = checkLangConfig() #检查是否存在语言配置
        if not langed: #如果没有就写入
            language = easygui.buttonbox(msg='请选择软件语言。\nPlease select the language of interface.\n\n软件的语言会被保存在lrx.cfg中，如需修改请删除该文件或清除其内容或单击切换语言。\nThe language of the software will be saved in the lrx .cfg file. Delete the file or click the "Change Language" button if you need to modify it.', title='设置语言/Set language', choices=('中文', 'English'))
            with open(logfile, 'w+', encoding='utf-8') as log:
                if language != None:
                    log.write('Language: ' + str(language))
                    continue
        print(strings[language]['Welcome'])
        selection = firstSel()
        if selection:
            continue
        print(strings[language]['CopyrightTitle'] + '\nCopyright © 2023 Shimada Mizuki. All Rights Reserved.') #结尾版权信息 Copyright
        break
