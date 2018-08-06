# no-alttabf5
A python tool to refresh the browser when a file is modified.

## Sample Usage
```bash
# reload browser when file1.txt or file2.txt changes
$ no-alttabf5 file1.txt file2.txt

# reload browser when file1.txt is modified and
# the selected window has a name that matches ".*RELOAD.*"
$ no-alttabf5 --winpat ".*RELOAD.*" file1.txt

```
Use -h to see other options.
