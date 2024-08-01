"""
TODO async menu
"""
if False:

    import asyncio
    from IPython.display import display, clear_output
    from pathlib import Path
    from .menu import check


    # Placeholder functions for the menu options
    async def check():
        pass


    async def setup():
        pass


    async def create_options_file():
        pass


    async def create_series_file():
        pass


    async def setup_series_steps():
        pass


    async def get():
        pass


    async def get_categories_main():
        pass


    async def help_():
        pass


    async def show_apikey():
        pass


    async def set_apikey_input():
        pass


    async def remove_cache():
        pass


    async def console_main_from_the_menu():
        pass


    async def version():
        pass


    async def py_version():
        pass


    async def check_compat():
        pass


    async def main_exit_function():
        pass


    # Menu item class
    class MenuItem:
        def __init__(self, function, description):
            self.function = function
            self.description = description


    # Menu maker class
    class MenuMaker:
        def __init__(self, menu_items, exit_item, exit_menu_call_back):
            self.menu_items = menu_items
            self.exit_item = exit_item
            self.exit_menu_call_back = exit_menu_call_back

        async def display(self):
            while True:
                clear_output(wait=True)
                print("Please choose an option:")
                for idx, item in enumerate(self.menu_items):
                    print(f"{idx + 1}. {item.description}")
                if self.exit_item:
                    print(f"{len(self.menu_items) + 1}. Exit")

                user_input = await asyncio.get_event_loop().run_in_executor(None, input, "Enter choice: ")
                try:
                    choice = int(user_input) - 1
                    if choice == len(self.menu_items):
                        await self.exit_menu_call_back()
                        break
                    elif 0 <= choice < len(self.menu_items):
                        await self.menu_items[choice].function()
                    else:
                        print("Invalid choice, please try again.")
                except ValueError:
                    print("Invalid input, please enter a number.")

                await asyncio.sleep(0.1)


    # Function to display the menu
    async def menu_display():
        funcs = [
            ("check setup", check),
            ("setup", setup),
            ("create user options file", create_options_file),
            ("create series file", create_series_file),
            ("add new series group", setup_series_steps),
            ("get data", get),
            ("get categories (get all series of a datagroup)", get_categories_main),  # next version
            # ("get data groups (on development)", get_datagroups_data_main),  # next version
            ("help", help_),
            ("show api key", show_apikey),
            ("save api key to file", set_apikey_input),
            ("remove cache folders", remove_cache),
            ("evdspy as a command line prompt", console_main_from_the_menu),
            ("version", version),
            ("py version", py_version),
            ("check compatibility of your python version", check_compat),
        ]

        menu_items = list(map(lambda x: MenuItem(x[1], x[0]), funcs))
        menu_maker = MenuMaker(
            menu_items=menu_items,
            exit_item=True,
            exit_menu_call_back=main_exit_function
        )
        await menu_maker.display()


    # Helper function to start the menu
    async def menu_helper_async():
        global menu_already_displayed
        menu_already_displayed = True
        await menu_display()


    # Global variable to store the menu task
    menu_task = None


    # Function to start the menu
    def start_menu():
        global menu_task
        if menu_task and not menu_task.done():
            menu_task.cancel()
        menu_task = asyncio.create_task(menu_helper_async())


    # Function to stop the menu
    def stop_menu():
        global menu_task
        if menu_task and not menu_task.done():
            menu_task.cancel()
            menu_task = None
            print("Menu stopped.")


    # Start the menu using asyncio.run in a script
    if __name__ == "__main__":
        asyncio.run(menu_helper_async())

    # In Jupyter Notebook, call start_menu and stop_menu functions
    # start_menu()
    # stop_menu()
