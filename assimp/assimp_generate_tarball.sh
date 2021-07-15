#!/bin/bash
RELEASE=5.0.1
git clone -b v${RELEASE} --depth=1 https://github.com/assimp/assimp.git assimp-${RELEASE}

cd assimp-${RELEASE}
git checkout -b free
find ./ -name "*.dll" -exec git rm -r {} \;
git rm -rf test/models-nonbsd
git commit -m "- Remove non free bits."
git archive --prefix=assimp-${RELEASE}/ free | xz > ../assimp-${RELEASE}-free.tar.xz
cd ..
