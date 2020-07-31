# mdr

### 초반 setting 방법

원하는 폴더에서 하세요.
가상 환경 설정 후 폴더명 변경하면 안돌아갑니다.

```
pip3 install virtualenv # virtual environment 설치
python3 -m venv mdr_env
source mdr_env/bin/activate # 앞으로 가상 환경안에서 코딩하게 될것임
git clone https://github.com/lcpnine/mdr.git
cd mdr
pip3 install -r requirements.txt
```

가상 환경 종료는 deactivate
