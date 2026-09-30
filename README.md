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

1. Copy this repo, then rename `template-container` everywhere: the spec file name
   and `Name:`, `%global appimage` (must be `ghcr.io/gemini-rtsw/<repo name>`),
   and the two files in `deploy/`.
2. Replace `Dockerfile` with your service.
3. Add the submodule and grant the repo **Write** access to `rpm-repo`, as
   described in the gemini-rtsw-ci README ("Start a new repo").
4. Make the image package **public** on GitHub (or give root a GHCR login),
   because the unit runs `docker pull` as root.

## Build locally

```bash
./gemini-rtsw-ci/build_rpm.sh --profile lightweight --el 9   # RPM -> rpms/ (first)
./gemini-rtsw-ci/build_app_image.sh --no-push                # then the image
```
