sudo apt-get update
sudo apt update

#copy files
sudo cp dash.service /etc/systemd/system
sudo cp dash.conf /etc/nginx/sites-available

#create symbolic link to enable the config
sudo ln -s /etc/nginx/sites-available/dash.conf /etc/nginx/sites-enabled/

sudo apt install python3-pip
pip3 install -r requirements.txt --no-cache-dir

sudo systemctl restart nginx
sudo systemctl daemon-reload




