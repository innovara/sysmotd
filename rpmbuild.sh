#!/bin/sh

DIR=$(pwd)
APP=$(basename "${DIR}")
VERSION=$(awk '/^Version:/ {print $2;}' rpmbuild/SPECS/"${APP}".spec)
BUILD="${APP}"-$VERSION

tar cvfz rpmbuild/SOURCES/"${BUILD}".tar.gz --transform s/^"${APP}"/"${BUILD}"/ "${APP}"
rpmbuild --define "_topdir "${DIR}"/rpmbuild" -ba "${DIR}"/rpmbuild/SPECS/"${APP}".spec

