# container内のproject top directoryで実行.

PROJECT_TOP=/data/OtterTemplate/;  # TODO: 要編集

echo "export PYTHONPATH=${PROJECT_TOP}src/" >> ~/.bashrc
source ~/.bashrc

apt -y update;
apt -y upgrade;
apt -y install git vim nano tmux build-essential cmake;

# ssh setting. (わからない人は使用禁止)
#apt -y install openssh-server;
#/etc/init.d/ssh restart

cd $PROJECT_TOP;
pip install pipenv
cp Pipfile.gpu Pipfile
pipenv install

# see: https://pytorch.org/get-started/locally/
pip install torch==1.7.1+cu110 -f https://download.pytorch.org/whl/torch_stable.html

cd $PROJECT_TOP/external_tools/easse_mod/
pip install .

# inside pipenv shell


