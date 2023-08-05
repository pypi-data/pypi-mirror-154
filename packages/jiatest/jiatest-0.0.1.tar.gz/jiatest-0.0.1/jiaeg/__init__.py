import wda
from time import sleep

# Enable debug will see http Request and Response
# wda.DEBUG = True
wda.DEBUG = True
c = wda.Client('http://localhost:8100')

# get env from $DEVICE_URL if no arguments pass to wda.Client
# http://localhost:8100 is the default value if $DEVICE_URL is empty
launchParam = dict(isUITest = "YES")
s = c.session('com.meituan.imeituan-beta',None,launchParam)
sleep(3)
print("hello")
elementList = ["//XCUIElementTypeButton[@name=\"同意\"]","//XCUIElementTypeButton[@name=\"快速开启定位\"]"]
def test_setting():
    
    title = None
    for element in elementList: 
        title = clickAlert(s, 1)
        clickElement(s, element)
        print('clickelement final')
        title = clickAlert(s, 1)
    s.close()
    s1 = c.session()
    sleep(2)
    clickOtherAlert(s1, title)
    


def clickAlert(s, count):
    title = None
    for i in range(0, count):
        try:
            text = s.alert.text
            
            print('---------')
            print(text)
            if text is None:
                break
            title = text
            print(title)
            if title is not None and (title.find("位置") > -1 or title.find("通知") > -1 or title.find("无线数据") > -1 or title.find("跟踪") > -1):
                buttons = s.alert.buttons()
 
                if len(buttons) > 2:#有三个button
           
                    s.alert.click(buttons[0])
                elif len(buttons) > 1:#有两个button
        
                    s.alert.click(buttons[1])
            sleep(2)
        except wda.WDAError as e:
            if e.status == 27 or (("UserInfo" in e.value) and e.value.find("Failed to find button with label") > -1):
                print ("catch exception")
            else:
                raise
    return title

def clickOtherAlert(s, title=None):
    for i in range(0, 2):
        try:
            buttons = s.alert.buttons()
            if len(buttons) > 2:#有三个button
                button = buttons[0].encode()#点击第一个
                s.alert.click(button)
            elif len(buttons) > 1:#有两个button
                if title is not None and title.find("信任") > -1:
                    button = buttons[0].encode()#点击第一个
                    s.alert.click(button)
                else:
                    button = buttons[1].encode()#点击第二个
                    s.alert.click(button)
        except wda.WDAError as e:
            if e.status != 27:
                raise
        sleep(2)
def clickElement(s, element):
    try:
        sleep(5)
        print (element)
        s(xpath=element).click_exists(timeout=5.0)
        sleep(5)
    except wda.WDAError as e:
        print ("wda error:" + e.value)
    finally:
        print ("handle done.")
