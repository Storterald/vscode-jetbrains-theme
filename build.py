import os
import re
import sys
import stat
import json
import shutil
import subprocess

from pathlib import Path

def getFileData(path: str) -> str:
        def removeComments(fileData: str) -> str:
                return re.sub(r"\/\/ .+", "", fileData)
        
        def mergeJson(jsonData: dict, other: dict) -> dict:
                for key, value in other.items():
                        if key in jsonData and isinstance(jsonData[key], dict) and isinstance(value, dict):
                                # If both values are dictionaries, merge them
                                jsonData[key] = mergeJson(jsonData[key], value)
                        else:
                                # Otherwise, overwrite the value
                                jsonData[key] = value
                return jsonData
        
        def getJsonData(_path: str) -> dict:
                with open(_path, 'r', encoding="utf-8") as f:
                        DATA: str = removeComments(f.read())

                jsonData: dict = json.loads(DATA)
                if "include" in jsonData:
                        INCLUDED_FILE_PATH: str = os.path.join(os.path.dirname(_path), jsonData["include"])
                        INCLUDED_JSON: dict = getJsonData(INCLUDED_FILE_PATH)
                        jsonData = mergeJson(jsonData, INCLUDED_JSON)

                return jsonData

        return json.dumps(getJsonData(path), indent=2)

def convert() -> None:
        subprocess.run(["git", "clone", "https://github.com/microsoft/theme-converter-for-vs", "--branch", "main", "--single-branch", "./theme-converter"])
        subprocess.run(["dotnet", "build"], cwd="./theme-converter/ThemeConverter/ThemeConverter", shell=True)

        EXECUTABLE_DIR: str = "../theme-converter/ThemeConverter/ThemeConverter/bin/debug/net6.0"
        PATH: str = os.path.abspath("./vsthemes/")
        THEMES_PATH: str = os.path.abspath("./themes/")
        
        # Change working directory
        os.chdir(PATH)

        # Create complete JSON files
        for file in [file for file in os.listdir(THEMES_PATH) if file.endswith(".json")]:
                # Delete converted theme if it exists
                OUTPUT_FILE: str = Path(file).stem + ".pkgdef"
                if os.path.exists(OUTPUT_FILE):
                        os.remove(OUTPUT_FILE)

                # Get full JSON data without comments
                with open(f"./{Path(file).stem}.json", 'w', encoding="utf-8") as f:
                        f.write(getFileData(f"{THEMES_PATH}/{file}"))
        
        for file in [file for file in os.listdir("./") if file.endswith(".json")]:
                # Convert all themes
                subprocess.run(["ThemeConverter.exe", "-i", f"{PATH}/{file}", "-o", PATH], cwd=EXECUTABLE_DIR, shell=True)

                if not os.path.exists(f"{PATH}/{file}"):
                        assert False, "Error creating converted file"

                # Delete temporary JSONs
                os.remove(file)
        
        # Remove cloned repo
        def onerror(func, path: str, _):
                if not os.access(path, os.W_OK):
                        # Change file permission
                        os.chmod(path, stat.S_IWUSR)
                        func(path)
                else:
                        # If error is not due to permission issues, raise
                        assert False, "Could not delete cloned directory."

        # Delete cloned converter
        shutil.rmtree("../theme-converter/", onexc=onerror)

if __name__ == "__main__":
        # Compile extension
        subprocess.run(["vsce", "package"], shell=True)        
        
        # Run through all the flags
        for flag in sys.argv[1:]:
                match flag:
                        case "-I":
                                FILE: str = [path for path in os.listdir("./") if path.endswith(".vsix")][0]
                                subprocess.run(["code", "--install-extension", FILE], shell=True)
                        case "-C":
                                convert()
                