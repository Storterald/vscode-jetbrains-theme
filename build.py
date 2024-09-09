import os
import re
import sys
import shutil
import subprocess

from pathlib import Path

if __name__ == "__main__":
        # Compile extension
        subprocess.run(["vsce", "package"], shell=True)

        # Install the extension
        FILE: str = [path for path in os.listdir("./") if path.endswith(".vsix")][0]
        subprocess.run(["code", "--install-extension", FILE], shell=True)

        if len(sys.argv) > 1 and sys.argv[1] == "-C":
                EXECUTABLE_DIR: str = "../theme-converter/ThemeConverter/ThemeConverter/bin/debug/net6.0"
                PATH: str = os.path.abspath("./themes")
                
                # Change working directory
                os.chdir(PATH)

                for file in [file for file in os.listdir("./") if file.endswith(".json")]:
                        OUTPUT_FILE: str = Path(file).stem[:-len("-color-theme")] + ".pkgdef"

                        if os.path.exists(OUTPUT_FILE):
                                print(f"Visual studio conversion for file {file} already exists.")
                                continue

                        with open(file, 'r', encoding="utf-8") as f:
                                data: str = f.read()
                        
                        # Remove all comments
                        data = re.sub(r"\/\/.+", "", data)

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