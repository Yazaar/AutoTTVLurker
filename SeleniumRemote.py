from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time, ctypes, tkinter, threading, requests, json, pickle, os, string, datetime

with open("Settings.json", "r") as f:
    json_data = json.load(f)

WaitTime = json_data["loop_interval"]

ScreenshotsToggle = False
ScreenshotSession = ''

print("Loop through tabs interval: " + str(WaitTime) + " minutes")

QueueQuit = False
looping = False
delayedAdds = set()
delayedRemoves = set()

ActiveTabs = []

timestamp = time.time()

def bootTk():

    tk = tkinter.Tk()
    tk.title("Auto TTV Lurker")
    tk.protocol("WM_DELETE_WINDOW", CloseProgram)
    
    ShutdownButton = tkinter.Button(tk, text="Shutdown", command=CloseProgram, bg = "Red", font=("Courier", 30), width=10)
    ShutdownButton.grid(row=0, column=1)

    TakeScreenshots = tkinter.Button(tk, text="Clear screen", command=clearScreen, bg = "grey", width=34)
    TakeScreenshots.grid(row=1, column=1)

    TakeScreenshots = tkinter.Button(tk, text="Take screenshots", command=takeScreenshots, bg = "Yellow", width=34)
    TakeScreenshots.grid(row=2, column=1)

    ChangeStreams = tkinter.Entry(tk, bg = "light grey", width=40)
    ChangeStreams.grid(row=3, column=1)

    AddStreamsButton = tkinter.Button(tk, text="Add User", command=lambda: AddStream(ChangeStreams.get()), bg = "Green", width=34)
    AddStreamsButton.grid(row=4, column=1)

    RemoveStreamsButton = tkinter.Button(tk, text="Remove User", command=lambda: RemoveStream(ChangeStreams.get()), bg = "Red", width=34)
    RemoveStreamsButton.grid(row=5, column=1)

    tk.mainloop()

def CloseProgram():
    global QueueQuit
    driver.quit()
    QueueQuit = True

def AddStream(streamer):
    global timestamp
    if len(streamer) > 0:
        delayedAdds.add(streamer.lower())
    timestamp = time.time() - 60 * WaitTime

def RemoveStream(streamer):
    global timestamp
    if len(streamer) > 0:
        delayedRemoves.add(streamer.lower())
    timestamp = time.time() - 60 * WaitTime

def takeScreenshots():
    global ScreenshotsToggle, timestamp, ScreenshotSession
    ScreenshotSession = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    if not os.path.exists('screenshots\\' + ScreenshotSession):
        os.makedirs('screenshots\\' + ScreenshotSession)
    timestamp = time.time() - 60 * WaitTime
    ScreenshotsToggle = True

def clearScreen():
    os.system(json_data['clear_screen_command'])
    print("Loop through tabs interval: " + str(WaitTime) + " minutes")
    print('Active streams: ' + ', '.join(ActiveTabs))

def validateFilename(rawinput):
    valid_letters = string.ascii_letters + string.digits + ' '
    valid_letters = list(valid_letters)
    res = list(rawinput)
    index = len(rawinput) - 1
    for _ in rawinput:
        if not res[index] in valid_letters:
            res.pop(index)
        index -= 1
    return ''.join(res)

def waitForBody():
    while True:
        try:
            driver.find_element_by_tag_name("body")
            break
        except Exception:
            time.sleep(1)

tkthread = threading.Thread(target=bootTk)
tkthread.daemon = True

options = Options()

options.add_argument("window-size=1000,1000")
options.add_argument("log-level=3")
if json_data['headless'] == True:
    options.add_argument('--headless')
    options.add_argument("--mute-audio")

driver = webdriver.Chrome(options=options)

try:
    driver.execute_script('window.open("https://twitch.tv","_blank");')
except Exception:
    pass

time.sleep(0.5)
try:
    driver.switch_to.window(driver.window_handles[-1])
except Exception:
    pass

try:
    driver.execute_script('localStorage.setItem("quality-bitrate", 230000)')
except Exception:
    pass

try:
    driver.execute_script('localStorage.setItem("video-quality", "{\\"default\\":\\"160p30\\"}")')
except Exception:
    pass

time.sleep(1)

driver.refresh()

if os.path.isfile("browserdata.data"):
    with open("browserdata.data", "rb") as f:
        temp = pickle.load(f)
        for i in temp:
            try:
                driver.add_cookie(i)
            except Exception:
                pass
    driver.refresh()

waitForBody()
time.sleep(1)

printed = False

try:
    driver.find_element_by_xpath("//button[@data-a-target='gdpr-banner-accept']").click()
    time.sleep(1)
except Exception:
    pass

while True:
    try:
        driver.find_element_by_xpath("//div[@class='onsite-notifications']")
        break
    except Exception:
        if printed == False:
            printed = True
            if json_data['headless'] == True:
                print("To use headerless mode, please restart the software without headless mode to login with save data enabled!")
            else:
                print("Please login to your twitch account. I would recommend to put a stream on low quality BEFORE logging in to make all streams low quality.")
        time.sleep(1)

if json_data["save_data"] == True and printed == True and json_data['headless'] == False:
    with open("browserdata.data", "wb") as temp:
        pickle.dump(driver.get_cookies(), temp)

time.sleep(1)
#if printed == False and json_data['headless'] == False:
#    ctypes.windll.user32.MessageBoxW(0, "I would recommend to put a stream on low quality before proceeding (to make all streams low quality)\nReady? Click OK", "Ready?", 0x0)
#else:
#    time.sleep(0.5)

driver.close()

time.sleep(0.5)
try:
    driver.switch_to.window(driver.window_handles[0])
except Exception:
    pass
tkthread.start()

while True:
    if QueueQuit == True:
        break

    if time.time() - timestamp > 60 * WaitTime:
        currentDelayedAdds = delayedAdds
        currentDelayedRemoves = delayedRemoves
        delayedAdds = set()
        delayedRemoves = set()
        currentTime = datetime.datetime.now().strftime('%H:%M:%S')
        for streamer in currentDelayedAdds:
            try:
                driver.execute_script(f'window.open("https://twitch.tv/{streamer}","_blank");')
            except Exception:
                pass
            time.sleep(0.5)
            try:
                driver.switch_to.window(driver.window_handles[-1])
            except Exception:
                pass
            ActiveTabs.append(streamer.lower())
            waitForBody()
            print(f'[{currentTime}] Opened {ActiveTabs[-1]}')
            time.sleep(2)

        looping = True
        if ScreenshotsToggle == True:
            TakeScreenshots = True
        else:
            TakeScreenshots = False
        i = len(driver.window_handles)-1
        while i > 0:
            try:
                driver.switch_to.window(driver.window_handles[i])
            except Exception:
                pass
            time.sleep(1)
            isLive = True
            try:
                if driver.find_element_by_xpath("//div[contains(@class, 'live-indicator')]").text != 'LIVE':
                    raise Exception
            except Exception:
                isLive = False
            title = driver.title.split(' ')
            if len(title) == 3:
                title = title[0].lower()
            else:
                title = title[1].lower()
            if title != ActiveTabs[i-1]:
                isLive = False
            if title in currentDelayedRemoves:
                isLive = False
            if isLive == False:
                print(f'[{currentTime}] Closed {ActiveTabs[i-1]}')
                ActiveTabs.pop(i-1)
                driver.close()
                time.sleep(1)
                try:
                    driver.switch_to.window(driver.window_handles[0])
                except Exception:
                    pass
                i -= 1
                continue
            try:
                driver.find_element_by_xpath("//button[contains(@class, 'tw-button tw-button--success tw-interactive')]").click()
                time.sleep(1)
            except Exception:
                pass
            try:
                driver.find_element_by_xpath("//button[@data-a-target='player-overlay-mature-accept']").click()
                time.sleep(2)
            except Exception:
                pass
            if TakeScreenshots == True:
                filename = validateFilename(title)
                originalFilename = filename
                separator = 0
                while filename + '.png' in os.listdir('screenshots\\' + ScreenshotSession):
                    separator += 1
                    filename = originalFilename + str(separator)
                driver.save_screenshot('screenshots\\' + ScreenshotSession + '\\' + filename + '.png')
            i -= 1
        if TakeScreenshots == True:
            ScreenshotsToggle = False
        if ScreenshotsToggle == False and len(delayedAdds) == 0 and len(delayedRemoves) == 0:
            timestamp = time.time()
            looping = False
    else:
        time.sleep(1)