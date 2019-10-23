#
#a general purpose instagram bot class that lets you do common instagram stuff.
#

from device import device
import random
import time
package = 'com.instagram.android'

class Instabot(device):
    def __init__(self,deviceId,model="pixel2", verbose=False):
        super(Instabot,self).__init__(deviceId,model,verbose)
        self.tapLocations.update({
            "a30": {
              "search": (300, 2145),
              "typeBar": (300, 151),
              "searchClear": (1003,149),
              "firstResult": (545,450),
              "firstPost" : (200,1050),
              "postComment": (180,1590),
              "submitComment": (983,1287),
              "backToProfile": (65,150),
              "writeComment":(290,1260),
              "notification": (757,2140),
              "firstNotification": (990,587)
            },
            "pixel2" : {
              "search": (319, 1732),
              "typeBar": (300, 127),
              "searchClear": (1003,125),
              "firstResult": (545,403),
              "firstPost" : (200,1450),
              "postComment": (180,1590),
              "submitComment": (1005,994),
              "backToProfile": (65,125),
              "writeComment":(290,1260),
              "notification": (750,1730),
              "firstNotification": (773,587),
              "confirmTag": (500,125),
              "emojis" :(345,1716),
              "heartEmoji": (991,1368),
              "textChars": (75,1750),
              "homePage": (980,1733),
              "videoExit": (330,425),
              "forceBack":(275,1870)
            }
        })
        # when ctrl + c is used in the terminal, remove monkey processes on the phones before ending the process
        if(self.verbose):
            print "Connected to device "+deviceId+"."
        self.openInstagram()
        print "wtffff"

    def openInstagram(self):
        activity = 'com.instagram.mainactivity.MainActivity'
        runComponent = package + '/' + activity
        self.device.startActivity(component=runComponent)
        if(self.verbose):
            print "Started instagram."

    def search(self,account='no_account_provided!'):
        self.device.drag((319,1732),(319,1732),1,300)
        self.sleep(2)
        self.touch("searchClear")
        self.type(account)
        self.sleep(3)
        self.touch("firstResult")
        self.sleep(4)

    def comment(self,account,toWhom,text="nice pic",last=False):
        self.chooseRandomPost()
        time.sleep(4)
        self.touchCommentButton()# 1550 1665
        time.sleep(5)
        self.type("@"+account[0:4])
        time.sleep(1)
        self.touch("confirmTag")
        time.sleep(.2)
        self.type(text.replace(" ","%s"),True)
        time.sleep(2)
        if(last == True):
            self.typeHeartEmoji();
        self.touch("submitComment")
        time.sleep(4)
        self.touch("backToProfile")
        time.sleep(2)

    def chooseRandomPost(self,choice=-1):
        if(self.model=="a30"):
           self.touchPoint((str(30+random.randint(0,970)),str(1390+random.randint(1,650))))
        elif(choice>-1):
            self.touchPoint((str(100+320*(choice % 3)),str(1610)))
            print "choosing at " +str(choice)+ " "+str(320*(choice % 3))
        else:
            #this value is 1610 bc 1600 sometimes tapped right in between posts
            self.touchPoint((str(300*random.randint(1,3)),str(1610)))

    def checkNotification(self):
        self.touch("notification")
        time.sleep(5)

    def touchCommentButton(self,xOffset=0):
        inBlack = False
        image = self.device.takeSnapshot()
        sub_image = image.getSubImage((180,500,20,1400))
        blackList = []
        #Finds the vertical sequence of black and white pixels that match the comment button.
        for x in xrange(4,1400):
            px = sub_image.getRawPixel(1,x)
            #if the current pixel is black
            if(px[1] < 50 and px[2] < 50 and px[3] < 50):
                if not inBlack:
                    blackList.append(x+500)
                inBlack = True
            else:
                inBlack = False
            pass
        target = 0;
        for i in range(len(blackList)-1):
            distanceBetweenBlack = abs(blackList[i+1]-blackList[i])
            if(abs(distanceBetweenBlack-50))<2 and target == 0:
                print "blacklist entry is "+str(blackList[i])
                abovepx = sub_image.getRawPixel(1,blackList[i]-10-500)
                isWhiteAbove = abovepx[1] > 250 and abovepx[2] > 250 and abovepx[3] > 250
                middlepx = sub_image.getRawPixel(1,blackList[i]-10-500)
                isWhiteInside = middlepx[1] > 250 and middlepx[2] > 250 and middlepx[3] > 250
                underpx = sub_image.getRawPixel(1,blackList[i]-10-500)
                isWhiteUnder = underpx[1] > 250 and underpx[2] > 250 and underpx[3] > 250
                if(isWhiteAbove and isWhiteInside and isWhiteUnder):
                    target = (blackList[i+1]+blackList[i])/2
        if(target == 0):
            self.scroll(770,500)
            time.sleep(1)
            self.touchCommentButton()
        print "the target is "+str(target)
        time.sleep(.1)
        if(target != 0):
            self.device.shell("input tap "+str(180+xOffset)+" "+str(target))
            return target

    def touchLikeButton(self):
        return self.touchCommentButton(-60)
