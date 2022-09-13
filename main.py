from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import *
import os
import sys


class MainWindow(QMainWindow):
    history = []
    def __init__(self,*args, **kwargs):
        super(MainWindow,self).__init__(*args,**kwargs)


        # Creating a tab widget

        self.tabs = QTabWidget()

        # Making document mode ture
        self.tabs.setDocumentMode(True)

        # adding action when double clicked
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)

        # adding action when tab is changed
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.contextMenuEvent = self.mycontextMenuEvent
        
        # making tabs closeable
        self.tabs.setTabsClosable(True)

        # adding action when tab close is requested
        self.tabs.tabCloseRequested.connect(self.close_current_tab)

        # Making tabs as a central widget
        self.setCentralWidget(self.tabs)

        self.status = QStatusBar()

        # setting status bar to the main window
        self.setStatusBar(self.status)
        # navbar

        navbar = QToolBar("Navigation")
        self.addToolBar(navbar)

        back_btn = QAction('Back',self)
        back_btn.triggered.connect(lambda:self.tabs.currentWidget().back())
        navbar.addAction(back_btn)

        forward_btn = QAction('Forward',self)
        forward_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
        navbar.addAction(forward_btn)

        reload_btn = QAction('Reload',self)
        reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
        navbar.addAction(reload_btn)

        home_btn = QAction('Home',self)
        home_btn.triggered.connect(self.navigateHome)
        navbar.addAction(home_btn)

        # adding a separator
        navbar.addSeparator()

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)



        historyBtn = QAction('history',self)
        historyBtn.triggered.connect(self.browserHistory)
        navbar.addAction(historyBtn)
        
        # Creating the first tab
        self.add_new_tab(QUrl('http://www.google.com'), 'Homepage')
        
        self.show()
        self.setWindowTitle("Vedant's browser")

    def mycontextMenuEvent(self,event):
        menu = QtWidgets.QMenu(self)
        oneAction = menu.addAction("&Open New Tab")
        menu.exec_(event.globalPos())
        print(oneAction)


    def add_new_tab(self,qurl=None,label='BLANK'):
        if(qurl==None):
            qurl = QUrl('http://www.google.com')
        # setting url to browser
        browser = QWebEngineView()
        browser.setUrl(qurl)

        browser.setUrl(qurl)
        
        # setting tab index
        i=self.tabs.addTab(browser,label)
        self.tabs.setCurrentIndex(i)
        
        browser.urlChanged.connect(lambda qurl=qurl,browser=browser:self.update_urlbar(qurl,browser))

        # adding action to the browser when loading is finished
        # set the tab title
        browser.loadFinished.connect(lambda _,i=i,browser=browser:
                                        self.tabs.setTabText(i,browser.page().title()))

    
    def tab_open_doubleclick(self,i):
        # checking index i.e
        # No tab under the click
        if i==-1:
            self.add_new_tab()

    # wen tab is changed
    def current_tab_changed(self,i):
        qurl = self.tabs.currentWidget().url()
        self.update_urlbar(qurl,self.tabs.currentWidget())
        self.update_title(self.tabs.currentWidget())

    # when tab is closed
    def close_current_tab(self,i):
        if(i<1):
            return
        self.tabs.removeTab(i)

    def update_title(self, browser):
  
        # if signal is not from the current tab
        if browser != self.tabs.currentWidget():
            # do nothing
            return
  
        # get the page title
        title = self.tabs.currentWidget().page().title()
  
        # set the window title
        self.setWindowTitle("% s - Vedant's browser" % title)

    def navigateHome(self,browser):
        browser.setUrl(QUrl('http://google.com'))

    def navigate_to_url(self):
        url = QUrl(self.url_bar.text())
        if url.scheme()=="":
            url.setScheme("http")
        self.tabs.currentWidget().setUrl(url)
        
    def update_urlbar(self,qurl,browser=None):

        # If this signal is not from the current tab, ignore
        if(browser != self.tabs.currentWidget()):
            return
        url = qurl.toString()
        self.url_bar.setText(url)
        self.history.append(url)
        browseHistory = open('browseHistory.txt',"a")
        browseHistory.write(url+" \n")
        browseHistory.close()

    def browserHistory(self):
        with open("browseHistory.txt","r") as f:
            history_urls = f.readlines()
        history = [x.strip() for x in history_urls]
        print("length ",len(history))

app = QApplication(sys.argv)
QApplication.setApplicationName("Vedants Browser")
window = MainWindow();
app.exec_();