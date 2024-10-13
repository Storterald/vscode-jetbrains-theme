import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {
  // Listen for theme changes
  vscode.window.onDidChangeActiveColorTheme(handleThemeChange);

  // Call the handler to set settings based on the current theme
  handleThemeChange(vscode.window.activeColorTheme);
}

function handleThemeChange(theme: vscode.ColorTheme) {
  const configuration = vscode.workspace.getConfiguration();

  // Check which theme is active and update settings
  if (theme.kind === vscode.ColorThemeKind.Dark) {
    configuration.update('workbench.iconTheme', 'vscode-jetbrains-icon-theme-2023-dark', vscode.ConfigurationTarget.Global);
  } else if (theme.kind === vscode.ColorThemeKind.Light) {
    configuration.update('workbench.iconTheme', 'vscode-jetbrains-icon-theme-2023-light', vscode.ConfigurationTarget.Global);
  }
}

export function deactivate() {}