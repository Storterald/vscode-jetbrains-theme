import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {
        // Listen for theme changes
        vscode.window.onDidChangeActiveColorTheme(handleThemeChange);

        // Call the handler to set settings based on the current theme
        handleThemeChange(vscode.window.activeColorTheme);
}

function handleThemeChange(theme: vscode.ColorTheme) {
        const configuration = vscode.workspace.getConfiguration();

        switch (theme.kind) {
                case vscode.ColorThemeKind.Dark: {
                        configuration.update('workbench.iconTheme', 'vscode-jetbrains-icon-theme-2023-dark', vscode.ConfigurationTarget.Global);
                        configuration.update('better-comments.tags', getDarkCommentTags(), vscode.ConfigurationTarget.Global);
                        break;
                }
                case vscode.ColorThemeKind.Light: {
                        configuration.update('workbench.iconTheme', 'vscode-jetbrains-icon-theme-2023-light', vscode.ConfigurationTarget.Global);
                        configuration.update('better-comments.tags', getLightCommentTags(), vscode.ConfigurationTarget.Global);
                        break;
                }
        }
}

function getDarkCommentTags() {
        return [
                {
                        "tag": "TODO",
                        "color": "#8bb33d",
                        "strikethrough": false,
                        "underline": false,
                        "backgroundColor": "transparent",
                        "bold": false,
                        "italic": true
                }
        ];
}

function getLightCommentTags() {
        return [
                {
                        "tag": "TODO",
                        "color": "#008dde",
                        "strikethrough": false,
                        "underline": false,
                        "backgroundColor": "transparent",
                        "bold": false,
                        "italic": true
                }
        ];
}