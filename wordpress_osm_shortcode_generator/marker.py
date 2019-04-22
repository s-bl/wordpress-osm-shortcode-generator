from constants import workout_type_to_marker

class Marker:

    @classmethod
    def lineStyle(cls, id, color, width):
        xml = f'''   <Style id="{id}">
    <LineStyle>
      <color>{color}</color>
      <width>{width}</width>
    </LineStyle>
  </Style>
'''
        return xml

    @classmethod
    def iconStyle(cls, id, workout_type, href, scale, x, y, units):
        xml = f'''   <Style id="{id}">
    <IconStyle>
     <Icon> 
        <href>{workout_type_to_marker[workout_type]}</href>
      </Icon>
       <scale>{scale}</scale>
       <hotSpot x="{x}" y="{y}" xunits="{units}" yunits="{units}"/>
    </IconStyle>
  </Style>
'''
        return xml

    @classmethod
    def placemark(cls, name, description, styleURL, coordinates):
        xml = f'''    <Placemark>
    <name>{name}</name>
    <description>{description}</description>
    <styleUrl>#{styleURL}</styleUrl>
    <Point>
      <coordinates>{coordinates}</coordinates>
    </Point>
  </Placemark>
'''
        return xml

    @classmethod
    def create_marker_xml(cls, name, description, workouts):
        xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://earth.google.com/kml/2.2">
<Document>
  <name>{name}</name>
  <description>{description}</description>
'''

        for workout_type in workout_type_to_marker:
            xml += Marker.iconStyle(workout_type.replace(' ', '').replace(',', ''), workout_type, '../../', 0.75, 0, 0, 'pixels')

        for workout in workouts:
            marker = {
                'name': workout.workout_type + ' - ' + str(workout.time),
                'description': workout.workout_type,
                'styleURL': workout.workout_type.replace(' ', '').replace(',', ''),
                'coordinates': f'{workout.longitude}, {workout.latiude}'
            }
            xml += Marker.placemark(**marker)

        xml += '''</Document>
    </kml>'''

        return xml
