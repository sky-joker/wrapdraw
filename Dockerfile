FROM centos:8
ADD /etc/google-chrome.repo /etc/yum.repos.d/google-chrome.repo
RUN dnf -y install python3 google-chrome-stable
RUN pip3 install selenium \
                 werkzeug \
                 flask \
                 pyyaml \
                 chromedriver-binary==85.0.4183.87

RUN mkdir -p /app/{upload,save}
ADD src/app/app.py /app

WORKDIR /app
CMD python3 app.py
