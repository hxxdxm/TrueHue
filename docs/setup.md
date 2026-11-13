# 설치 · 데이터 · 실행

[← README로 돌아가기](../README.md)

## 환경 설정 (WSL Ubuntu 기준)

**Python 3.14 기준.** `requirements.txt`의 버전(numpy 2.5, pandas 3.1, opencv 4.14 등)은 최신 파이썬에서만 설치된다.
`python3 --version`으로 먼저 확인할 것.

```bash
git clone https://github.com/simpson92/TrueHue.git
cd TrueHue
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 데이터 준비

### 1. Gehler-Shi (SFU 재처리판, 약 4.2GB) — 색 이름 채점 (메인)

```bash
mkdir -p data/gehler_shi && cd data/gehler_shi

# 받기 (aria2c가 있으면 더 빠름: aria2c -x 8 -s 8 -j 5 -c <주소들>)
wget -c \
  http://www.cs.sfu.ca/~colour/data2/shi_gehler/png_canon1d.zip \
  http://www.cs.sfu.ca/~colour/data2/shi_gehler/png_canon5d_1.zip \
  http://www.cs.sfu.ca/~colour/data2/shi_gehler/png_canon5d_2.zip \
  http://www.cs.sfu.ca/~colour/data2/shi_gehler/png_canon5d_3.zip \
  https://www2.cs.sfu.ca/~colour/data/shi_gehler/groundtruth_568.zip

# 압축 검사 → 풀기 → 맥 찌꺼기 삭제
for f in *.zip; do unzip -tq "$f"; done
for f in *.zip; do unzip -q "$f"; done
rm -rf __MACOSX

# PNG를 png/ 폴더 하나로 모으기
mkdir -p png
find . -name "*.png" -not -path "./png/*" -exec mv {} png/ \;
ls png | wc -l          # 568 확인
rm -rf cs *.zip
cd ../..
```

### 2. SimpleCube++ (약 2GB) — 조명 추정 정확도 평가 (보조)

원래 계획한 Cube+는 배포 링크가 만료되어, 같은 카메라·기준 물체로 만든 후속판으로 대체했다
(이유: [`reports/decisions.md`](../reports/decisions.md) D1).

```bash
mkdir -p data/simplecube && cd data/simplecube
wget -c "https://zenodo.org/record/4153431/files/SimpleCube++.zip"
unzip -tq SimpleCube++.zip && unzip -q SimpleCube++.zip
find SimpleCube++/train SimpleCube++/test -name "*.png" | wc -l    # 2234 확인
rm SimpleCube++.zip
cd ../..
```

## 웹 화면 · 자기 점검

```bash
pip install -r requirements.txt          # fastapi · uvicorn · python-multipart 포함
python app/engine.py                     # 자기 점검 ①: 웹 계산이 평가 계산과 같은지 (✅ 600 / 600, data/ 필요)
python app/check_web.py                  # 자기 점검 ② · ③: 가짜 카메라로 보정 · 흰 종이 기준 · 안전장치 (✅ 49개, data/ 없이)
uvicorn app.main:app --port 8000         # 레포 폴더에서 → 브라우저로 http://localhost:8000 (WSL이면 Windows 브라우저)
python app/fake_ipwebcam.py              # (폰 없이 ③ 시험) 가짜 IP Webcam → ③에 주소 127.0.0.1:8080. --light warm 으로 조명 고정
```

웹 화면 설명은 [web.md](web.md)

## 스크립트 실행 순서 (src/00 ~ 22)

| 스크립트 | 하는 일 | 결과 |
|---|---|---|
| `src/00_check_data.py` | Gehler-Shi · SimpleCube++ PNG 개수·dtype·값 범위 확인 | 568장 · 1,772장 · 462장, uint16 선형 이미지 |
| `src/01_inspect_gt.py` | 정답 `.mat` 파일 구조 확인 | 24칸 색 (568×24×3), 조명 정답 (568×3) |
| `src/02_build_index.py` | 사진별 정보를 한 표로 묶고 정답 조명 검산 | `outputs/gehler_index.csv` (568×78), 오차 0 |
| `src/03_inspect_nan.py` | 24칸 빈칸(NaN) 패턴·규칙 조사 | 채점 가능 12,428 / 13,632 |
| `src/04_reference_colors.py` | 컬러체커 24칸 공식 Lab 값, 대표색과 비교 | `reports/patch_reference.csv`, `outputs/patches_preview.png` |
| `src/05_check_simplecube.py` | SimpleCube++ 장수·정답 짝·라벨·블랙 레벨·포화 확인 | 2,234장, 블랙 레벨 2048, 포화 약 15,303 |
| `src/06_test_namer.py` | 색 이름 규칙(`src/namer.py`)이 표준 색 24개를 정답표대로 맞히는지 검증 | 24/24 정답, `outputs/namer_hue_chroma.png` |
| `src/07_make_splits.py` | 보정용 1/3 · 봉인 평가용 2/3 분할 (이미 있으면 덮어쓰지 않음) | `splits/*.txt`, 보정용 190장 / 평가용 378장 |
| `src/08_fit_color_matrix.py` | 보정용 사진으로 카메라별 3×3 색 변환 행렬 맞추기 | `reports/color_matrix.json`, ΔE 중앙값 5D 2.55 · 1D 5.03 |
| `src/09_pilot_chart_detect.py` | (시험) 컬러체커 자동 검출 방법 비교 — 정답 색으로 찾기 3차, 처음 보는 30장 중 29장 | `outputs/chart_pilot*/`, 결과는 decisions.md D8 |
| `src/10_check_camera_white.py` | (점검) 1D 채널 순서 · 흰색 빈칸 원인 · SFU 정답 조명 의심 사진 | 순서 맞음, 9/9장 포화, 의심 3장 (data_notes · D9) |
| `src/11_detect_charts.py` | 568장 컬러체커 자동 검출(09 3차 방식) → 가림 영역(상자 긴 변 25% 여유) · 30장씩 한눈에 보기 그림 | `outputs/charts/sheet_*.jpg`, `reports/chart_boxes.csv`(처음 한 번만 만듦) |
| `src/12_fix_charts.py` | (사람) `outputs/charts/to_fix.txt`에 적은 사진만 열어 마우스로 가림 영역 다시 지정 | `reports/chart_boxes.csv` 수정(source = manual), `sheet_fixed.jpg` |
| `src/13_check_suspect_matrix.py` | (점검) 의심 사진 8D5U5541을 빼고 1D 행렬을 다시 맞춰 ΔE 변화 확인 (D9, 처리 흐름은 안 바꿈) | 같은 28장 ΔE 중앙값 4.83 → 4.73, 평균 5.85 → 5.84 |
| `src/14_illum_simplecube.py` | Gray World · White Patch를 SimpleCube++ train 1,772장에 돌려 각도 오차 (test는 열지 않음) | `outputs/illum/simplecube_train.csv`, 중앙값 1.91° · 2.44° |
| `src/15_sog_simplecube.py` | Shades of Gray p = 1~12를 SimpleCube++ train에서 비교 → 중앙값 최소 p (D11) | `reports/illum_params.json`(simplecube), p = 3 · 1.45° |
| `src/16_illum_gehler.py` | Gehler 보정용 190장에서 가림 영역을 빼고 p = 1~12 비교 → 색 이름 채점에 쓸 p (D11) | `reports/illum_params.json`(gehler), p = 3 · 2.51° |
| `src/17_check_cct.py` | (점검) 조명 그룹용 색온도 계산 — 우리 행렬(D10 원안) vs Adobe DNG 카메라 행렬, 흑체 궤적 거리 \|Duv\|로 확인 | `reports/illum_params.json`(cct), 1D = EOS-1Ds · 5D = EOS 5D (D10 보완) |
| `src/18_estimate_gehler.py` | 기준선 조명(카메라별 평균) 저장 + 사진마다 보정 3종 조명 추정. 평가용은 `--final`로 최종 1회만 | `outputs/illum/gehler_est_calib.csv`, `illum_params.json`(baseline) |
| `src/19_score_calib.py` | 보정용 190장 색 이름 채점 연습 — 정답률 · 일관성 · 칸별 · 회색 칸 채도 · 주 결과 부트스트랩 | `outputs/scores/calib_patches.csv`, SoG − 기준선 +11.8%p |
| `src/20_final_simplecube.py` | SimpleCube++ 각도 오차 최종 평가 (보조 결과). `--rehearsal` = train, `--final` = test 1회 (D12) | 리허설 1.91 · 1.45 · 2.44 (= 14 · 15), **최종 2.21 · 1.68 · 2.60** → `reports/final/simplecube_test.md` |
| `src/21_final_gehler.py` | Gehler 색 이름 채점 최종 평가 (주 결과). 조명 추정 + 채점 + D10 보고 범위 · 95% 구간 · 의심 2장 제외 376장. `--rehearsal` = 보정용, `--final` = 평가용 1회 (D12) | 리허설 = 19, **최종 SoG 85.1% vs 기준선 72.2% (+12.9%p)** → `reports/final/gehler_test.md` |
| `src/22_check_hint.py` | 웹 "○○에 가까움" 표시 기준 — 보정용 SoG 결과에서 경계 여유별 틀린 비율 (D13) | `reports/web_params.json`, 채도 < 7 · 색상 < 3° · 밝기 < 3 |

`src/common.py`(경로·규칙 숫자·데이터 읽기, 사진은 RGB로)와 `src/pipeline.py`(조명 → 노출 → 행렬 → Lab → 이름)는
다른 스크립트가 불러다 쓰는 부품이라 직접 실행하지 않는다 (`python src/common.py`는 채널 순서 자기 점검).
`src/namer.py`(이름 규칙), `src/chart.py`(컬러체커 검출 · 가림 영역), `src/illuminant.py`(조명 추정: p=1 Gray World · p=∞ White Patch · 그 사이 Shades of Gray), `src/scoring.py`(채점 · 일관성 · 조명 그룹 · 부트스트랩, `python src/scoring.py`는 자기 점검), `src/hint.py`(웹 "가까운 이름" 표시, 이름 규칙은 안 바꿈)도 부품이다.
07~13 · 16~19는 02가 만든 `outputs/gehler_index.csv`가 필요하다. Gehler 사진으로 조명을 추정할 때는 `common.load_gehler_image`(포화 + 컬러체커 가림 영역 제외)로만 읽는다.
19는 17 · 18을 먼저 실행해야 한다 (조명 그룹 행렬 · 추정 조명).
20 · 21은 `--rehearsal` 또는 `--final`을 붙여야 돈다 (아무것도 없으면 사용법만 출력). `--final`은 커밋 안 된 변경이 있거나 이미 실행했으면 멈춘다 (D12).
12는 사람이 마우스로 고치는 단계라 `to_fix.txt`에 적은 사진이 없으면 아무것도 하지 않는다.

```bash
for f in src/[0-9]*.py; do echo "== $f"; python "$f"; done    # 번호가 붙은 스크립트만 순서대로
```


## 데이터 출처

- Lilong Shi and Brian Funt, "Re-processed Version of the Gehler Color Constancy Dataset of 568 Images,"
  http://www.cs.sfu.ca/~colour/data/
- Peter Gehler et al., "Bayesian Color Constancy Revisited," CVPR 2008
- G. Hemrit et al., "Rehabilitating the ColorChecker Dataset for Illuminant Estimation," CIC 2018 (arXiv 1805.12262)
- E. Ershov et al., "The Cube++ Illumination Estimation Dataset," IEEE Access 2020 —
  SimpleCube++, https://github.com/Visillect/CubePlusPlus (CC BY 4.0)
- ColorChecker 공식 값: colour-science 라이브러리 (`ColorChecker24 - Before November 2014`)
- 11색 대표색: xkcd Color Survey
