../pyinstaller/pyinstaller.py ../$1/main.py --onefile -n$1
../pyinstaller/pyinstaller.py ../$1/server_run.py --onefile -n$1Server
mkdir $1
cd $1
cp ../dist/$1 .
cp ../dist/$1Server .
cp ../../$1/databases . -r
cp ../../$1/fonts . -r
cp ../../$1/images . -r
cp ../../$1/server_db . -r
sudo chmod 777 $1
sudo chmod 777 $1Server