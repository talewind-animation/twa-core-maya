name = "twacore_maya"
version = "0.1.2"

build_command = "python -m rezutil build {root}"
private_build_requires = ["rezutil-1",]

requires = [
        "maya-2014+",
        "mongoengine",
        "Qt.py"
    ]

def commands():
    global env

    env.PYTHONPATH.append("{root}/resources")
    env.MAYA_PLUG_IN_PATH.append("{root}/resources/plugins")
