#!/bin/bash

TEMPLATE=<<EOF > tmp.eu
x: foo
EOF

cat <<EOF | eu - tmp.eu
{ "foo": "bar" }
EOF
