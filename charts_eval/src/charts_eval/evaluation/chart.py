
from copy import copy

class Chart:
    repo = ""
    name = ""
    version = ""
    key=""
    status=[]
    tools={}
    _dict={}

    def __init__(self, chart_dic: dict):
        self._dict   = copy(chart_dic)
        self.repo    = chart_dic["repository"]["name"]
        self.url     = chart_dic["repository"]["url"]
        self.version = chart_dic["version"]

        self.name = self._get_chart_name( chart_dic["url"] )
        self.key = self.repo + "__" + self.name

        if "status" in chart_dic:
            self.status=chart_dic["status"]

    def _get_chart_name(self, url: str) -> str:
        parts = url.split("/")
        user  = parts[ len(parts) - 1 ]
        return user
    
    def get_tools(self) -> list:
        if len( self.tools ) > 0:
            return self.tools
        return []

    def get_dict(self):
        dict = copy(self._dict)
        dict["status"] = copy(self.status)
        dict["tools"] = copy(self.tools)
        return dict

    def is_chart_error(self) -> bool:
        if "generated" in self.status and self.status.generated[0:5]=='error':
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

    def needs_evaluation(self, tool: str) -> bool:
        if self.key not in self.tools:
            return True
        if not "cache" in self.status or \
            self.status["status"]["cache"] != "generated":
            print("  Chart templated not generated, status=%s" % self.status["cache"])
            return False
        if "chart_version" not in self.tool:
            print("  **Error, tool evaluation %s doesn't have chart version" % tool)
            return True
        if self.tool["chart_version"] != self.version:
            print("  Chart version for tool evaluation surpassed")
            return True
        print("  Tool %s up to date" % tool)
        return False
