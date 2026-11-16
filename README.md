<p align="center">
  <img src="docs/images/banner.png" alt="TrueHue — 조명에 속지 않는 색 이름 감별기" width="820">
</p>

<p align="center">
  <b>조명 색을 먼저 추정해 지운 뒤 색 이름을 붙이는 감별기</b><br>
  <sub>KH정보교육원 <a href="https://github.com/simpson92/KH_Project_Subject9">교과 9 머신비전(규칙 기반 영상처리)</a> 10일 과정을 바탕으로 만든 미니 프로젝트 · 1조 심준형 · 김하민 · 2026.10.27 ~</sub>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/OpenCV-4.14-5C3EE8?logo=opencv&logoColor=white">
  <img src="https://img.shields.io/badge/NumPy-2.5-013243?logo=numpy&logoColor=white">
  <img src="https://img.shields.io/badge/colour--science-0.4.7-ff6f00">
  <img src="https://img.shields.io/badge/FastAPI-웹-009688?logo=fastapi&logoColor=white">
</p>

<p align="center">
  <a href="https://www.figma.com/design/hzU3DnxlzOEoPqqOxaFbez/TrueHue-%ED%8F%AC%ED%8A%B8%ED%8F%B4%EB%A6%AC%EC%98%A4?node-id=0-1">
    <img src="https://img.shields.io/badge/Figma-포트폴리오_보기-F24E1E?logo=figma&logoColor=white" alt="Figma 포트폴리오 보기">
  </a>
</p>

<table align="center">
  <tr>
    <td align="center" width="230"><h2>72.2% → 85.1%</h2>색 이름 정답률<br><sub>+12.9%p · 봉인 평가 378장</sub></td>
    <td align="center" width="230"><h2>49.3% → 81.2%</h2>따뜻한 조명에서<br><sub>+31.9%p · 효과가 가장 큰 곳</sub></td>
    <td align="center" width="230"><h2>1.68°</h2>조명 추정 오차<br><sub>SimpleCube++ 462장 중앙값</sub></td>
  </tr>
</table>

<p align="center">
  <img src="docs/images/demo_live.gif" alt="실시간 카메라 시연" width="820"><br>
  <sub>폰 카메라 실시간 — 푸르게 찍힌 흰 종이: 보정 전 <b>파랑</b> → 자동 보정 <b>회색</b> → 흰 종이 기준 <b>흰색</b> · 빨간 통 <b>진한 빨강</b></sub>
</p>

## 무엇을 했나

| 단계 | 한 일 | 자세히 |
|---|---|---|
| 🎯 **문제** | 찍힌 픽셀 색을 그대로 이름으로 바꾸면 조명이 바뀔 때 이름도 바뀐다. 색각이상 사용자는 틀려도 알 수 없다 | [방법과 검증](docs/evaluation.md#문제) |
| 🔬 **방법** | 학습 없이 **조명 추정**(Gray World · White Patch · Shades of Gray) → 조명 빼기 → **사람이 정한 11색 규칙** | [방법](docs/evaluation.md#방법) |
| 📊 **검증** | 공개 데이터셋을 보정용/평가용으로 나누고, 채점 규칙을 먼저 고정한 뒤 **평가용은 단 한 번만** 채점 | [결과 리포트](reports/final/gehler_test.md) |
| 🖥️ **시제품** | FastAPI 웹 — 데이터셋 재현 · 내 사진 · **폰 실시간 카메라**, 틀릴 수 있을 땐 "판단하기 어려워요" | [웹 설명](docs/web.md) |

<p align="center"><img src="docs/images/pipeline.png" alt="처리 흐름: 사진 → 조명 색 추정 → 조명 빼기 → 색 공간 변환 → 11색 이름 규칙" width="900"></p>

## 교과 9에서 이어진 것

> **출발점** — 교과 9 실습(2일차 흰 뚜껑 검사)에서 직접 적은 한계: *"카메라 화이트밸런스가 바뀌면 실패할 수 있다"* ([실습 기록](https://github.com/simpson92/KH_Project_Subject9/blob/main/reports/day02_preprocess_reason.md))<br>
> → 색으로 판단하는 규칙이 조명에 약하다는 이 한계를 정면으로 푼 것이 TrueHue

| 교과 9 | 배운 것 | TrueHue에서 쓴 곳 |
|---|---|---|
| 1일차 ROI · IP Webcam | 검사 영역 지정, 스마트폰 카메라 연결 | 클릭 지점 11×11 평균 · 흰 종이 네모 · 컬러체커 가림 영역 · 실시간 카메라 |
| 2일차 색 공간 · 감마 | BGR · HSV · Lab, 감마 | BGR → RGB 순서 점검 · sRGB 감마를 되돌려 선형으로 · CIELAB |
| 3일차 Feature → Rule (+ FastAPI 확장) | 사람이 기준을 설계해 판정 · IP Webcam + FastAPI 실시간 | 학습 없는 11색 이름 규칙 · 웹 ③ 실시간 모드 |
| 5일차 Calibration → Freeze → Test | 보정용으로 기준을 정해 고정, Test는 한 번 | 보정용 190장 / 평가용 378장 · 리허설 뒤 `--final` 1회 잠금 |
| 9일차 MLOps · Drift | 결과 덮어쓰지 않기, Test 보고 기준 안 바꾸기 | `reports/final/` 고치지 않음 · 결과에 커밋 해시 · 조명 바뀜 경고 |
| 10일차 FastAPI · JSON · Web | 검사 로직 → API → 웹, Dictionary ≠ JSON | FastAPI 웹 3모드 · JSON 응답 자기 점검 · 폰 · PC 브라우저 |

**교과 9 위에 새로 공부해 더한 것**: 조명 추정 3종(Gray World · White Patch · Shades of Gray) · 공개 데이터셋 2개로 자동 채점 · 카메라 색 변환 행렬 · 부트스트랩 오차 범위

## 결과

<p align="center"><img src="docs/images/result_by_light.png" alt="조명별 색 이름 정답률" width="760"></p>

| 방법 | 정답률 | 기준선 대비 |
|---|---|---|
| 기준선 (고정 보정) | 72.2% | — |
| Gray World | 79.9% | +7.7%p |
| White Patch | 66.6% | −5.5%p |
| **Shades of Gray (p=3)** | **85.1%** | **+12.9%p** [95% 구간 +10.7, +15.1] |
| 상한선 (정답 조명) | 95.4% | +23.3%p |

<sub>Gehler-Shi 평가용 378장 · 8,240칸, 최종 1회 (2026-10-30). 웹의 ② 내 사진 · ③ 실시간은 체험용이라 정답률을 따로 재지 않았다 · 한계: 실제 색각이상 사용자 시험 전, 약 일곱 번에 한 번 틀림 → [한계](docs/troubleshooting.md#아직-아닌-것-한계)</sub>

## 신경 쓴 점

| 포인트 | 내용 |
|---|---|
| 🔒 **숫자를 믿을 수 있게** | 평가용 사진은 끝까지 열지 않고, 채점 규칙을 미리 문서로 고정, 최종 실행은 코드 잠금으로 1회만 → [결정 기록](reports/decisions.md) |
| 👀 **사람이 직접 확인** | 컬러체커 568장을 눈으로 전수 검수 (자동 528 · 수정 40), 정답표 24칸도 근거를 적어 사람이 정함 |
| 🧪 **스스로 점검하는 코드** | 웹 계산 = 평가 계산 600/600 일치, 가짜 카메라로 49개 자동 점검 → [문제 해결 기록](docs/troubleshooting.md) |

## 폴더 구조

| 폴더 | 내용 |
|---|---|
| [`src/`](src) | 데이터 확인 → 분할 → 색 변환 → 조명 추정 → 채점 (00 ~ 22 순서) |
| [`app/`](app) | 웹 (FastAPI) — 계산 · 서버 · 화면 · 자기 점검 · 가짜 카메라 |
| [`reports/`](reports) | [결정 기록](reports/decisions.md) · [데이터 노트](reports/data_notes.md) · 정답표 · 설정값 |
| [`reports/final/`](reports/final) | 최종 1회 평가 결과 (봉인) |
| [`splits/`](splits) | 보정용 190장 / 평가용 378장 목록 |
| [`docs/`](docs) | README 그림 · 상세 문서 |
| `data/` · `outputs/` | 데이터셋 원본 · 실행 결과 (깃 제외) |

## 실행

```bash
pip install -r requirements.txt
uvicorn app.main:app --port 8000      # → http://localhost:8000
```

설치 · 데이터 받기 · 전체 실행 순서 → [docs/setup.md](docs/setup.md) · 개발 과정 → [docs/dev_log.md](docs/dev_log.md)

<sub>데이터: Gehler-Shi (Shi & Funt 재처리판) · SimpleCube++ (Ershov et al., CC BY 4.0) — 출처 전체는 [setup.md](docs/setup.md#데이터-출처)</sub>