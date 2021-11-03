# Telegram Bot  

A simple python program for retrieving notes stored in MongoDB  
> ．enter /notes_all in Telegram for all notes  
> ．InlineKeyboardMarkup will list all notes that found in MongoDB  
> ．Press the note Title list above will show the Note details(date, content etc.)  
  
## Preparation
1. <pre># pip install python-telegram-bot --upgrade</pre>
2. <pre># pip install pymongo</pre>
3. You may need dnspython for pymongo.MongoClient, if promt:
> <pre># pip install pypi</pre>
> <pre># pip install dnspython</pre>
> Then (may not need): 
> <pre>from pypi import dnspython</pre>
4. Check out the [Telegram Bot Official Page](https://core.telegram.org/bots/) for more info about Telegram Bot  

## More
Data structure(json format): 
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
