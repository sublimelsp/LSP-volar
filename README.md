# LSP-volar

This is a helper package that automatically installs and updates the [Volar Language Server](https://github.com/johnsoncodehk/volar) for you.

## Table of Contents
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Take over mode 🤝](#enable-for-non-vue-files)
  - [Inlay hints](#inlay-hints)
  - [Vue 2 support](#vue-2-support)

### Installation

* Install [LSP](https://packagecontrol.io/packages/LSP), [Vue Syntax Highlight](https://packagecontrol.io/packages/Vue%20Syntax%20Highlight) and [LSP-volar](https://packagecontrol.io/packages/LSP-volar) from Package Control.
* Restart Sublime.

### Configuration

Open the configuration file using Command Palette with `Preferences: LSP-volar Settings` command or opening it from the Sublime menu (`Preferences > Package Settings > LSP > Servers > LSP-volar`).

### Enable for non-Vue files

Allow LSP-volar to start in `*.ts | *.tsx | *.js | *.jsx` files.

#### Per project:

Create a sublime project file with the following contents:

```js
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

```js
// Settings in here override those in "LSP-volar/LSP-volar.sublime-settings"

{
    "selector": "text.html.vue | source.ts | source.tsx | source.js | source.jsx"
}
```

> NOTE: When enabling LSP-volar for non-Vue files, it is advisable to disable the `LSP-typescript` package to avoid showing duplicate results.

### Inlay hints

Inlay hints are short textual annotations that show parameter names, type hints.

![inlay-hints](./images/inlay-hints.png)

To enable inlay hints:
1. Open the command palette and select `Preferences: LSP Settings`, then enable `show_inlay_hints`:
```js
{
    "show_inlay_hints": true
}
```

2. Modify the following settings through `Preferences: LSP-volar Settings`:

```js
{
  "settings": {
    // javascript inlay hints options.
    "javascript.inlayHints.enumMemberValues.enabled": false,
    "javascript.inlayHints.functionLikeReturnTypes.enabled": false,
    "javascript.inlayHints.parameterNames.enabled": "none",
    "javascript.inlayHints.parameterNames.suppressWhenArgumentMatchesName": false,
    "javascript.inlayHints.parameterTypes.enabled": false,
    "javascript.inlayHints.propertyDeclarationTypes.enabled": false,
    "javascript.inlayHints.variableTypes.enabled": false,
    // typescript inlay hints options.
    "typescript.inlayHints.enumMemberValues.enabled": false,
    "typescript.inlayHints.functionLikeReturnTypes.enabled": false,
    "typescript.inlayHints.parameterNames.enabled": "none",
    "typescript.inlayHints.parameterNames.suppressWhenArgumentMatchesName": false,
    "typescript.inlayHints.parameterTypes.enabled": false,
    "typescript.inlayHints.propertyDeclarationTypes.enabled": false,
    "typescript.inlayHints.variableTypes.enabled": false,
  }
}
```

> NOTE: Inlay hints require TypeScript 4.4+.

### Vue 2 support

Please see [Volar's Installation](https://github.com/johnsoncodehk/volar/blob/master/docs/installation.md) for setup instructions.

