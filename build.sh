rm -rf flat
rm ML.app
mkdir flat
cp -r main.py src/*.py src/*/*.py src/*/*/*.py src/*/*/*/*.py src/*/*/*/*/*.py src/*/*/*/*/*/*.py data main.spec flat/
cd flat
pyinstaller main.spec
mv dist/main.app ../ML.app
cd ..
rm -rf flat