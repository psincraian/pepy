sudo pipx uninstall ansible-core
sudo pip3 install 'rich>=10.0.0,<11.0.0'
sudo pip3 install ansible-lint[community]==5.3.2
sudo pip3 install molecule[docker]==3.6.0


ansible --version
ansible-lint --version
molecule --version
