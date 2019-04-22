# wordpress-osm-shortcode-generator
Create shortcode and markers file for the [OSM wordpress plugin](https://wp-osm-plugin.hanblog.net/) from gpx tracks

## Install

`python3 -m pip install git+https://github.com/s-bl/wordpress-osm-shortcode-generator.git`

## Usage

### Arguments

    --xml-path - Path to gpx files
    --base-url - Base URL of your website
    --relative-remote-paths/--no-relative-paths - Specify all path relative to base url or as absolute path (default: False)
    --uploads-folder - Remote folder containing gpx files relative to /wp-content/uploads/ (default: workouts)
    --output-dir - Directory to which all outputs are written
