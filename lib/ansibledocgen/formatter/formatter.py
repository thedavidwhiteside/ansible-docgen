from jinja2 import Template
import os
import codecs
class Formatter(object):
    def __init__(self, style, parserdata, paths, project, params):
        
        self.parserdata = parserdata
        self.paths = paths
        self.project = project
        self.params = params
        self.render_files = { 'playbook': None, 'role': None, 'host': None }
        self.templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
        self.templates_files = {
                "playbook": "{}_playbook.j2".format(style),
                "role": "{}_role.j2".format(style),
                "host": "{}_host.j2".format(style)
            }
        
    def parse_data(self):
        self.__make_playbook_template__()
        self.__make_role_template__()
        self.__make_host_vars__()
    
    def write_files(self):
        for dic_name in self.render_files:
            file_dest = os.path.join(self.paths[dic_name][0], "README.md")
            render_file = self.render_files[dic_name]
            with codecs.open(file_dest, "w", encoding="utf-8") as f:
                f.write(render_file)
                
    def __make_playbook_template__(self):
        with open(os.path.join(self.templates_dir,self.templates_files['playbook'])) as file_:
            template = Template(file_.read())
        self.render_files['playbook'] = template.render(data=self.parserdata['playbooks'], params=self.params) 
    
    def __make_role_template__(self):
        with open(os.path.join(self.templates_dir,self.templates_files['role'])) as file_:
            template = Template(file_.read())
        self.render_files['role'] = template.render(data=self.parserdata['roles'], params=self.params) 
    
    def __make_host_vars__(self):
        with open(os.path.join(self.templates_dir,self.templates_files['host'])) as file_:
            template = Template(file_.read())
        self.render_files['host'] = template.render(data=self.parserdata['host_vars'], params=self.params) 

if __name__ == "__main__":
    import cPickle
    return_get_parserdata = cPickle.load( open('return_get_parserdata.pickle', 'rb'))
    f = Formatter(return_get_parserdata, '/home/lautaro/rmacfgm/', {'show_tags': True})
    #f.make_playbook_template()
    #f.make_role_template()
    #f.make_host_vars()