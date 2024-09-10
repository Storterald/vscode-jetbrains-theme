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

if __name__ == "__main__":
        # Compile extension
        subprocess.run(["vsce", "package"], shell=True)

        # Install the extension
        FILE: str = [path for path in os.listdir("./") if path.startswith("jetbrains-themes-for-vs-code") and path.endswith(".vsix")][0] # Not specifying version
        subprocess.run(["code", "--install-extension", FILE], shell=True)

        if len(sys.argv) > 1 and sys.argv[1] == "-C":
                subprocess.run(["git", "clone", "https://github.com/microsoft/theme-converter-for-vs", "--branch", "main", "--single-branch", "./theme-converter"])
                subprocess.run(["dotnet", "build"], cwd="./theme-converter/ThemeConverter/ThemeConverter", shell=True)

                EXECUTABLE_DIR: str = "../theme-converter/ThemeConverter/ThemeConverter/bin/debug/net6.0"
                PATH: str = os.path.abspath("./themes")
                
                # Change working directory
                os.chdir(PATH)

                FILES: list[str] = [file for file in os.listdir("./") if file.endswith(".json")]
                for file in FILES:              
                        OUTPUT_FILE: str = Path(file).stem[:-len("-color-theme")] + ".pkgdef"

                        # Clear old converted theme
                        if os.path.exists(OUTPUT_FILE):
                                os.remove(OUTPUT_FILE)

                        data: str = getFileData(file)                             

                        # Create fixed temporary file
                        with open(f"tmp-{file}", 'w', encoding="utf-8") as f:
                                f.write(data)

                        subprocess.run(["ThemeConverter.exe", "-i", f"{PATH}/tmp-{file}", "-o", f"{PATH}/"], cwd=EXECUTABLE_DIR, shell=True)
                        if os.path.exists(f"tmp-{Path(OUTPUT_FILE).stem}-color-theme.pkgdef"):
                                print(f"Successfully converted {file} in VS theme.")
                        else:
                                assert False, f"Error converting {file}"

                        # Remove tmp- prefix and -color-theme suffix and delete file
                        os.rename(f"tmp-{Path(OUTPUT_FILE).stem}-color-theme.pkgdef", OUTPUT_FILE)
                        os.remove(f"tmp-{file}")
                
                # Remove cloned repo
                def onerror(func, path: str, _):
                        if not os.access(path, os.W_OK):
                                # Change file permission
                                os.chmod(path, stat.S_IWUSR)
                                func(path)
                        else:
                                # If error is not due to permission issues, raise
                                assert False, "Could not delete cloned directory."

                shutil.rmtree("../theme-converter", onexc=onerror)