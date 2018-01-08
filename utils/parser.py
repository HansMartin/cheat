

class preparser:


    def __init__(self):
        self.meta = {"author":"",
                     "tags": [],
                     "ref":[]
                     }


    """ Some Mardown like syntax parsing. """
    def parse(self, ln):
        if self.getMeta(ln):
            return False

        if ln.startswith("# "):
            ln = "{at=bold}" + ln[2:-1] + "{end}"
        elif ln.startswith("## "):
            ln = "{at=bold}" + ln[3:-1] + "{end}"
        elif ln.startswith("### "):
            ln = "{at=bold}" + ln[4:-1] + "{end}"

        return ln

    def getMeta(self, ln):
        if ln.startswith("[author]: "):
           self.meta["author"] = ln[10:].strip()
        elif ln.startswith("[tags]: "):
            self.meta["tags"] = ln[8:].strip().split(",")
        elif ln.startswith("[ref]: "):
            self.meta["ref"].append(ln[7:].strip())
        else:
            return False
        return True
