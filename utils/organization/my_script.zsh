rm -rf utils/organization/requirements.txt
rm -rf utils/organization/tree.txt


cd ../..

pip3 freeze > utils/organization/requirements.txt


tree > utils/organization/tree.txt