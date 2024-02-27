from os import listdir, getcwd, getlogin, remove, path, system
from json import load, dump
from sys import argv
from logos import dye

args = argv[1:]


def status_string(status: bool):
    if status:
        return "enabled"
    else:
        return "disabled"


class ModManager:

    def __init__(self):

        self.base_paths = {
            "mod_manager": getcwd(),
            "mods": "/mnt/sda/games/Mods",
            "games": f"/home/{getlogin()}/.local/share/Steam/steamapps/common"
        }

        self.settings = self.get_mods()

    @staticmethod
    def copy_file(src_path, dst_path):
        arg = ""
        if path.isdir(src_path):
            arg = "-r "
        system(f"cp {arg}'{src_path}' '{dst_path}'")

    @staticmethod
    def remove_file(src_path):
        system(f"rm -rf {src_path}")

    def enable_mods(self, _game=None, _mod=None):

        def move_files(location, move_mode: bool, special_behavior=None):
            if special_behavior is None:
                if move_mode:
                    if not path.exists(location['game_path']):
                        self.copy_file(location['mod_path'], location['game_path'])

                else:
                    if path.exists(location['game_path']):
                        self.remove_file(location['game_path'])

            else:
                if special_behavior.lower() == "backup":

                    # If enabling the mod
                    if move_mode:
                        self.remove_file(location["game_path"])
                        self.copy_file(location["mod_path"], location["game_path"])

                    else:
                        # Remove the file from the game path, then restore the backup file
                        self.remove_file(location["game_path"])
                        self.copy_file(location["backup_path"], location["game_path"])

        def get_color(mode):
            if mode:
                return "green"
            else:
                return "red"

        try:
            if _game is not None:
                game_settings = {_game: self.settings[_game]}
                if _mod is not None:
                    game_settings = {_game: {_mod: self.settings[_game][_mod]}}
            else:
                game_settings = self.settings

        except KeyError:
            return

        for game, settings in game_settings.items():
            for mod, options in settings.items():

                # Uninstall conflicting mods
                if "conflicts" in options.keys() and options['enabled']:
                    for con in options['conflicts']:

                        # If the conflicting mod is installed. Otherwise, ignore it
                        if self.settings[game][con]['enabled']:
                            print(dye(f"{game} {mod} conflicts with {con}. Uninstall {con}? [Y/n]", "yellow"))
                            user = input(">>> ").lower()

                            if "y" in user or user == "":
                                print(dye(f"Uninstalling conflicting mod: {con}", "yellow"))
                                self.update_settings(game, con, False)
                                self.enable_mods(game, con)

                            elif "n" in user:
                                print(dye(f"Can't install {mod} because of conflicting mod {con}", "red"))
                                continue

                # Install requirements if needed
                if "requirements" in options.keys() and options['enabled']:
                    for req in options['requirements']:
                        if not self.settings[game][req]["enabled"]:
                            print(dye(f"{game.capitalize()} {mod} mod requires {req}.\nActivating requirements.",
                                      "yellow"))
                        self.update_settings(game, req, True)
                        self.enable_mods(game, req)

                font_color = get_color(options['enabled'])
                g_path = options['game_path']
                b_path = options['mod_path']
                status = options['enabled']
                mode = None
                if "backup_path" in options.keys():
                    mode = "backup"

                if isinstance(g_path, str) and isinstance(b_path, str):
                    move_files(options, status, mode)

                elif isinstance(g_path, list) and isinstance(b_path, list):
                    for i in range(len(g_path)):
                        src = g_path[i]
                        dst = b_path[i]
                        d = {"game_path": src, "mod_path": dst}
                        if mode is not None:
                            d["backup_path"] = options["backup_path"][i]

                        move_files(d, status, mode)

                else:
                    raise ValueError("Paths must be in string format, or list of strings for multiple files")

                if status:
                    print(dye(f"{game.replace('_', ' ').title()} mod {mod}", "cyan"),
                          dye("enabled", font_color))

                else:
                    print(dye(f"{game.replace('_', ' ').title()} mod {mod}", "cyan"),
                          dye("disabled", font_color))

    def get_mods(self, reset=False):
        if reset:
            remove(f"{self.base_paths['mod_manager']}/mods.json")

        if "mods.json" not in listdir("config_data"):
            default = {
                "name_of_game": {
                    "name_of_mod": {
                        "enabled": False,
                        "mod_path": "path/to/the/mod/file/in/storage/some_mod.pak",
                        "game_path": "path/to/the/mod/file/install/location/some_mod.pak"
                    },
                    "name_of_multi_file_mod": {
                        "enabled": False,
                        "mod_path": ["path/to/the/first/mod/some_file.type", "path/to/the/second/mod/some_file.type"],
                        "game_path": ["path/to/the/first/mod/some_file.type", "path/to/the/second/mod/some_file.type"]
                    },
                    "name_of_mod_with_requirements": {
                        "enabled": False,
                        "mod_path": "mod/path/or/paths/as/examples/above/demonstrate/file.type",
                        "game_path": "mod/path/or/paths/as/examples/above/demonstrate/file.type",
                        "requirements": ["name_of_required_mod_which_is_also_installed_and_named_in_this_file"]
                    },
                    "name_of_mod_with_conflicts": {
                        "enabled": False,
                        "mod_path": "/you/know/the/drill",
                        "game_path": "/same/drill/here",
                        "conflicts": ["name_of_conflicting_mod"]
                    }
                }
            }

            with open(f"config_data/mods.json", "w") as file:
                dump(default, file, indent=2)

        with open("config_data/mods.json", "r") as file:
            settings = load(file)

        return settings

    @staticmethod
    def get_aliases():
        with open("config_data/aliases.json") as file:
            aliases = load(file)

        return aliases

    def update_settings(self, game: str, mod: str, status: bool):

        if game in self.settings.keys():

            if mod in self.settings[game].keys():
                if self.settings[game][mod]['enabled'] != status:
                    self.settings[game][mod]['enabled'] = status
                    with open(f"{self.base_paths['mod_manager']}/config_data/mods.json", "w") as file:
                        dump(self.settings, file, indent=2)

            else:
                print(dye(f"That mod doesn't exist in {game} settings", "red"))
                return 1

        else:
            print("That game is not yet supported")

    def view_active_mods(self, game, mode):

        if mode == "-v" or mode == "--view":
            if game in self.settings.keys():
                print(dye(f"\n{game.replace('_', ' ').title()} Mods:", "blue"))
                sp_mult = max([len(i) for i in self.settings[game].keys()])
                for mod, options in self.settings[game].items():
                    color = "green" if options['enabled'] else "red"
                    sp = " " * (sp_mult - len(mod))
                    print(dye(f"\t{mod}{sp}:", "cyan"),
                          dye(f"{status_string(options['enabled'])}", color))


def test():
    """For feature testing"""
    pass


def main():

    mod_manager = ModManager()

    aliases = mod_manager.get_aliases()
    for k, v in aliases.items():
        if args[0] in v:
            args[0] = k
            break

    game = args[0]

    if len(args) == 3:

        mod = args[1]
        mode = args[2]

        if mode == "-e" or mode == "--enable":
            mode = True

        elif mode == "-d" or mode == "--disable":
            mode = False

        else:
            print(f"Argument for 'mode' must be -e to enable or -d to disable. Got '{mode}'")

        if isinstance(mode, bool):
            code = mod_manager.update_settings(game, mod, mode)
            if code == 1:
                exit()
            mod_manager.enable_mods(_game=game, _mod=mod)

    elif len(args) == 2:

        mode = args[1]

        if mode == "-v" or mode == "--view":
            mod_manager.view_active_mods(game, mode)

    elif len(args) == 1:

        mode = args[0]
        if mode == "-r" or mode == "--reset":
            mod_manager.get_mods(True)
            print(dye(f"Mod settings file reset", "cyan"))
            print(dye(f"Enabling and disabling mods to match it", "yellow"))
            mod_manager.enable_mods()

        else:
            print(dye(f"Pass -r or --reset as the second argument to reset the settings document", "yellow"))

    else:
        msg = "Must pass game, mod, and -e/-d to enable or disable."
        msg += "\nOtherwise, pass -v as the second argument to view the active mods"
        print(dye(msg, "red"))


if __name__ == "__main__":
    main()
