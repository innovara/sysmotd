#!/bin/sh

# Downloads built RPMs from a COPR build, organises them into the local
# rpmbuild tree, and cleans up the temporary chroot directories.
#
# Usage: ./copr-download.sh <build_id>
#
# The script picks one x86_64 chroot per distro version (sufficient for
# noarch packages) and moves:
#   - noarch RPMs -> rpmbuild/RPMS/noarch/
#   - src    RPMs -> rpmbuild/SRPMS/
#
# Requires: copr-cli, curl, python3

set -e

if [ -z "$1" ]; then
    echo "Usage: $0 <build_id>" >&2
    exit 1
fi

BUILD_ID="$1"
DIR=$(pwd)

# Find succeeded chroots via the COPR API and pick one x86_64 per distro.
echo "Querying COPR API for build $BUILD_ID..."
CHROOTS=$(curl -s "https://copr.fedorainfracloud.org/api_3/build-chroot/list?build_id=${BUILD_ID}" | \
    python3 -c "
import json, sys
data = json.load(sys.stdin)
items = data.get('items', [])
seen = set()
for item in items:
    state = item.get('state', '')
    name  = item.get('name', '')
    if state == 'succeeded' and name.endswith('x86_64'):
        # strip architecture to use as distro key
        distro = name.rsplit('-', 1)[0]
        if distro not in seen:
            seen.add(distro)
            print(name)
")

if [ -z "$CHROOTS" ]; then
    echo "No succeeded x86_64 chroots found for build $BUILD_ID." >&2
    exit 1
fi

echo "Downloading from chroots:"
echo "$CHROOTS"

# Build -r arguments for copr-cli
CHROOT_ARGS=""
for chroot in $CHROOTS; do
    CHROOT_ARGS="$CHROOT_ARGS -r $chroot"
done

# Download into a temporary directory under rpmbuild/RPMS/
TMPDIR="${DIR}/rpmbuild/RPMS/_copr_tmp"
# shellcheck disable=SC2086
copr-cli download-build "$BUILD_ID" --rpms $CHROOT_ARGS --dest "$TMPDIR"

# Move noarch RPMs and SRPMs to the right places, then clean up.
find "$TMPDIR" -name "*.noarch.rpm" -exec mv {} "${DIR}/rpmbuild/RPMS/noarch/" \;
find "$TMPDIR" -name "*.src.rpm"    -exec mv {} "${DIR}/rpmbuild/SRPMS/" \;
rm -rf "$TMPDIR"

echo "Done."
