# LSP-volar

This is a helper package that automatically installs and updates the
[Volar Language Server](https://github.com/johnsoncodehk/volar) for you.

### Installation

* Install [LSP](https://packagecontrol.io/packages/LSP), [Vue Syntax Highlight](https://packagecontrol.io/packages/Vue%20Syntax%20Highlight) and [LSP-volar](https://packagecontrol.io/packages/LSP-volar) from Package Control.
* Restart Sublime.

### Configuration

Open configuration file using command palette with `Preferences: LSP-volar Settings` command or opening it from the Sublime menu (`Preferences > Package Settings > LSP > Servers > LSP-volar`).

### Take over mode

Allow LSP-volar to start in `*.ts | *.tsx | *.js | *.jsx` files.

You can enable the take over mode:
- per project
- globally

#### Per project

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

#### Globally

From the command palette select `Preferences: LSP-volar Settings` and paste the following:

```
// Settings in here override those in "LSP-volar/LSP-volar.sublime-settings"

{
	"selector": "source.vue | source.ts | source.tsx | source.js | source.jsx"
}
```

> NOTE: It is advisable to disable the LSP-typescript package when in take over mode to avoid showing duplicate results.

