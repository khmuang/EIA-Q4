import os
import json
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
html_file = os.path.join(BASE_DIR, 'index.html')
data_file = os.path.join(BASE_DIR, 'data.js')

if not os.path.exists(html_file):
    print(f"[ERROR] HTML file not found: {html_file}")
    exit(1)

if not os.path.exists(data_file):
    print(f"[ERROR] data.js not found: {data_file}")
    exit(1)

with open(html_file, 'r', encoding='utf-8') as f:
    html_content = f.read()

with open(data_file, 'r', encoding='utf-8') as f:
    data_content = f.read()

json_str = re.search(r'const DASHBOARD_DATA = ({.*?});', data_content, re.DOTALL).group(1)
data = json.loads(json_str)

topic_order = ['1.1', '1.2', '2', '3', '4', '5', '6', '7', '8']
topic_names = {
    '1.1': '1.1 IT Asset', '1.2': '1.2 GLPI agent', '2': '2 Update OS',
    '3': '3 Patch Update', '4': '4 Antivirus', '5': '5 Firewall',
    '6': '6 Client join domain', '7': '7 Privileged User', '8': '8 Document Request'
}

def get_status_class(pct):
    if pct >= 85: return 'color: #10b981; font-weight: bold;'
    if pct >= 65: return 'color: #3b82f6; font-weight: bold;'
    if pct >= 45: return 'color: #f59e0b; font-weight: bold;'
    return 'color: #f43f5e; font-weight: bold;'

def get_bg_color(pct):
    if pct >= 85: return 'rgba(16,185,129,0.15)'
    elif pct >= 65: return 'rgba(59,130,246,0.15)'
    elif pct >= 45: return 'rgba(245,158,11,0.15)'
    else: return 'rgba(244,63,94,0.15)'

def get_text_color(pct):
    if pct >= 85: return 'var(--accent-emerald)'
    elif pct >= 65: return 'var(--accent-blue)'
    elif pct >= 45: return 'var(--accent-amber)'
    else: return 'var(--accent-rose)'

def get_chart_color(pct):
    if pct >= 85: return 'var(--accent-emerald)', 'rgba(16,185,129,0.5)'
    elif pct >= 65: return 'var(--accent-blue)', 'rgba(59,130,246,0.5)'
    elif pct >= 45: return 'var(--accent-amber)', 'rgba(245,158,11,0.5)'
    return 'var(--accent-rose)', 'rgba(244,63,94,0.5)'

html_tables = """<div class="summary-info-card" style="grid-column: 1 / -1;">
<style>
.detailed-table { width: 100%; border-collapse: collapse; margin-top: 15px; font-size: 0.8rem; color: #fff; background: rgba(0, 0, 0, 0.2); border-radius: 8px; overflow: hidden; margin-bottom: 25px; }
.detailed-table th { background: rgba(255, 255, 255, 0.1); padding: 8px 10px; text-align: left; font-weight: 600; font-size: 0.75rem; }
.detailed-table td { padding: 8px 10px; border-bottom: 1px solid rgba(255, 255, 255, 0.05); }
.detailed-table tr:hover { background: rgba(255, 255, 255, 0.05); }
.team-summary-box { display: flex; align-items: center; justify-content: space-between; margin-top: 5px; flex-wrap: wrap; gap: 10px; }
.team-stats { display: flex; gap: 10px; font-size: 0.85rem; }
.stat-badge { padding: 4px 10px; border-radius: 6px; font-weight: bold; }
.team-desc { font-size: 0.85rem; color: var(--text-dim); width: 100%; margin-top: 5px; }
</style>
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
        <h4 style="font-size: 1.2rem; margin: 0;">📊 สรุปความคืบหน้าและข้อมูลเจาะลึกรายทีม Q4 (Team Performance & Deep Dive)</h4>
    </div>
"""

for team in ['HO', 'DC', 'Branch']:
    team_q4_t, team_q4_s = 0, 0
    for tid in topic_order:
        phases = data.get(team, {}).get(tid, {})
        team_q4_t += phases.get('Q4', {}).get('total', 0)
        team_q4_s += phases.get('Q4', {}).get('success', 0)

    team_all_t = team_q4_t
    team_all_s = team_q4_s
    all_pct = round((team_all_s/team_all_t)*100) if team_all_t > 0 else 0
    q4_pct = round((team_q4_s/team_q4_t)*100) if team_q4_t > 0 else 0

    medal = '🥇' if team == 'HO' else ('🥈' if team == 'DC' else '🥉')

    html_tables += f"""
    <div class="ranking-item" style="{'border: 1px solid rgba(250,204,21,0.3);' if team=='HO' else ''}">
        <div class="rank-header">
            <span class="rank-name" style="font-size: 1.15rem;">{medal} ทีม {team}</span>
            <span class="rank-val" style="font-size: 1.1rem; color: {get_text_color(all_pct)};">
                ภาพรวม Q4: {all_pct}% 
                <span style="font-size: 0.85rem; color: #9ca3af; font-weight: normal; margin-left: 5px;">({team_all_s:,} / {team_all_t:,})</span>
            </span>
        </div>
        <div class="team-summary-box">
            <div class="team-stats">
                <div class="stat-badge" style="background: {get_bg_color(q4_pct)}; color: {get_text_color(q4_pct)};">Q4 Target: {team_q4_t:,} Units ({q4_pct}%)</div>
            </div>
        </div>
        
        <table class="detailed-table">
            <thead>
                <tr>
                    <th>Topic</th>
                    <th>Phase Q4 Targets</th>
                    <th>Overall Q4 Status</th>
                </tr>
            </thead>
            <tbody>
    """

    for tid in topic_order:
        phases = data.get(team, {}).get(tid, {})
        q4_t = phases.get('Q4', {}).get('total', 0)
        q4_s = phases.get('Q4', {}).get('success', 0)
        q4_pct_row = round((q4_s/q4_t)*100) if q4_t > 0 else 0
        q4_str = f'<span style="{get_status_class(q4_pct_row)}">{q4_s:,}/{q4_t:,} ({q4_pct_row}%)</span>' if q4_t > 0 else '-'

        all_t = q4_t
        all_s = q4_s
        all_pct_row = round((all_s/all_t)*100) if all_t > 0 else 0
        all_str = f'<span style="{get_status_class(all_pct_row)}">{all_s:,}/{all_t:,} ({all_pct_row}%)</span>' if all_t > 0 else '-'

        if all_t > 0:
            color, shadow = get_chart_color(all_pct_row)
            topic_html = f"""<div style="margin-bottom: 6px; font-weight: bold; color: #fff;">{topic_names[tid]}</div>
                            <div style="width: 100%; max-width: 180px; margin-top: 5px;">
                                <div style="display: flex; justify-content: space-between; font-size: 0.7rem; margin-bottom: 3px;">
                                    <span style="color: {color}; font-weight: bold;">{all_pct_row}%</span>
                                    <span style="color: #9ca3af;">{all_s:,} / {all_t:,}</span>
                                </div>
                                <div style="height: 5px; background: rgba(255,255,255,0.1); border-radius: 3px; overflow: hidden; position: relative;">
                                    <div style="height: 100%; background: {color}; width: {all_pct_row}%; border-radius: 3px; box-shadow: 0 0 5px {shadow};"></div>
                                </div>
                            </div>"""
        else:
            topic_html = f"""<div style="font-weight: bold; color: #fff;">{topic_names[tid]}</div>"""

        html_tables += f"""
                <tr>
                    <td>{topic_html}</td>
                    <td>{q4_str}</td>
                    <td>{all_str}</td>
                </tr>
        """

    team_all_t = team_q4_t
    team_all_s = team_q4_s
    team_all_pct = round((team_all_s/team_all_t)*100) if team_all_t > 0 else 0
    team_all_str = f'<span style="{get_status_class(team_all_pct)}">{team_all_s:,}/{team_all_t:,} ({team_all_pct}%)</span>' if team_all_t > 0 else '-'
    team_all_n = team_all_t - team_all_s

    if team_all_t > 0:
        gt_color, gt_shadow = get_chart_color(team_all_pct)
        gt_html = f"""<div style="margin-bottom: 6px; font-weight: bold; color: #fff;">Grand Total (ผลรวม)</div>
                        <div style="width: 100%; max-width: 180px; margin-top: 5px;">
                            <div style="display: flex; justify-content: space-between; font-size: 0.7rem; margin-bottom: 3px;">
                                <span style="color: {gt_color}; font-weight: bold;">{team_all_pct}%</span>
                                <span style="color: #9ca3af;">{team_all_s:,} / {team_all_t:,}</span>
                            </div>
                            <div style="height: 5px; background: rgba(255,255,255,0.1); border-radius: 3px; overflow: hidden; position: relative;">
                                <div style="height: 100%; background: {gt_color}; width: {team_all_pct}%; border-radius: 3px; box-shadow: 0 0 5px {gt_shadow};"></div>
                            </div>
                        </div>"""
    else:
        gt_html = f"""<div style="font-weight: bold; color: #fff;">Grand Total (ผลรวม)</div>"""

    html_tables += f"""
                <tr style="background: rgba(255, 255, 255, 0.1); border-top: 2px solid rgba(255, 255, 255, 0.2);">
                    <td style="font-weight: 800; font-size: 0.85rem;">{gt_html}</td>
                    <td style="font-weight: 800; font-size: 0.85rem;">{team_all_str}</td>
                    <td style="font-weight: 800; font-size: 0.85rem;">{team_all_str}</td>
                </tr>
                <tr style="background: rgba(16, 185, 129, 0.1);">
                    <td style="font-weight: 700; font-size: 0.8rem; color: var(--accent-emerald);">Total Y (สำเร็จ)</td>
                    <td style="font-weight: 700; font-size: 0.8rem; color: var(--accent-emerald);">{team_all_s:,}</td>
                    <td style="font-weight: 700; font-size: 0.8rem; color: var(--accent-emerald);">{team_all_s:,}</td>
                </tr>
                <tr style="background: rgba(244, 63, 94, 0.1);">
                    <td style="font-weight: 700; font-size: 0.8rem; color: var(--accent-rose);">Total N (รอดำเนินการ)</td>
                    <td style="font-weight: 700; font-size: 0.8rem; color: var(--accent-rose);">{team_all_n:,}</td>
                    <td style="font-weight: 700; font-size: 0.8rem; color: var(--accent-rose);">{team_all_n:,}</td>
                </tr>
            </tbody>
        </table>
    </div>
    """

# ====================================================
# BU MATRIX GENERATION
# ====================================================
bu_html = """
<div class="summary-info-card" style="grid-column: 1 / -1; margin-top: 30px; border: 1px dashed rgba(255, 255, 255, 0.3);">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
        <h4 style="font-size: 1.2rem; margin: 0; color: var(--accent-blue);">🏢 สรุปผลตาม Business Unit (BU Matrix) แยกตามทีม Q4</h4>
    </div>
"""

for team in ['HO', 'DC', 'Branch']:
    bu_data = {}
    for tid in topic_order:
        phases = data.get(team, {}).get(tid, {})
        for phase, metrics in phases.items():
            if phase in ['Q4', 'ALL']:
                bu_breakdown = metrics.get('bu_breakdown', {})
                for bu, nums in bu_breakdown.items():
                    if bu not in bu_data: bu_data[bu] = {}
                    if tid not in bu_data[bu]: bu_data[bu][tid] = {'success': 0, 'total': 0}
                    bu_data[bu][tid]['success'] += nums['success']
                    bu_data[bu][tid]['total'] += nums['total']

    if not bu_data: continue

    medal = '🥇' if team == 'HO' else ('🥈' if team == 'DC' else '🥉')

    bu_html += f"""
    <div class="ranking-item" style="{'border: 1px solid rgba(250,204,21,0.3);' if team=='HO' else ''} margin-bottom: 20px;">
        <div class="rank-header">
            <span class="rank-name" style="font-size: 1.15rem;">{medal} ทีม {team} - BU Breakdown</span>
        </div>
        <div style="overflow-x: auto;">
            <table class="detailed-table" style="min-width: 800px; text-align: center;">
                <thead>
                    <tr>
                        <th style="text-align: left; position: sticky; left: 0; background: #1e293b; z-index: 10;">BU Name</th>
    """
    for tid in topic_order:
        topic_short_name = topic_names[tid].split(' ', 1)[1] if ' ' in topic_names[tid] else topic_names[tid]
        bu_html += f"<th>Topic {tid}<br><span style='font-size:0.65rem; color:#9ca3af;'>{topic_short_name}</span></th>"
    bu_html += "<th>Overall<br><span style='font-size:0.65rem; color:#9ca3af;'>Total</span></th></tr></thead><tbody>"

    sorted_bus = sorted([b for b in bu_data.keys() if b != 'Unknown' and b != 'nan'])
    if 'Unknown' in bu_data: sorted_bus.append('Unknown')

    for bu in sorted_bus:
        bu_html += f"<tr><td style='text-align: left; font-weight: bold; position: sticky; left: 0; background: #1e293b;'>{bu}</td>"
        bu_all_s = 0
        bu_all_t = 0
        for tid in topic_order:
            metrics = bu_data[bu].get(tid, {'success': 0, 'total': 0})
            s, t = metrics['success'], metrics['total']
            bu_all_s += s
            bu_all_t += t
            if t > 0:
                pct = round((s/t)*100)
                color, shadow = get_chart_color(pct)
                bu_html += f"<td><span style='color: {color}; font-weight: bold;'>{pct}%</span><br><span style='font-size: 0.65rem; color: #9ca3af;'>{s:,}/{t:,}</span></td>"
            else:
                bu_html += "<td><span style='color: #4b5563;'>-</span></td>"

        if bu_all_t > 0:
            pct = round((bu_all_s/bu_all_t)*100)
            color, shadow = get_chart_color(pct)
            bu_html += f"<td><span style='color: {color}; font-weight: bold;'>{pct}%</span><br><span style='font-size: 0.65rem; color: #9ca3af;'>{bu_all_s:,}/{bu_all_t:,}</span></td>"
        else:
            bu_html += "<td><span style='color: #4b5563;'>-</span></td>"
        bu_html += "</tr>"

    bu_html += "</tbody></table></div></div>"

bu_html += "</div><!-- End of BU Matrix -->"
html_tables += bu_html
html_tables += "\n</div> <!-- End of Detailed Tables summary-info-card -->"

pattern = re.compile(r'<div class="summary-info-card" style="grid-column: 1 / -1;">.*?<!-- End of Detailed Tables summary-info-card -->', re.DOTALL)
if pattern.search(html_content):
    new_html = pattern.sub(html_tables, html_content)
else:
    # If not found, inject before summary-report-section or footer
    new_html = html_content.replace('<!-- End of Detailed Tables summary-info-card -->', '')
    if '<div class="summary-report-section"' in new_html:
        new_html = new_html.replace('<div class="summary-report-section"', html_tables + '\n<div class="summary-report-section"')
    elif '<footer>' in new_html:
        new_html = new_html.replace('<footer>', html_tables + '\n<footer>')

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(new_html)

print(f"[SUCCESS] Static tables generated and injected into {html_file}")
