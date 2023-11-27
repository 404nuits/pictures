import os, json
from PIL import Image
from datetime import datetime

def check_dir(mode):

    thumbspath = "./thumbs/" + mode
    dirpath = "./images/" + mode
    filepath = "./jsons/" + mode + ".json"

    files_in_dir = os.listdir(dirpath)
    files_in_dir.remove(".gitkeep")

    f = open(filepath)
    files_in_list = json.load(f)
    f.close()

    registered_files = [f["name"] for f in files_in_list if f["name"] in files_in_dir]
    new_files = [f for f in files_in_dir if f not in registered_files]
    deleted_files = [f["name"] for f in files_in_list if f["name"] not in files_in_dir]

    sorted_list = []

    # Creating thumbnails for new images
    for file in new_files:

        image = Image.open(dirpath + '/' + file)
        
        # --- Image date ---
        date = image.getexif().get(306)
        print(date)
        print(image.getexif())

        # --- Image size ---
        w, h = image.size

        # --- Image thumbnail ---
        t_h = 700
        t_w = round(w*t_h/h)

        image.thumbnail((t_w, t_h))
        thumb_name = file[:-4] + "_thumb.jpg"
        image.save(thumbspath + '/' + thumb_name)

        # --- Prompt location ---
        
        new_file = {
            "src": "/images/"+mode+"/"+file,
            "thumb": "/images/"+mode+"/thumbs/"+thumb_name,
            "alt": file,
            "location": "",
            "width": w,
            "height": h,
            "name": file,
            "date": date if date is not None else "1990:01:01 01:00:00"
        }

        files_in_list.append(new_file)
        sorted_list = sorted(files_in_list, reverse=True, key=lambda e: datetime.strptime(e["date"], '%Y:%m:%d %H:%M:%S'))
    
    # Serializing json
    json_object = json.dumps(sorted_list, indent=4)
    
    # Writing to sample.json
    with open(filepath, "w") as out:
        out.write(json_object)

if __name__ == '__main__':
    print("Processing pictures...")
    check_dir('photos')
    print("Processing designs...")
    check_dir('designs')
    print("Processed!")
