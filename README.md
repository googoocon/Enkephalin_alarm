# Enkephalin_alarm
## Limbus Company Enkephalin_alarm<br />
- build code

```
pyinstaller --onefile --noconsole --icon=enkephalin_icon.ico --add-data "enkephalin_icon.ico;." --add-data "araya_alarm.wav;." --hidden-import=pygame enkephalin_alarm.py
```
