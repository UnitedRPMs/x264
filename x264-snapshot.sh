#!/bin/bash

set -e

tmp=$(mktemp -d)

trap cleanup EXIT
cleanup() {
    set +e
    [ -z "$tmp" -o ! -d "$tmp" ] || rm -rf "$tmp"
}

unset CDPATH
pwd=$(pwd)
date=$(date +%Y%m%d)
name=x264
package=x264
branch=master

pushd "$tmp"
git clone http://git.videolan.org/git/${package}.git 
cd ${package}
tag=$(git rev-list HEAD -n 1 | cut -c 1-7)
API=`grep '#define X264_BUILD' < x264.h | sed -e 's/.* \([1-9][0-9]*\).*/\1/'`

cd ${tmp}
tar Jcf "$pwd"/${name}-0.$API-${date}-${tag}.tar.xz ${package}

popd
upload_source=$( curl --upload-file ${name}-0.${API}-${date}-${tag}.tar.xz https://transfer.sh/${name}-0.${API}-${date}-${tag}.tar.xz )

if [ -n "$upload_source" ]; then
GCOM=$( sed -n '/Source0:/=' x264.spec)
sed -i "${GCOM}s#.*#Source0:	${upload_source}#" x264.spec
fi
