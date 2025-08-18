import pandas as pd
import webbrowser
import tempfile
import os

# CSV 경로 확장
file_path = os.path.expanduser("~/Desktop/django-project/result/output.csv")

# CSV 불러오기
df = pd.read_csv(file_path, encoding="utf-8")

# 표 HTML
table_html = df.to_html(index=False, classes="excel-table", border=0, escape=False)

# 다크/헤비 스타일 HTML
html = f"""
<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>CSV 미리보기</title>
<style>
  :root {{
    --bg: #0b1220;               /* 전체 배경 (어두움) */
    --card-bg: #0f172a;          /* 카드/표 배경 */
    --text: #e5e7eb;             /* 기본 텍스트 */
    --muted: #94a3b8;            /* 보조 텍스트 */
    --header-bg: #0a0f1a;        /* 헤더 배경(더 어둡게) */
    --header-text: #f8fafc;      /* 헤더 텍스트 */
    --header-border: #1e293b;    /* 헤더 하단 보더(두껍게 보이도록) */
    --grid: #334155;             /* 셀 그리드(짙은 회청) */
    --row-alt: #0d1626;          /* 줄무늬 배경(미세 차이) */
    --hover: #1f2937;            /* 호버 시 강조 */
    --sticky-shadow: 0 2px 0 rgba(0,0,0,0.35);
    --sticky-col-shadow: 2px 0 0 rgba(0,0,0,0.35);
    --radius: 10px;
  }}

  * {{ box-sizing: border-box; }}
  html, body {{ height: 100%; }}
  body {{
    margin: 0;
    background: var(--bg);
    color: var(--text);
    font-family: system-ui, -apple-system, Segoe UI, Roboto, Noto Sans, Apple SD Gothic Neo, "Malgun Gothic", sans-serif;
  }}

  .wrap {{
    padding: 20px;
  }}

  .table-shell {{
    background: var(--card-bg);
    border: 2px solid var(--header-border);
    border-radius: var(--radius);
    box-shadow: 0 8px 32px rgba(0,0,0,0.35);
  }}

  .toolbar {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 12px 14px;
    border-bottom: 2px solid var(--header-border);
    background: linear-gradient(180deg, #0d1524 0%, #0b1220 100%);
    border-top-left-radius: var(--radius);
    border-top-right-radius: var(--radius);
    color: var(--muted);
    font-size: 13px;
    letter-spacing: .2px;
  }}

  .table-scroll {{
    overflow: auto;
    max-height: 78vh;  /* 스크롤 */
    border-bottom-left-radius: var(--radius);
    border-bottom-right-radius: var(--radius);
  }}

  /* 스크롤바도 묵직하게 */
  .table-scroll::-webkit-scrollbar {{ height: 12px; width: 12px; }}
  .table-scroll::-webkit-scrollbar-thumb {{ background: #263244; border-radius: 8px; }}
  .table-scroll::-webkit-scrollbar-track {{ background: #0a0f1a; }}

  table.excel-table {{
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    table-layout: auto;
    color: var(--text);
    background: var(--card-bg);
    font-size: 14px;
  }}

  /* 헤더: 스티키 + 두꺼운 느낌 */
  table.excel-table thead th {{
    position: sticky;
    top: 0;
    z-index: 3;
    background: var(--header-bg);
    color: var(--header-text);
    font-weight: 800;
    text-transform: none;
    border-bottom: 2px solid var(--header-border);
    padding: 12px 14px;
    white-space: nowrap;
    letter-spacing: .1px;
    box-shadow: var(--sticky-shadow);
  }}

  /* 셀 공통 */
  table.excel-table th, table.excel-table td {{
    border-right: 1px solid var(--grid);
    border-bottom: 1px solid var(--grid);
    padding: 10px 14px;
    vertical-align: middle;
  }}

  /* 좌측 테두리 */
  table.excel-table tr th:first-child,
  table.excel-table tr td:first-child {{
    border-left: 1px solid var(--grid);
  }}

  /* 첫 번째 열 스티키(엑셀 느낌 강화) */
  table.excel-table tbody td:first-child,
  table.excel-table thead th:first-child {{
    position: sticky;
    left: 0;
    z-index: 2;
    background: var(--card-bg);
    box-shadow: var(--sticky-col-shadow);
  }}
  /* 헤더의 첫 열은 헤더 배경 유지 */
  table.excel-table thead th:first-child {{
    background: var(--header-bg);
    z-index: 4;
  }}

  /* 줄무늬 */
  table.excel-table tbody tr:nth-child(even) td {{
    background: var(--row-alt);
  }}

  /* 호버 강조 (더 어둡게) */
  table.excel-table tbody tr:hover td {{
    background: var(--hover);
  }}

  /* 숫자 우측 정렬 + 등폭 */
  table.excel-table td[data-num="1"] {{
    text-align: right;
    font-variant-numeric: tabular-nums;
  }}

  /* 긴 텍스트 줄바꿈 & 최대 라인 높이 */
  table.excel-table td {{
    word-break: break-word;
    line-height: 1.45;
  }}
</style>
</head>
<body>
  <div class="wrap">
    <div class="table-shell">
      <div class="toolbar">
        <div>CSV 미리보기 • 엑셀 스타일(Heavy)</div>
        <div>행: {len(df)} / 열: {len(df.columns)}</div>
      </div>
      <div class="table-scroll">
        {table_html}
      </div>
    </div>
  </div>

<script>
  // 숫자 컬럼 자동 감지(샘플 50행 기반)
  (function() {{
    const table = document.querySelector('table.excel-table');
    if (!table) return;
    const rows = table.tBodies[0]?.rows || [];
    const cols = table.tHead?.rows[0]?.cells.length || 0;

    for (let c = 0; c < cols; c++) {{
      let numericCount = 0, checked = 0;
      for (let r = 0; r < rows.length && r < 50; r++) {{
        const cell = rows[r].cells[c];
        if (!cell) continue;
        const txt = cell.textContent.trim().replace(/,/g,'');
        if (txt) {{
          checked++;
          if (!isNaN(Number(txt))) numericCount++;
        }}
      }}
      if (checked > 0 && numericCount / checked >= 0.7) {{
        for (let r = 0; r < rows.length; r++) {{
          const cell = rows[r].cells[c];
          if (cell) cell.setAttribute('data-num', '1');
        }}
      }}
    }}
  }})();
</script>
</body>
</html>
"""

# 임시 HTML 저장 후 열기
with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html', encoding='utf-8') as f:
    f.write(html)
    webbrowser.open(f.name)
