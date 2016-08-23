Set WshShell = CreateObject("WScript.Shell")
cmds = WshShell.RUN("starter.bat", 0, True)
Set WshShell = Nothing
