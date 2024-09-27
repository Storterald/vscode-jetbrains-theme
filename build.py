import os
import sys
import stat
import yaml
import shutil
import subprocess

# Load mappings
with open("./colors/CLion.yaml", 'r', encoding="utf-8") as f:
        CLION_MAP: dict = yaml.safe_load(f)
with open("./colors/Intellij.yaml", 'r', encoding="utf-8") as f:
        INTELLIJ_MAP: dict = yaml.safe_load(f)
with open("./colors/Dark.yaml", 'r', encoding="utf-8") as f:
        DARK_MAP: dict = yaml.safe_load(f)
with open("./colors/Light.yaml", 'r', encoding="utf-8") as f:
        LIGHT_MAP: dict = yaml.safe_load(f)

def onerror(func, path: str, _) -> None:
        if not os.access(path, os.W_OK):
                # Change file permission
                os.chmod(path, stat.S_IWUSR)
                func(path)
        else:
                # If error is not due to permission issues, raise
                assert False, "Could not delete cloned directory."

def getVersion() -> str:
        os.mkdir("./tmp/")
        subprocess.run(["git", "clone", "--depth", "1", "--no-checkout", "https://github.com/Storterald/Jetbrains-Themes", "."], cwd="./tmp/", shell=True)
        subprocess.run(["git", "fetch", "--tags", "--depth", "1"], cwd="./tmp/", shell=True)
        
        version: str = subprocess.check_output(["git", "for-each-ref", "--sort=-creatordate", "--format", "%(refname:short)", "refs/tags"], cwd="./tmp/", shell=True)
        version = version.decode("utf-8")
        version = version[:version.find('\n')]
        print(f"Current extension version is: {version}")

        shutil.rmtree("./tmp/", onexc=onerror)
        return version

def copyTemplate(DIR: str, EXT_SRC: str, EXT_DST: str) -> None:
        os.mkdir(f"{DIR}")
        shutil.copyfile(f"./templates/template{EXT_SRC}", f"{DIR}/template{EXT_DST}")
        shutil.copyfile(f"./{DIR}/template{EXT_DST}", f"{DIR}/CLion New UI Dark{EXT_DST}")
        shutil.copyfile(f"./{DIR}/template{EXT_DST}", f"{DIR}/Intellij New UI Dark{EXT_DST}")
        shutil.copyfile(f"./{DIR}/template{EXT_DST}", f"{DIR}/CLion New UI Light{EXT_DST}")
        os.rename(f"{DIR}/template{EXT_DST}", f"{DIR}/Intellij New UI Light{EXT_DST}")

def fixFiles(DIR: str, EXT: str, TYPE: str, IDE_MAP: dict) -> None:
        # Fix CLion theme
        with open(f"{DIR}/{CLION_MAP[TYPE]["--name"]}{EXT}", 'r', encoding="utf-8") as f:
                clionData: str = f.read()
        with open(f"{DIR}/{CLION_MAP[TYPE]["--name"]}{EXT}", 'w', encoding="utf-8") as f:
                DICT: dict = CLION_MAP[TYPE] | IDE_MAP
                for substitution in DICT:
                        clionData = clionData.replace(substitution, DICT[substitution])
                f.write(clionData)

        # Fix Intellij theme
        with open(f"{DIR}/{INTELLIJ_MAP[TYPE]["--name"]}{EXT}", 'r', encoding="utf-8") as f:
                intellijData: str = f.read()
        with open(f"{DIR}/{INTELLIJ_MAP[TYPE]["--name"]}{EXT}", 'w', encoding="utf-8") as f:
                DICT: dict = INTELLIJ_MAP[TYPE] | IDE_MAP
                for substitution in DICT:
                        intellijData = intellijData.replace(substitution, DICT[substitution])
                f.write(intellijData)

if __name__ == "__main__":
        VERSION: str = getVersion()

        for flag in sys.argv[1:]:
                match flag:
                        case "--vscode":
                                copyTemplate("./themes", ".json", ".json")
                                fixFiles("./themes", ".json", "dark", DARK_MAP)
                                fixFiles("./themes", ".json", "light", LIGHT_MAP)

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