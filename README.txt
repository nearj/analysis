===================
MpEntropy v1.0 안내
===================

 해당 연구는 모션플랫폼 기반 VR 콘텐츠에서 발생하는 멀미를 객관적으로 평가하기 위한 정보 이론 기반의 객관적 척도인 MP 엔트로피를
설계하고, 모션 플랫폼의 움직임 신호를 제어하여MP Entropy 수치를 줄이기 위해 움직임 신호에 대해 Savitzky-Golay Filtering을 적용
하였다. 해당 프로그램은 이를 구현하였으며, 실제 상황에 적용이 용이하도록 Absolute Category Rating을 적용하여 사용자의 멀미에 대한
수치를 5 단계로 나누어서 표시하는 결과를 첨부하였다.


# 개발환경
OS: Windows 10 Pro 1903 / Ubuntu 16.04 / conda 4.7.12
PYTHON_VERSION: python 3.7.4


# 설치방법
1. 첨부파일 압축 해제
2. git clone https://github.com/nearj/mpvr-motionfiltering.git
3. $pip install -r requirements.txt


# Dependcies
pandas==0.24.2
numba==0.44.1
numpy==1.16.4
scipy==1.3.0
matplotlib==3.1.1
opencv_python==4.1.0.25
config==0.4.2


# 사용법
python3 main.py motion_file(csv) video_file(mp4) output_file_path(csv) [--mute_svg] [--mute_acr] [--mute_norm]

- motion_file: csv 형식의 모션플랫폼의 움직임 신호를 기록한 파일의 위치
- video_file: mp4 형식의 VR 콘텐츠의 영상의 위치
- output_file_path: 출력 값을 저장할 위치 (csv 형식)
- --mute_svg: 모션플랫폼의 신호에 대해 Savitzky-Golay를 적용을 안 하는 옵션
- --mute_acr: 출력 값의 형식이 5단계가 아닌 -100~100의 값을 가지도록 하는 옵션
- --mute_norm: 출력 값의 형식이 -100에서 100의 정규화된 값을 가지지 않고 원래의 MP Entropy 값을 나타내도록 하는 옵션


# 상세 설명
 해당 프로그램은 모션플랫폼 기반 VR 컨텐츠에서 MP Entropy를 계산하고, 모션플랫폼의 신호 데이터를 필터링하여 MP Entropy를
저감하기 위해 Savitzky-Golay Filtering을 이용하여 모션플랫폼 데이터를 신호처리하였다. main.py는 두 입력 파일인 motion_file과
video_file을 통해 MP Entropy를 계산한다. 이 때 default로 motion_file의 데이터에 대해 Savitzky-Golay Filtering을 적용한다.
MP Entropy는 -100에서 100의 수치를 나타내기 위해 정규화를 하며, 사용자의 경험을 5단계로 구분하기 위해 Absolute Category
Rating에 기반하여 5 단계로 나타낸다.
 Savitzky Golay Filtering이 적용되지 않은 결과를 확인하기 위해서는 --mute_svg 옵션을 적용하여 파일을 실행한다. 예를 들어
다음과 같다

python3 main.py motion_file(csv) video_file(mp4) output_file_path(csv) --mute_svg

 Absolute Category Rating이 적용되지 않은 결과를 확인하기 위해서는 --mute_acr 옵션을 적용하여 파일을 실행한다. 예를 들어
다음과 같다.

python3 main.py motion_file(csv) video_file(mp4) output_file_path(csv) --mute_acr

정규화되지 않은 결과를 확인하기 위해서는 --mute_norm 옵션을 적용하여 파일을 실행한다. 예를 들어 다음과 같다.

python3 main.py motion_file(csv) video_file(mp4) output_file_path(csv) --mute_norm

 Savitzky Golay Filtering이 적용되기 전후의 결과에 대한 예시를 나타내기 위해 [test]3D1_01.csv와 [test]3D1_01.mp4 파일을
입력파일로 [with_savitzky-golay_filtering]test_output.csv, [without_savitzky-golay_filtering]test_output.csv를
프로젝트 홈에 결과를 넣었다.
