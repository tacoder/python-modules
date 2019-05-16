Helper scripts that run through a JSON output of "tree" command

Sample command:

tree -J -a -f -s --du

Sample output:
[{"type":"directory","name": ".","contents":[
    {"type":"file","name":"./README.md","size":458},
    {"type":"file","name":"./basic_menu_example.py","size":469},
    {"type":"directory","name":"./bms-bot","size":3501,"contents":[
      {"type":"file","name":"./bms-bot/test.py","size":3405}
    ]},
    {"type":"directory","name":"./curses_modules","size":21245,"contents":[
      {"type":"file","name":"./curses_modules/basic_menu.py","size":8127},
      {"type":"file","name":"./curses_modules/basic_menu_driver.py","size":1170},
      {"type":"file","name":"./curses_modules/filtering_menu.py","size":9963},
      {"type":"file","name":"./curses_modules/filtering_menu_driver.py","size":1793}
    ]},
    {"type":"file","name":"./filtered_menu_example.py","size":542},
    {"type":"directory","name":"./tree-output-parser","size":160,"contents":[
      {"type":"file","name":"./tree-output-parser/README.md","size":64}
    ]}
  ]},
  {"type":"report","size":26695,"directories":3,"files":9}
]