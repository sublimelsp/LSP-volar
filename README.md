# LSP-volar

This is a helper package that automatically installs and updates the [Volar Language Server](https://github.com/johnsoncodehk/volar) for you.

### Installation

* Install [LSP](https://packagecontrol.io/packages/LSP), [Vue Syntax Highlight](https://packagecontrol.io/packages/Vue%20Syntax%20Highlight) and [LSP-volar](https://packagecontrol.io/packages/LSP-volar) from Package Control.
* Restart Sublime.

### Configuration

Open the configuration file using Command Palette with `Preferences: LSP-volar Settings` command or opening it from the Sublime menu (`Preferences > Package Settings > LSP > Servers > LSP-volar`).

### Vue 2 support

Please see [Volar's Installation](https://github.com/johnsoncodehk/volar/blob/master/docs/installation.md) for setup instructions.

### Enable for non-Vue files

Allow LSP-volar to start in `*.ts | *.tsx | *.js | *.jsx` files.

#### Per project:

Create a sublime project file with the following contents:

```
{
    "folders":
    [
        {
            "path": "."
        }
    ],
    "settings": {
        "LSP": {
            "LSP-volar": {
                "selector": "text.html.vue | source.ts | source.tsx | source.js | source.jsx"
            },
            "LSP-typescript": {
                "enabled": false
            }
        }
    }
}
```

#### Globally:

From the Command Palette select `Preferences: LSP-volar Settings` and paste the following:

```
// Settings in here override those in "LSP-volar/LSP-volar.sublime-settings"

{
    "selector": "text.html.vue | source.ts | source.tsx | source.js | source.jsx"
}
```

> NOTE: When enabling LSP-volar for non-Vue files, it is advisable to disable the `LSP-typescript` package to avoid showing duplicate results.

