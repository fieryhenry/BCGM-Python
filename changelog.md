# Changelog

## [1.0.6] - 2024-03-20

#### Fixed

- Not removing padding from the end of the file after decrypting

- Modifying files in order to add padding before encryption, this is now done in
  memory. This should fix any issues with incorrect file permissions (e.g
  desktop.ini)

- Display error message if no files are in the folder that you are trying to
  encrypt

#### Removed

- Broken patch libnative option

## [1.0.5] - 2023-07-08

#### Fixed

- Changed colored to version 1.4.4 because newer versions of colored don't work with the tool

## [1.0.4] - 2022-05-24

#### Fixed

- Some adb issues with shell=True thanks to [!j0](https://github.com/j0912345)

## [1.0.3] - 2022-05-20

#### Changed

- Removed wxPython, and for stage mod the tool now uses tk, the reason for why i used it was because in tkinter the file filters automatically have a `*` before them.

#### Fixed

- Stage mod crashing
