import json
import os
from typing import Dict, Any

ConfigPath = "config.json"
config: Dict[str, Any] = {}


def read():
    def readJson():
        global config
        with open(ConfigPath, encoding="utf-8") as jsonF:
            content: str = jsonF.read()
            config = json.loads(content)

    createWhenNonexist()
    try:
        readJson()
    except:
        os.remove(ConfigPath)
        createWhenNonexist()
        readJson()


def f(key: str, *args, **kwargs) -> Any:
    if key not in config:
        return key
    original: str = config[key]
    try:
        return original.format(*args, **kwargs)
    except:
        return key


def v(key: str, default: Any = None) -> Any:
    if key not in config:
        return default
    value = config[key]
    if default is not None and not isinstance(value, type(default)):
        return default
    else:
        return value


def createWhenNonexist():
    if not os.path.exists(ConfigPath):
        with open(ConfigPath, "w", encoding="utf-8") as jsonF:
            jsonF.write(DefaultContent)


DefaultContent: str = """{
  "Title": "距离高考还有{0}天{1}小时",
  "HourDigits": 0,
  "FontPath": "SourceHanSans.ttf",
  "FontSize": 70,
  "AutoStartShToAppdata": false,
  "AutoStartShName": "AutoUpdateGaoKaoWallpaper.bat",
  "AutoStartDir": "Microsoft/Windows/Start Menu/Programs/Startup"
}"""
