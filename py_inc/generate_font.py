from pathlib import Path
HERE = Path(__file__).parent


def generate_font_from_cpp():
    """ Generate Python list representations of all the characters in font12.c """
    with open(HERE / ".." / "font12.c") as f:
        lines = f.readlines()

    char_data = {}
    for i, line in enumerate(lines):
        if "'" in line and "(7 pixels wide)" in line:
            if "@84" in line:
                char = "'"
                continue
            char = line.split("'")[1]
            byte_data = lines[i + 1 : i + 13] # Characters are 12 bytes
            byte_data = [b.strip().split(",")[0] for b in byte_data]
            
            binary = [bin(int(b, 16)) for b in byte_data]
            binary_lists = []
            for n, b in enumerate(binary):
                if len(b) != 10:
                    # Length of 10 is '0b' + 8 bits
                    nzero_pad = 10 - len(b)
                    b = f"0b{nzero_pad*'0'}{b[2:]}"
                    binary[n] = b
                b_as_list = [x for x in b[2:]]
                binary_lists.append(b_as_list)

            char_data[char] = binary_lists

    string = "font12 = {\n"
    for key, data in char_data.items():
        if key == "\"":
            string += f"{' '*4}r'\"': [\n"
        elif key == "\\":
            string += f"{' '*4}\"\\\": [\n"
        else:
            string += f"{' '*4}r\"{key}\": [\n"
        for row in data:
            string += f"{' '*8}{row},\n"
        string += f"{' '*4}],\n"
    string += "}\n"

    with open("font12.py", "w") as f:
        f.write(string)


if __name__ == "__main__":
    generate_font_from_cpp()
