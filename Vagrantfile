Vagrant.configure("2") do |config|
  config.vm.box = "hashicorp/bionic64"
  config.vm.network "forwarded_port", guest: 5000, host: 5000
  
  config.vm.provision "shell", privileged: false, inline: <<-SHELL
    sudo apt-get update
    sudo apt-get install -y build-essential libssl-dev zlib1g-dev libbz2-dev \
    libedit-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
    xz-utils tk-dev libffi-dev liblzma-dev python-openssl git pip3 python3-distutils
  
    git clone https://github.com/pyenv/pyenv.git ~/.pyenv
    echo 'PYENV_ROOT="$HOME/.pyenv"' >> ~/.profile
    echo 'PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.profile
    echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.profile
    source ~/.profile
    pyenv install 3.8.5
    sudo python-build 3.8.5 /usr/local/
    pyenv global 3.8.5
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
  
  SHELL

  config.trigger.after :up do |trigger|
    trigger.name = "Launching App"
    trigger.info = "Running the TODO app setup script"
    trigger.run_remote = {privileged: false, inline: "
    cd /vagrant
    poetry install
    nohup poetry run flask run --host=0.0.0.0 > logs.txt 2>&1 &
    "}
    end
end