
input_file_name = "lecture_notes_full_utf8.tex"
output_file_name = "lecture_notes_full.tex"

with open(input_file_name, "rt", encoding="utf-8") as input_file,\
        open(output_file_name, "wt", encoding="ascii") as output_file:
    output_file.write(input_file.read())

with open(output_file_name, "rt") as output_file:
    assert all(ord(c) < 128 for c in output_file.read())
