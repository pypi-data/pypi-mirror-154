import os.path
__dir__ = os.path.split(os.path.abspath(os.path.realpath(__file__)))[0]
data_location = os.path.join(__dir__, "system_verilog")
src = "https://github.com/openhwgroup/cv32e40x"

# Module version
version_str = "0.4.0.post159"
version_tuple = (0, 4, 0, 159)
try:
    from packaging.version import Version as V
    pversion = V("0.4.0.post159")
except ImportError:
    pass

# Data version info
data_version_str = "0.4.0.post17"
data_version_tuple = (0, 4, 0, 17)
try:
    from packaging.version import Version as V
    pdata_version = V("0.4.0.post17")
except ImportError:
    pass
data_git_hash = "d5ed77f70b924886ebc280b35df24053d5d78cee"
data_git_describe = "0.4.0-17-gd5ed77f7"
data_git_msg = """\
commit d5ed77f70b924886ebc280b35df24053d5d78cee
Merge: c2cd76dd 4195cd70
Author: silabs-oysteink <66771756+silabs-oysteink@users.noreply.github.com>
Date:   Tue Jun 14 11:08:03 2022 +0200

    Merge pull request #582 from Silabs-ArjanB/ArjanB_mctrl6
    
    Typos, style

"""

# Tool version info
tool_version_str = "0.0.post142"
tool_version_tuple = (0, 0, 142)
try:
    from packaging.version import Version as V
    ptool_version = V("0.0.post142")
except ImportError:
    pass


def data_file(f):
    """Get absolute path for file inside pythondata_cpu_cv32e40x."""
    fn = os.path.join(data_location, f)
    fn = os.path.abspath(fn)
    if not os.path.exists(fn):
        raise IOError("File {f} doesn't exist in pythondata_cpu_cv32e40x".format(f))
    return fn
