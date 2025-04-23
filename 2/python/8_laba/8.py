import toga
from toga.style import Pack
from toga.style.pack import COLUMN
from toga import Label
from toga import Window

class MyError(Exception):
    def __init__(self, message):
        super().__init__(message)

class PasswordManager(toga.App, MyError):
    def __init__(self, **kwargs):
        super().__init__(formal_name="Password Manager", app_id="pswrdmngr", **kwargs)

    def startup(self):
        main_box = toga.Box(style=Pack(direction=COLUMN))

        service_input = toga.TextInput(placeholder='Service')
        username_input = toga.TextInput(placeholder='Username')
        password_input = toga.PasswordInput(placeholder='Password')

        save_button = toga.Button('Save', on_press=self.save_password)

        self.table = toga.Table(
            headings=["Service", "Username", "Password"],
        )

        self.error_label = toga.Label(text='')

        main_box.add(service_input)
        main_box.add(username_input)
        main_box.add(password_input)
        main_box.add(save_button)
        main_box.add(self.error_label)
        main_box.add(self.table)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()    

    def save_password(self, widget):
        service = widget.parent.children[0].value
        username = widget.parent.children[1].value
        password = widget.parent.children[2].value

        try:
            if not service:
                raise MyError("Заполните поле Service")
            elif not username:
                raise MyError("Заполните поле Username")
            elif not password:
                raise MyError("Заполните поле Password")

            self.table.data.append([service, username, password])
            self.error_label.text = ''
        
        except MyError as e:
            self.error_label.text = f'Error: {e}'

def main():
    return PasswordManager()

if __name__ == '__main__':
    main().main_loop()  
