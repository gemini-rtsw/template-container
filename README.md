# template-container

Minimal repo that **ships a container** through the
[gemini-rtsw-ci](https://github.com/gemini-rtsw/gemini-rtsw-ci) pipeline.
CI builds two things from one version:

- the image `ghcr.io/gemini-rtsw/template-container:<version>-git<hash>`, from `Dockerfile`
- an RPM with a systemd unit pinned to exactly that image, plus
  `/etc/sysconfig/template-container` for host settings

On a host, `dnf install template-container && systemctl start template-container`
pulls and runs the image. Nothing is built on the host.

## Use it for a new package

1. On GitHub, click **Use this template** → **Create a new repository**, then clone it
   with its submodule:
   ```bash
   git clone --recurse-submodules git@github.com:gemini-rtsw/<name>.git
   ```
   The `gemini-rtsw-ci` submodule comes with the copy; there is nothing to add.
2. Grant the new repo **Write** access to `rpm-repo`: org **Packages** → `rpm-repo` →
   **Package settings** → **Manage Actions access** → add the repo, role **Write**.
   This can only be done once the repo exists, so the build GitHub starts on the new
   repo's first commit fails here, harmlessly.
3. **Rename before you push to `main`**: `template-container` everywhere -- the spec
   file name and `Name:`, the two files in `deploy/` (and the container name inside the
   unit), and **`%global appimage`, which must be `ghcr.io/gemini-rtsw/<repo name>`**.
   CI pushes the image under the *repo's* name, not the spec's; with the template's
   `appimage` left in, the build is green but the unit pins an image that was never
   pushed, and it only fails on the host at `docker pull`. An unrenamed `Name:` also
   publishes a second `template-container` RPM into the shared rpm-repo. Doing the
   rename on a branch with a PR is safe, since PR builds publish nothing.
4. Replace `Dockerfile` with your service.
5. Make the image package **public** on GitHub (or give root a GHCR login),
   because the unit runs `docker pull` as root.

## Build locally

```bash
./gemini-rtsw-ci/build_rpm.sh --profile lightweight --el 9   # RPM -> rpms/ (first)
./gemini-rtsw-ci/build_app_image.sh --no-push                # then the image
```
