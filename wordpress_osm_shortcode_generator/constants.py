EQUATORIAL_CIRCUMFERENCE = 40075 # km

# https://mapicons.mapsmarker.com/
workout_type_to_marker = {
    'cycling, sport': '{base_url}/wp-content/uploads/{uploads_folder}/cycling_sprint.png',
    'mountain biking': '{base_url}/wp-content/uploads/{uploads_folder}/mountainbiking.png',
    'hiking': '{base_url}/wp-content/uploads/{uploads_folder}/hiking.png',
    'running': '{base_url}/wp-content/uploads/{uploads_folder}/jogging.png',
    'cycling, {base_url}/transport': 'wp-content/uploads/{uploads_folder}/cycling.png',
}

workout_mappings = {
    'walking': 'hiking',
    'cycling_sport': 'cycling, sport'
}

workout_type_to_color = {
    'cycling, sport': 'blue',
    'mountain biking': 'red',
    'hiking': 'green',
    'running': 'orange',
    'cycling, transport': 'magenta',
}
