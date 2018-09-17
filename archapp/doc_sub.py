"""
doc_sub defines docstring substitution macros
"""
import re

def doc_sub_txt(txt, **shared):
    """ 
    Returns a copy of docstring txt with the substitutions in **shared.
    {meta}

    Parameters
    ----------
    txt : string
        docstring to make substitutions in

    {shared}

    Returns
    -------
    txt : string
        copy of input docstring with substitutions.
    """
    regex = re.compile("{.*}")
    lines = txt.split("\n")
    target_lines = {}
    for line in lines:
        match = regex.search(line)
        if match:
            key = match.group()[1:-1]
            if key in shared:
                target_lines[key] = line
    if not target_lines:
        return txt 
    indent_levels = {}
    for key, line in list(target_lines.items()):
        indent = 0 
        for c in line:
            if c == " ":
                indent += 1
            else:
                break
        indent_levels[key] = indent
    indented_text = {}
    for key, doc in list(shared.items()):
        if doc[0] == "\n":
            doc = doc[1:]
        if doc[-1] == "\n":
            doc = doc[:-1]
        indented = doc.replace("\n", "\n" + " " * indent_levels[key])
        indented_text[key] = indented
    return txt.format(**indented_text)

def doc_sub_func(func, **shared):
    """
    Edits func's docstring to the substitutions in **shared.
    {meta}

    Parameters
    ----------
    func : function
        function to make docstring changes to

    {shared}

    Returns
    -------
    func : function
        changed function, returned so we can use this as a decorator.
    """
    func.__doc__ = doc_sub_txt(func.__doc__, **shared)

def doc_sub_decorator(**shared):
    """
    Function decorator to apply doc_sub_func.
    {meta}

    Parameters
    ----------
    {shared}

    Returns
    -------
    adjustor : function
        decorator that applies doc_sub_func(func, **shared) for decorated
        function func.
    """
    def adjustor(func):
        doc_sub_func(func, **shared)
        return func
    return adjustor

doc_sub = doc_sub_decorator

# Documentation for documenation adjustors
meta_doc = \
"""
Expects docstring to be formatted like the docstrings in this module, with
triple quotes and spaced out like this docstring.

For every key, value pair in **shared:
Finds instances of
{{key}}
And puts the text block value in it's place, indented the correct amount.
The values should, in themselves, be docstrings.

Expects that every {{key}} will be used. Please use {{{{word}}}} when they are
not used. (Uses python string.format(**kwargs))
"""

# Documentation for the common **shared parameter
shared_rule = \
"""
**shared : dict
    substitutions to make in docstring
"""

# Hilariously, this works.
doc_sub_func(doc_sub_txt, meta=meta_doc, shared=shared_rule)
doc_sub_func(doc_sub_func, meta=meta_doc, shared=shared_rule)
doc_sub_func(doc_sub_decorator, meta=meta_doc, shared=shared_rule)
