# How it works
Open the config_data/mods.json file and view the template. To set up a new mod
whether it was downloaded or created yourself, simply edit the mods.json file so
that the mod manager knows where to find the storage location of the mod, as well
as the installation location.

This script simply moves mod files from one location to another. Nothing more
complex than that. The mod_path lets the script know where to find the mod files
that are stored somewhere on your computer, and the game_path lets the script
know where the file needs to be installed. All paths should include a file name.

### Sample:

```json
{
  "palworld": {
    "mod_name": {
      "enabled": false,
      "mod_path": "/path/to/mod/in/storage/mod_name.pak",
      "game_path": "/path/to/game/directory/mod_name.pak"
    },
    "character_skin_mod": {
      "enabled": false,
      "mod_path": "/path/to/mod/in/storage/mod_name.pak",
      "game_path": "/path/to/game/directory/mod_name.pak",
      "requirements": [
        "name_of_mod_that_character_skin_mod_requires.pak"
      ],
      "conflicts": [
        "name_of_other_character_skin_mod.pak"
      ]
    },
    "other_character_skin_mod": {
      "mod_path": "path",
      "game_path": "path",
      "conflicts": [
        "character_skin_mod"
      ]
    }
  }
}
```

All mods require the "enabled", "mod_path", and "game_path" keys. Both
"requirements" and "conflicts" are optional fields that allow you to define which
mods may require other mods to be enabled, and which mods conflict with others.
If any conflicting mods are detected, the user will be prompted to confirm whether
the conflicting mod should be enabled or not. If the user enters "yes" or "y"
then the conflicting mod will be disabled. Otherwise, the mod that's attempting to be
installed will not be enabled.


## CLI interactions
The mod manager can be interacted with via command line. To get started,<br>
run the script, then pass in the name of the game, the mod, and the option<br>
`python main.py <game_name> <mod_name> <option>`.<br>
Options are listed below<br>

### Mod Options
-d, --disable = Disables the mod<br>
-e, --enable  = Enables the mod

Examples:<br>
`python main.py palworld foxparks_spyro -e`<br>
`python main.py palworld foxparks_spyro --disable`

### Other options
You can view which mods are installed for a certain game by running the script 
with the game name followed by the -v, or --view flag.<br>

Example:<br>
`python main.py palworld -v`


# Launch script
The following bash script can be used to more easily interact with the mod manager

gamemod.sh
```bash
#!/bin/bash

cd /home/dpad/software/python/game_mods/.venv/bin/
source activate
cd /home/dpad/software/python/game_mods
python main.py "$@"
deactivate
exit
```

Examples:<br>
`gamemod palworld -v`<br>
`gamemod palworld infinite_ammo --enable`


# Aliases
The aliases.json file is simply there to make it easier to enable and disable mods.<br>
Create your own by adding new lines to the json file. Many can be added for each game.<br>
Such as...<br>
```json
{
  "palworld": ["pw", "pal"],
  "tomb_raider": ["tr"]
}
```
This will allow you to enable or disable a mod by running a shorter command, like<br>
`gamemod tr god_mode -e` rather than `gamemod tome_raider god_mode -e`
