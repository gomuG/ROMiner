# ROMiner
GUI tool to extract files from Ragnarok Mobile Eternal Love

Download link here: https://github.com/gomuG/ROMiner/releases

Reach out to me @ Gomu#4730 on discord

## Description
This tool streamlines the process, from download patch files to extracting to readable formats.

## Functionalities
- Download Patch files with given IDs in respective servers
- Extract from APK files to unity files
- Unpack unity files to their respective assets (TextAsset, MonoScript, MonoBehaviours, Texture2D, Sprite)
  - TextAssets are mostly in byte files 
- Decrypt the byte files, with ROM Cipher, into compiled lua files and decompile them back to lua file
  - See https://github.com/shalzuth/ROMEncryption for bytes reading method
  - See https://gitlab.com/_rom/unluac for decompiling method


## Getting started
1. Java SE RunTime Environment(JRE) 13.0.2 required

## Instruction
- Run ROMiner.exe
- Each functionality can be used as a standalone. Just click the checkbox and click extract button
- Downloaded/Extracted files can be found in an output folder with date and time suffix to prevent duplication

### Instruction on how to download with patch id and extract files
1. Run ROMiner.exe
2. Enter Patch ID e.g "52345_55512" and select the server for the patch.
3. Tick the checkbox beside it. The ID will be validated and will untick if its invalid.
4. Tick 2, and 3 as well
5. Press Extract

![Get your own patch ID](https://github.com/gomuG/ROMiner/blob/master/Example.PNG)


## TODO
- [ ] Remove dependency on JRE (Maybe some portable JRE or just package the java files together)
- [ ] Improve on UI
- [ ] Detect and strip Lua tables in files
- [ ] Convert Tables to JSON
- [ ] Convert Tables to CSV
- [ ] Automatic diff with original files


