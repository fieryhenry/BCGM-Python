# Battle Cats Game Modding Tool

A python game modding tool for the mobile game The Battle Cats that can decrypt, encrypt, and modify some game files.

It is a pretty much direct port from my [C# game modding tool](https://github.com/fieryhenry/Battle-Cats-Game-Modder) with a few bug fixes.

Join the [discord server](https://discord.gg/DvmMgvn5ZB) if you want to suggest new features, report bugs or get help on how to use the modder.

PyPi: https://pypi.org/project/battle-cats-game-modder/

If you want to support me then consider gifting me some ko-fi here: https://ko-fi.com/fieryhenry

## Thanks to:

- EasyMoneko for the original keys for decrypting/encrypting: https://www.reddit.com/r/battlecats/comments/41e4l1/is_there_anyone_able_to_access_bc_files_your_help/

- Battle Cats Ultimate for what some of the numbers mean in various csvs. https://github.com/battlecatsultimate 

- This resource for unit csvs: https://pastebin.com/JrCTPnUV

- Vi on discord for enemy csvs

## How to use:

I recommed putting adb in your Path system variable. To do that do this:

1. If you are using an emulator: Go to your emulator's install directory, if 
   using LDPlayer it will most likely be in `C:/LDPlayer/LDPlayer4.0`.
   Then find `adb` in that folder (other emulators might have it in the `bin`
    directory)

2. If you aren't using an emulator [Download the Android SDK Platform Tools ZIP file for Windows](https://dl.google.com/android/repository/platform-tools-latest-windows.zip), and unzip it.

3. Copy the path to the directory that you are in

4. Then open the start menu and search: `edit the system environment 
   variables` and press enter.

5. Then click on the `Environment Variables` button.

6. Then in the `System variables` box find the variable named `Path`, then 
   click on the `edit` button.

7. Then click `New` and paste the path into it.

8. Click `Ok` then `Ok` again then `Ok` again.

9. Relaunch powershell and maybe restart your whole pc, and try the command
    again.
   If this method is too dificult, just use a root file explorer instead 
   and manually get the files that you want. The paths that you will need are:
   `/data/data/jp.co.ponos.battlecatsen/files` and
   
   `/data/app/jp.co.ponos.battlecatsen-1`

---

### How to edit game data

1. Install python (If you haven't already) https://www.python.org/downloads/

2. Enter the command: `python -m pip install -U battle-cats-game-modder` into cmd or another terminal to install the editor. If that doesn't work then use `py` instead of `python` in the command

3. Unpack the apk file for the game using apktool/APK Easy Tool

4. Get the .pack and .list files that contain the files you want to edit:
   
   - Most stats are in DataLocal
   
   - Most text is in resLocal
   
   - Sprites are in various Server files

5. Then enter the command: `python -m BCGM_Python` to run the tool. If that doesn't work then use `py` instead of `python` in the command

6. Select option to decrypt .pack files

7. Select .pack files that you want, they will be in `/assets` for local files in the extracted apk, or `/data/data/jp.co.ponos.battlecatsen/files ` for downloaded server files

8. Once completed the files will be in `/game_files` in your current working directory

9. You can manually edit the data, or use the option in the tool that you want

10. Once edited, open the tool and select the `encrypt` option

11. Select the folder of the game files

12. Once complete the encrypted files will be `/encrypted_files` in your current working directory

13. Get your `libnative-lib.so` file for your system architecture. You can find it in:
    
    - The `/lib` folder of the extracted `apk`
    
    - `/data/app/jp.co.ponos.battlecatsen-1/{architecture}/`
    
    - `/data/data/jp.co.ponos.battlecatsen/lib`

14. Run the tool and select the option to `Set md5 hashes in libnative-lib.so file`

15. Select your encrypted files in `/encrypted_files` in your current working directory

16. Once done you can either:
    
    1. Say yes to `push your modified libnative-lib.so file to the game`
    
    2. Replace the libnative file in the apk for a permanent change.
       
       - The `apk` must be signed - `APK Easy Tool`- for most devices to install the apk
       
       - Then you must re-install app or replace the apk in `/data/app/jp.co.ponos.battlecats.../base.apk`
    
    3. Manually replace the libnative file in `/data/app` 
    
    4. Replace the libnative file in `/data/data/jp.co.ponos.battlecatsen/lib`  only if you modifed server files for your device.
    
    I recommend doing 1 and 2 for local files. And all 3 for server files.

17. You now need to put your encrypted files either into:
    
    1. The apk if you modified local files
       
       - The `apk` must be signed - `APK Easy Tool`- for most devices to install the apk
       
       - Then you must re-install app or replace the apk in `/data/app/jp.co.ponos.battlecats.../base.apk`
    
    2. `/data/data/jp.co.ponos.battlecatsen/files` if you modified server files

18. Open the game and see if it works
    
    ---

19. If you modifed server files, you will need to find the associated `download.tsv` file for your .pack and .list files in the apk in `/assets/{language}`

20. Open the file in notepad, you will see the `name` of the file, then a tab, then the `file size` in bytes, then a tab, then the `md5 hash` of that file.

21. You need to modify that `md5 hash` so that the game doesn't re-download the server data

22. Go to here: https://emn178.github.io/online-tools/md5_checksum.html and drag and drop the file in

23. Copy the hash and replace the one in the `tsv` with that one.

24. Replace the apk in `/data/app/jp.co.ponos.battlecats.../base.apk` with your apk, use `apktool/APK Easy Tool` to sign the app and pack it into an apk again.

25. Open the game and see if it works.

26. If it re-downloads game data maybe also try to replace the `file size` in bytes for the .pack file. Right click->properties->Size (not Size on disk)

27. 
