ssh pi "~/tree-1.8.0/tree -D -J -a -f -s --du /mnt/seagate2tb/DATA/Movies/  > ~/tree-output.json" ; scp pi:tree-output.json ~/Documents/clone/python-modules/tree-output-parser/data/movies-tree.json
cat ~/Documents/clone/python-modules/tree-output-parser/data/movies-tree.json
