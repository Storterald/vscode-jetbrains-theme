# Infos

A theme with languages support from across all [`Jetbrains`](https://www.jetbrains.com) IDEs.
You can view the full changelog [here](./CHANGELOG.md).

# Product Icons

All product icons are from [**Intellij Platform Icons**](https://intellij-icons.jetbrains.design) and follow the
[`Apache 2.0 License`](https://www.apache.org/licenses/LICENSE-2.0). All icons are resized to be **1024px** using an
[online tool](https://www.iloveimg.com/resize-image/resize-svg#resize-options,pixels). Sometimes manually edited with
[inkscape](https://gitlab.com/inkscape/inkscape).

# Compatibility and Incompatibilities

## Extension Incompatibilities

- [`twxs.cmake`](https://marketplace.visualstudio.com/items?itemName=twxs.cmake):<br>
  `CMake` semantic token highlighting depends on `josetr.cmake-language-support-vscode`, **not** `twxs.cmake`.
  This because the latter has a *worse* and sometimes *broken* tokenization.

## Languages compatibility

 - `CSS`
 - `HTML`
 - `Javascript`
 - `Json`
 - `Python`
 - `Regex`
 - `Shell`
 - `Typescript`
 - `XML`
 - `YAML`,

### From CLion:
 - `C++`
 - `CMake`: requires [*josetr.cmake-language-support-vscode*](https://marketplace.visualstudio.com/items?itemName=josetr.cmake-language-support-vscode)
 - `Assembly x86`: requires [*maziac.asm-code-lens*](https://marketplace.visualstudio.com/items?itemName=maziac.asm-code-lens)

### From Rider:
 - `C#`