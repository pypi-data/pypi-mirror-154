# Shōtokatan
Functions that facilitate certain actions. Which needs to cite some parts for it to work.

## Update 0.4.9
- ### Console()
- Fixed cd command
- ### MySQL Functions
- mysql_create_value
- mysql_create_tables
- mysql_show_database
- mysql_show_tables
- ### Others Functions
- fix_name_files

## Features

- NEW **mysql_create_value**
- NEW **mysql_create_tables**
- NEW **mysql_show_database**
- NEW **mysql_show_tables**
- NEW **fix_name_files** Will replace "undelines" with space and make the first letters of words uppercase.
- **convertmillis** convert milliseconds in seconds, minutes and hours Ex: (convertmillis(62000) -> output: (00, 01, 02))
- **crypto_key** create a key of any size.
- **sql_create_values** generates the value within the cited table and columns.
- **sql_create_table** create the table and its columns.
- **file_to_binary**, onvert digital data to binary format.
- **hex_to_rgb**. convert hex to rgb.
- **rgb_to_hex** convert rgb to hex.
- **cal_math** solve math accounts and show if you want.
- **token_generate** Just generate a Token with "uuid4".
- **write_file** It places the desired content in the file and maintains the
     information that exists within the file..
- **read_file** Show the current date.
- **check_date** Show the current time.
- **check_time** its every key piano on keyboard.
- **keyboard_piano** its every key piano on keyboard (https://virtualpiano.net/).
- **check_file** It will check if the file exists.
- **console** Execute command in computer terminal.
- **tempo** Delay execution for a given number of milliseconds.
- **detect_pixel** Check color pixel.
- **random_num** Random Value.
- **openweb** Open website with a Key.
- **pos_color** Shows color and coordinate based on mouse pointer.
- **sorteio** makes a random choice from a list.
- **on_off** One key for activate and other to desactivate.
- **sorteio_porcentagem** Generate random percentage.
- **click** clicks on the screen based on the mentioned coordinates.
- **screen** Collects the cited coordinates of the corners. Useful to check the colors of pixels in a certain area.
- **check_imports** Checks if pip(s) exists, if not, it does the installation if possible.
- **check_def** Look for "def" in the file behind the return.
- **read_midi** reads the desired midi file and returns with notes and click time
- **play_sheet** plays the music with the notes and the click time informed. For its operation, a piano with transpose is required that works on the keyboard arrows.
- **search_files** based on the given directory and the given search information, it creates a list of the files.
- **pags** with the list of items and the limit items in each page quoted, it will return the required value of pages for all items.
- **show_pages** with the list of items, the number of pages and the number of the desired page, it will show the items in the list corresponding to the page.
- **shou_pages** is a function based on the values ​​received (type file=None, path=None, range_list=None), it shows the pages and their contents, which you can navigate between the pages and do searches for a file, after citing the selected file numbering, it returns the file name.
- **check_updates_packages** check if you need to update any package and it tells you

## Examples of How To Use some functions.


```python
import Shotokatan as Shtan

# MySQL ---------

info = [
    "host=localhost",
    "user=root",
    "passwd=159"
]

basedata = 'yup_test'

table = [
    "tablename=People",
    "age INT(100) NULL, name TEXT",
    "COMMENT='comment'"
]

Shtan.mysql_create_tables(table, basedata, info)

data = shoto.mysql_show_tables(basedata, info)
print(data)

data = shoto.mysql_show_database(info)
print(data)

# MySQL ----------


# SQLITE --------

file = 'test.db'

Shtan.sql_create_table(file, 'People', ['Name, Age, weight'], ['int', 'str', 'float'])

tables = Shtan.sql_show_tables(file)
print(tables)

People = Shtan.sql_read_table(file, 'Clientes')
print(People)

Shtan.sql_create_values(file, 'People', ['Name', 'Age'], ['Osvaldo', '20'])

Shtan.sql_update_value(file, 'People', 'Name', 'Finn', 'weight', '20')

Shtan.sql_delete_value(file, 'People', 'Name', 'Osvaldo')

Shtan.sql_delete_table(file, 'People')

# SQLITE --------


files = Shtan.search_files('b') #will make a list with files that have the letter "b"

file = Shtan.shou_pages('.mid', '.',)

output = Shtan.console('start notepad')

clock = Shtan.check_time() # output : 16:30

data = Shtan.check_date('%Y-%m-%d') # output: 2022-04-17

Shtan.openweb('T', 'youtube.com', 'chrome') # pressing T, he will open youtube on chrome

Shtan.click(600, 500) # mouse click on X, Y

hex_color = Shtan.rgb_to_hex((255, 0, 0)) #return red color (255,0 , 0) in to hex

rgb_color = Shtan.hex_to_rgb(hex_color)

float_value = Shtan.random_num(0, 100, 2) # output: random float value

int_value = Shtan.random_num(0, 100, 1) # output: random int value

content = Shtan.read_midi('file.txt') # output: abc123 --> (file_content)

color_pixel = Shtan.detect_pixel(500, 500) # output: some color on that pixel. Ex: (100, 50, 255)

Shtan.write_file(['Hello', '123', '44pb'], 'some.txt', 1, '/game') # write content ['Hello', '123', '44pb'], in /game/some.txt and keep content on some.txt.

Shtan.write_file(['Hello', '123', '44pb'], 'some.txt', 0, '/game') # write content ['Hello', '123', '44pb'], in /game/some.txt and delete everything content on some.txt.

```

Developed by Aleph from Lotexiu(c) 2020