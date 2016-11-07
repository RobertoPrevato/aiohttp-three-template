"""
 Copyright 2016, Roberto Prevato roberto.prevato@gmail.com

 This module contains functions to read configuration file for JavaScript resources, to generate <script> tags using
 dynamically.
 The configuration file is read both by Grunt/Gulp to generate built and minified javascript,
 and by the Python application, to generate <script> tags.
"""
import re
import json
from os import path, pardir
from core.literature.scribe import Scribe
from core.literature.text import Text

CONFIGURATION = None

def resources(names,
              conf=None,
              development=False,
              cache_seed=None):
    """
        Defines an helper function to generate links to scripts elements, by set names.
        1. it reads the file /configuration/scripts.js to generate the required script elements.
        2. if bundling is enabled, a single script element per set is generated, for bundled files.
        3. if also minification is enabled, a single script element per set is generated, for minified files.
        4. the same configuration file is read by Grunt.js to generate bundled and minified scripts upon publishing.
    """
    global CONFIGURATION

    if cache_seed is None:
        cache_seed = "0"

    if isinstance(names, str):
        names = [names]

    if conf is None:
        if CONFIGURATION is None or development:
            CONFIGURATION = load_resources_config()
        conf = CONFIGURATION

    bundling = conf["bundling"]
    minification = conf["minification"]
    sets = conf["sets"]

    a = []
    for name in names:
        if not name in sets:
            raise ValueError("The set `{}` is not configured inside /configuration/scripts.js".format(name))
        if minification:
            a.append("<script src=\"/scripts/{}{}?s={}\"></script>".format(name, ".min.js", cache_seed))
        elif bundling:
            a.append("<script src=\"/scripts/{}{}?s={}\"></script>".format(name, ".built.js", cache_seed))
        else:
            files = sets[name]
            for f in files:
                a.append("<script src=\"/{}?s={}\"></script>".format(f, cache_seed))

    return "\n".join(a)


comment_re = re.compile(
    r'(^)?[^\S\n]*/(?:\*(.*?)\*/[^\S\n]*|/[^\n]*)($)?',
    re.DOTALL | re.MULTILINE
)


def comment_replacer(match):
    start, mid, end = match.group(1,2,3)
    if mid is None:
        # single line comment
        return ""
    elif start is not None or end is not None:
        # multi line comment at start or end of a line
        return ""
    elif "\n" in mid:
        # multi line comment with line break
        return "\n"
    else:
        # multi line comment without line break
        return " "


def remove_comments(text):
    return comment_re.sub(comment_replacer, text)


def load_resources_config():
    """
    Loads the resources configuration.
    """
    try:
        base_path = path.abspath(path.join(path.dirname(__file__), pardir))
        scripts_config = path.join(base_path, "configuration", "scripts.js")
        contents = Scribe.read(scripts_config)
        # extract the information that we care about
        contents = remove_comments(contents).replace("module.exports = {", "{")
        contents = Text.remove_line_breaks(contents)
        contents = re.sub(";\s*$", "", contents)
        data = json.loads(contents)
        return data
    except Exception as ex:
        print("ERROR: while loading the scripts configuration for the resources helper.")
        print(str(ex))
        raise
