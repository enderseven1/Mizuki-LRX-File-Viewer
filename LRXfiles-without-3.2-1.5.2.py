#-*- coding:utf-8 -*-
# coding:unicode_escape
# without 3.2
'''
    中文: 
    @ 作者：岛田水木
    @ 版本：1.5.2
    @ 创建日期：2023/5/28
    @ 最后更新：2023/6/4
    @ 更新日志：
        v1.0 2023/5/28: 初版发布。
        v1.1 2023/5/29: 1.添加英语语言。2.支持LRX文件3.0、3.1。3.修复bug。
        v1.2 2023/5/30: 1.修复bug。
        v1.3 2023/5/31: 1.修复bug。
        v1.4 2023/6/1: 1.修复bug。2.增强了对文件尾的修复能力。
        v1.5 2023/6/2: 1.简化了代码结构。2.文件尾损坏时可以选择不打开。
        v1.5.1 2023/6/3: 1.合并窗口。2.简洁代码，去掉很多if语句及循环结构，以递归函数替换。
        v1.5.2 2023/6/4: 1.添加了3.2版本文件。2.创造了很多bug。3.使用Tkinter。
        
    English:
    @ Author: Shimada Mizuki
    @ Version: 1.5.2
    @ Create Date: 2023/5/28
    @ Last Update: 2023/6/4
    @ Changelog: 
        v1.0 2023/5/28: First version. 
        v1.1 2023/5/29: (1)Add English language. (2)Add LRX 3.0,3.1 file. (3)Fix some bugs.
        v1.2 2023/5/30: (1)Fix some bugs.
        v1.3 2023/5/31: (1)Fix some bugs.
        v1.4 2023/6/1: (1)Fix some bugs.
        v1.5 2023/6/2: (1)Fix some bugs. (2)You can choose not to open the end of the file if it is damaged.
        v1.5.1 2023/6/3: (1)Consolidated some windows. (2)The code is concise, removing a lot of if statements and loop structures.
        v1.5.2 2023/6/4: (1)Add LRX 3.2 file. (2)Made a lot of bug. (3)Use Tkinter.

    LRX文件版本概述：
        LRX 1.0/2.0/3.0 一样，只是文件头不同。
        LRX 3.1 在 3.0 的基础上将文件头的字母区分大小写，并将内容也从数字改为字母。
        LRX 3.2 在 3.1 的基础上启用了密码。

    LRX file version description:
        LRX 1.0/2.0/3.0 is the same, except that the file header is different.
        LRX 3.1 builds on 3.0 to make the letters of the file header case-sensitive and change the content from numbers to letters.
        LRX 3.2 has passwords enabled from 3.1.
'''

print('检查依赖项（Checking modules）...')
#导入模块
try:
    module = 'os'
    print('查找' + module + '库（Checking module named ' + module + '）...', end=' ')
    import os #操作系统库
    print('Yes.')
    module = 'easygui'
    print('查找' + module + '库（Checking module named ' + module + '）...', end=' ')
    import easygui #简易GUI
    print('Yes.')
    module = 'random'
    print('查找' + module + '库（Checking module named ' + module + '）...', end=' ')
    import random #随机库
    print('Yes.')
    module = 'sys'
    print('查找' + module + '库（Checking module named ' + module + '）...', end=' ')
    import sys #系统库
    print('Yes.')
    module = 're'
    print('查找' + module + '库（Checking module named ' + module + '）...', end=' ')
    import re #正则表达式
    print('Yes.')
    module = 'tkinter'
    print('查找' + module + '库（Checking module named ' + module + '）...', end=' ')
    import tkinter #GUI界面库
    print('Yes.')
    print('依赖项全部齐全，启动（Modules are available, launching）...\n')
except ModuleNotFoundError as description:
    description = str(description)
    print(description.replace('No module named ', '对不起，找不到模块').replace('\'', '') + '（' + description + '）。')
    MODULE_APPLY = False
else:
    MODULE_APPLY = True

#初始化Tkinter
root = tkinter.Tk() 
root.withdraw()

#设置常量
#以下每次更新都要改变
VERSION = '1.5.2'
OLD_VERS = ('1.0','1.1','1.2','1.3','1.4','1.5','1.5.1') #以往版本，判断上一个使用的版本是什么版本
WHAT_S_NEW = {'中文':('感谢你更新到 v' + VERSION + ' 版本！以下是该版本的最新特性：\n'
                    '一、新增带密码保护的 LRX 3.2 版本。\n二、采用C++语言模块，提升安全性和速度。\n'
                    '三、使用Tkinter的文件/文件夹选择窗口替代easygui里的。\n四、优化源代码的结构。\n'
                    '五、修正了一些BUG。\n六、新增“新增特性”窗口。\n七、依赖项检查。'),
              'English':('Thank you for update to version ' + VERSION + '!\nWhat\'s new:\n'
                         '1. Add LRX 3.2 with password protection.\n2. Using a module made by C++ to improve running speed.\n'
                         '3. Using filedialog of tkinter instead of easygui.\n4. Optimize the structure of the source code.\n'
                         '5. Fix some bugs.\n6. Add What\'s New window.\n7. Auto-check modules.')}

#以下则不用每次都改变
HEADERS = {'1.0':'6025631696 5160966048 7622076112 5654449360 4936184512 6177212832 4576714240', 
         '2.0':'6025631696 5160966048 7622076112 5654449360 6584207056 4576714240', 
         '3.0':'xwauxioxnx uoxwnxxwra uxaawuxooa uxurrrnixw xuarawuwux ruuxuorarw',
         '3.1':'xwAUxIoxnx UoxwnxxwRa uxAAwuxooA UxURRRnIxw xUaRAwuwUx RUuxuoRARw'} #定义头 Header
TRAILERS = {'3.0':'18694256 23424128 23649360 24550288 21847504 22523200 21847504 7207424 17342864 23649360 27478304 26352144 24099824 23649360',
        '3.1':'oaxnRAUx AIRARoAa AIxRnIxw ARUUwAaa AoaRuUwR AAUAIAww AoaRuUwR uAwuRAR ouIRAaxR AIxRnIxw AuRuaIwR AxIUAoRR ARwnnaAR AIxRnIxw'} #定义尾 Ending
ALLOWED_CHARS = r'(1)|(2)|(3)|(4)|(5)|(6)|(7)|(8)|(9)|(0)'
ALLOWED_CHARS_31 = r'(w)|(o)|(A)|(I)|(R)|(U)|(x)|(u)|(a)|(n)' #3.1版本文件中允许出现的文字
BANLISTWORDS = r'(梁如萱我喜欢你)|(梁如萱我爱你)|(Liang Ruxuan I Love You)|(Liang Ruxuan I Like You)' #违禁词表
ALPHABET = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0') #随机生成用字母数字表 Alphabet for random filename
KEY_OF_VER_31 = ('w','o','A','I','R','U','x','u','a','n') #3.1解码器
BANED_CHARS_IN_FILENAME = ('"', '?', '>', '<', '\\', '|', '*', '/', ' ') #不能出现在文件名中的字符
EXTRA_NEWLINE = r'(\n)+' #多余的换行符
STRINGS_OF_PY = {'中文': {'BrokenTrailer': ('错误编辑等原因破坏了尾信息，若读取的文本异常，可能该文件已损坏。' #定义语言
                                    '从正规渠道取得lrx文件可以有效避免产生此问题。若要强制打开请点击继续。（修改并保存后自动修复尾信息）'), 
                    'Cancel': '取消',
                    'ContentRead': '已成功打开文件，单击OK即可保存。', 
                    'ContentWrited': '内容已完整写入文件中：', 
                    'Continue': '继续',
                    'CopyrightTitle': '\n感谢使用', 
                    'CreateFile1': '将在', 
                    'CreateFile2': '/创建文件。', 
                    'DelLang': '切换语言', 
                    'ErrorTip': '错误提示', 
                    'FileCreated': '文件已创建：', 
                    'FileExists': '文件已存在，请重新输入。', 
                    'FilenameSetWays': '请在输入框中输入文件名，若留空则为你随机生成。', 
                    'InvalidFile': '无效lrx文件', 
                    'LRXError1': '梁如萱她不爱我...o(╥﹏╥)o', 
                    'LRXFileType': 'LRX 文件',
                    'NewFile': '新建文件', 
                    'NewSuccess': '创建成功', 
                    'No': '否', 
                    'OpenFile1': '打开文件', 
                    'OpenFile2': '打开文件', 
                    'Period': '。',
                    'PlsSelectAction': '请选择你的操作：', 
                    'Read': '读取文件', 
                    'ReadingLog': '读取中...', 
                    'ReadDoneLog': '读取完毕', 
                    'SavingFile': '正在保存...', 
                    'Select': '选择文件', 
                    'SelectFile': '请选择你的LRX文件。', 
                    'SelectFolder': '选择文件夹', 
                    'SetFilenameTitle': '文件名', 
                    'TheSameChars': '有相同的字符：',
                    'Tips': '提示信息', 
                    'TooShort': '不能少于十个字符',
                    'UnsupportedChar': '不支持此字符：',
                    'Welcome': ('欢迎使用LRX文件查看器！\n本查看器可以新建、读取和写入各种版本的LRX文件！\n'
                                '作者岛田水木，QQ：2068651347。\n'), 
                    'WelcomeTitle': '欢迎使用\n', 
                    'WhatsNew': '新增特性',
                    'Whichver': '请选择文件版本', 
                    'WriteDoneLog': '保存完毕', 
                    'Yes': '是'},
            'English': {'BrokenTrailer': ('Bad editing or other reasons that corrupted the trailer. '
                                        'If the text read is abnormal, the file may be corrupted. '
                                        'Obtaining the LRX file from a regular source can avoid this problem to the greatest extent. '
                                        'To force it on, click Continue.'
                                        '(Automatically fix the trailer after modifying and saving)'), 
                    'Cancel': 'Cancel',
                    'ContentRead': 'The file was successfully opened. Click OK to save.', 
                    'ContentWrited': 'Content written: ', 
                    'Continue': 'Continue',
                    'CopyrightTitle': '\nThanks for Using.', 
                    'CreateFile1': 'A new file will be created at ', 
                    'CreateFile2': '/.', 
                    'DelLang': 'Change Language', 
                    'ErrorTip': 'Error', 
                    'FileCreated': 'File created at ', 
                    'FileExists': 'The file already exists, please re-enter a filename.', 
                    'FilenameSetWays': 'Please enter a file name in the input box. If left blank, a random file name is generated for you.', 
                    'InvalidFile': 'Invalid LRX file', 
                    'LRXError1': "Sharon (Ruxuan) Liang don't love me...o(╥﹏╥)o", 
                    'LRXFileType': 'LRX files',
                    'NewFile': 'New File', 
                    'NewSuccess': 'Created successfully.', 
                    'No': 'No', 
                    'OpenFile1': 'Open a file', 
                    'OpenFile2': 'Opening a file', 
                    'Period': '.',
                    'PlsSelectAction': 'Please select your action.', 
                    'Read': 'Read', 
                    'ReadingLog': 'Reading...', 
                    'ReadDoneLog': 'Read completed.', 
                    'SavingFile': 'Saving file...', 
                    'Select': 'Select a File', 
                    'SelectFile': 'Please select your LRX file.', 
                    'SelectFolder': 'Select a Folder', 
                    'SetFilenameTitle': 'Set a filename',
                    'TheSameChars': 'There are the same characters: ',
                    'Tips': 'Message', 
                    'TooShort': 'Must not be less than 10 characters', 
                    'UnsupportedChar': 'Unsupported character: ',
                    'Welcome': ('Welcome to LRX File Viewer!\nThe viewer can create, read, and write various versions of LRX files!\n'
                                'By Shimada Mizuki, QQ: 2068651347.\n'), 
                    'WelcomeTitle': 'Welcome', 
                    'WhatsNew': 'What\'s New',
                    'Whichver': 'Please select a version for new file.', 
                    'WriteDoneLog': 'Saved successfully.', 
                    'Yes': 'Yes'}}

class LRXError(Exception): #自定义异常
    '''
        定义一个新异常。
        用法：raise LRXError(message)
        message：异常描述。
    '''
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
    global version_of_file
    if (lrxfileend != 'Ending: ' + TRAILERS[version_of_file]
        and lrxfileend != 'Trailer: ' + TRAILERS[version_of_file]):
        if version_of_file == '3.0' or version_of_file == '3.1':
            print(STRINGS_OF_PY[language]['BrokenTrailer'])
            trailerset = easygui.buttonbox(msg=STRINGS_OF_PY[language]['BrokenTrailer'], title=STRINGS_OF_PY[language]['ErrorTip'], choices=(STRINGS_OF_PY[language]['Continue'], STRINGS_OF_PY[language]['Cancel']))
            if trailerset == STRINGS_OF_PY[language]['Continue']:
                if lrxfileend.startswith('E'):
                    return 'FakeEnd' #以E开头但是尾不对（可能是尾被破坏）
                elif not lrxfileend.startswith('E'):
                    if ((version_of_file == '3.0' and not re.match(ALLOWED_CHARS,lrxfileend.replace('n','')))
                        or (version_of_file == '3.1' and not re.match(ALLOWED_CHARS_31,lrxfileend.replace('n','')))):
                        return 'FakeEnd'
                    else:
                        return False #不是以E开头（可能是尾损坏）
            else:
                return False
        else:
            return 'Cencelled'

    else:
        return True

def checkHead(lrxfilecontect):
    '''
        检查头信息是否合法。
        lrxfilecontect：文件内容
    '''
    global head_of_this_file, end_of_this_file, version_of_file
    head_of_this_file = lrxfilecontect[0]
    if (head_of_this_file == 'Heading: ' + HEADERS['1.0']
        or head_of_this_file == 'Header: ' + HEADERS['1.0']): #以文件头判断文件版本 File version
        version_of_file = '1.0'
    elif (head_of_this_file == 'Heading: ' + HEADERS['2.0']
          or head_of_this_file == 'Header: ' + HEADERS['2.0']):
        version_of_file = '2.0'
    elif (head_of_this_file == 'Heading: ' + HEADERS['3.0'] or head_of_this_file == 'Heading: ' + HEADERS['3.1']
          or head_of_this_file == 'Header: ' + HEADERS['3.0'] or head_of_this_file == 'Header: ' + HEADERS['3.1']):
        end_of_this_file = lrxfilecontect[-1]
        if (head_of_this_file == 'Heading: ' + HEADERS['3.0']
            or head_of_this_file == 'Header: ' + HEADERS['3.0']):
            version_of_file = '3.0'
        elif (head_of_this_file == 'Heading: ' + HEADERS['3.1']
              or head_of_this_file == 'Header: ' + HEADERS['3.1']):
            version_of_file = '3.1'
    else:
        return False
    return True

def checkLastVersion():
    '''
        检查语言配置。
    '''
    global config_file
    config_file = os.getcwd() + '\\lrx.cfg'
    with open(config_file, 'a+', encoding='utf-8') as configobj:
        configobj.seek(0)
        cntent_of_cfg = configobj.readlines()
        for lines in cntent_of_cfg:
            if lines.startswith('Version: ') and lines.replace('Version: ','').strip() == VERSION:
                return False  #就是更新的
        return True #不是更新的
    
def checkLangConfig():
    '''
        检查语言配置。
    '''
    global config_file
    config_file = os.getcwd() + '\\lrx.cfg'
    with open(config_file, 'a+', encoding='utf-8') as configobj:
        configobj.seek(0)
        cntent_of_cfg = configobj.readlines()
        for lines in cntent_of_cfg:
            if lines.startswith('Language: ') and lines.replace('Language: ','').strip() in STRINGS_OF_PY:
                return lines.replace('Language: ','').strip()
        return False

def convert(content_list):
    '''
        将字符转换为文字。
        content_list：需要转换的内容列表
    '''
    processed_content = []
    lrxcont = []
    for csdf in content_list: #用空格分隔每个数字
        lrxcont.append(csdf.split(' '))
    for c in lrxcont:
        if c == ['']:
            processed_content.append('')
        else:
            aaaaaaa = []
            for b in c:
                if b == '':
                    pass
                elif int(b)//14//8//2011 > sys.maxunicode: #挨个将数字转换成文字，如果超过能解码的范围，就取最大值
                    aaaaaaa.append(chr(sys.maxunicode))
                else:
                    aaaaaaa.append(chr(int(b)//14//8//2011))
            processed_content.append(''.join(aaaaaaa))
    return '\n'.join(processed_content)
    
def firstSel():
    '''
        主菜单。
    '''
    global selected_version, language, config_file, Folderpath, version_of_file
    version_of_file = 0
    selected_item = easygui.buttonbox(msg=STRINGS_OF_PY[language]['Welcome'] + '\n\n' +STRINGS_OF_PY[language]['PlsSelectAction'], 
                             title=STRINGS_OF_PY[language]['WelcomeTitle'], choices=(STRINGS_OF_PY[language]['Select'], STRINGS_OF_PY[language]['NewFile'], STRINGS_OF_PY[language]['DelLang'])) #selected_item is selection of this window to select an action. *selected_item 是用户在此窗口选择的项，用于获取用户的操作。
    if selected_item == STRINGS_OF_PY[language]['Select']: #If "Select a file" is selected. *如果选择“选择文件”。
        selected_file = tkinter.filedialog.askopenfilename(title=STRINGS_OF_PY[language]['Select'], filetypes=((STRINGS_OF_PY[language]['LRXFileType'], "*.lrx"),)) #选择文件
        if selected_file != None and selected_file != '': #Open it if a file is selected. *打开选择的文件。
            readfile(selected_file)
        selected_item = firstSel()
    elif selected_item == STRINGS_OF_PY[language]['NewFile']: #If "New File" is selected. *如果选择“新建文件”。
        Folderpath = tkinter.filedialog.askdirectory(title=STRINGS_OF_PY[language]['SelectFolder'])
        if Folderpath != '':
            selected_version = easygui.buttonbox(msg=STRINGS_OF_PY[language]['CreateFile1'] + Folderpath + STRINGS_OF_PY[language]['CreateFile2'] + '\n\n' + STRINGS_OF_PY[language]['Whichver'], 
                                         title=STRINGS_OF_PY[language]['NewFile'], choices=('1.0', '2.0', '3.0', '3.1')) #selected_version is version is selected of file. *selected_version是选择的文件版本
            if selected_version != None:
                setFilename()
                newFile(path_of_newfile) #新建文件
        selected_item = firstSel()
    elif selected_item == STRINGS_OF_PY[language]['DelLang']: #清除语言信息
        with open(config_file, 'a+', encoding='utf-8') as log:
            log.seek(0)
            content_of_log = log.readlines()
            for index_of_log, content_of_line in enumerate(content_of_log):
                if content_of_line.strip() == ('Language: ' + language):
                    content_of_log[index_of_log] = '\n'
            log.seek(0)
            log.truncate()
            log.write(''.join(content_of_log))
            del language
        selected_item = 'DelLang'
    return selected_item

def lrxdecode(content_of_lrxfile):
    '''
        3.1解码器。
    '''
    content_list_of_file = []
    for char_will_be_converted in ''.join(content_of_lrxfile):
        if version_of_file == '3.1':
            temp_of_converting = []
            if char_will_be_converted == ' ':
                temp_of_converting.append(' ')
            elif char_will_be_converted == '\n':
                temp_of_converting.append('\n')
            else:
                try:
                    temp_of_converting.append(str(KEY_OF_VER_31.index(char_will_be_converted ))) #挨个将字母转换成数字
                except ValueError:
                    temp_of_converting.append('')
            content_list_of_file.append(''.join(temp_of_converting))
        else:
            content_list_of_file.append(char_will_be_converted )
    processed_content = convert(''.join(content_list_of_file).split('\n'))
    return processed_content

def newFile(filepath):
    '''
        新建文件。
        New File.
        filepath：文件路径 *File path.
    '''
    with open(filepath,'w+', encoding='utf-8') as lrx:
        if selected_version == '1.0' or selected_version == '2.0':
            lrx.write('Header: ' + HEADERS[selected_version] + '\n')
        elif selected_version == '3.0' or selected_version == '3.1':
            lrx.write('Header: ' + HEADERS[selected_version] + '\n')
            lrx.write('Trailer: ' + TRAILERS[selected_version])
    print(STRINGS_OF_PY[language]['FileCreated'] + filepath)
    easygui.msgbox(STRINGS_OF_PY[language]['FileCreated'] + filepath, STRINGS_OF_PY[language]['NewSuccess'])

def randomFilename():
    '''
        随机生成文件名。
        Generate a filename randomly.
    '''
    global path_of_newfile
    name_of_new_file = [ALPHABET[random.randint(0,35)] for a in range(random.randint(8,15))]
    name_of_new_file = ''.join(name_of_new_file)
    path_of_newfile = Folderpath + '/' + name_of_new_file + '.lrx'
    if os.path.isfile(path_of_newfile):
        randomFilename()
    return path_of_newfile

def readfile(filename):
    '''
        读取文件。
    '''
    global version_of_file, end_of_this_file, head_of_this_file
    with open(filename,'a+', encoding='utf-8') as lrx: #打开文件
        edited_content = reads(filename,lrx)
        if ((edited_content != None and edited_content != False and edited_content == processed_content)
             or edited_content == 'None'):
            pass
        elif edited_content:
            writes(edited_content, lrx)
        else: #如果文件头无效
            print(STRINGS_OF_PY[language]['InvalidFile'])
            easygui.msgbox(STRINGS_OF_PY[language]['InvalidFile'], STRINGS_OF_PY[language]['ErrorTip'])

def reads(lrxfilename,fileobj):
    '''
        读取文件内容。
        lrxfilename：文件路径
        fileobj：已打开的文件对象
    '''
    global processed_content, end_of_this_file, password
    fileobj.seek(0)
    content_for_check = ''.join(fileobj.readlines()).strip('\n').split('\n')
    if checkHead(content_for_check): #检查头
        if version_of_file == '3.0' or version_of_file == '3.1': 
            got_trailer = checkEnd(end_of_this_file) #检查尾
            if got_trailer == 'Cencelled': #如果用户不选择强制访问
                return False
            elif not got_trailer or got_trailer == 'FakeEnd' or got_trailer == 'NoneEnd':
                trailerFix(got_trailer, fileobj)
        print('=========================LRX ' + version_of_file + ' File=========================')
        print(STRINGS_OF_PY[language]['ReadingLog'] + '\n——————————————————————————')
        fileobj.seek(0)
        unprocessed_content = fileobj.readlines()
        del unprocessed_content[0] #删除头
        if version_of_file == '3.0' or version_of_file == '3.1': 
            del unprocessed_content[-1]
            if unprocessed_content != []:
                unprocessed_content[-1] = unprocessed_content[-1][:-1]
        processed_content = lrxdecode(unprocessed_content)
        if processed_content == 'Cancelled': #若用户取消访问
            return 'None'
        elif processed_content != False:
            print(processed_content + '\n——————————————————————————\n' + STRINGS_OF_PY[language]['ReadDoneLog'] + '\n——————————————————————————\n') #输出读取完成日志，并输出文件内容
            edited_content = easygui.textbox(msg=STRINGS_OF_PY[language]['ContentRead'], title=lrxfilename, text=processed_content) #弹出文件窗口
            if edited_content == None or edited_content == '':
                return 'None'
            return edited_content
    else:
        return False

def setFilename():
    '''
        设置文件名窗口。
    '''
    global path_of_newfile
    file_name = easygui.enterbox(msg=STRINGS_OF_PY[language]['FilenameSetWays'], title=STRINGS_OF_PY[language]['SetFilenameTitle'])
    if file_name: #自己输入文件名
        file_name = ''.join([file_name,'.lrx'])
        for BANED_CHAR in BANED_CHARS_IN_FILENAME:
            file_name = file_name.replace(BANED_CHAR,'') #替换文件名中不能使用的字符
        path_of_newfile = Folderpath + '/' + file_name
        if os.path.isfile(path_of_newfile):
            print(STRINGS_OF_PY[language]['FileExists'])
            easygui.msgbox(STRINGS_OF_PY[language]['FileExists'], STRINGS_OF_PY[language]['ErrorTip'])
            setFilename()
    elif file_name == '': #随机生成文件名
        file_name = path_of_newfile = randomFilename()
    return file_name

def trailerFix(broken_trailer, fileobj):
    '''
        文件尾修复。
        broken_trailer：checkEnd函数返回值。
        fileobj：文件对象。
    '''
    global end_of_this_file
    if not broken_trailer: #不是以E开头（可能是尾缺失）
        fileobj.seek(0,2)
        fileobj.write('\nTrailer: ' + TRAILERS[version_of_file])
    elif broken_trailer == 'FakeEnd': #以E开头但是尾不对（可能是尾被破坏），删除此行换新尾
        fileobj.seek(0)
        fix = fileobj.readlines()[:-1]
        fileobj.seek(0)
        fileobj.truncate(0)
        fileobj.write(''.join(fix)[:-1] + '\nTrailer: ' + TRAILERS[version_of_file])
    fileobj.flush()
    end_of_this_file = 'Trailer: ' + TRAILERS[version_of_file]

def writes(edited, fileobj):
    '''
        写入文件。
    '''
    print(STRINGS_OF_PY[language]['SavingFile']) #输出正在保存日志
    fileobj.seek(0)
    fileobj.truncate(0)
    fileobj.write(head_of_this_file + '\n')
    error = False
    subed_content = re.sub(BANLISTWORDS,'',edited,0,re.I) #将违禁词替换
    if subed_content != edited: #如果有违禁词被替换掉了
        error = 1
        edited = subed_content #把违禁词从写入的内容里替换掉
    del subed_content
    splited_content = edited.split('\n')
    line_of_content = []
    for unprocessed_line in splited_content:
        char_of_line = []
        for unprocessed_char in unprocessed_line:
            if version_of_file == '3.1': #字母编码法
                temp_of_converting = []
                for number_of_charcode in str(ord(unprocessed_char)*2011*8*14):
                    temp_of_converting.append(KEY_OF_VER_31[int(number_of_charcode)])
                char_of_line.append(''.join(temp_of_converting))
            else:
                char_of_line.append(str(ord(unprocessed_char)*2011*8*14)) #数字编码法
        line_of_content.append(' '.join(char_of_line))
    fileobj.write('\n'.join(line_of_content))
    if version_of_file == '3.0' or version_of_file == '3.1':
        fileobj.write('\n' + end_of_this_file)
    if error:
        raise LRXError(STRINGS_OF_PY[language]['LRXError1']) #我无法面对残酷的现实，救命啊
    fileobj.flush()
    print(processed_content + '\n——————————————————————————\n' + STRINGS_OF_PY[language]['WriteDoneLog'] + '\n——————————————————————————\n')
    easygui.msgbox(STRINGS_OF_PY[language]['WriteDoneLog'], STRINGS_OF_PY[language]['Tips'])

def writetoConfig(fileobj, writestarts, writends):
    fileobj.seek(0)
    con_content = fileobj.readlines() #读取全部内容
    if con_content != []:
        con_content[0] = writestarts + str(writends) + '\n' + con_content[0]
        fileobj.seek(0)
        fileobj.truncate()
        fileobj.write(re.sub(EXTRA_NEWLINE,'\n',''.join(con_content).strip()))
    else:
        fileobj.write(writestarts + str(writends) + '\n')

if __name__ == '__main__' and MODULE_APPLY: #当其不是作为模块出现时
    version_of_file = 0 #文件版本
    firstboot = True #是否为第一次启动
    is_updated = checkLastVersion() #是否是从其他版本更新的
    while True:
        language = checkLangConfig() #检查是否存在语言配置
        if not language: #如果没有就写入
            language = easygui.buttonbox(msg='请选择软件语言。\nPlease select the language of interface.\n\n软件的语言会被保存在lrx.cfg中，如需修改请删除该文件或清除其内容或单击切换语言。\nThe language of the software will be saved in the lrx .cfg file. Delete the file or click the "Change Language" button if you need to modify it.', title='设置语言/Set language', choices=('中文', 'English'))
            with open(config_file, 'a+', encoding='utf-8') as configobj: #写入语言信息
                if language != None:
                    writetoConfig(configobj, 'Language: ', language)
                    continue
                else:
                    break
        if is_updated: #如果是更新的（版本信息不对应）
            with open(config_file, 'a+', encoding='utf-8') as configobj:
                writetoConfig(configobj, 'Version: ', VERSION)
            print(WHAT_S_NEW[language])
            easygui.msgbox(WHAT_S_NEW[language] + '\nBy Shimada Mizuki', STRINGS_OF_PY[language]['WhatsNew'])
            is_updated = False
        if firstboot:
            print(STRINGS_OF_PY[language]['Welcome'])
            firstboot = False
        selection = firstSel()
        if selection == 'DelLang':
            continue
        print(STRINGS_OF_PY[language]['CopyrightTitle'] + '\nCopyright © 2023 Shimada Mizuki. All Rights Reserved.') #结尾版权信息 Copyright
        break
