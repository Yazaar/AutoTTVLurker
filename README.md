<h1>Auto TTV Lurker</h1>
all cridentials seen in these images are removed.
<h3>Setup:</h3>
Click on the images for better quality!
<br><br>
First of all, head over to the <a href="https://dev.twitch.tv/login">twitch devoloper page</a> and sign in to your normal twitch account.
<img src="https://raw.githubusercontent.com/Yazaar/Project-Assets/master/AutoTTVLurker/Step1.png">
<br>
Head over to your dashboard.
<img src="https://raw.githubusercontent.com/Yazaar/Project-Assets/master/AutoTTVLurker/Step2.png">
<br>
Click on apps, click on applications if you are on the new interface (yeah probably)
<img src="https://raw.githubusercontent.com/Yazaar/Project-Assets/master/AutoTTVLurker/Step3.png">
<br>
You should be here. Click on register your application.
<img src="https://raw.githubusercontent.com/Yazaar/Project-Assets/master/AutoTTVLurker/Step4.png">
<br>
1. Give your project an epic name, does not matter what.<br>
2. write "http://localhost" in the redirect URL box. Does not really matter in this case either.<br>
3. Pick the category "Application integration", does not really matter either but make the twitch gods happy.<br>
4. Click create! ( good job :) )
<img src="https://raw.githubusercontent.com/Yazaar/Project-Assets/master/AutoTTVLurker/Step5.png">
<br>
You should be back to last page, click manage on your new project.
<img src="https://raw.githubusercontent.com/Yazaar/Project-Assets/master/AutoTTVLurker/Step6.png">
<br>
Copy your Client ID, you may close the window. You are now done in your browser.
<img src="https://raw.githubusercontent.com/Yazaar/Project-Assets/master/AutoTTVLurker/Step7.png">
<br>
One more step, head over to the downloaded files, rightclick and edit the Settings.json file.<br>
Paste your client ID.<br>
"streamers" includes a list of all streams that you want to keep up with. Insert them here and follow the example. (remove the example ones!)<br>
"save_data" tells the software to save your cridentials in the directory which means that it saves you from repeatedly logging in on boot.<br>
"check_streams_interval" is the amount of minutes between each check to the twitch API for livestreams.<br>
"loop_interval" is the amount of minutes before the browser loop thru all tabs, this may be essential to keep streams active (now or in the future).
<img src="https://raw.githubusercontent.com/Yazaar/Project-Assets/master/AutoTTVLurker/Step8v2.png">
