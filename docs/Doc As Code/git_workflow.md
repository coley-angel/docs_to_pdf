### forking workflow
The Forking Workflow is fundamentally different from other popular Git workflows. Instead of using a single server-side repository to act as the “central” codebase, it gives every developer their own server-side repository.

This means that each contributor has not one, but two Git repositories: a private local one and a public server-side one. The Forking Workflow is most often seen in public open-source projects.

![docascode]({{img_dir}}docascode.png "doc as code")

The main advantage of the Forking Workflow is that contributions can be integrated without the need for everybody to push to a single central repository. Developers push to their own server-side repositories, and only the project maintainer can push to the official repository. This allows the maintainer to accept commits from any developer without giving them write access to the official codebase.

#### The following is a step-by-step example of this workflow.

 1. A developer ‘forks’ an ‘official’ server-side repository. This creates their own server-side copy.
 1. The new server-side copy is cloned to their local system.
 1. A Git remote path for the ‘official’ repository is added to the local clone.
 1. A new local feature branch is created.
 1. The developer makes changes on the new branch.
 1. New commits are created for the changes.
 1. The branch gets pushed to the developer’s own server-side copy.
 1. The developer opens a pull request from the new branch to the ‘official’ repository.
 1. The pull request gets approved for merge and is merged into the original server-side repository.