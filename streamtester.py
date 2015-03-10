# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities  
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re, math, operator
import time
import os
import smtplib
from PIL import Image

class MVPD(unittest.TestCase):
    def setUp(self):
        d = DesiredCapabilities.CHROME
        d['loggingPrefs'] = { 'browser':'ALL' }
        self.driver = webdriver.Chrome(desired_capabilities=d)
        self.driver.set_window_size(1080, 800)
        self.driver.implicitly_wait(30)
        self.base_url = "http://youtube.com/#YOUR STREAM#"
        self.verificationErrors = []
        self.accept_next_alert = True
        self.screenGrabs = []
        self.user = 'AKIAIFVP6R4CTX5UTIPA'
        self.pw   = '#KEY#'
        self.seshost = 'email-smtp.us-east-1.amazonaws.com'
    
    def test_m_v_p_d(self):
        driver = self.driver
        driver.get(self.base_url)
        cur = 1
        fullround = 0
        while 1:
            print "saving a screenshot: " + str(cur)
            driver.save_screenshot('screenie'+ str(cur) + '.png')
            self.screenGrabs.append(str(cur))
            cur +=1
            time.sleep( 2 )
            if len(self.screenGrabs)>4:
                print 'remove screenie'+ str(self.screenGrabs[0]) + '.png'
                os.remove ('screenie'+ str(self.screenGrabs[0]) + '.png')
                del self.screenGrabs[0]
                self.calcImages ()
 
    def calcImages(self):
        images = [Image.open("screenie"+self.screenGrabs[0]+".png").histogram(), Image.open("screenie"+self.screenGrabs[1]+".png").histogram(), Image.open("screenie"+self.screenGrabs[2]+".png").histogram(), Image.open("screenie"+self.screenGrabs[3]+".png").histogram()]
        index = 0
        for x in range(len(images)-1):
            index = x
            for y in range(len(images)-x):
                if (index == index +y):
                    continue
                if (sum(images[index+y]) > 2240080 & sum(images[index+y]) < 2244080):
                    print "Getting slate"
                    continue
                rms = math.sqrt(reduce(operator.add, map(lambda a,b: (a-b)**2, images[index], images[index+y]))/len(images[index]))
                print "Different between screenshot", index+1 , "and", index+y+1, "is" , rms
                if rms < 1:
                    print "dispatching email.."
                    self.sendmail ()
                    self.fail("Screenshot are equal")
                    
    def sendmail (self):
        smtp = smtplib.SMTP(self.seshost)
        smtp.starttls()
        smtp.login(self.user, self.pw)
        smtp.sendmail('wenster9@gmail.com', 'wenster9@gmail.com', 'Subject:Stream Test\nResult equal')
        smtp.quit()
          
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
