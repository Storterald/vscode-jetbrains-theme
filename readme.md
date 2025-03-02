# Infos

A theme with languages support from across all [`Jetbrains`](https://www.jetbrains.com) IDEs.
You can view the full changelog [here](./CHANGELOG.md).

# Jetbrains Icons

It is suggested to use the [`chadalen.vscode-jetbrains-icon-theme`](https://marketplace.visualstudio.com/items?itemName=chadalen.vscode-jetbrains-icon-theme)
extension and the [`storterald.jetbrains-product-icons`](https://marketplace.visualstudio.com/items?itemName=storterald.jetbrains-product-iconse)
extension to have both **icon theme** and **product icon theme**.

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
 - `C`
 - `C++`
 - `CMake`: requires [*josetr.cmake-language-support-vscode*](https://marketplace.visualstudio.com/items?itemName=josetr.cmake-language-support-vscode)
 - `Assembly x86`: requires [*maziac.asm-code-lens*](https://marketplace.visualstudio.com/items?itemName=maziac.asm-code-lens)

### From Rider:
 - `C#`