# docs/make_figures.py
# 목적: README에 넣는 결과 그래프를 최종 평가 리포트(reports/final/gehler_test.md)의 숫자로 그린다
#   - 숫자를 손으로 옮겨 적지 않고 리포트 표에서 직접 읽는다 → README 그림과 평가 결과가 어긋날 수 없음
#   - 평가를 다시 돌리지 않는다 (reports/final/은 읽기만)
# 실행 (레포 폴더에서):  python docs/make_figures.py   → docs/images/result_by_light.png
import re
from pathlib import Path
import matplotlib
matplotlib.use("Agg")                                   # 창 없이 파일로만 저장
import matplotlib.pyplot as plt
from matplotlib import font_manager

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports" / "final" / "gehler_test.md"
OUT = ROOT / "docs" / "images" / "result_by_light.png"

# 그릴 열(리포트 표의 열 이름)과 그래프에 쓸 짧은 이름
COLS = [("전체 24칸", "전체\n378장"), ("따뜻한 조명 <4000K", "따뜻한 조명\n95장"),
        ("주광 4000~6500K", "주광\n274장"), ("푸른 조명 >6500K", "푸른 조명\n9장")]
ROWS = [("기준선(고정)", "기준선 (고정 보정)", "#eb6834"), ("SoG(p=3)", "Shades of Gray (p=3)", "#2a78d6")]


def read_table(title):
    """title로 시작하는 절의 첫 표에서 방법별 · 열별 숫자(앞의 숫자만, %나 %p)를 읽는다"""
    text = REPORT.read_text(encoding="utf-8")
    sec = text.split("## " + title, 1)[1]                # 그 절부터
    lines = []
    for l in sec.splitlines():                           # 첫 표만: 표 줄이 끝나면 멈춤
        if l.startswith("|"):
            lines.append(l)
        elif lines:
            break
    header = [c.strip() for c in lines[0].strip("|").split("|")]
    table = {}
    for l in lines[2:]:                                  # 0 = 머리줄, 1 = |---|
        cells = [c.strip() for c in l.strip("|").split("|")]
        if cells[0] == "문제 수":                         # 정답률 표 마지막 줄 (숫자가 아님)
            break
        table[cells[0]] = {h: float(re.match(r"[-+]?[\d.]+", c).group()) for h, c in zip(header[1:], cells[1:])}
    return table


def pick_font():
    """한글 글꼴: 있는 것 중 첫 번째 (없으면 기본 글꼴 → 한글이 네모로 보일 수 있음)"""
    have = {f.name for f in font_manager.fontManager.ttflist}
    for name in ("Noto Sans CJK KR", "NanumGothic", "Malgun Gothic", "AppleGothic"):
        if name in have:
            return name
    return None


acc = read_table("정답률")                                # 정답률 % (전체 378장 표)
gain = read_table("보조 결과")                            # 방법 − 기준선 %p (같은 사진끼리 짝지어 계산한 리포트 값)
font = pick_font()
if font:
    plt.rcParams["font.family"] = font
plt.rcParams["axes.unicode_minus"] = False

INK, MUTED, GRID, SURF = "#0b0b0b", "#52514e", "#e6e5e0", "#fcfcfb"
fig, ax = plt.subplots(figsize=(9, 4.6), dpi=160)
fig.patch.set_facecolor(SURF)
ax.set_facecolor(SURF)

n, width, gap = len(COLS), 0.36, 0.02                    # 막대 두 개 사이 2px 정도의 틈
x = range(n)
for i, (key, label, color) in enumerate(ROWS):
    vals = [acc[key][c] for c, _ in COLS]
    xs = [k + (i - 0.5) * (width + gap) for k in x]
    bars = ax.bar(xs, vals, width, color=color, label=label, zorder=2)
    for b, v in zip(bars, vals):                         # 막대 위에 값 (글자는 검은 잉크, 색은 막대가 담당)
        ax.text(b.get_x() + b.get_width() / 2, v + 1.2, f"{v:.1f}", ha="center", va="bottom",
                fontsize=9.5, color=INK)

for k, (c, _) in enumerate(COLS):                        # 그룹 위에 차이(%p)
    d = gain["SoG(p=3)"][c]                              # 두 정답률을 빼면 반올림 때문에 0.1 어긋날 수 있어 리포트 값을 씀
    top = max(acc["SoG(p=3)"][c], acc["기준선(고정)"][c])
    ax.text(k, top + 8, f"+{d:.1f}%p", ha="center", va="bottom", fontsize=11, fontweight="bold", color=INK)

ax.set_xticks(list(x), [s for _, s in COLS], fontsize=10, color=INK)
ax.set_ylim(0, 105)
ax.set_yticks([0, 25, 50, 75, 100])
ax.tick_params(axis="y", colors=MUTED, labelsize=9, length=0)
ax.tick_params(axis="x", length=0)
ax.set_ylabel("색 이름 정답률 (%)", color=MUTED, fontsize=9.5)
ax.grid(axis="y", color=GRID, linewidth=0.8, zorder=0)
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color(GRID)
ax.set_title("조명별 색 이름 정답률 — Gehler-Shi 봉인 평가용 378장 (최종 1회)", loc="left",
             fontsize=12, color=INK, pad=28)
ax.legend(loc="upper left", bbox_to_anchor=(0, 1.1), ncol=2, frameon=False, fontsize=9.5,
          labelcolor=INK, handlelength=1.2)
fig.text(0.01, 0.01, "숫자 출처: reports/final/gehler_test.md · 푸른 조명은 9장뿐이라 참고만", fontsize=8, color=MUTED)
fig.tight_layout(rect=(0, 0.03, 1, 1))
OUT.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(OUT, facecolor=SURF)
print(f"저장: {OUT.relative_to(ROOT)}")
for key, _, _ in ROWS:
    print(f"  {key}: " + " · ".join(f"{c} {acc[key][c]}" for c, _ in COLS))