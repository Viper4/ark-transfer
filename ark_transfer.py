import os
import shutil
from zipfile import ZipFile, ZIP_DEFLATED
import pathlib


def save_world():
    map_path = f"{ark_path}\\{map_name}SavedArksLocal"
    if not os.path.exists(map_path):
        print("Path doesn't exist: " + map_path)
        return
    map_folder = pathlib.Path(map_path)

    settings_path = f"{ark_path}\\Config\\WindowsNoEditor\\GameUserSettings.ini"
    if not os.path.exists(settings_path):
        print("Path doesn't exist: " + settings_path)
        return

    dump_file = f"{dump_path}\\{map_name}Save.zip"

    with ZipFile(dump_file, 'w', ZIP_DEFLATED) as zip_object:
        # Adding files that need to be zipped
        for file in map_folder.iterdir():
            zip_object.write(file, arcname=file.name)
        zip_object.write(settings_path, arcname="GameUserSettings.ini")

    # Check to see if the zip file is created
    if os.path.exists(f"{dump_file}"):
        print(f"ZIP file created at {dump_file}")
    else:
        print("ZIP file not created")


def load_world(player_id,
               ark_path="C:\\Program Files (x86)\\Steam\\steamapps\\common\\ARK\\ShooterGame\\Saved"):
    save_file = f"{dump_path}\\{map_name}Save.zip"
    with ZipFile(save_file, 'r') as zip_object:
        save_path = f"{dump_path}\\ExtractedSave"
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        zip_object.extractall(save_path)
        save_folder = pathlib.Path(save_path)
        dst_path = f"{ark_path}\\{map_name}SavedArksLocal"
        if not os.path.exists(dst_path):
            os.makedirs(dst_path)
        else:
            # Delete all contents of dst
            for filename in os.listdir(dst_path):
                file_path = os.path.join(dst_path, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print('Failed to delete %s. Reason: %s' % (file_path, e))
        for file in save_folder.iterdir():
            if file.name == "GameUserSettings.ini":
                settings_path = f"{ark_path}\\Config\\WindowsNoEditor"
                if not os.path.exists(settings_path):
                    os.makedirs(settings_path)
                shutil.move(file, f"{ark_path}\\Config\\WindowsNoEditor\\GameUserSettings.ini")
                print(f"Moved GameUserSettings.ini to {ark_path}\\Config\\WindowsNoEditor\\")
            else:
                if file.stem == "LocalPlayer":
                    rename = True
                    with open(file, encoding='utf-8', errors='ignore', mode="r") as f:
                        for j in range(9):
                            if player_id in f.readline():
                                rename = False
                                break
                    if rename:
                        os.rename(file, f"{dst_path}\\{player_id}{file.suffix}")
                        print(f"Renamed {file.name} to {player_id}{file.suffix}")
                    else:
                        shutil.move(file, dst_path)
                elif file.stem == player_id:
                    os.rename(file, f"{dst_path}\\LocalPlayer{file.suffix}")
                    print(f"Renamed {file.name} to LocalPlayer{file.suffix}")
                else:
                    shutil.move(file, dst_path)
                print(f"Moved {file.name} to {dst_path}")
    print("Transfer Complete.")


map_names = ["Fjordur"]

player_names = [
    "Viper",
    "Supernuts",
    "Goody",
    "Hermes",
    "Hibernation"
]
players = {
    "Viper": "76561198829086762",
    "Supernuts": "76561199018448241",
    "Goody": "76561198800818448",
    "Hermes": "76561198277107732",
    "Hibernation": "76561198798240623"
}

# Press the green play button in the gutter to run the script.
if __name__ == '__main__':
    user_input = ""

    ark_path = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\ARK\\ShooterGame\\Saved"
    if not os.path.exists("C:\\Program Files (x86)\\Steam\\steamapps\\common\\ARK\\ShooterGame\\Saved"):
        ark_path = input("Couldn't find ark game files folder. Enter the path of your ark game (usually ends with ...\\ARK\\ShooterGame\\Saved)")

    while user_input != "e" and user_input != "exit" and user_input != "quit":
        print("Map #s:")
        for i in range(len(map_names)):
            print(f"{i}: {map_names[i]}")
        map_name = map_names[int(input("Enter # of map to save/load: "))]

        dump_path = f"C:\\Users\\{os.getlogin()}\\Documents\\ArkTransfer"
        if not os.path.exists(dump_path):
            os.makedirs(dump_path)

        user_input = input('Type "s" or "l" to save or load ark world: ')
        if user_input == "s":
            save_world()
        elif user_input == "l":
            print("Player #s: ")
            for i in range(len(player_names)):
                print(f" {i}: {player_names[i]}")

            index = int(input("Enter # of player to transfer ownership to: "))
            if input(f"Are you sure? This will erase everything in your {map_name} save folder. (y/n): ") == "y":
                load_world(players[player_names[index]])
