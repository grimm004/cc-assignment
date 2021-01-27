import re
import sys
import glob


def main() -> int:
    commands = set()

    for filepath in glob.glob("./data/*.tex"):
        print(f"Searching in '{filepath}'.")
        with open(filepath, "rt") as file:
            file_data = file.read()
            if not file_data.isascii():
                continue
            for command in re.finditer(r"\\[a-zA-Z]+( |{|\r\n|\r|\n)", file_data):
                commands.add(command.group().replace("\n", "").replace("\r", "").replace(" ", "").replace("{", ""))

    with open("./data/latex_dict.txt", "wt", encoding="ascii") as latex_dict_file, \
         open("./data/30k.txt", "rt", encoding="ascii") as dict_file:
        latex_dict_file.write("\n".join(sorted(commands)))
        latex_dict_file.write("\n" + dict_file.read())

    return 0


if __name__ == "__main__":
    sys.exit(main())
