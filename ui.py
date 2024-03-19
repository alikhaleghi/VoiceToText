from time import sleep
from config import config, saveSetting
from history import get_history, add_history
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
    page.update()
    text = listen()
    page.update()
    # sleep(1)
    
    print(text)
    
    if text:
      whatISaid.value = text
      whatISaid.label = 'What You Said:' if whatISaid.value else 'Please click Start listening and talk.'
      add_history(text)
      if(config.get('Settings', 'autocopy') == 'active'):
        pyperclip.copy(text)
        print("Text copied to clipboard!")
    
    page.splash = None
    btn.disabled = False
    page.update()

  btn = ft.FilledButton("Start Listening!", on_click=startRecording)

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
    min_lines=10,
    max_lines=10,
    # value=config.get('Settings', "language"),
  )

  whatISaid.label = 'What You Said:' if whatISaid.value else 'Please click Start listening and talk.'

  c1 = ft.Switch(label="AutoCopy",on_change=set_auto_copy, value=True if config.get('Settings', 'autocopy') == 'active' else False)

  page.window_height, page.window_width = 500, 400

  def close_yes_dlg(e):
    page.close_dialog()
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
      page.show_dialog(dlg)
    else: # left-to-right slide
      e.control.confirm_dismiss(True)

  def handle_dismiss(e):
    # history.controls.remove(e.control)
    page.update()

  def handle_update(e: ft.DismissibleUpdateEvent):
    print(f"Update - direction: {e.direction}, progress: {e.progress}, reached: {e.reached}, previous_reached: {e.previous_reached}")
  items = None
  def realHistory(): 
    return ft.ListView(
    controls=[
      ft.Dismissible(
        content=ft.ListTile(title=ft.Text(f"Item {i}")),
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
      for i in get_history()
    ],
    expand=True,
  )
  
  
  def updateTabs(e):
    page.update()
  t = ft.Tabs(
    on_change=updateTabs,
    selected_index=0,
    animation_duration=300,
    tabs=[
      ft.Tab(
        text="Transcribe",
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
              ]),
              ft.Column(
              [
                c1,
              ]) 
            ],spacing=10,alignment=ft.MainAxisAlignment.CENTER))
            
          ]), alignment=ft.alignment.center
        ),
      ),
      ft.Tab(
        tab_content=ft.Text("History"),
        content= realHistory()
      ),
      ft.Tab(
        text="Setting",
        icon=ft.icons.SETTINGS,
        content=ft.IconButton(darkmodeIcon, on_click=switch_theme_mode),
      ),
    ],
    expand=1,
  )

  page.add(t)
  


  # page.add(ft.Row([
  #     ft.Container(expand=4, content=dd),
  # ]))
  # page.add(
  #     ft.Divider(height=35),
  #     whatISaid
  # )
  # page.add(
  #     ft.Divider(height=35),
  #     ,
  #     ft.Row([
  # ]))


ft.app(target=main)