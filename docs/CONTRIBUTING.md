# Contributing

When contributing to this repository, please first discuss the change you wish to make via issue,
email, or any other method with the owners of this repository before making a change. 

Please note we have a code of conduct, please follow it in all your interactions with the project.

## Code of Conduct

### General Guidelines

1. Please follow Python standard guidelines given in PEP-8.
2. Ensure that you remove any output files (eg: .txt, .pickle or any binary files) while committing any changes or simply generate a report if you want to add them as a result in the repository.
2. Ensure any install or build dependencies are removed before the end of the layer when doing a 
   build.
3. Update the README.md with details of changes to the interface, this includes new environment 
   variables, exposed ports, useful file locations and container parameters.

### Pull Request Process

1. Fork this repository in your account.
2. Clone it on your local machine.
3. Add a new remote using `git remote add upstream https://github.com/PranjalGupta2199/OFFLINE-ERP.git`.
4. Create a new feature branch with `git checkout -b my-feature`.
5. Make your changes.
6. Commit your changes.
7. Rebase your commits with `upstream/master`:
  - `git checkout master`
  - `git fetch upstream master`
  - `git reset --hard FETCH_HEAD`
  - `git checkout my-feature`
  - `git rebase master`
8. Resolve any merge conflicts, and then push the branch with `git push origin my-feature`.
9. Create a Pull Request detailing the changes you made and wait for review/merge.

It might seem a little complicated at a glance, but the fundamental concept is simple: we
want to ensure that your changes are always made on top of the latest changes to the
project and thus, we can easily merge your code.

### Commit Message Guidelines

The commit message:

- is written in the imperative (e.g., "Fix ...", "Add ...")
- is kept short, while concisely explaining what the commit does.
- is clear about what part of the code is affected -- often by prefixing with the name of the subsystem and a colon, like "server: ..." or "docs: ...".
- is a complete sentence, ending with a period.

### Our Standards

Examples of behavior that contributes to creating a positive environment
include:

* Using welcoming and inclusive language
* Being respectful of differing viewpoints and experiences
* Gracefully accepting constructive criticism
* Focusing on what is best for the community
* Showing empathy towards other community members

Examples of unacceptable behavior by participants include:

* The use of sexualized language or imagery and unwelcome sexual attention or
advances
* Trolling, insulting/derogatory comments, and personal or political attacks
* Public or private harassment
* Publishing others' private information, such as a physical or electronic
  address, without explicit permission
* Other conduct which could reasonably be considered inappropriate in a
  professional setting

### Our Responsibilities

Project maintainers are responsible for clarifying the standards of acceptable
behavior and are expected to take appropriate and fair corrective action in
response to any instances of unacceptable behavior.

Project maintainers have the right and responsibility to remove, edit, or
reject comments, commits, code, wiki edits, issues, and other contributions
that are not aligned to this Code of Conduct, or to ban temporarily or
permanently any contributor for other behaviors that they deem inappropriate,
threatening, offensive, or harmful.

### Scope

This Code of Conduct applies both within project spaces and in public spaces
when an individual is representing the project or its community. Examples of
representing a project or community include using an official project e-mail
address, posting via an official social media account, or acting as an appointed
representative at an online or offline event. Representation of a project may be
further defined and clarified by project maintainers.

### Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be
reported by contacting the project team. All complaints will be reviewed and 
investigated and will result in a response that is deemed necessary and appropriate 
to the circumstances. The project team is obligated to maintain confidentiality 
with regard to the reporter of an incident. Further details of specific enforcement 
policies may be posted separately.

Project maintainers who do not follow or enforce the Code of Conduct in good
faith may face temporary or permanent repercussions as determined by other
members of the project's leadership.
