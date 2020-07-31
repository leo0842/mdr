# mdr

### 초반 setting 방법

원하는 폴더에서 하세요.
가상 환경 설정 후 폴더명 변경하면 안돌아갑니다.(후에 변경하기 좀 번거로움)

**Python은 3.8.5로 업그레이드(혹은 다운로드)하고 venv를 실행해야합니다.**
**venv는 python version을 선택할 수 없음**

- Python 3.8.5
- Django==2.2.13
- django-rest-framework==0.1.0
- djangorestframework==3.11.0

```
pip3 install virtualenv # virtual environment 설치
python3 -m venv mdr_env
source mdr_env/bin/activate # 앞으로 가상 환경안에서 코딩하게 될것임
git clone https://github.com/lcpnine/mdr.git
cd mdr
pip3 install -r requirements.txt
```

가상 환경 종료는 deactivate
