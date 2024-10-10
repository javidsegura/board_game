rm -rf utils/requirements.txt
rm -rf utils/tree.txt

pip3 freeze > requirements.txt
cd dsa/
tree > utils/tree.txt