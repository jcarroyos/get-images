import csv

def remove_logo_rows(input_file, output_file):
    filenames_to_remove = {
        'CasaAbierta_color-300x165.jpg',
        'CasaAbierta_light.png',
        'Asset-1.png',
        'zoom-in.png',
        'zoom-out.png',
        'PlantillaAudios-1.png'
    }
    
    seen_urls = set()
    
    with open(input_file, mode='r', newline='') as infile, open(output_file, mode='w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        header = next(reader)
        writer.writerow(header)
        
        for row in reader:
            image_url = row[0].strip()
            # Check for "logo" in a case-insensitive manner and strip whitespace
            if (not any('logo' in cell.lower().strip() for cell in row) and 
                not any(any(filename in cell for filename in filenames_to_remove) for cell in row) and 
                image_url not in seen_urls):
                writer.writerow(row)
                seen_urls.add(image_url)

if __name__ == "__main__":
    input_file = 'images_original.csv'
    output_file = 'images.csv'
    remove_logo_rows(input_file, output_file)
