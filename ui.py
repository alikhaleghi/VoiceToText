from time import sleep
from config import config, saveSetting
from history import get_history, add_history, delete_history
from start_listening import listen, speak
import flet as ft
import pyperclip

# import pyi_splash 
# pyi_splash.update_text("PyInstaller is a great software!")
# pyi_splash.update_text("Second time's a charm!") 
# pyi_splash.close()

def main(page: ft.Page):
  page.title = "Voice To Text (AK)"
  page.window_width = 400
  page.window_height = 600
  if(config.get('Settings', 'alwaysontop') == 'active'):
    page.window_always_on_top = True
  page.window_resizable = False
  # page.window_frameless = True
  page.window_maximizable = False
  page.padding = 0
  page.spacing = 0
  page.window_center()
  page.update() 
  
  page.theme_mode = ft.ThemeMode.LIGHT if config.get('Settings', 'theme') == 'light' else ft.ThemeMode.DARK

  def switch_theme_mode(e):
    color = None
    if page.theme_mode == ft.ThemeMode.LIGHT:
      page.theme_mode = ft.ThemeMode.DARK
      color = 'dark'
    else:
      color = 'light'
      page.theme_mode = ft.ThemeMode.LIGHT

    config.set('Settings', 'theme', color)
    saveSetting()
    page.update()
 
  
  def check_item_clicked(e):
    e.control.checked = not e.control.checked
    page.update()

  if page.theme_mode == ft.ThemeMode.LIGHT:
    darkmodeIcon = ft.icons.WB_SUNNY
  else:
    darkmodeIcon = ft.icons.WB_SUNNY_OUTLINED

  def set_on_top(e):
    config.set('Settings', 'alwaysontop', 'active' if AlwaysOnTopCheck.value else 'no')
    page.window_always_on_top = AlwaysOnTopCheck.value
    saveSetting()
    page.update()
  def set_lang(e):
    config.set('Settings', 'language', dd.value)
    saveSetting()
    page.update()

  def set_auto_copy(e):
    if(config.get('Settings', 'autocopy') == 'active'):
      config.set('Settings', 'autocopy', 'no')
    else:
      config.set('Settings', 'autocopy', 'active')
    saveSetting()
    page.update()

  def startRecording(e):
    page.splash = ft.ProgressBar()
    btn.disabled = True
    btn.text = "Listening..."
    
    page.update()
    text = listen()
    page.update()
    # sleep(1)
    
    if text:
      whatISaid.value = text
      whatISaid.label = 'What You Said:' if whatISaid.value else 'Please click Start listening and talk.'
      
      id = add_history(text)

      history.controls.insert(0,ft.Dismissible(
        content=ft.ListTile(data=id, title=ft.Text(f"{text}")),
        dismiss_direction=ft.DismissDirection.HORIZONTAL,
        background=ft.Container(bgcolor=ft.colors.GREEN),
        secondary_background=ft.Container(bgcolor=ft.colors.RED),
        on_dismiss=handle_dismiss, 
        on_update=handle_update,
        on_confirm_dismiss=handle_confirm_dismiss,
        dismiss_thresholds={
          ft.DismissDirection.END_TO_START: 0.2,
          ft.DismissDirection.START_TO_END: 0.2,
        },
      ))

      page.update()

      if(config.get('Settings', 'autocopy') == 'active'):
        pyperclip.copy(text)
        print("Text copied to clipboard!")
    
    page.splash = None
    btn.text = "Start Listening..."
    btn.disabled = False
    page.update() 
 
  btn = ft.FilledButton(('Start Listening!'),  on_click=startRecording)

  dd = ft.Dropdown( 
    label="Language",
    options=[
      ft.dropdown.Option("fa-IR"),
      ft.dropdown.Option("en-US"),
      ft.dropdown.Option("es-AR"),
    ],
    on_change=set_lang
  )
  dd.value =config.get('Settings', "language")
  
  whatISaid = ft.TextField( 
    multiline=True, 
    read_only=True, 
    min_lines=12,
    max_lines=12,
    # value=config.get('Settings', "language"),
  )

  whatISaid.label = 'What You Said:' if whatISaid.value else 'Please click Start listening and talk.'



  def close_yes_dlg(e):
    page.close_dialog()
    print(dlg)
    print(dlg.data)
    dlg.data.confirm_dismiss(True)

  def close_no_dlg(e):
    page.close_dialog()
    dlg.data.confirm_dismiss(False)

  dlg = ft.AlertDialog(
    modal=True,
    title=ft.Text("Please confirm"),
    content=ft.Text("Do you really want to delete this item?"),
    actions=[
      ft.TextButton("Yes", on_click=close_yes_dlg),
      ft.TextButton("No", on_click=close_no_dlg),
    ],
    actions_alignment=ft.MainAxisAlignment.CENTER,
  )

  def handle_confirm_dismiss(e: ft.DismissibleDismissEvent):
    if e.direction == ft.DismissDirection.END_TO_START: # right-to-left slide
      # save current dismissible to dialog's data
      dlg.data = e.control
      print(e.page)
      page.show_dialog(dlg)
    else: # left-to-right slide
      e.control.confirm_dismiss(True)

  def handle_dismiss(e):
    if(e.control.content.data):
      delete_history(e.control.content.data)
    print(history)
    history.controls.remove(e.control)
    page.update()

  def handle_update(e: ft.DismissibleUpdateEvent):
    e
    # print(f"Update - direction: {e.direction}, progress: {e.progress}, reached: {e.reached}, previous_reached: {e.previous_reached}")
  
  items = get_history()
  page.update()
  history = ft.ListView(
    controls=[
      ft.Dismissible(
        
        content=ft.ListTile(data=i[0], title=ft.Text(f"{i[1]}")),
        dismiss_direction=ft.DismissDirection.HORIZONTAL,
        background=ft.Container(bgcolor=ft.colors.GREEN),
        secondary_background=ft.Container(bgcolor=ft.colors.RED),
        on_dismiss=handle_dismiss, 
        on_update=handle_update,
        on_confirm_dismiss=handle_confirm_dismiss,
        dismiss_thresholds={
          ft.DismissDirection.END_TO_START: 0.2,
          ft.DismissDirection.START_TO_END: 0.2,
        },
      )
      for i in items
    ],
    expand=True,
  )

  ## settings 

  AlwaysOnTop = ft.CupertinoListTile(
    leading=(AlwaysOnTopCheck:=ft.Checkbox(label="", value=True if config.get('Settings', 'alwaysontop') == 'active' else False,on_change=set_on_top)) ,
    title=ft.Text("On-Top"),
    subtitle=ft.Text("Keep app Always On Top."),
  )
  AutoCopy = ft.CupertinoListTile(
    leading=ft.Checkbox(label="", value=True if config.get('Settings', 'autocopy') == 'active' else False,on_change=set_auto_copy) ,
    title=ft.Text("Auto-Copy"),
    subtitle=ft.Text("Whether or not to auto-copy messages."),
  )
  ThemeMode = ft.CupertinoListTile(
    leading=ft.Checkbox(label="", value=True if config.get('Settings', 'theme') == 'dark' else False, on_change=switch_theme_mode) ,
    title=ft.Text("Night-Mode"),
    subtitle=ft.Text("Use the Dark Theme."),
    
  )


  def updateTabs(e): 
    page.update()

  # page itself
  t = ft.Tabs(
    on_change=updateTabs,
    selected_index=0,
    animation_duration=500,
    tabs=[
      ft.Tab(
        text="Transcribe",
        icon=ft.icons.MIC,
        content=ft.Container(
          padding=10,
          content=ft.Column([
            ft.Container(), 
            dd, 
            ft.Container(expand=4, content=whatISaid),

            ft.Container(ft.Row([
              ft.Column(
              [
                ft.Container(
                  content=btn,
                  alignment=ft.alignment.center,
                  width=200,
                  height=50, 
                  border_radius=ft.border_radius.all(5),
                )
              ]) 
            ],spacing=10,alignment=ft.MainAxisAlignment.CENTER))
            
          ]), alignment=ft.alignment.center
        ),
      ),
      ft.Tab(
        icon=ft.icons.HISTORY,
        text="History",
        content= history
      ),
      ft.Tab(
        text="Setting",
        icon=ft.icons.SETTINGS,
        content=ft.Column([
          ft.Container(
            ft.Dropdown( 
              label="Language",
              options=[
                ft.dropdown.Option("fa-IR"),
                ft.dropdown.Option("en-US"),
                ft.dropdown.Option("es-AR"),
              ],
              on_change=set_lang
            ),
            padding=20,
          ),
          AlwaysOnTop,
          AutoCopy,
          ThemeMode
        ]),
      ),
    ],
    expand=1,
  )

  page.add(t)

ft.app(target=main)