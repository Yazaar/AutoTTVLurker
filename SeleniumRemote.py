from selenium import webdriver
import time, ctypes, tkinter, threading, requests, json, pickle, os


#-------------
# CONFIG START
#-------------

# (minutes)   Interval to check twitch API for online and offline streams
#WaitTime = 15

with open("Settings.json", "r") as f:
    json_data = json.load(f)

WaitTime = json_data["check_streams_interval"]
WaitTime2 = json_data["loop_interval"]
OAuth = json_data["client_id"]
last_success = []

print("Check streams interval: " + str(WaitTime) + " minutes")
print("Loop thru tabs interval: " + str(WaitTime2) + " minutes")

Streams = json_data["streamers"]

print("Streams: " + ", ".join(Streams))

StreamData = ""

for i in Streams:
    if StreamData == "":
        StreamData += "?user_login=" + i.lower()
    else:
        StreamData += "&user_login=" + i.lower()

#-------------
# CONFIG END
#-------------

QueueQuit = False

def bootTk():

    tk = tkinter.Tk()
    tk.title("Auto TTV Lurker")
    tk.protocol("WM_DELETE_WINDOW", CloseProgram)
    
    ShutdownButton = tkinter.Button(tk, text="Shutdown", command=CloseProgram, bg = "Red", font=("Courier", 30), width=10)
    ShutdownButton.grid(row=0, column=1)

    WhiteSpace1 = tkinter.Label(tk, text="", height = 2)
    WhiteSpace1.grid(row=1, column=1)

    ChangeStreams = tkinter.Entry(tk, bg = "light grey", width=40)
    ChangeStreams.grid(row=2, column=1)

    AddStreamsButton = tkinter.Button(tk, text="Add User", command=lambda: AddStream(ChangeStreams.get()), bg = "Green", width=34)
    AddStreamsButton.grid(row=3, column=1)

    RemoveStreamsButton = tkinter.Button(tk, text="Remove User", command=lambda: RemoveStream(ChangeStreams.get()), bg = "Red", width=34)
    RemoveStreamsButton.grid(row=4, column=1)

    tk.mainloop()

def CloseProgram():
    global QueueQuit
    driver.quit()
    QueueQuit = True

def ReloadStreams():
    global Timestamp, StreamData
    print(Streams)
    StreamData = ""
    for i in Streams:
        if StreamData == "":
            StreamData += "?user_login=" + i.lower()
        else:
            StreamData += "&user_login=" + i.lower()
    Timestamp = time.time() - 60 * WaitTime

def AddStream(NewData):
    global Streams
    Temp = NewData.replace(" ", "").lower()
    if Temp != "":
        if not Temp in Streams:
            Streams.append(Temp)
            print(Temp + " added!")
    ReloadStreams()

def RemoveStream(NewData):
    global Streams, ActiveTabs
    Temp = NewData.replace(" ", "")
    
    if Temp in Streams:
        Streams.remove(Temp)
        print(Temp + " removed!")

        if NewData in ActiveTabs:
            driver.switch_to.window(driver.window_handles[ActiveTabs.index(NewData)])
            time.sleep(1)
            driver.close()
            ActiveTabs.remove(NewData)
    ReloadStreams()

tkthread = threading.Thread(target=bootTk)
tkthread.daemon = True

ActiveTabs = ["****"]

driver = webdriver.Chrome()

try:
    driver.execute_script('window.open("https://twitch.tv","_blank");')
except Exception:
    pass

time.sleep(0.5)
try:
    driver.switch_to.window(driver.window_handles[-1])
except Exception:
    pass

if os.path.isfile("browserdata.data"):
    with open("browserdata.data", "rb") as f:
        temp = pickle.load(f)
        for i in temp:
            driver.add_cookie(i)
    driver.refresh()

while True:
    try:
        driver.find_element_by_tag_name("body")
        break
    except Exception:
        time.sleep(1)
time.sleep(1)

printed = False

while True:
    try:
        driver.find_element_by_xpath("//div[@class='onsite-notifications']")
        break
    except Exception:
        if printed == False:
            printed = True
            print("Please login to your twitch account. I would recommend to put a stream on low quality BEFORE logging in to make all streams low quality.")
        time.sleep(1)

if json_data["save_data"] == True and printed == True:
    temp = open("browserdata.data", "wb")
    pickle.dump(driver.get_cookies(), temp)
    temp.close()

if printed == False:
    ctypes.windll.user32.MessageBoxW(0, "I would recommend to put a stream on low quality before proceeding (to make all streams low quality)\nReady? Click OK", "Ready?", 0x0)

driver.close()

time.sleep(0.5)
try:
    driver.switch_to.window(driver.window_handles[0])
except Exception:
    pass
tkthread.start()
Timestamp = time.time() - 60 * WaitTime
Timestamp2 = time.time()

while True:
    if QueueQuit == True:
        break

    if time.time() - Timestamp2 > 60 * WaitTime2:
        for i in driver.window_handles:
            try:
                driver.switch_to.window(i)
            except Exception:
                pass
            time.sleep(1)
            try:
                driver.find_element_by_id("mature-link").click()
                time.sleep(2)
            except Exception:
                time.sleep(1)
        Timestamp2 = time.time()

    if time.time() - Timestamp > 60 * WaitTime:
        try:
            res = json.loads(requests.get("https://api.twitch.tv/helix/streams" + StreamData, headers={"Client-ID": OAuth}).text)["data"]
            last_success = res.copy()
        except Exception as e:
            res = last_success.copy()
        Timestamp = time.time()
        temp = []
        for i in res:
            if i["type"] == "live":
                temp.append(i["user_name"].lower())
        for i in reversed(ActiveTabs):
            if i == "****":
                continue
            if i not in temp:
                driver.switch_to.window(driver.window_handles[ActiveTabs.index(i)])
                time.sleep(0.5)
                driver.close()
                ActiveTabs.remove(i)
                time.sleep(0.5)
        for i in temp:
            if not i in ActiveTabs:
                try:
                    driver.execute_script(f'window.open("https://twitch.tv/{i}","_blank");')
                except Exception:
                    pass
                ActiveTabs.append(i)
                time.sleep(1)
                driver.switch_to.window(driver.window_handles[-1])
                while True:
                    try:
                        driver.find_element_by_tag_name("body")
                        break
                    except Exception:
                        time.sleep(1)
                time.sleep(1)
                try:
                    driver.find_element_by_id("mature-link").click()
                except Exception:
                    pass
    else:
        time.sleep(1)

raise SystemExit