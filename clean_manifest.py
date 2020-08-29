import json

if __name__ == '__main__':

    manifest = {}

    with open('modules.manifest', 'r') as f:

        for i in f:
            entry = json.loads(i)

            code = entry['code']
            entry.pop('code')

            if code not in manifest:
                manifest[code] = entry

    with open('modules.csv', 'w') as f:
        
