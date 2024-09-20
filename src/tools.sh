sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt install golang-go -y
current_user=$(whoami)
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
sudo cp /home/$current_user/go/bin/httpx /usr/bin
go install -v github.com/projectdiscovery/naabu/v2/cmd/naabu@latest
sudo cp /home/$current_user/go/bin/naabu /usr/bin
go install -v github.com/tomnomnom/assetfinder@latest
sudo cp /home/$current_user/go/bin/assetfinder /usr/bin
go install -v github.com/projectdiscovery/uncover/cmd/uncover@latest
sudo cp /home/$current_user/go/bin/uncover /usr/bin
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
sudo cp /home/$current_user/go/bin/subfinder /usr/bin
go install -v github.com/projectdiscovery/katana/cmd/katana@latest
sudo cp /home/$current_user/go/bin/katana /usr/bin
go install -v github.com/projectdiscovery/notify/cmd/notify@latest
sudo cp /home/$current_user/go/bin/notify /usr/bin
go install -v github.com/MrEmpy/mantra@latest
sudo cp /home/$current_user/go/bin/mantra /usr/bin
go install -v github.com/Emoe/kxss@latest
sudo cp /home/$current_user/go/bin/kxss /usr/bin
git clone https://github.com/s0md3v/Arjun.git
python3 Arjun/setup.py install
go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
sudo cp /home/$current_user/go/bin/nuclei /usr/bin
# nuclei templates
go install github.com/tomnomnom/waybackurls@latest
sudo cp /home/$current_user/go/bin/waybackurls /usr/bin
go install -v github.com/lc/gau/v2/cmd/gau@latest
sudo cp /home/$current_user/go/bin/gau /usr/bin
cd  && git clone # gau config file
git clone https://github.com/devanshbatham/paramspider
cd paramspider
pip install .
sudo cp /home/$current_user/.local/bin/paramspider /usr/bin
git clone https://github.com/ffuf/ffuf ; cd ffuf ; go get ; go build
sudo apt install amass-common -y
sudo apt install nmap -y
sudo apt install nikto -y
sudo apt install beef-xss -y
sudo apt install wireshark -y
sudo apt install snort -y
sudo apt install hashcat -y
sudo apt install john -y
sudo apt install sqlmap -y
sudo apt install spiderfoot -y
sudo apt install wifite -y
sudo apt install dirb -y
sudo apt install gobuster -y
sudo apt install maltego -y
sudo apt install wafw00f -y
sudo apt install sublist3r -y
sudo apt install python3-scapy -y
sudo apt install whatweb -y
sudo apt install recon-ng -y
sudo apt install subfinder -y
sudo apt install libyara-dev -y
sudo apt install yara -y
sudo apt install tcpdump -y