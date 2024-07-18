# This script generates subroutes from the route files 'route_1_avddiem' and 'route_4_avddiem'
from copy import deepcopy
import os
from xml.etree import ElementTree as ET
from xml.dom import minidom

base_routes = ['route_1_avddiem.xml', 'route_4_avddiem.xml']
route_0_ignored_scenarios = {
    'ControlLoss_3',
    'ParkedObstacleTwoWays_2',
    'NonSignalizedJunctionRightTurn_1',
    'InvadingTurn_6',
    'DynamicObjectCrossing_3',
    'ParkedObstacleTwoWays_3',
    'HardBreakRoute_4',
    'InvadingTurn_7',
    'ControlLoss_4',
    'ParkedObstacleTwoWays_4',
    'BlockedIntersection_3',
    'HazardAtSideLaneTwoWays_7',
    'HazardAtSideLaneTwoWays_8',
    'ParkedObstacleTwoWays_5',
    'BlockedIntersection_4',
    'DynamicObjectCrossing_4',
    'HazardAtSideLaneTwoWays_9',
    'AccidentTwoWays_2',
    'ControlLoss_5',
    'ControlLoss_6',
    'HardBreakRoute_5',
    'InvadingTurn_8',
    'InvadingTurn_9',
    'ControlLoss_7',
    'ParkedObstacleTwoWays_6',
    'HazardAtSideLaneTwoWays_10',
    'ConstructionObstacleTwoWays_2',
    'ControlLoss_8',
    'ParkedObstacleTwoWays_7',
    'BlockedIntersection_5' 
}

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    xml_string = ET.tostring(elem, 'utf-8').decode('utf-8')   
    dom = minidom.parseString(xml_string)
    xml_pretty_string = dom.toprettyxml()
    # Remove empty lines from the xml string
    return '\n'.join([line for line in xml_pretty_string.split('\n') if line.strip()])

def get_scenarios_start_stop(route, ignored_scenarios={}):
    def extract_xyz(p):
        x = float(p.get('x'))
        y = float(p.get('y'))
        z = float(p.get('z'))
        return (x, y, z)
    def extract_scenario_trigger_point(x):
        trigger_point = x.find('trigger_point')
        return extract_xyz(trigger_point)
    res = {}
    scenarios = route.find('scenarios')
    scenario_list = list(scenarios.iter('scenario'))
    route_start_pos, *_, route_end_pos = route.find('waypoints').iter('position')
    scenario_triggers: list = list(map(extract_scenario_trigger_point, scenario_list))
    scenario_triggers.insert(0, extract_xyz(route_start_pos))
    scenario_triggers.append(extract_xyz(route_end_pos))
    for i, scenario in enumerate(scenario_list):
        scenario_name = scenario.get('name')
        if scenario_name in ignored_scenarios:
            continue
        res[scenario_name] = {"start": scenario_triggers[i],
                              "stop": scenario_triggers[i+2],
                              "scenario": scenario}
    return res

def make_day_time(tree):
    root = tree.getroot()
    route = root.find('route')
    weathers = route.find('weathers')
    for weather in weathers.iter('weather'):
        weather.set('sun_altitude_angle', '45.0')
    return tree

def generate_subroutes(route_name, ignored_scenarios={}, make_day=False):
    print("Parsing route: ", route_name)
    tree = ET.parse(route_name)
    route = tree.find('route')
    scenarios_start_stop = get_scenarios_start_stop(route, ignored_scenarios)
    empty_template = deepcopy(tree)
    empty_template.find('route').find('scenarios').clear()
    empty_template.find('route').find('waypoints').clear()
    if make_day:
        empty_template = make_day_time(empty_template)
    scenario_id = 0
    for scenario_name, scenario_data in scenarios_start_stop.items():
        print("\tGenerating subroute for scenario: ", scenario_name)
        subroute = deepcopy(empty_template)
        start_pos = ET.Element('position', x=str(scenario_data['start'][0]), y=str(scenario_data['start'][1]), z=str(scenario_data['start'][2]))
        end_pos = ET.Element('position', x=str(scenario_data['stop'][0]), y=str(scenario_data['stop'][1]), z=str(scenario_data['stop'][2]))
        subroute.find('route').find('scenarios').append(scenario_data['scenario'])
        subroute.find('route').find('waypoints').append(start_pos)
        subroute.find('route').find('waypoints').append(end_pos)
        subroute_name = f"{route_name.split('.')[0]}_scenario{scenario_id}.xml"
        xml_str = prettify(subroute.getroot())
        with open(subroute_name, 'w') as f:
            f.write(xml_str)
        scenario_id += 1

def main():
    global base_routes
    os.chdir('/workspace/team_code/routes')
    generate_subroutes(base_routes[0], route_0_ignored_scenarios, make_day=True)
    generate_subroutes(base_routes[1])

if __name__ == '__main__':
    main()