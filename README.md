## How it works
Open the config_data/mods.json file and view the template. To set up a new mod<br>
whether it was downloaded or created yourself, simply edit the mods.json file so<br>
that the mod manager knows where to find the storage location of the mod, as well<br>
as the installation location.

This script simply moves mod files from one location to another. Nothing more<br>
complex than that. The mod_path lets the script know where to find the mod files<br>
that are stored somewhere on your computer, and the game_path lets the script<br>
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

All mods require the "enabled", "mod_path", and "game_path" keys. Both<br>
"requirements" and "conflicts" are optional fields that allow you to define which<br>
mods may require other mods to be enabled, and which mods conflict with others.<br>
If any conflicting mods are detected, the user will be prompted to confirm whether<br>
or not the conflicting mod should be enabled or not. If the user enters "yes" or "y"<br>
then the conflicting mod will be disabled. Otherwise, the mod that's attempting to be<br>
installed will not be enabled.