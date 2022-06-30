#!/usr/local/bin/zsh

TEXT_OPENING="
*** ASSUMPTIONS
*** - You are not using a root account
*** - sudo is an installed package
"

TEXT_CLOSING="
*** This install script only makes it easier for jailmin to be run.
*** DO NOT remove the jailmin Git folder.
*** Your config files should be placed in /usr/local/etc/jailmin/
"

RELEASE_LATEST='13.1-RELEASE'

echo $TEXT_OPENING

echo "- Create local bin/ if not exist"
[ -d ~/bin ] || mkdir ~/bin

echo "- Create /usr/local/etc/jailmin/ if not exist"
[ -d /usr/local/etc/jailmin ] || sudo mkdir /usr/local/etc/jailmin

echo "- Linking executing to local bin/"
rm ~/bin/jailmin
ln -s "$(pwd)/bin/jailmin.py" ~/bin/jailmin

echo "- Copying templates/ to /usr/local/etc/jailmin/"
sudo rm -rf /usr/local/etc/jailmin/templates
sudo cp -R templates /usr/local/etc/jailmin

echo "- Install external dependencies"
sudo pkg install -y bastille py38-pip

echo "- Install Python dependencies"
sudo rm -rf /usr/local/etc/jailmin/packages
sudo pip install -t /usr/local/etc/jailmin/packages -r requirements.txt 

printf '- Fetch latest RELEASE base files? y/N '
read YESNO
# read YESNO\?"Fetch latest RELEASE base files?"
#[[ $YESNO == 'y' ]] && sudo iocage fetch -r $RELEASE_LATEST

#echo -e "alias siocage='sudo iocage'" >> ~/.zshrc
#alias siocage='sudo iocage'

echo $TEXT_CLOSING