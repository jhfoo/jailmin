echo - Create local bin/ if not exist
[ -d ~/bin ] || mkdir ~/bin

echo - Linking executing to local bin/
rm ~/bin/jailmin
ln -s "$(pwd)/bin/jailmin.py" ~/bin/jailmin

echo - Install required packages
sudo pkg install -y py38-iocage py38-yaml

echo - Fetch latest RELEASE base files
sudo iocage fetch -r LATEST
#echo -e "alias siocage='sudo iocage'" >> ~/.zshrc
#alias siocage='sudo iocage'
