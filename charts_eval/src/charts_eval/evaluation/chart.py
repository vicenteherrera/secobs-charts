
from copy import deepcopy

class Chart:
    repo = ""
    name = ""
    version = ""
    key=""
    status={}
    tools={}
    _dict={}

    def __init__(self, chart_dic: dict):
        self._dict   = deepcopy(chart_dic)
        self.repo    = chart_dic["repository"]["name"]
        self.url     = chart_dic["repository"]["url"]
        self.version = chart_dic["version"]

        self.name = self._get_chart_name( chart_dic["url"] )
        self.key = self.repo + "__" + self.name

        if "status" in chart_dic:
            self.status=chart_dic["status"]
        if "tools" in chart_dic:
            self.tools = chart_dic["tools"]

    def _get_chart_name(self, url: str) -> str:
        parts = url.split("/")
        user  = parts[ len(parts) - 1 ]
        return user
    
    def get_tools(self) -> list:
        if len( self.tools ) > 0:
            return self.tools
        return []

    def get_dict(self):
        dict = deepcopy(self._dict)
        dict["status"] = deepcopy(self.status)
        dict["tools"] = deepcopy(self.tools)
        return dict

    def is_error(self) -> bool:
        if "cache" in self.status:
            if self.status["cache"][0:5]=='error':
                return True
        return False

    def needs_update(self, charts_db: dict) -> bool:
        if self.key not in charts_db:
            return True
        if not "status" in charts_db[self.key] or \
           "chart_version" not in charts_db[self.key]["status"] or \
            not "chart_version" in charts_db[self.key]["status"]:
            # No status info
            return True
        if charts_db[self.key]["status"]["chart_version"] != self.version:
            # Old chart version in status
            return True
        return False

    def is_generated(self) -> bool:
        if not "cache" in self.status:
            return False
        if self.status["cache"] != "generated":
            return False
        return True

    def needs_evaluation(self, tool: str) -> bool:
        if not self.is_generated():
            print("  Chart not generated")
            return False
        if tool not in self.tools:
            print("  Chart doesn't have tool evaluation")
            return True
        if "template_filename" not in self.status:
            print("  **Error, template filename not in chart status %s" % self.status)
            exit(1)
        if tool not in self.tools:
            print("  Tool not evaluated before")
            return True
        if "chart_version" not in self.tools[tool]:
            print("  **Error, tool evaluation doesn't have chart version: %s" % self.tools)
            exit(1)
        if self.tools[tool]["chart_version"] != self.version:
            print("  Chart version %s for tool evaluation %s surpassed" % \
                (self.version, self.tools[tool]["chart_version"]))
            return True
        print("  Tool %s up to date" % tool)
        return False
