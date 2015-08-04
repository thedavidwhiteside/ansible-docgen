""" Markup Formatter Module """
import re
import os


class FormatterMarkup(object):
    """ Format Annotations as Markup Documentation """

    def __init__(self, parserdata, project):
        """ @parserdata is an array of dictionaries
            @project is the path to the project
        """
        self.parserdata = parserdata
        self.project = project
        self.supported_attributes = ["author", "description", "task_names"]
        """ Example parserdata:
        [ { "author": "test",
        "description": "test2",
        "task_names": ["str1", "str2"],
        "rolename" : None,
        "relative_path" : "./myplaybook.yml"}, ] """
        self.role_outfiles = {}
        self.playbook_outfiles = {}

    def parse_data(self):
        """ Write Each Individual Markup File """
        for sourcefile in self.parserdata:
            self.write_doc(sourcefile)

    def write_doc(self, sourcefile):
        """ @sourcefile is a dictionary, example:
              { "author": "", "description": "", "task_names": "", .....}
        """
        # Detect Attributes
        attributes = []
        for attribute in self.supported_attributes:
            if attribute in sourcefile:
                attributes.append(attributes)
        # Skip Playbooks With No Annotation or Tasks
        if len(attributes) <= 0:
            return

        # Parse a Role
        if sourcefile["rolename"] is not None:
            m = re.match("^(.*?)%s/tasks" %
                         sourcefile["rolename"], sourcefile["relative_path"])
            if m:
                roledir = m.group(1)
                if roledir not in self.role_outfiles:
                    self.role_outfiles[roledir] = []
                self.role_outfiles[roledir].append(
                    "## Role: [%s](%s)\n" % (sourcefile["rolename"], sourcefile["rolename"]))
                self.write_attribute(sourcefile, roledir, "author", is_role=True)
                self.write_attribute(sourcefile, roledir, "description", is_role=True)
                if "task_names" in sourcefile:
                    for task_name in sourcefile["task_names"]:
                        self.role_outfiles[roledir].append(
                            "> Task: %s\n\n" % task_name)
            self.role_outfiles[roledir].append("\n")
        # Parse a Playbook
        else:
            playbookpath = self.project
            if playbookpath not in self.playbook_outfiles:
                self.playbook_outfiles[playbookpath] = []
            self.playbook_outfiles[playbookpath].append(
                "## Playbook: [%s](%s)\n" % (sourcefile["relative_path"].replace(playbookpath, ""),
                    sourcefile["relative_path"].replace(playbookpath, "")))
            self.write_attribute(sourcefile, playbookpath, "author")
            self.write_attribute(sourcefile, playbookpath, "description")
            if "task_names" in sourcefile:
                for task_name in sourcefile["task_names"]:
                    self.playbook_outfiles[playbookpath].append(
                        "> **Task:** %s\n\n" % task_name)
            self.playbook_outfiles[playbookpath].append("\n")

    def write_attribute(self, sourcefile, path, attribute, is_role=False):
        """ Write a comment attribute to sourcefile """
        if attribute in sourcefile:
            if sourcefile[attribute] is not None and sourcefile[attribute] is not "":
                # Make First Letter Capital and end with an :
                pretty_attribute = attribute.capitalize()

                # Add to Output File
                if is_role:
                    self.role_outfiles[path].append(
                        "> **%s:** %s\n\n" % (pretty_attribute, sourcefile[attribute]))
                else:
                    self.playbook_outfiles[path].append(
                        "> **%s:** %s\n\n" % (pretty_attribute, sourcefile[attribute]))

    def write_files(self):
        """ Write Formatted Markup Files """
        # Write Role Markup Files
        for rolepath in self.role_outfiles:
            # Make sure there is a trailing /
            playbookpath = os.path.join(rolepath, "")
            # Open Output File
            filename = os.path.join(rolepath, "README.md")
            with open(filename, "w") as p:
                for line in self.role_outfiles[rolepath]:
                    p.write("%s" % line)
                p.write("\n")
                p.write("Generated by [ansible-docgen](https://www.github.com/starboarder2001/ansible-docgen)")
                p.write("\n")
            print("Generated Markup File %s" % filename)

        # Write Playbook Markup Files
        for playbookpath in self.playbook_outfiles:
            # Make sure there is a trailing /
            playbookpath = os.path.join(playbookpath, "")
            # Open Output File
            filename = os.path.join(playbookpath, "README.md")
            with open(filename, "w") as p:
                for line in self.playbook_outfiles[playbookpath]:
                    p.write("%s" % line)
                p.write("\n")
                p.write("Generated by [ansible-docgen](https://www.github.com/starboarder2001/ansible-docgen)")
                p.write("\n")
            print("Generated Markup File %s" % filename)
