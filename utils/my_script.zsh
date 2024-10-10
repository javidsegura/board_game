rm -rf utils/requirements.txt
rm -rf utils/tree.txt

pip3 freeze > requirements.txt
cd ~
cd /Users/javierdominguezsegura/Programming/College/Sophomore/Algos/Final_project/dsa
tree > utils/tree.txt