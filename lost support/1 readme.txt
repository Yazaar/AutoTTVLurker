Welcome to Auto TTV Lurker, by Yazaar!
This version is only working on windows!

This can run in the background of your main PC or on annother machine.
The window can not be minimized (because of windows) but it will not go
to focus each time it loops or opens tabs.

SeleniumRemote, or Auto TTV Lurker is used to support the streamers you love.
No need to open up tabs manually, SeleniumRemote will do it for you.
It will as well close the stream whenever the streamer goes offline.

Python is not essential for this to work, but feel free to use it
if you prefer.

Thanks for using my Auto TTV Lurker!
// Yazaar

!!! DO NOT CLOSE OR OPEN TABS ON YOUR OWN, BREAKS SOFTWARE... !!!
!!!     You are still able to open up a new chrome window     !!!

How to use:

Method 1 (recommended):
Follow the instructions found here:
https://github.com/Yazaar/Auto-TTV-Lurker/blob/master/README.md


Method 2:
1. Install python! (Python 3) (Built with Python 3.6.6)

2. Run this in CMD ---> pip install selenium

3. Open MyStreamers.txt and fill with your streamers (1 streamer per row)
   (max 30 streamers, twitch has a max limit of 30 requests per minute and all are scanned at once)
   (might make an update to support more streams but this is not scheduled)

4. Open https://dev.twitch.tv/login and login to your twitch account (safe)
   Click "Your Dashboard" (top right)
   Click "REGISTER APP"
   Click "Register your application"

   Pick a fitting name (does not matter, but have to be available)
   Set redirecting url to: http://localhost
   Pick a fitting category (maybe "Application Integration" or "Analytics Tool")

   Click "Save"
   Click "Manage" on your new application
   Copy your Client-ID (Paste it in Settings.txt under "OAuth:")

5. Run RunAutoTTV.bat