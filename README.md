# ROMiner
GUI tool to extract files from Ragnarok Mobile Eternal Love

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


## Setup environments
1. Java SE RunTime Environment(JRE) 13.0.2 required

## Instruction
- Each functionality can be used as a standalone. Just click the checkbox and click extract button

### Instruction on how to download with patch id and extract files
1. Enter Patch ID e.g "52345_55512" and select the server for the patch.
2. Tick the checkbox beside it. The ID will be validated and will untick if its invalid.


## TODO
 [ ] Remove dependency on JRE (Maybe some portable JRE or just package the java files together)
 [ ] Improve on UI
 [ ] Detect and strip Lua tables in files
 [ ] Convert Tables to JSON
 [ ] Convert Tables to CSV
 [ ] Automatic diff with original files