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

1. On GitHub, click **Use this template** → **Create a new repository**.
2. Within a minute, the **Template cleanup** workflow (Actions tab) renames everything
   called `template-container` after your repo — file names, the spec's name, and their
   contents — and commits it as `Rename template-container to <repo>`. Clone after that,
   or `git pull` if you already had:
   ```bash
   git clone --recurse-submodules git@github.com:gemini-rtsw/<name>.git
   ```
   The `gemini-rtsw-ci` submodule comes with the copy; there is nothing to add.
3. Grant the new repo **Write** access to `rpm-repo`: org **Packages** → `rpm-repo` →
   **Package settings** → **Manage Actions access** → add the repo, role **Write**.
   This can only be done once the repo exists, so the **Build** run GitHub starts on
   the first commit fails at the rpm-repo push, harmlessly. **Do not re-run it** after
   granting: it builds the template as it was before the rename, and would publish a
   second `template-container` RPM. Push a commit or open a PR instead.
4. Replace `Dockerfile` with your service.
5. Make the image package **public** on GitHub (or give root a GHCR login),
   because the unit runs `docker pull` as root.

The RPM may be named differently from the repo (`hrwfs` for `hrwfs_dm`, say): change
`Name:` in the spec, and rename the files named after it with it.

**If the cleanup did not run** (an org that keeps `GITHUB_TOKEN` read-only, say), rename
by hand before pushing to `main`: the spec file name and `Name:`, the two files in `deploy/` and the container name inside the unit, `.gitignore`, and **`%global appimage`, which must be `ghcr.io/gemini-rtsw/<repo name>` in lowercase** — CI pushes the image under the repo's name, so a mismatch builds green and fails on the host at `docker pull`. CI finds the spec by `*.spec`, so its file
name does not matter to the build, but `Name:` does — an unrenamed copy publishes a
second `template-container` RPM into the shared rpm-repo. Doing it in a PR is safe, since PR builds
publish nothing.

## Build locally

```bash
./gemini-rtsw-ci/build_rpm.sh --profile lightweight --el 9   # RPM -> rpms/ (first)
./gemini-rtsw-ci/build_app_image.sh --no-push                # then the image
```
