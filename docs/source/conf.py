# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import shutil
from recommonmark.parser import CommonMarkParser

# -- Project information -----------------------------------------------------

# General information about the project.
project = 'eo-learn'
copyright = '2018, eo-learn'
author = 'Sinergise EO research team'
doc_title = 'eo-learn Documentation'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The release is read from __init__ file and version is shortened release string.
for line in open(os.path.join(os.path.dirname(__file__), '../../core/eolearn/core/__init__.py')):
    if line.find("__version__") >= 0:
        release = line.split("=")[1].strip()
        release = release.strip('"').strip("'")
version = release.rsplit('.', 1)[0]

# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.inheritance_diagram',
    'sphinx.ext.autosummary',
    'nbsphinx',
    'IPython.sphinxext.ipython_console_highlighting',
    'm2r'
]

# Both the class’ and the __init__ method’s docstring are concatenated and inserted.
autoclass_content = 'both'

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path .
exclude_patterns = []

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True

# Mock modules
# autodoc_mock_imports = ["eolearn"]

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
# html_theme_options = {}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
#
# html_sidebars = {}


# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'eo-learndoc'
# show/hide links for source
html_show_sourcelink = False

# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'eo-learn.tex', doc_title,
     author, 'manual'),
]


# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'eo-learn', doc_title,
     [author], 1)
]


# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'eo-learn', doc_title,
     author, 'eo-learn', 'One line description of project.',
     'Miscellaneous'),
]


# -- Options for Epub output ----------------------------------------------

# Bibliographic Dublin Core info.
epub_title = project
epub_author = author
epub_publisher = author
epub_copyright = copyright

# The unique identifier of the text. This can be a ISBN number
# or the project homepage.
#
# epub_identifier = ''

# A unique identification for the text.
#
# epub_uid = ''

# A list of files that should not be packed into the epub file.
epub_exclude_files = ['search.html']

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {'https://docs.python.org/3.6/': None}

# copy examples
shutil.rmtree('./examples', ignore_errors=True)

try:
    shutil.copytree('../../examples', './examples')
except FileExistsError:
    pass

# Create a list of all EOTasks

def get_subclasses(cls):
    direct_subclasses = cls.__subclasses__()
    nested_subclasses = [ s for c in direct_subclasses
                          for s in get_subclasses(c) ]

    return list(set(direct_subclasses).union(nested_subclasses))


def get_eotasks():
    import eolearn.core
    import eolearn.coregistration
    import eolearn.features
    import eolearn.geometry
    import eolearn.io
    import eolearn.mask
    import eolearn.ml_tools

    return get_subclasses(eolearn.core.EOTask)

with open('eotasks.rst', 'w') as f:
    f.write('********\n')
    f.write('EO Tasks\n')
    f.write('********\n')
    f.write('\n')

    eopackage_tasks = {}

    for eotask_cls in get_eotasks():
        eopackage = eotask_cls.__module__.split('.')[1]
        eotask = eotask_cls.__module__ + '.' + eotask_cls.__name__

        if eopackage not in eopackage_tasks:
            eopackage_tasks[eopackage] = []

        eopackage_tasks[eopackage].append(eotask)

    for eopackage in sorted(eopackage_tasks.keys()):
        f.write(eopackage + '\n')
        f.write('-' * len(eopackage) + '\n')
        f.write('\n')

        f.write('.. currentmodule:: eolearn.' + eopackage + '\n')
        f.write('.. autosummary::\n')
        f.write('\t:nosignatures:\n')
        f.write('\n')

        eotasks = eopackage_tasks[eopackage]
        eotasks.sort()

        for eotask in eotasks:
            # tilde is used to show only the class name without the module
            f.write('\t~' + eotask + '\n')

        f.write('\n')

