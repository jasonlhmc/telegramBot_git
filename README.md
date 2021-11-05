# Telegram Bot  

#### A simple python program for retrieving notes stored in MongoDB  
> ．enter /notes_all in Telegram for all notes  
> ．InlineKeyboardMarkup will list all notes that found in MongoDB  
> ．Press the note Title list above will show the Note details(date, content etc.)  
> ．Added new functions below:
> <pre>
> /notes_txt
> /notes_pnt
> /notes_tsk
> </pre>
  
## Preparation
1. <pre># pip install python-telegram-bot --upgrade</pre>
2. <pre># pip install pymongo</pre>
3. You may need dnspython for pymongo.MongoClient(mongodb+srv://), if promt:
> <pre># pip install pypi</pre>
> <pre># pip install dnspython</pre>
> Then (may not need): 
> <pre>from pypi import dnspython</pre>
4. Check out the [Telegram Bot Official Page](https://core.telegram.org/bots/) for more info about Telegram Bot  

## Data structure(json format):  
<pre>
{
    "_id": {
        "$oid": "54ds65f1a65f46ds85fv16sd"
    },
    "title": "task test",
    "content": "test",
    "isPaint": false,
    "isFPLock": true,
    "isPinLock": false,
    "encryptedPin": "",
    "isTask": true,
    "taskList": [{
        "isFinished": false,
        "task": "task1"
    }, {
        "isFinished": true,
        "task": "task2"
    }, {
        "isFinished": false,
        "task": "task test add new"
    }],
    "editDateStr": "2021-11-02 04:39:35",
    "editDate": {
        "$date": "2021-11-01T20:39:35.994Z"
    },
    "dateStr": "2021-11-02 03:19:20",
    "date": {
        "$date": "2021-11-01T19:19:20.304Z"
    }
}
</pre>  

## Other Functions
#### ．Simple check curreny function command  
<pre>/check_cur</pre>  
> ![Example](https://github.com/jasonlhmc/telegramBot_git/blob/main/img/check_cur_1.png?raw=true)  
> Using Free API: https://tw.rter.info/capi.php  

#### ．A simple downloader for download video on specific site
<pre>/dl </pre>
> Following with an url argument 
> <pre>e.g. /dl https://XxxxXX.xxx/video/xxx.html</pre>  
> Using selenium in python
> <pre>from selenium import webdriver
> from selenium.webdriver.chrome.options import Options
> .
> .
> driver_path = '' #<--Chromedriver loaction, check: https://chromedriver.chromium.org/downloads
> .
> .
> </pre>
> Getting background Network Activities by using:
> <pre>
> .
> .
> options = Options()
> options.add_experimental_option('w3c', False)
> .
> .
> cap = DesiredCapabilities.CHROME
> cap["goog:loggingPrefs"] = {"performance": "ALL"}
> .
> .
> driver = webdriver.Chrome(executable_path=driver_path, options=options, desired_capabilities=cap)
> .
> .
> log = driver.get_log("performance")
> .
> .
> </pre>  
> Check the code in the repsitory to get more information

## More  
#### Can also my native java android application repository [HERE](https://github.com/jasonlhmc/AndroidNativeJavaApp). Including functions below:  
> ．Check Currency  
> ．QR Code Scanner <- submenu [Generate QR Code, Read QR Code from image]  
> ．Jot Notes  
#### Extras:
/setcommands in @BotFather in Telegram
> ![step.1](https://github.com/jasonlhmc/telegramBot_git/blob/main/img/others-setcommands_1.png?raw=true)  
> Select you bot in the ReplyKeyboard at the bottom, then
> ![step.2](https://github.com/jasonlhmc/telegramBot_git/blob/main/img/others-setcommands_2.png?raw=true)  
> Result:  
> ![step.3](https://github.com/jasonlhmc/telegramBot_git/blob/main/img/others-setcommands_3.png?raw=true)  
