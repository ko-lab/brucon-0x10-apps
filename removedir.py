import os

def remove_dir_recursively(path):
    print('removing dir: '+path)
    for item in os.listdir(path):
        item_path = path+'/'+ item
        try:
            print('removing file: '+item_path)
            os.remove(item_path)
        except:
            remove_dir_recursively(item_path)
    os.rmdir(path)

remove_dir_recursively('/apps')
remove_dir_recursively('/None')
