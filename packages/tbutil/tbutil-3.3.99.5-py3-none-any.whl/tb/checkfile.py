def say0(s,t=.1,color='91',**args):
    from time import time
    print(end='\033[?25l\033[%sm'%color)
    st=time()
    for i in range(len(s)):
        while time()<st+i*t:
            pass
        print(end=s[i],flush=1)
    print('\033[0m\033[?25h',**args)
def say1(s,t=.1,color='91',**args):
    from time import time
    print(end='\033[?25l\033[%sm'%color)
    st=time()
    for i in range(len(s)):
        print(end='\033[90m_\033[%sm\033[D'%color,flush=1)
        while time()<st+i*t:
            pass
        print(end=' \033[D'+s[i],flush=1)
    print('\033[0m\033[?25h',**args)
def say2(s,t=.1,c1='91',c2='93',**args):
    from time import time
    from urwid.old_str_util import get_width
    print(end='\033[?25l\033[%sm'%c2)
    st=time()
    for i in range(len(s)):
        if s[i] not in '\r\n\t ':
            print(end='\033[%sm%s\033[%sm\033[%iD'%(c2,s[i],c1,get_width(ord(s[i]))),flush=1)
        while time()<st+i*t:
            pass
        print(end=s[i],flush=1)
    print('\033[0m\033[?25h',**args)
if __name__=='__main__':
    a='''我是云南的，云南怒江的；
怒江泸水市，泸水市六库；
六库傈僳族，傈僳族是这样叫；
乌鸦叫作阿南，青蛙叫作欧巴；
老公叫作搓趴，老婆叫作搓嘛；
香菜叫作野穴，红薯叫作阿梦；
老虎叫作喇嘛，黄瓜叫作阿布；
南瓜叫作阿普，鸡蛋叫作嘛啊耶夫。'''
    say0(a)
    say1(a)
    say2(a)
