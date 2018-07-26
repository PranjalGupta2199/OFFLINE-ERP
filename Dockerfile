FROM dorowu/ubuntu-desktop-lxde-vnc
RUN apt update && apt upgrade -y
RUN apt install default-jre git python-pip python-gi python-gi-cairo gir1.2-gtk-3.0 -y
RUN git clone https://github.com/PranjalGupta2199/OFFLINE-ERP
RUN cd OFFLINE-ERP/ && pip install -r requirements.txt --ignore-installed --no-cache-dir
# docker run -v `pwd`:/root/time-table -p 6080:80 --rm kbharadwaj/offline-erp
