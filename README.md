# Plenoptic binder

Binder environment repository for plenoptic. Inspired by [this thread](https://discourse.jupyter.org/t/how-to-reduce-mybinder-org-repository-startup-time/4956), this repository is an "environment repository" which has all the various configuration required to define the environment Binder will build. The main [plenoptic repository](https://www.github.com/plenoptic-porg/plenoptic) is then used as the "content repository", pulled into the built environment on launch. This separation allows a more consistent built repository (so we rebuild less often) and also separates out the (distracting) configuration files from the main repository.

