# Battle Cats Game Modding Tool

A python game modding tool for the mobile game The Battle Cats that can decrypt,
encrypt, and modify some game files.

Note: I am no longer actively working on this tool so there may be bugs.

If you know how to program and want to do more powerful things with the game
then you should use [TBCML](https://github.com/fieryhenry/tbcml) instead.

Join the [discord server](https://discord.gg/DvmMgvn5ZB) if you want to suggest
new features, report bugs or get help on how to use the modder. (Discord is the
same one as for save editing as I haven't made a modding specific one yet)

PyPi: <https://pypi.org/project/battle-cats-game-modder/>

If you want to support me then consider gifting me some ko-fi here:
<https://ko-fi.com/fieryhenry>

## Thanks to

- EasyMoneko for the original keys for decrypting/encrypting:
  <https://www.reddit.com/r/battlecats/comments/41e4l1/is_there_anyone_able_to_access_bc_files_your_help/>

- Battle Cats Ultimate for what some of the numbers mean in various csvs.
  <https://github.com/battlecatsultimate>

- This resource for unit csvs: <https://pastebin.com/JrCTPnUV>

- Vi on discord for enemy csvs

## How to use

1. Install python (If you haven't already) <https://www.python.org/downloads/>

1. Enter the command: `py -m pip install -U battle-cats-game-modder` into cmd or
   another terminal to install the editor. If that doesn't work then use
   `python` instead of `py` in the command

1. Download the apk you want to edit from somewhere like
   [uptodown](https://the-battle-cats.en.uptodown.com/android/download) or
   [apkmirror](https://www.apkmirror.com/apk/ponos/the-battle-cats)

1. Unpack the apk file for the game using
   [Apktool](https://ibotpeaches.github.io/Apktool/) or
   [APKToolGui](https://github.com/AndnixSH/APKToolGUI).

1. You can then find the .pack and .list files in the assets folder of the
   extracted APK.

1. Get the .pack and .list files that contain the files you want to edit:

   - Most stats are in DataLocal

   - Most text is in resLocal

   - Sprites are in various Server files

1. Then enter the command: `py -m BCGM_Python` to run the tool. If that doesn't
   work then use `python` instead of `py` in the command

1. Select option to decrypt .pack files

1. Select .pack files that you want, they will be in the `assets` folder in the
   apk for local files, or `/data/data/jp.co.ponos.battlecatsen/files` on your
   device (if rooted) for downloaded server files

1. Also decrypt the DownloadLocal pack as you will need it for later

1. Once completed the files will be in a `game_files` folder in the folder you
   ran the command from

1. You can manually edit the data, or use the option in the tool that you want

1. Once edited, you should place any modified files in the DownloadLocal pack
   folder instead of the original pack folder. This is because the game does not
   check if DownloadLocal has been modified, but it does check if the original
   pack has been modified. The game also prioritises DownloadLocal over the
   original pack, so if you have a file in both, the game will use the one in
   DownloadLocal.

1. Open the tool again and select the `encrypt` option

1. Select the DownloadLocal folder

1. Once complete the encrypted .pack and .list files will be in
   an`encrypted_files` folder in the folder you ran the command from

1. If you are asked if you want to patch the libnative file, say no as this
   featrue is currently broken and you do not need to do it if you placed your
   files in DownloadLocal

1. Then you need to place the encrypted .pack and .list files back into the
   assets folder of the apk

1. You then need to pack the apk using apktool or apktoolgui

1. You then need to sign the apk using apktool or apktoolgui

1. You then need to install the apk, you may have to uninstall the game first
   before installing the modified apk for the first time

1. Open the game and see if it works
