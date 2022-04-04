#!/usr/bin/python

import sys

if len(sys.argv) <= 1:
    pass

filename = sys.argv[1]

with open(filename) as f:
    lines = f.readlines()

exploded_lines = list(map(lambda x: list(x.rstrip().upper()), lines))

next_clue = 1
across_clues = ["Across"]
down_clues = ["Down"]
border = f"border=1"
super_start = f"<sup><small><small>"
super_end = f"</sup></small></small>"
square_style = f"style=\"min-width: 30px; height: 30px\""
blank_square = f"<td bgcolor=\"black\">&nbsp;</td>"
blank_table = f"<table {border} style=\"border-collapse:collapse\">\n"
answer_table = f"<table {border} style=\"border-collapse:collapse\">\n"

max_columns = max(map(lambda x: len(x), exploded_lines))
for row_num, row in enumerate(exploded_lines):
    blank_table += "<tr>"
    answer_table += "<tr>"
    for col_num, col in enumerate(row):
        start_down_word = False
        start_across_word = False
        if col != " ":
            if (row_num == 0) or (len(exploded_lines[row_num - 1]) <= col_num) or (exploded_lines[row_num - 1][col_num] == " "):
                # Make sure that there is something below where we are
                if ((row_num + 1) < len(exploded_lines)) and (exploded_lines[row_num + 1][col_num] != " "):
                    start_down_word = True
            if (col_num == 0) or (row[col_num - 1] == " "):
                # Make sure that this is really the beginning of the word - make sure that there is a letter following
                if ((col_num + 1) < len(row)) and (row[col_num + 1] != " "):
                    start_across_word = True

            if start_down_word or start_across_word:
                blank_table += f"<td {square_style}>{super_start}{next_clue}{super_end}</td>"
                answer_table += f"<td {square_style}>{super_start}{next_clue}{super_end}{col}</td>"
                if start_down_word:
                    down_clues.append(next_clue)
                if start_across_word:
                    across_clues.append(next_clue)
                next_clue += 1
            else:
                blank_table += f"<td {square_style}>&nbsp;</td>"
                answer_table += f"<td {square_style}>{col}</td>"
        else:
            blank_table += blank_square
            answer_table += blank_square

    if (len(row) < max_columns):
        fill_squares = (blank_square * (max_columns - len(row)))
        blank_table += fill_squares
        answer_table += fill_squares

    blank_table += "</tr>\n"
    answer_table += "</tr>\n"

answer_table += "\n</table>\n"
blank_table += "\n</table>\n"

print(f"<html><body>")
print(blank_table)

across_clues_table = list(map(lambda x: f"<td>{x}. </td>", across_clues))
down_clues_table = list(map(lambda x: f"<td>{x}. </td>", down_clues))

if (len(across_clues_table) < len(down_clues_table)):
    across_clues_table.extend(["<td></td>"] * (len(down_clues_table) - len(across_clues_table)))
if (len(down_clues_table) < len(across_clues_table)):
    down_clues_table.extend(["<td></td>"] * (len(across_clues_table) - len(down_clues_table)))

clues_table = "\n".join(list(map(lambda across,down: f"<tr>{across}{down}</tr>\n", across_clues_table, down_clues_table)))

print(f"<table>{clues_table}<table>\n")
print(answer_table)
print(f"</body></html>")

