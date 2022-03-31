import sys
from datetime import date, timedelta, datetime
from io import StringIO
from time import sleep

import config
from imglib import *
from iolib import *
from winlib import *

DEBUG = False
DefaultFontPath = "SourceHanSans.ttf"
DefaultFontSize = 70
DefaultAutoStartShToAppdata = False
DefaultAutoStartShName = "AutoUpdateGaoKaoWallpaper.bat"
DefaultAutoStartDir = "Microsoft\Windows\Start Menu\Programs\Startup"
DefaultHourDigits = 0
DefaultUpdateInterval = 1800

Config2Default = {
    "FontPath": DefaultFontPath,
    "FontSize": DefaultFontSize,
    "AutoStartShToAppdata": DefaultAutoStartShToAppdata,
    "AutoStartShName": DefaultAutoStartShName,
    "AutoStartDir": DefaultAutoStartDir,
    "HourDigits": DefaultHourDigits,
    "UpdateInterval": DefaultUpdateInterval,
}

Day = int
Hour = float
Time = Tuple[Day, Hour]

AppdataDir = os.getenv("APPDATA")


def loop():
    config.read()
    restDays, restHours = checkRestDate()
    ScreenSize = winSize()
    img = newImg(ScreenSize, bk="#000000")
    hourDigits = ConfigV("HourDigits")
    tip = config.f("Title", restDays, formatNumber(restHours, hourDigits))
    fontPath = ConfigV("FontPath")
    fontSize = ConfigV("FontSize")
    drawText(
        img, (ScreenSize[0] / 2, ScreenSize[1] / 2),
        tip, fontPath, fontSize, color="#FFFFFF"
    )
    AutoStartShToAppdata = ConfigV("AutoStartShToAppdata")
    if AutoStartShToAppdata:
        genAutoStartSh(os.path.join(AppdataDir, AutoStartDir, AutoStartShName))
    else:
        AutoStartShName = ConfigV("AutoStartShName")
        genAutoStartSh(AutoStartShName)

    if DEBUG:
        img.show()
    else:
        TodayWallpaper = "today_wallpaper.png"
        deleteF(TodayWallpaper)
        img.save(TodayWallpaper)
        setWallpaper(os.path.abspath(TodayWallpaper))


def main():
    config.read()
    while True:
        loop()
        sleep(ConfigV("UpdateInterval"))


def ConfigV(key: str):
    return config.v(key, Config2Default[key])


def formatNumber(number: float, digits: int):
    return ("{:." + str(digits) + "f}").format(number)


def checkRestDate() -> Time:
    today: date = datetime.now()
    year: int = today.year
    if today.month >= 6 and today.day > 9:
        year += 1
    nextGaoKao: date = datetime(year, 6, 7)
    rest: timedelta = (nextGaoKao - today)
    days = rest.days
    hours = (rest.seconds / 3600)
    return days, hours


def genAutoStartSh(shPath):
    thisFilePath = sys.argv[0]
    symbol, path = os.path.splitdrive(thisFilePath)
    dirN, fileN = os.path.split(thisFilePath)
    with StringIO() as sh:
        sh.write(symbol)
        sh.write('\n')
        sh.write(f'cd "{dirN}"')
        sh.write('\n')
        sh.write(f'python "{fileN}"')
        content = sh.getvalue()
        with open(shPath, "w") as f:
            f.write(content)


if __name__ == "__main__":
    main()
