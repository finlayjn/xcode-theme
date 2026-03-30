# Xcode Default — VS Code Theme

A faithful port of Apple's **Xcode Default Light** and **Xcode Default Dark** color themes for Visual Studio Code.

## Installation

1. Open VS Code
2. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on macOS)
3. Type **"Install from VSIX"** and select the command
4. Choose the `.vsix` file
5. Reload VS Code
6. Open **Preferences → Color Theme** and select **Xcode Default Light** or **Xcode Default Dark**

## Color Mapping

All colors were programmatically converted from Xcode's `.xccolortheme` RGBA float format to hex using the included `convert_colors.py` script — no manual guessing. Some colors were manually adjusted for contrast (e.g. warning squiggles).

Both light and dark variants are included, each mapped from their respective Xcode source themes.

## Adding a New Theme

### Exporting an `.xccolortheme` file from Xcode

1. Open **Xcode → Settings → Themes**
2. Click on the theme dropdown and select **Manage Themes...** at the bottom
4. Select the desired theme in the list
5. Press the **+** button and choose **Duplicate "(Theme Name)"**
6. The duplicated theme file will be saved to:
   ```
   ~/Library/Developer/Xcode/UserData/FontAndColorThemes/
   ```

### Converting and adding the theme

1. Run the conversion script to extract hex colors:
   ```
   python3 convert_colors.py /path/to/MyTheme.xccolortheme
   ```
2. Use the output to create a new theme JSON under `themes/`, following the structure of the existing themes.
3. Register the new theme in `package.json` under `contributes.themes`.
4. Rebuild with `npx @vscode/vsce package --allow-missing-repository`.

### Prompt for AI agents

> Given the attached `.xccolortheme` file, add a new VS Code theme variant to this extension. Run `convert_colors.py` on the file to get hex values. Create a new theme JSON in `themes/` using the existing light or dark theme as a template (match `"type": "light"` or `"dark"` based on the background color). Map all Xcode syntax token colors to their VS Code scope equivalents following the same pattern as the existing themes. Register the new theme in `package.json` and rebuild the VSIX.

## AI Disclaimer
Development of this extension was assisted by Claude Opus 4.6 (Anthropic), used via GitHub Copilot. All color values were programmatically extracted from Xcode's `.xccolortheme` file, ensuring an exact match without manual approximation, except for some manual adjustments for contrast. The conversion script is included in this repository for transparency.