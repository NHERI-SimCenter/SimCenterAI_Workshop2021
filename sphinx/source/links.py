# Claudio Perez
import urllib.parse
NL = '\n'

# Github
gh_templ = "https://github.com/{gh_user}/{gh_repo}/tree/{branch}/{path}"
gh_badge = "https://img.shields.io/github/forks/{gh_user}/{gh_repo}?label=Github&style=social"
# Binder
binder_badge = "https://mybinder.org/badge_logo.svg"
binder_templ = "https://mybinder.org/v2/gh/{gh_user}/{gh_repo}/HEAD?filepath={path}"
# Colab
colab_badge = "https://colab.research.google.com/assets/colab-badge.svg"
colab_templ = "https://colab.research.google.com/github/{gh_user}/{gh_repo}/blob/{branch}/{path}"

def link_colab(path, gh_user, gh_repo, branch="master")->str:
    return colab_templ.format(
            gh_user=gh_user,gh_repo=gh_repo,branch=branch,path=urllib.parse.quote(path))

def link_binder(path, gh_user, gh_repo, branch="master")->str:
    return binder_templ.format(
            gh_user=gh_user,gh_repo=gh_repo,path=urllib.parse.quote(path))

def link_github(path, gh_user, gh_repo, branch="master")->str:
    lnk = gh_templ.format(gh_user=gh_user,gh_repo=gh_repo,branch=branch,path=urllib.parse.quote(path))
    img = gh_badge.format(gh_user=gh_user,gh_repo=gh_repo,branch=branch,path=urllib.parse.quote(path))
    return f"""<a href="{lnk}"><img src="{img}" alt="Open in Github"/></a>"""


HEADER = """
**********
Notebooks
**********

The following sets of links can be used to access the exercise files by various means.

The first link will open the exercise file on Github. From here, the user can download the files and run on their locally installed Jupyter server, or just view the rendered notebooks along with their source code and results.

The second link will open the notebook on Googles Colab platform. Users with a Google accound can use this service to freely run the exercises directly from their browsers with no installation whatsoever. Code will be executed on Google's servers.

The final link opens the notebook in Binder. This service is similar to Colab in that it allows users to freely execute notebooks from their browsers. However, this service requires absolutely no account registration. This option also provides a more familiar exerpience for working with notebooks than that of Colab as the user interface is nearly identical to a local Jupyter server.

To learn more about these tools, visit the :ref:`Tools` page.

"""

DAY = """
Day {i}: {title}
=======================

.. 
    * Content:
    {content}

{exercises}

"""

def make_content(c):
    if not isinstance(c,dict):
        return f"    * {c}\n"
    else:
        title, link = list(c.items())[0]
    return f"""
    *  .. raw:: html

            {title} <p><iframe width="560" height="315" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen src="{link}" ></iframe></p>
"""

def make_exercise(title, notebook="", colab="", **gh_data):
    colab_link = colab if colab else link_colab(notebook,**gh_data) if notebook else ""
    binder_link = link_binder(notebook,**gh_data) if notebook else ""
    colab = f"""<li><a href="{colab_link}"><img src="{colab_badge}" alt="Open in Colab"/></a></li>""" if colab_link else ""
    binder = f"""<li><a href="{binder_link}"><img src="{binder_badge}" alt="Open in Binder"/></a></li>""" if binder_link else ""
    return f"""
* {title}

  .. raw:: html

     <ul><li>{link_github(notebook,**gh_data)}</li>{colab}{binder}</ul>

"""

if __name__ == "__main__":
    import sys
    import yaml
    if len(sys.argv) < 2:
        print("usage: python <script> links.yml > notebooks.rst")
        exit()
    with open(sys.argv[1], "r") as f:
        data = yaml.load(f, Loader=yaml.Loader)


    print(HEADER)
    for i,day in enumerate(data["days"]):
        day_data = dict(
            exercises = "\n".join(make_exercise(**e,**data["github"]) for e in day["exercises"]),
            content = "\n".join(make_content(c) for c in day["content"]),
        )
        print(DAY.format(i=i+1,title=day["title"],**day_data))


