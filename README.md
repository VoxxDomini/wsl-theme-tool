# wsl-theme-tool
 
## Installation and usage
- open ~/.bashrc
- add

```
fuction theme() {
    python3 ~/wsl-theme.tool.py "$@"
}
```

- Change theme to whatever you want the command to be
- Open wsl settings, click View Json and copy its path and replace it in the script
- Make a folder to put terminal backgrounds, add its path to the script
- Run "source ~/.bashrc"
- Type "theme -h" to view commands

## Command overview
```
-o -opacity 1-100 background opacity
-bo -bg-opacity 1-100 background image opacity
-a 1/0 or empty to toggle, background acrylic effect
-bi -bg-img index number, empty for random image selected from specified folder
-c -color 1-6 or empty for random, picks one of the default WSL color schemes
```
