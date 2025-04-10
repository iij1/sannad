import streamlit as st
import json
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import numpy as np
from datetime import datetime

# Set page config as the first Streamlit command
st.set_page_config(
    page_title="Sanaad Analytics",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Font Awesome for icons
st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">', unsafe_allow_html=True)

# Load data with error handling
try:
    json_path = Path("player_data_realistic.json")
    with open(json_path, "r", encoding="utf-8") as f:
        players_data = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    st.error(f'<div style="color: #ff4d4f;"><i class="fas fa-exclamation-triangle"></i> خطأ في تحميل البيانات: {str(e)}</div>', unsafe_allow_html=True)
    st.stop()

# Enhanced CSS with formal colors and no glow/icon animations
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
        
        :root {
            --primary-bg: linear-gradient(135deg, #0f172a, #1e293b);
            --secondary-bg: #1e293b;
            --accent-blue: #3b82f6;
            --text-primary: #f8f9fa;
            --text-secondary: #94a3b8;
            --card-bg-low: #2d3748;    /* Dark slate gray */
            --card-bg-medium: #4a5568; /* Medium slate gray */
            --card-bg-high: #742a2a;  /* Deep red */
            --success: #38a169;       /* Professional green */
            --warning: #d69e2e;       /* Professional yellow */
            --danger: #9b2c2c;        /* Professional red */
            --border-radius: 15px;
            --shadow: 0 10px 30px rgba(0,0,0,0.4);
        }

        body {
            background: var(--primary-bg);
            color: var(--text-primary);
            font-family: 'Poppins', sans-serif;
        }

        .main .block-container {
            padding: 3rem;
            max-width: 1800px;
            background: var(--primary-bg);
            border-radius: var(--border-radius);
        }

        h1 {
            font-size: 3rem;
            font-weight: 700;
            background: linear-gradient(to right, var(--accent-blue), #60a5fa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: fadeIn 1s ease-in;
        }

        h2 {
            font-size: 2rem;
            font-weight: 600;
            color: var(--text-primary);
            margin-bottom: 2rem;
            animation: slideIn 0.8s ease-out;
        }

        .metric-card-low, .metric-card-medium, .metric-card-high {
            border-radius: var(--border-radius);
            padding: 2rem;
            box-shadow: var(--shadow);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        .metric-card-low {
            background: var(--card-bg-low);
            border: 2px solid var(--success);
        }

        .metric-card-medium {
            background: var(--card-bg-medium);
            border: 2px solid var(--warning);
        }

        .metric-card-high {
            background: var(--card-bg-high);
            border: 2px solid var(--danger);
        }

        .metric-card-low:hover, .metric-card-medium:hover, .metric-card-high:hover {
            transform: translateY(-10px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.5);
        }

        .metric-icon {
            font-size: 2rem;
            color: var(--accent-blue);
            margin-right: 1rem;
        }

        .risk-indicator {
            padding: 0.8rem 1.2rem;
            border-radius: 10px;
            text-align: center;
            font-weight: 600;
            font-size: 1.1rem;
            color: white;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            transition: transform 0.3s ease;
        }

        .risk-indicator:hover {
            transform: scale(1.05);
        }

        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        @keyframes slideIn {
            from { transform: translateY(20px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }

        .sidebar .sidebar-content {
            background: var(--secondary-bg);
            border-radius: 0 var(--border-radius) var(--border-radius) 0;
            box-shadow: var(--shadow);
        }

        .stSelectbox > div {
            background: var(--card-bg-low);
            border-radius: 12px;
            color: var(--text-primary);
            border: 2px solid var(--accent-blue);
        }

        .stButton > button {
            background: linear-gradient(45deg, var(--accent-blue), #60a5fa);
            color: var(--text-primary);
            border-radius: 12px;
            padding: 0.6rem 2rem;
            font-weight: 500;
            transition: all 0.4s ease;
        }

        .stButton > button:hover {
            background: linear-gradient(45deg, #2563eb, #3b82f6);
            transform: scale(1.1);
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar with enhanced controls
with st.sidebar:
    st.markdown('<h3><i class="fas fa-cog"></i> لوحة التحكم</h3>', unsafe_allow_html=True)
    heatmap_opacity = st.slider("شفافية خريطة الحرارة", 0.1, 1.0, 0.5)
    show_advanced = st.checkbox("عرض التحليلات المتقدمة", value=True)
    st.markdown(f'<p style="color: var(--text-secondary);"><i class="fas fa-clock"></i> آخر تحديث: {datetime.now().strftime("%Y-%m-%d %H:%M")}</p>', unsafe_allow_html=True)

# Title
st.markdown('<h1><i class="fas fa-futbol"></i> منصة سَند </h1>', unsafe_allow_html=True)

# Enhanced risk analysis with logical scoring
def analyze_injury_risk(player_data):
    last_match = player_data["matches"][-1]
    inbody = player_data["inbody"]
    
    # Initialize risk score (0-100)
    risk_score = 0
    warnings = []
    recommendations = []
    
    # Fatigue: >80% is high risk
    fatigue = last_match["fatigue"]
    if fatigue > 80:
        risk_score += 30
        warnings.append("إجهاد شديد")
        recommendations.append("زيادة فترات الراحة")
    elif fatigue > 60:
        risk_score += 15
        warnings.append("إجهاد متوسط")
        recommendations.append("مراقبة الإجهاد")

    # Heart Rate: >140 bpm is high risk
    heart_rate = last_match["heart_rate"]
    if heart_rate > 140:
        risk_score += 25
        warnings.append("نبض مرتفع جدًا")
        recommendations.append("مراجعة طبيب رياضي")
    elif heart_rate > 120:
        risk_score += 10
        warnings.append("نبض مرتفع")

    # Tackles: >15 is high risk
    tackles = last_match["tackles"]
    if tackles > 15:
        risk_score += 20
        warnings.append("تدخلات مكثفة")
        recommendations.append("تقليل الاحتكاك الجسدي")
    elif tackles > 10:
        risk_score += 8

    # Steps: >12000 is high risk
    steps = last_match["steps"]
    if steps > 12000:
        risk_score += 15
        warnings.append("نشاط زائد")
        recommendations.append("تعديل خطة التدريب")
    elif steps > 10000:
        risk_score += 5

    # Hydration: <60% is high risk
    hydration = inbody["hydration"]
    if hydration < 60:
        risk_score += 25
        warnings.append("ترطيب منخفض")
        recommendations.append("زيادة تناول السوائل")
    elif hydration < 70:
        risk_score += 10

    # Distance (if available): >8000m is high risk
    distance = last_match.get("distance", 5000)  # Default to 5000 if missing
    if distance > 8000:
        risk_score += 20
        warnings.append("مسافة مرتفعة")
        recommendations.append("تقليل الحمل الحركي")
    elif distance > 6000:
        risk_score += 8

    # Cap risk score at 100
    risk_score = min(risk_score, 100)
    
    # Determine level based on score
    if risk_score > 70:
        level = "مرتفع"
        card_class = "metric-card-high"
    elif risk_score > 40:
        level = "متوسط"
        card_class = "metric-card-medium"
    else:
        level = "منخفض"
        card_class = "metric-card-low"

    return {
        'percentage': risk_score,
        'warnings': warnings,
        'recommendations': recommendations,
        'level': level,
        'card_class': card_class
    }

# Risk Analysis Section with formal cards
st.markdown('<h2><i class="fas fa-shield-alt"></i> تحليل مخاطر الإصابة</h2>', unsafe_allow_html=True)
risk_cols = st.columns(4)
high_risk_players = []

for i, player in enumerate(players_data):
    risk_analysis = analyze_injury_risk(player)
    if risk_analysis['percentage'] > 70:
        high_risk_players.append(player['name'])
    
    with risk_cols[i % 4]:
        color = "var(--danger)" if risk_analysis['percentage'] > 70 else "var(--warning)" if risk_analysis['percentage'] > 40 else "var(--success)"
        st.markdown(f"""
            <div class="{risk_analysis['card_class']}">
                <h4 style="display: flex; align-items: center;">
                    <i class="fas fa-user metric-icon"></i> {player['name']}
                </h4>
                <div style="font-size: 2rem; color: {color}; font-weight: 700; margin: 0.5rem 0;">{risk_analysis['percentage']}%</div>
                <div class="risk-indicator" style="background: {color};">{risk_analysis['level']}</div>
                <p style="color: var(--text-secondary); font-size: 0.95rem; margin-top: 0.5rem;">
                    <strong>التحذيرات:</strong> {'; '.join(risk_analysis['warnings']) if risk_analysis['warnings'] else 'لا توجد تحذيرات'}
                </p>
                <p style="color: var(--success); font-size: 0.95rem; margin-top: 0.5rem;">
                    <strong>التوصيات:</strong> {'; '.join(risk_analysis['recommendations']) if risk_analysis['recommendations'] else 'لا توجد توصيات'}
                </p>
            </div>
        """, unsafe_allow_html=True)

if high_risk_players:
    st.markdown(f'<div style="color: var(--danger); margin: 1.5rem 0; font-weight: 600;"><i class="fas fa-exclamation-circle"></i> لاعبون في خطر: {", ".join(high_risk_players)}</div>', unsafe_allow_html=True)

# Enhanced Interactive Field
st.markdown('<h2><i class="fas fa-map-marked-alt"></i> خريطة الملعب التفاعلية</h2>', unsafe_allow_html=True)
fig = go.Figure()

# Draw realistic field with gradient and details
fig.add_shape(type="rect", x0=0, y0=0, x1=10, y1=7, fillcolor="rgba(34,197,94,0.9)", line=dict(color="white", width=3))
fig.add_shape(type="rect", x0=0.5, y0=2, x1=9.5, y1=5, fillcolor="rgba(0,0,0,0)", line=dict(color="white", width=2, dash="dash"))
fig.add_shape(type="line", x0=5, y0=0, x1=5, y1=7, line=dict(color="white", width=2))
fig.add_shape(type="circle", xref="x", yref="y", x0=4.5, y0=2.5, x1=5.5, y1=4.5, line=dict(color="white", width=2))
fig.add_shape(type="rect", x0=0, y0=0, x1=2, y1=1, fillcolor="rgba(0,0,0,0)", line=dict(color="white", width=2))  # Left penalty area
fig.add_shape(type="rect", x0=8, y0=0, x1=10, y1=1, fillcolor="rgba(0,0,0,0)", line=dict(color="white", width=2))  # Right penalty area

# Add players with enhanced markers
positions = [(1,3), (2,2), (2,4), (3,1), (3,5), (4,2), (4,4), (5,3), (6,2), (6,4), (7,3)]
for i, player in enumerate(players_data):
    last_match = player["matches"][-1]
    risk_analysis = analyze_injury_risk(player)
    color = "var(--danger)" if risk_analysis['percentage'] > 70 else "var(--warning)" if risk_analysis['percentage'] > 40 else "var(--success)"
    
    hover_text = (
        f"اللاعب: {player['name']}<br>"
        f"مخاطر الإصابة: {risk_analysis['percentage']}%<br>"
        f"الإجهاد: {last_match['fatigue']}%<br>"
        f"النبض: {last_match['heart_rate']} نبضة/دقيقة<br>"
        f"الخطوات: {last_match['steps']}<br>"
        f"التدخلات: {last_match['tackles']}<br>"
        f"التوصيات: {'; '.join(risk_analysis['recommendations']) if risk_analysis['recommendations'] else 'لا توجد'}"
    )
    
    fig.add_trace(go.Scatter(
        x=[positions[i][0]], y=[positions[i][1]],
        mode="markers+text",
        marker=dict(
            size=70,
            color=color,
            symbol="circle",
            line=dict(color="white", width=4),
            gradient=dict(type="radial", color="rgba(255,255,255,0.4)")
        ),
        text=[player["name"]],
        textfont=dict(color="white", size=18, family="Poppins"),
        textposition="middle center",
        hoverinfo="text",
        hovertext=hover_text,
        name=player["name"]
    ))

# Add heatmap
heatmap_data = np.random.rand(10, 7)  # Replace with real movement data
fig.add_trace(go.Heatmap(
    z=heatmap_data,
    x=np.linspace(0, 10, 10),
    y=np.linspace(0, 7, 7),
    colorscale="Viridis",
    opacity=heatmap_opacity,
    showscale=True,
    colorbar=dict(
        title=dict(text="كثافة الحركة", side="top"),
        thickness=25,
        len=0.9,
        tickfont=dict(size=12)
    )
))

fig.update_layout(
    width=1400,
    height=900,
    plot_bgcolor="var(--secondary-bg)",
    paper_bgcolor="var(--secondary-bg)",
    margin=dict(l=40, r=40, t=40, b=40),
    xaxis=dict(range=[-0.5, 10.5], showgrid=False, zeroline=False, visible=False),
    yaxis=dict(range=[-0.5, 7.5], showgrid=False, zeroline=False, visible=False),
    font=dict(color="var(--text-primary)", family="Poppins", size=16),
    showlegend=False,
    autosize=True
)
st.plotly_chart(fig, use_container_width=True)

# Player Performance Dashboard
st.markdown('<h2><i class="fas fa-user-check"></i> لوحة أداء اللاعب</h2>', unsafe_allow_html=True)
selected_player = st.selectbox("اختر اللاعب", [p["name"] for p in players_data], label_visibility="collapsed")
player = next(p for p in players_data if p["name"] == selected_player)

# Enhanced Key Metrics
st.markdown('<h3><i class="fas fa-tachometer-alt"></i> المقاييس الرئيسية</h3>', unsafe_allow_html=True)
cols = st.columns(4)
metrics = [
    {"icon": "fa-heartbeat", "label": "معدل النبض", "value": f"{player['matches'][-1]['heart_rate']} نبضة/دقيقة"},
    {"icon": "fa-shoe-prints", "label": "الخطوات", "value": f"{player['matches'][-1]['steps']}"},
    {"icon": "fa-dumbbell", "label": "الكتلة العضلية", "value": f"{player['inbody']['muscle_mass']} كجم"},
    {"icon": "fa-tint", "label": "الترطيب", "value": f"{player['inbody']['hydration']}%"}
]

for col, metric in zip(cols, metrics):
    col.markdown(
        f"""
        <div class="metric-card-low">
            <h4 style="display: flex; align-items: center;">
                <i class="fas {metric['icon']} metric-icon"></i> {metric['label']}
            </h4>
            <p style="font-size: 2rem; font-weight: 700; color: var(--text-primary);">{metric['value']}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Enhanced Performance Trends
performance_df = pd.DataFrame(player["matches"])
fig_performance = px.line(
    performance_df,
    x=performance_df.index,
    y=["heart_rate", "fatigue", "steps", "tackles"],
    title="تطور الأداء عبر المباريات",
    labels={"value": "القيمة", "index": "رقم المباراة", "variable": "المقياس"}
)
fig_performance.update_traces(line=dict(width=4, dash="solid"))
fig_performance.update_layout(
    template="plotly_dark",
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Poppins", color="var(--text-primary)", size=16),
    title_font_size=22,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    hovermode="x unified",
    margin=dict(l=40, r=40, t=60, b=40)
)
st.plotly_chart(fig_performance, use_container_width=True)

# Advanced Analytics with deeper insights
if show_advanced:
    st.markdown('<h3><i class="fas fa-chart-pie"></i> تحليلات متقدمة</h3>', unsafe_allow_html=True)
    adv_cols = st.columns(2)
    
    with adv_cols[0]:
        # Radar Chart with more metrics
        categories = ['الإجهاد', 'النبض', 'الخطوات', 'التدخلات', 'الترطيب']
        values = [
            player["matches"][-1]["fatigue"],
            player["matches"][-1]["heart_rate"] / 2,
            player["matches"][-1]["steps"] / 200,
            player["matches"][-1]["tackles"] * 5,
            player["inbody"]["hydration"]
        ]
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=values + [values[0]],
            theta=categories + [categories[0]],
            fill='toself',
            line=dict(color="var(--accent-blue)", width=3),
            name=player["name"]
        ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=True,
            template="plotly_dark",
            font=dict(family="Poppins", color="var(--text-primary)", size=14),
            margin=dict(l=20, r=20, t=20, b=20)
        )
        st.plotly_chart(fig_radar, use_container_width=True)
    
    with adv_cols[1]:
        # Detailed Team Comparison with additional metrics
        team_avg = {
            "heart_rate": np.mean([p["matches"][-1]["heart_rate"] for p in players_data]),
            "steps": np.mean([p["matches"][-1]["steps"] for p in players_data]),
            "fatigue": np.mean([p["matches"][-1]["fatigue"] for p in players_data]),
            "tackles": np.mean([p["matches"][-1]["tackles"] for p in players_data]),
            "hydration": np.mean([p["inbody"]["hydration"] for p in players_data])
        }
        comparison_df = pd.DataFrame({
            "المقياس": ["النبض", "الخطوات", "الإجهاد", "التدخلات", "الترطيب"],
            "اللاعب": [
                player["matches"][-1]["heart_rate"],
                player["matches"][-1]["steps"],
                player["matches"][-1]["fatigue"],
                player["matches"][-1]["tackles"],
                player["inbody"]["hydration"]
            ],
            "متوسط الفريق": [
                team_avg["heart_rate"],
                team_avg["steps"],
                team_avg["fatigue"],
                team_avg["tackles"],
                team_avg["hydration"]
            ]
        })
        fig_comparison = px.bar(
            comparison_df,
            x="المقياس",
            y=["اللاعب", "متوسط الفريق"],
            barmode="group",
            title="مقارنة اللاعب مع متوسط الفريق",
            color_discrete_map={"اللاعب": "#3b82f6", "متوسط الفريق": "#94a3b8"}
        )
        fig_comparison.update_layout(
            template="plotly_dark",
            font=dict(family="Poppins", color="var(--text-primary)", size=14),
            bargap=0.2,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig_comparison, use_container_width=True)

# Footer
st.markdown("""
    <footer style="text-align: center; padding: 2.5rem; background: var(--secondary-bg); margin-top: 4rem; border-radius: var(--border-radius); box-shadow: var(--shadow);">
        <p style="color: var(--text-secondary); font-size: 1.1rem;"><i class="fas fa-copyright"></i> سَند 2025 | مدعوم من </p>
    </footer>
""", unsafe_allow_html=True)
