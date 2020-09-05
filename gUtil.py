#!<path_from_which_python_command>
import sys
import os
from datetime import date
import datetime
import pkgutil
import os
import shutil
import subprocess
import time
import urllib.request # To download files
from tkinter import Tk, ttk # Download bar
import zipfile
from pathlib import Path
import urllib.request as requests
import tkinter

import CustomLogger
logger = CustomLogger.logger

import tempfile



# import Vendor libraries

# Unity Unpacker/Extractor
from UnityPy import AssetsManager
from collections import Counter
# https://github.com/K0lb3/UnityPy
# https://github.com/K0lb3/UnityPy/blob/master/AssetBatchConverter.py

TYPES = ['TextAsset','Sprite', 'Texture2D', 'MonoScript','MonoBehaviour']
IGNOR_DIR_COUNT = 2

# Convert lua table to json
# https://github.com/SirAnthony/slpp
from slpp import slpp as lua



def validateURL(url:str):
    try:
        rsp = requests.get(url)
        logger.info("%s - %s"% (rsp.status_code, url))
        if rsp.status_code == 200:
            return True
    except:
        logger.info("%s does not exist on Internet" % url)
    return False

import requests 

def downloadFile(url, save_path, chunk_size=128):
    r = requests.get(url, stream=True)
    with open(save_path, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)

def ValidateJava():
    try:
        proc = subprocess.Popen('java -version', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        result = proc.stdout.read().decode('utf-8')
        if "command not found" not in result:
            logger.info("Located JRE \n"+result)
        else:
            logger.error("Java Runtime Environment (JRE) is required to decrypt the byte files.")
    except:
            logger.error("Java Runtime Environment (JRE) is required to decrypt the byte files.")

def GetPatchLink(p_serv : str, p_name:str) -> str:
    serverLink : str = ""
    if p_serv == "CN":
        serverLink = "http://ro.xdcdn.net/res/Alpha/Android/"  + p_name + ".zip"
    elif p_serv == "SEA":
        serverLink = "http://sea-cdn.ro.com/assets/Release/Android/" + p_name + ".zip"
    elif p_serv == "GLOBAL":
        serverLink = "http://na-cdn.ro.com/assets/Release/Android/" +p_name + ".zip"
    elif p_serv == "Others":
        serverLink = p_name
    return serverLink  
#End of GetPatchLink

def DownloadPatchFile(p_server:str, p_patchString:str, p_outputPath:str):
    file_url = GetPatchLink(p_server,p_patchString)
    if "Others" in p_server:
        p_server, p_patchString = os.path.split(p_patchString)
        p_patchString, ext = os.path.splitext(p_patchString)
    file_name ="ROM_Patch_"+p_patchString
    file_path = p_outputPath + "/" + file_name +".zip"
    logger.info("Downloading to %s" % file_path)
    downloadFile(file_url, file_path)
    logger.info ("Download complete")
    return file_path

def UnloadZip(p_zipFilePath:str, p_outputPath:str):
    # Extract to folder with same name as zip file
    zfFolder, zfFileName = os.path.split(p_zipFilePath)
    zfFileName, ext = os.path.splitext(zfFileName)
    extracted_zfPath = os.path.join(p_outputPath, zfFileName)

    logger.info("Beginning extraction of %s" % zfFileName)
    with zipfile.ZipFile(p_zipFilePath) as zf:
        zf.extractall(extracted_zfPath)
    logger.info("Complete extraction of %s" % zfFileName)
    os.remove(p_zipFilePath) # delete zip file

    return zfFileName
    



def UnloadAPK(p_apkFilePath : str, p_outputPath:str) -> bool:
    hasAPK:bool = False
    obbPath = ""

    if "apk" in p_apkFilePath:
        hasAPK = True
    elif not "obb" in p_apkFilePath:
        logger.error("No valid apk or obb file selected")
        return False


    # create a copy of the apk to tmp folder
    fileDir, fileName = os.path.split(p_apkFilePath)            # split folder and file name
    CopyFile(fileDir, p_outputPath,fileName)                    # Copy file to output
    newApkFilePath = os.path.join(p_outputPath, fileName)
    # Rename apk to zip
    apkfilename,ext = os.path.splitext(newApkFilePath)
    os.rename(newApkFilePath, apkfilename +".zip" )
    newApkFilePath = apkfilename +".zip"
    apkExtractedFolder = os.path.join(p_outputPath, apkfilename)

    if hasAPK:
        # extract apk zip
        logger.info("Beginning extraction of raw apk")
        with zipfile.ZipFile(newApkFilePath) as zf:
            zf.extractall(apkExtractedFolder)
        logger.info("Completed APK extraction")
    else:
        obbPath = newApkFilePath

    if not obbPath:
        for path in Path(p_outputPath).rglob('*.obb'):
            obbPath = path
            break

        # Rename obb to zip
        filepath,ext = os.path.splitext(obbPath)
        os.rename(obbPath, filepath +".zip" )
        obbPath = obbPath + filepath +".zip"

    logger.info("Extracting obb")
    with zipfile.ZipFile(obbPath) as zf:
        zf.extractall(p_outputPath)
    logger.info("Completed obb extraction")

    # Cleanup copied apk file and folder after obb extraction
    if hasAPK:
        os.remove(newApkFilePath)
        shutil.rmtree(apkExtractedFolder)

    return True

def GetUnityFiles(p_folderPath :str) ->list:
    fileList : list = []
    for subdir, dirs, files in os.walk(p_folderPath):
        for dir in dirs:
            fileList.extend(GetUnityFiles(dir))
        for file in files:
            if R".unity3d" in file:
                fileList.append(os.path.join(subdir, file))
    return fileList
#end of GetUnityFiles

def CreateFolder(p_path:str, p_foldername:str):
    if p_foldername in p_path:
        return p_path

    newpath = os.path.join(p_path, p_foldername)
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    return newpath
#end of CreateFolder

def CopyFile(p_src:str, p_dst:str, p_fileName:str):
    if os.path.exists(p_dst+"/"+p_fileName):
        logger.info("Destination: %s/%s already exists. Aborting copy!" % (p_dst,p_fileName))
        return "dst"
    elif not os.path.exists(p_src+"/"+p_fileName):
        logger.info("Source file: %s/%s does not exist. Aborting copy!" % (p_src, p_fileName))
        return "src"
    else:
        shutil.copy(p_src+"/"+p_fileName,p_dst)
        logger.info("Succesfully copied %s to %s" %(p_fileName, p_dst))
        return p_dst+"/"+p_fileName
#end of CopyFile


# Create output directory based on today date
def GetOutputFolder(p_outputPath :str):
    return CreateFolder(p_outputPath, "OutputFile" + datetime.datetime.today().strftime("_%d%m%Y_%H%M%S"))
#end of SetupOutputFolder


def DecryptLuaFiles(p_workingDir:str, tkWin : tkinter.Tk):
    # Make sure execution files exists
    exeNP = CopyFile(os.getcwd(), p_workingDir, "RomEncryption.exe" )
    unluacNP = CopyFile(os.getcwd(), p_workingDir, "unLuac.jar" )
    
    if exeNP == "src":
        logger.error("Cannot find RomEncryption.exe")
        return False
    if unluacNP == "src":
        logger.error("Cannot find unLuac.exe")
        return False

    logger.info ("Decrypting to lua files...")
    cmd = "RomEncryption.exe";
    
    outputString = ""
    with tempfile.TemporaryFile(newline='\n', mode='w+', encoding='utf-8') as tempf:
        proc = subprocess.Popen(cmd, stdout=tempf, cwd=p_workingDir)
        proc.wait()
        tempf.seek(0)
        outputString = tempf.read()
        outList = outputString.split('\n')
        for line in outList:
            if "Exception" in line:
                logger.error(line)
            else:
                logger.info("Extracted file: " + line)
            tkWin.update()

    logger.info ("Decryption task completed")

    os.remove(exeNP)
    os.remove(unluacNP)
    return True



def unpack_all_assets(p_folderPath : str, p_outputPath : str):
    logger.info ("Start unpacking unity files via UnityPy")
    
    for root, dirs, files in os.walk(p_folderPath, topdown=False):
        for f in files:
            logger.info(f)
            extension = os.path.splitext(f)[1]
            src = os.path.realpath(os.path.join(root, f))

            if extension == ".zip":
                archive = zipfile.ZipFile(src, 'r')
                for zf in archive.namelist():
                    extract_assets(archive.open(zf),p_outputPath)
            else:
                extract_assets(src,p_outputPath)

    logger.info ("Completed unpacking of unity files")
    shutil.rmtree(p_folderPath)



def extract_assets(src, output_path):
    # load source
    am = AssetsManager(src)

    # iterate over assets
    for asset in am.assets.values():
        # assets without container / internal path will be ignored for now
        if not asset.container:
            continue

        # check which mode we will have to use
        num_cont = sum(1 for obj in asset.container.values() if obj.type in TYPES)
        num_objs = sum(1 for obj in asset.objects.values() if obj.type in TYPES)

        # check if container contains all important assets, if yes, just ignore the container
        if num_objs <= num_cont * 2:
            for asset_path, obj in asset.container.items():
                fp = os.path.join(output_path, *asset_path.split('/')[IGNOR_DIR_COUNT:])
                export_obj(obj, fp)

        # otherwise use the container to generate a path for the normal objects
        else:
            extracted = []
            # find the most common path
            occurence_count = Counter(os.path.splitext(asset_path)[0] for asset_path in asset.container.keys())
            local_path = os.path.join(output_path, *occurence_count.most_common(1)[0][0].split('/')[IGNOR_DIR_COUNT:])

            for obj in asset.objects.values():
                if obj.path_id not in extracted:
                    extracted.extend(export_obj(obj, local_path, append_name=True))


def export_obj(obj, fp: str, append_name: bool = False) -> list:
    if obj.type not in TYPES:
        return []
    data = obj.read()
    if append_name:
        fp = os.path.join(fp, data.name)

    fp, extension = os.path.splitext(fp)
    os.makedirs(os.path.dirname(fp), exist_ok=True)

    if obj.type == 'TextAsset':
        if not extension:
            extension = '.txt'
        with open(f"{fp}{extension}", 'wb') as f:
            f.write(data.script)

    elif obj.type == "Sprite":
        extension = ".png"
        data.image.save(f"{fp}{extension}")

        return [obj.path_id, data.m_RD.texture.path_id, getattr(data.m_RD.alphaTexture, 'path_id', None)]

    elif obj.type == "Texture2D":
        extension = ".png"
        fp = f"{fp}{extension}"
        if not os.path.exists(fp):
            try:
                data.image.save(fp)
            except EOFError:
                pass

    return [obj.path_id]