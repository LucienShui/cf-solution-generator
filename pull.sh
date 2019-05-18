#!/usr/bin/env bash
if [[ ${#} != 2 ]]; then
    echo "Usage: pull <contest id> <cur archive id>"
    exit -1
fi
BLOG_ID=$2
cf pull ac ${1}
cd ${1}
for id in `ls`; do
    cp ${id}/${id}.cpp .
    (( BLOG_ID++ ))
    python3 ../gen.py $1 ${id} ${BLOG_ID}
    rm -rf ${id}.cpp ${id}
done
