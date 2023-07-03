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

> **Warning**
> Don't use this unless you really have a specific reason. It provides worse experience than `LSP-typescript` in `.js/.ts` files due to not receiving diagnostic updates on modifying related files. Also it's missing some features of `LSP-typescript`.
> See related issue: https://github.com/vuejs/language-tools/issues/3229

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

### Commands

Package provides a few commands in the Command Palette that can be useful for debugging Volar issues.

#### `LSP-volar (Debug): Show Virtual Files`

Shows a tree view of all internal virtual files associated with the currently opened `vue` file and allows for seeing their contents.

#### `LSP-volar (Debug): Write Virtual Files`

Writes all internal virtual files to disk. The files will be created alongside the original `vue` files that Volar has loaded internally. This can also include `vue` files within `node_modules`. Those files can be useful in figuring out why there are type issues in `vue` files that maybe are due to a Volar bug.

> **Note**
> Type-checking those genearated `.ts` files using `LSP-typescript` is not equivalent to what `LSP-volar` does as Volar does some internal Vue type augmentations that `LSP-typescript` does not do. To get a more relevant type checking when inspecting those files it's recommended to disable `LSP-typescript` and enable `LSP-volar` for TS files instead. Check [Enable for non-Vue files](#enable-for-non-vue-files) section.

> **Note**
> If there are many `vue` files in the project then a lot of files can be created by this command and those could be a bit tiresome to clean up later. In a git-tracked project you might want to use `git clean -fx` to remove all untracked files. Just make sure you don't have any useful untracked files.

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

