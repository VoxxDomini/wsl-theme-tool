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