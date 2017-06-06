"""
epics.py defines EPICS constants
"""
sevr_enum = ("NO_ALARM", "MINOR", "MAJOR", "INVALID")
def get_sevr_enum(n):
    try:
        return sevr_enum[n]
    except:
        return ""

stat_enum = ("NO_ALARM", "READ", "WRITE", "HIHI", "HIGH", "LOLO", "LOW",
             "STATE", "COS", "COMM", "TIMEOUT", "HWLIMIT", "CALC", "SCAN",
             "LINK", "SOFT", "BAD_SUB", "UDF", "DISABLE", "SIMM",
             "READ_ACCESS", "WRITE_ACCESS")
def get_stat_enum(n):
    try:
        return stat_enum[n]
    except:
        return ""
