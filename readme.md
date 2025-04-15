# Infos

A theme with languages support from across all [`Jetbrains`](https://www.jetbrains.com) IDEs.
You can view the full changelog [here](./CHANGELOG.md).

# Compatibility and Incompatibilities

## Extension Incompatibilities

- [`twxs.cmake`](https://marketplace.visualstudio.com/items?itemName=twxs.cmake):<br>
  `CMake` semantic token highlighting depends on `josetr.cmake-language-support-vscode`, **not** `twxs.cmake`.
  This because the latter has a *worse* and sometimes *broken* tokenization.

## Languages compatibility

The extension provides *basic* colorization for **all** languages, but there are some languages that are better colored when using a **tokenizer** and **semantic token highlighter**. The languages that **depend** on other extensions for a better colorization are:

 - `Python`: [*ms-python.python*](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
 - `AHK`:  [*mark-wiemer.vscode-autohotkey-plus-plus*](https://marketplace.visualstudio.com/items?itemName=mark-wiemer.vscode-autohotkey-plus-plus)
 - `XML`: [*redhat.vscode-xml*](https://marketplace.visualstudio.com/items?itemName=redhat.vscode-xml)
 - `YAML`: [*redhat.vscode-yaml*](https://marketplace.visualstudio.com/items?itemName=redhat.vscode-yaml)
 - `C/C++`: [*ms-vscode.cpptools*](https://marketplace.visualstudio.com/items?itemName=ms-vscode.cpptools) or [*jeff-hykin.better-cpp-syntax*](https://marketplace.visualstudio.com/items?itemName=jeff-hykin.better-cpp-syntax)
 - `CMake`:  [*josetr.cmake-language-support-vscode*](https://marketplace.visualstudio.com/items?itemName=josetr.cmake-language-support-vscode)
 - `Assembly x86`:  [*maziac.asm-code-lens*](https://marketplace.visualstudio.com/items?itemName=maziac.asm-code-lens)
 - `C#`:  [*ms-dotnettools.csharp*](https://marketplace.visualstudio.com/items?itemName=ms-dotnettools.csharp)

Some languages have a good enough tokenizer already **built in** vscode, so they do not rely on extension for a proper colorization. These languages are:

 - `Javascript`
 - `Typescript`
 - `HTML`
 - `CSS`
 - `JSON`
 - `Shell`
 - `Batch`