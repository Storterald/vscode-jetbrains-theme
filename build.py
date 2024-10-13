import os
import re
import sys
import stat
import yaml
import shutil
import subprocess

VERSION_DIR: str = "./.version-getter/"

# Load mappings
with open("./colors/Dark.yaml", 'r', encoding="utf-8") as f:
        DARK_MAP: dict = yaml.safe_load(f)
with open("./colors/Light.yaml", 'r', encoding="utf-8") as f:
        LIGHT_MAP: dict = yaml.safe_load(f)

def getVersion() -> str:
        if not os.path.exists(VERSION_DIR):
                os.mkdir(VERSION_DIR)
                subprocess.run(["git", "clone", "--depth", "1", "--no-checkout", "https://github.com/Storterald/Jetbrains-Themes", "."], cwd=VERSION_DIR, shell=True)
                subprocess.run(["git", "fetch", "--tags", "--depth", "1"], cwd=VERSION_DIR, shell=True)
        else:
                subprocess.run(["git", "pull", "--depth", "1"], cwd=VERSION_DIR, shell=True)

        version: str = subprocess.check_output(["git", "for-each-ref", "--sort=-creatordate", "--format", "%(refname:short)", "refs/tags"], cwd=VERSION_DIR, shell=True)
        version = version.decode("utf-8")
        version = version[:version.find('\n')]
        print(f"Current extension version is: {version}")

        return version

def copyTemplate(DIR: str, EXT_SRC: str, EXT_DST: str) -> None:
        os.mkdir(f"{DIR}")
        shutil.copyfile(f"./templates/template{EXT_SRC}", f"{DIR}/template{EXT_DST}")
        shutil.copyfile(f"./{DIR}/template{EXT_DST}", f"{DIR}/Jetbrains New UI Dark{EXT_DST}")
        os.rename(f"{DIR}/template{EXT_DST}", f"{DIR}/Jetbrains New UI Light{EXT_DST}")

def fixFiles(DIR: str, EXT: str, MAP: dict) -> None:
        with open(f"{DIR}/{MAP["--name"]}{EXT}", 'r', encoding="utf-8") as f:
                themeData: str = f.read()

        def substitute(item) -> None:
                nonlocal themeData
                for key, value in item.items():
                        if isinstance(value, dict):
                                substitute(value)
                        else:
                                themeData = re.sub(rf"\"{key}(?!-)", '\"' + value, themeData)

        substitute(MAP)

        with open(f"{DIR}/{MAP["--name"]}{EXT}", 'w', encoding="utf-8") as f:
                f.write(themeData)

if __name__ == "__main__":
        VERSION: str = getVersion()

        for flag in sys.argv[1:]:
                match flag:
                        case "--vscode":
                                copyTemplate("./themes", ".json", ".json")
                                fixFiles("./themes", ".json", DARK_MAP)
                                fixFiles("./themes", ".json", LIGHT_MAP)

                                # Replace --version in package.json
                                with open("./templates/package-template.json", 'r', encoding="utf-8") as f:
                                        package: str = f.read()
                                with open("package.json", 'w', encoding="utf-8") as f:
                                        package = package.replace("--version", VERSION)
                                        f.write(package)

                                # Replace --version in package-lock.json
                                with open("./templates/package-lock-template.json", 'r', encoding="utf-8") as f:
                                        packageLock: str = f.read()
                                with open("package-lock.json", 'w', encoding="utf-8") as f:
                                        packageLock = packageLock.replace("--version", VERSION)
                                        f.write(packageLock)

                                subprocess.run(["npx", "tsc"], shell=True)
                                subprocess.run(["vsce", "package"], shell=True)

                                # Clear generated files
                                shutil.rmtree("./themes/")
                                os.remove("package.json")
                                os.remove("package-lock.json")
                        case "--vs":
                                copyTemplate("./vsthemes", ".xml", ".vstheme")
                                fixFiles("./vsthemes", ".vstheme")

                                # TODO subprocess.run(["dotnet", "build"], shell=True)

                                shutil.rmtree("./vsthemes/")
                        case "--install-vscode":
                                subprocess.run(["code", "--install-extension", f"jetbrains-themes-{VERSION}.vsix"], shell=True)
                        case "--install-vs":
                                # TODO subprocess.run(["code", "--install-extension", f"jetbrains-themes-{VERSION}.vsix"], shell=True)
                                ""