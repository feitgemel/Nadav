from pywinauto.application import Application
from pywinauto import Desktop

windows = Desktop(backend="win32").windows()

for w in windows:
    print(w.window_text())


print()
#print([w.window_text() for w in windows])


app = Application(backend='win32').connect(title = 'Grid 3 - Nadav - Home',timeout=2)
app.top_window().set_focus()


#app = Application(backend='win32').connect(title = '22.txt - Notepad',timeout=2)

#app.UntitledNotepad.menu_select("Help->About Notepad")
#app.AboutNotepad.OK.click()
#app.UntitledNotepad.Edit.type_keys("pywinauto Works!", with_spaces = True)