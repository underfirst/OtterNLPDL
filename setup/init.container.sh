# container内のproject top directoryで実行.

PROJECT_TOP=/data/OtterTemplate/;  # TODO: 要編集
echo "export PYTHONPATH=${PROJECT_TOP}src/" >> ~/.bashrc
source ~/.bashrc

apt -y update;
apt -y upgrade;
apt -y install git vim nano tmux build-essential cmake;

# ssh setting.
#apt -y install openssh-server;
#/etc/init.d/ssh restart

pip install pipenv
pip install torch==1.7.1+cu110 -f https://download.pytorch.org/whl/torch_stable.html
cp Pipfile.gpu Pipfile
pipenv install
# inside pipenv shell
