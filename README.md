# LSP-volar

This is a helper package that automatically installs and updates the
[Volar Language Server](https://github.com/johnsoncodehk/volar) for you.

### Installation

* Install [LSP](https://packagecontrol.io/packages/LSP), [Vue Syntax Highlight](https://packagecontrol.io/packages/Vue%20Syntax%20Highlight) and [LSP-volar](https://packagecontrol.io/packages/LSP-volar) from Package Control.
* Restart Sublime.

### Configuration

Open configuration file using command palette with `Preferences: LSP-volar Settings` command or opening it from the Sublime menu (`Preferences > Package Settings > LSP > Servers > LSP-volar`).


### Take over mode

Allow LSP-volar to start in `*.ts` and `*.js` files.

To enable take over mode, from the command palette select `Preferences: LSP-volar Settings` and put the following in `LSP-volar.sublime-settings`.

```
{
	"settings": {
		"volar.takeOverMode.enabled": true
	}
}
```

It is advisebale to disable the LSP-typescript plugin to avoid showing duplicate results.