#!/usr/bin/env bash
if [[ ${#} != 2 ]]; then
    echo "Usage: pull <contest id> <cur archive id>"
    exit -1
fi
BLOG_ID=$2
cf pull ac ${1}
for id in `ls ${1}`; do
    cp ${1}/${id}/${id}.cpp .
    (( BLOG_ID++ ))
    python3 gen.py $1 ${id} ${BLOG_ID}
    rm ${id}.cpp
done
rm -rf $1
