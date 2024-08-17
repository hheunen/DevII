from graphviz import Digraph

# Créez un nouveau diagramme dirigé
dot = Digraph(comment='Class Diagram for File Management System')

# Définissez les classes et leurs attributs/méthodes
dot.node('A', 'CSVManager\n- csv_path\n+ __init__()\n+ write_metadata()\n+ update_metadata()\n+ find_metadata()\n+ remove_metadata()')
dot.node('B', 'FileReader\n- file_path\n- file_state\n- metadata\n- file_content\n+ __init__()\n+ open_file()\n+ extract_metadata()')
dot.node('C', 'Metadata\n- file_path\n- name\n- created_date\n- modification_date\n- size\n+ __init__()\n+ from_filepath()\n+ save_to_csv()\n+ update_in_csv()')
dot.node('D', 'Repertory\n- path\n- file_path_list\n+ __init__()\n+ read_directory()')
dot.node('E', 'WatchdogHandler\n- path\n- observer\n- csv_manager\n+ __init__()\n+ start()\n+ on_modified()\n+ on_created()\n+ on_deleted()')
dot.node('F', 'FileMonitorShell\n- csv_manager\n- handler\n+ __init__()\n+ do_start()\n+ do_reboot()\n+ do_exit()')

# Définir les relations
dot.edge('B', 'A', label='uses')
dot.edge('B', 'C', label='uses')
dot.edge('E', 'A', label='uses')
dot.edge('F', 'E', label='uses')
dot.edge('F', 'A', label='uses')

# Sauvegardez le diagramme
dot.format = 'png'
dot.render('class_diagram')