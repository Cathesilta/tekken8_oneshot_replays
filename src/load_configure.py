import yaml




class load_configure(object):
    
    def __init__(self, config_path):
        
        with open(config_path, 'r') as file:
            self.yml_data = yaml.safe_load(file)