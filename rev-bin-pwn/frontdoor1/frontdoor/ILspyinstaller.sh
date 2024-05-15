sudo apt update && sudo apt upgrade
sudo apt install mono-complete
sudo apt install git
git clone https://github.com/icsharpcode/ILSpy.git
cd ILSpy
sudo apt-get install msbuild
msbuild /t:Restore
msbuild /p:Configuration=Release
mono ILSpy.exe
