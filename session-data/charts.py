"""
Chart library for READING DATA masterclass.
Palette: dataviz reference instance (validated light mode).
Rules: emphasis over categorical, no dual-axis, direct labels, recessive chrome.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import csv, statistics, os
from collections import defaultdict

# ---- Validated palette (dataviz reference, light mode) ----
# Aurex brand tokens (from /Downloads/Product/Aurex assets)
S1='#E01E29'   # Aurex red - the emphasis colour
S2='#0E8F7A'   # teal
S3='#C79A2F'   # gold
S4='#4E79CF'   # blue
S5='#8F0013'   # deep maroon
S6='#0E8F7A'; S7='#4E79CF'; S8='#E01E29'
CRITICAL='#B51D2A'; GOOD='#0E8F7A'; WARNING='#C79A2F'
SURFACE='#FBF9F8'; INK='#121111'; INK2='#5F5D5C'
MUTED='#8A857F'; GRID='#EAE7E4'; BASELINE='#D8D3CD'
GRAY='#CFCAC4'      # de-emphasis fill
GRAY_D='#AEA8A1'    # de-emphasis line

IMG='/private/tmp/claude-502/-Users-dishantsingla-Downloads-projects-aurex-backend/affd460f-5448-4470-a3bb-58de722ad050/scratchpad/img'
os.makedirs(IMG, exist_ok=True)

plt.rcParams.update({
    'font.family':'sans-serif',
    'font.sans-serif':['Helvetica Neue','Arial','DejaVu Sans'],
    'axes.spines.top':False,'axes.spines.right':False,
    'axes.edgecolor':BASELINE,'axes.labelcolor':INK2,
    'xtick.color':MUTED,'ytick.color':MUTED,
    'text.color':INK,'figure.facecolor':SURFACE,'axes.facecolor':SURFACE,
})

def finish(fig, name, dpi=160):
    p=f'{IMG}/{name}.png'
    fig.savefig(p, dpi=dpi, bbox_inches='tight', facecolor=SURFACE)
    plt.close(fig); return p

def title(ax, text, sub=None):
    """Title + optional subtitle placed in axes coords so they never collide."""
    if sub:
        ax.text(0, 1.155, text, transform=ax.transAxes, fontsize=15,
                fontweight='bold', color=INK, va='bottom')
        ax.text(0, 1.045, sub, transform=ax.transAxes, fontsize=11,
                color=MUTED, va='bottom')
    else:
        ax.text(0, 1.045, text, transform=ax.transAxes, fontsize=15,
                fontweight='bold', color=INK, va='bottom')

def softgrid(ax, axis='y'):
    ax.grid(True, axis=axis, color=GRID, linewidth=0.8, alpha=1, zorder=0)
    ax.set_axisbelow(True)

def nospine_x(ax):
    ax.spines['bottom'].set_visible(False)
    ax.tick_params(axis='x', bottom=False, labelbottom=False)

# ---------------- LOAD DATA ----------------
with open('/Users/dishantsingla/Downloads/session-data/ad-sales-data.csv') as f:
    ROWS=[r for r in csv.DictReader(f)]
CONF=[r for r in ROWS if r['status']=='Confirmed' and r['net_amount']]
def n(r,k): return float(r[k])
def city(c): return {'Mumabi':'Mumbai'}.get(c.strip().title(), c.strip().title())

# ============================================================
# TYPE 1 — COMPARISON  (emphasis form: one hue + gray)
# ============================================================
def t1_comparison():
    rev=defaultdict(float)
    for r in CONF: rev[city(r['city'])]+=n(r,'net_amount')
    items=sorted(rev.items(), key=lambda x:x[1])
    names=[k for k,_ in items]; vals=[v/1e7 for _,v in items]
    colors=[S1 if k=='Mumbai' else GRAY for k in names]

    fig,ax=plt.subplots(figsize=(9,4.6))
    b=ax.barh(names, vals, color=colors, height=0.68, zorder=3)
    for bar,v,nm in zip(b,vals,names):
        ax.text(v+0.12, bar.get_y()+bar.get_height()/2, f'{v:.2f}',
                va='center', fontsize=11, color=INK if nm=='Mumbai' else INK2,
                fontweight='bold' if nm=='Mumbai' else 'normal')
    title(ax,'Mumbai bills 2.1× what Ahmedabad does','Net ad revenue by city, ₹ crore, 2022–24')
    ax.set_xlim(0,9.2); nospine_x(ax); softgrid(ax,'x')
    ax.tick_params(axis='y', labelsize=11, left=False)
    for lbl in ax.get_yticklabels():
        if lbl.get_text()=='Mumbai': lbl.set_color(INK); lbl.set_fontweight('bold')
    return finish(fig,'t1_comparison')

# ============================================================
# TYPE 2 — RANKING  (top/bottom emphasis)
# ============================================================
def t2_ranking():
    rep=defaultdict(float)
    for r in CONF: rep[r['sales_rep']]+=n(r,'net_amount')
    s=sorted(rep.items(), key=lambda x:-x[1])
    sel=s[:5]+s[-5:]
    names=[k for k,_ in sel][::-1]; vals=[v/1e7 for _,v in sel][::-1]
    colors=[S1]*5+[GOOD]*5      # after the reverse: bottom 5 then top 5

    fig,ax=plt.subplots(figsize=(9,5.2))
    b=ax.barh(names, vals, color=colors, height=0.66, zorder=3)
    for bar,v in zip(b,vals):
        ax.text(v+0.03, bar.get_y()+bar.get_height()/2, f'{v:.2f}',
                va='center', fontsize=10.5, color=INK2)
    title(ax,'Your best rep bills 2.7× your weakest','Top 5 and bottom 5 of 30 reps · ₹ crore, 3-year total')
    ax.set_xlim(0,2.95); nospine_x(ax); softgrid(ax,'x')
    ax.tick_params(axis='y', labelsize=10.5, left=False)
    ax.text(2.62,7.0,'TOP 5',fontsize=11,color=GOOD,fontweight='bold',va='center')
    ax.text(2.62,2.0,'BOTTOM 5',fontsize=11,color=S1,fontweight='bold',va='center')
    ax.axhline(4.5, color=BASELINE, linewidth=1, linestyle=(0,(4,3)), zorder=2)
    return finish(fig,'t2_ranking')

# ============================================================
# TYPE 3 — TREND  (4 series, adjacent form, direct labels)
# ============================================================
def t3_trend():
    """Indexed to 2022=100 — the only honest way to compare growth across
    series whose absolute sizes differ by 40x."""
    d=defaultdict(float)
    for r in CONF:
        d[(r['ad_type'], r['booking_date'][:4])]+=n(r,'net_amount')
    yrs=['2022','2023','2024']
    series=[('Branded Content',S4),('Digital',S3),('Display',S1),
            ('Classified',GRAY_D),('Supplement',S2)]

    fig,ax=plt.subplots(figsize=(9.6,5.2))
    ax.axhline(100, color=BASELINE, linewidth=1.2, zorder=2)
    ax.text(1.0, 102, 'flat vs 2022', fontsize=9.5, color=MUTED, ha='center')

    ends=[]
    for t,c in series:
        v=[d[(t,y)] for y in yrs]
        idx=[x/v[0]*100 for x in v]
        ax.plot(yrs, idx, color=c, linewidth=2.6, marker='o', markersize=6.5,
                markeredgecolor=SURFACE, markeredgewidth=1.8, zorder=4)
        ends.append([idx[-1], t, c, v[-1]])

    # de-collide the right-hand labels
    ends.sort(key=lambda e:-e[0])
    MINGAP=11.5
    for i in range(1,len(ends)):
        if ends[i-1][0]-ends[i][0] < MINGAP:
            ends[i][0]=ends[i-1][0]-MINGAP
    for y,t,c,absv in ends:
        ax.add_patch(plt.Rectangle((2.08,y-3.4),0.045,6.8,facecolor=c,
                     edgecolor='none',clip_on=False,zorder=5))
        ax.text(2.16, y+2.2, t, color=INK if c!=GRAY_D else MUTED,
                fontsize=11, fontweight='bold', va='center')
        ax.text(2.16, y-4.0, f'₹{absv/1e7:.2f} Cr today',
                color=MUTED, fontsize=9.5, va='center')

    title(ax,'Branded Content and Digital are up ~70%. Print supplements are down 35%.',
          'Net revenue indexed to 2022 = 100, with today\u2019s absolute size on the right')
    ax.set_xlim(-0.15, 3.05); ax.set_ylim(55, 185)
    softgrid(ax); ax.tick_params(axis='x', labelsize=11.5, bottom=False)
    ax.set_ylabel('Index (2022 = 100)', fontsize=10.5, color=MUTED)
    return finish(fig,'t3_trend')

# ============================================================
# TYPE 4 — COMPOSITION  (100% stacked, 2px surface gaps)
# ============================================================
def t4_composition():
    d=defaultdict(float)
    for r in CONF: d[(r['ad_type'], r['booking_date'][:4])]+=n(r,'net_amount')
    yrs=['2022','2023','2024']
    order=['Display','Supplement','Digital','Branded Content','Classified']
    cols=[S1,S2,S3,S4,GRAY]
    tot={y:sum(d[(t,y)] for t in order) for y in yrs}

    fig,ax=plt.subplots(figsize=(9,5))
    bottom=np.zeros(3)
    for t,c in zip(order,cols):
        share=np.array([d[(t,y)]/tot[y]*100 for y in yrs])
        ax.bar(yrs, share, bottom=bottom, color=c, width=0.5,
               edgecolor=SURFACE, linewidth=2, zorder=3)
        for i,(s,b) in enumerate(zip(share,bottom)):
            if s>4.5:
                ax.text(i, b+s/2, f'{s:.0f}%', ha='center', va='center',
                        fontsize=10, color='white' if c in (S1,S2,S6) else INK,
                        fontweight='bold')
        bottom+=share
    # direct labels on right: ink text + colour chip carries identity
    bottom=0
    for t,c in zip(order,cols):
        s=d[(t,'2024')]/tot['2024']*100
        y=bottom+s/2
        ax.add_patch(plt.Rectangle((2.30,y-1.6),0.075,3.2,facecolor=c,
                     edgecolor='none',clip_on=False,zorder=4))
        ax.text(2.42, y, t, color=INK if c!=GRAY else MUTED,
                fontsize=10.5, va='center', fontweight='bold')
        bottom+=s
    title(ax,'Digital + Branded Content grew from 12% to 20% of the mix',
          'Share of net revenue by ad type · % of year total')
    ax.set_ylim(0,100); ax.set_xlim(-0.5,3.3)
    ax.spines['left'].set_visible(False)
    ax.tick_params(axis='y', left=False, labelleft=False)
    ax.tick_params(axis='x', labelsize=11.5, bottom=False)
    return finish(fig,'t4_composition')

# ============================================================
# TYPE 5 — DISTRIBUTION  (single hue + mean/median markers)
# ============================================================
def t5_distribution():
    v=np.array([n(r,'net_amount') for r in CONF])/1e5
    clip=v[v<=12]
    mean=v.mean(); med=np.median(v)
    fig,ax=plt.subplots(figsize=(9.4,4.8))
    ax.hist(clip, bins=45, color=S1, edgecolor=SURFACE, linewidth=0.6, zorder=3)
    ax.axvline(med, color=S6, linewidth=2.4, zorder=4)
    ax.axvline(mean, color=CRITICAL, linewidth=2.4, zorder=4)
    ymax=ax.get_ylim()[1]
    ax.text(med+0.22, ymax*0.90, f'Median ₹{med:.2f}L', color=S6, fontsize=12,
            fontweight='bold', va='center')
    ax.text(med+0.22, ymax*0.83, 'half of all deals are smaller than this',
            color=MUTED, fontsize=9.5, va='center')
    ax.text(mean+0.22, ymax*0.63, f'Mean ₹{mean:.2f}L', color=CRITICAL, fontsize=12,
            fontweight='bold', va='center')
    ax.text(mean+0.22, ymax*0.56, 'dragged up by a handful of whales',
            color=MUTED, fontsize=9.5, va='center')
    title(ax,'The average deal is 2.3× the size of the typical deal',
          'Confirmed deal value · ₹ lakh · tail beyond ₹12L trimmed so the shape is visible')
    ax.set_xlabel('Deal value (₹ lakh)', fontsize=10.5, color=MUTED)
    ax.set_ylabel('Number of deals', fontsize=10.5, color=MUTED)
    softgrid(ax)
    return finish(fig,'t5_distribution')

# ============================================================
# TYPE 6 — CORRELATION  (scatter, 1 series, r annotated)
# ============================================================
def t6_correlation():
    x=np.array([n(r,'discount_pct') for r in CONF])
    y=np.array([n(r,'net_amount') for r in CONF])/1e5
    m=y<=15
    fig,ax=plt.subplots(figsize=(9,4.9))
    ax.scatter(x[m], y[m], s=22, color=GRAY_D, alpha=0.40,
               edgecolors='none', zorder=3)
    z=np.polyfit(x,y,1); xs=np.linspace(0,55,10)
    ax.plot(xs, np.polyval(z,xs), color=S1, linewidth=2.6,
            linestyle=(0,(5,3)), zorder=4)
    ax.text(38, 13.4, 'r = −0.05', fontsize=15, fontweight='bold', color=S1)
    ax.text(38, 12.3, 'No relationship', fontsize=11, color=MUTED)
    title(ax,'Deeper discounts do not buy bigger deals',
          'Each dot is one confirmed booking · discount % vs deal value')
    ax.set_xlabel('Discount given (%)', fontsize=10.5, color=MUTED)
    ax.set_ylabel('Deal value (₹ lakh)', fontsize=10.5, color=MUTED)
    ax.set_xlim(-2,57); ax.set_ylim(0,15.5); softgrid(ax)
    return finish(fig,'t6_correlation')

# ============================================================
# TYPE 7 — OUTLIERS  (emphasis: gray normal, critical outliers)
# ============================================================
def t7_outliers():
    v=np.array([n(r,'net_amount') for r in CONF])
    med=np.median(v); thr=10*med
    idx=np.arange(len(v))
    rng=np.random.default_rng(7); jit=rng.uniform(-0.34,0.34,len(v))
    normal=v<=thr
    fig,ax=plt.subplots(figsize=(9.4,4.6))
    ax.scatter(v[normal]/1e5, jit[normal], s=16, color=GRAY, alpha=0.55,
               edgecolors='none', zorder=3)
    ax.scatter(v[~normal]/1e5, jit[~normal], s=52, color=CRITICAL, alpha=0.85,
               edgecolors=SURFACE, linewidths=0.8, zorder=4)
    ax.axvline(thr/1e5, color=BASELINE, linewidth=1.4, linestyle=(0,(4,3)), zorder=2)
    ax.text(thr/1e5+1.2, 0.44, f'10× median (₹{thr/1e5:.1f}L)', fontsize=10, color=MUTED)
    share=v[~normal].sum()/v.sum()*100
    ax.text(46, -0.30, f'{(~normal).sum()} deals\n{share:.0f}% of all revenue',
            fontsize=12, color=CRITICAL, fontweight='bold', ha='center')
    title(ax,f'{(~normal).sum()} deals carry {share:.0f}% of the revenue',
          'Every confirmed booking plotted by value · ₹ lakh')
    ax.set_xlabel('Deal value (₹ lakh)', fontsize=10.5, color=MUTED)
    ax.set_ylim(-0.6,0.6); ax.set_yticks([])
    ax.spines['left'].set_visible(False); softgrid(ax,'x')
    return finish(fig,'t7_outliers')

# ============================================================
# TYPE 8 — DECOMPOSITION  (waterfall, diverging)
# ============================================================
def t8_decomposition():
    y23=[r for r in CONF if r['booking_date'][:4]=='2023']
    y24=[r for r in CONF if r['booking_date'][:4]=='2024']
    r23=sum(n(r,'net_amount') for r in y23)/1e7
    r24=sum(n(r,'net_amount') for r in y24)/1e7
    o23,o24=len(y23),len(y24)
    a23,a24=r23/o23,r24/o24
    vol=(o24-o23)*a23          # more orders at old avg
    size=(a24-a23)*o24         # bigger deals
    labels=['2023','More\norders','Bigger\ndeals','2024']
    vals=[r23, vol, size, r24]
    bottoms=[0, r23, r23+vol, 0]
    cols=[GRAY, S1, S1, S1]

    fig,ax=plt.subplots(figsize=(8.4,5))
    ax.bar(labels, vals, bottom=bottoms, color=cols, width=0.52,
           edgecolor=SURFACE, linewidth=2, zorder=3)
    for i in (0,1,2):
        ax.plot([i+0.26, i+1-0.26],[bottoms[i]+vals[i]]*2,
                color=BASELINE, linewidth=1, zorder=2)
    for i,(b,v) in enumerate(zip(bottoms,vals)):
        if i in (0,3):
            ax.text(i, b+v+0.30, f'₹{v:.2f} Cr', ha='center', fontsize=12.5,
                    fontweight='bold', color=INK)
        else:
            pct=v/(r24-r23)*100
            ax.text(i, b+v+0.30, f'+₹{v:.2f} Cr', ha='center', fontsize=12,
                    fontweight='bold', color=S1)
            # share label sits below the step, never inside a thin bar
            ax.text(i, b-0.55, f'{pct:.0f}% of the growth', ha='center', va='top',
                    fontsize=10.5, color=S1, fontweight='bold')
    title(ax,'Revenue grew 21%. Bigger deals did four-fifths of it.',
          'Net revenue bridge, 2023 to 2024 · ₹ crore · the parts sum to the total')
    ax.set_ylim(0,19); softgrid(ax)
    ax.tick_params(axis='x', labelsize=11, bottom=False)
    ax.set_ylabel('₹ crore', fontsize=10.5, color=MUTED)
    return finish(fig,'t8_decomposition')

# ============================================================
# STATS — RATE vs COUNT  (the killer teaching chart)
# ============================================================
def s_rate_vs_count():
    cnt=defaultdict(int); rev=defaultdict(float)
    for r in CONF:
        c=city(r['city']); cnt[c]+=1; rev[c]+=n(r,'net_amount')
    cities=sorted(cnt, key=lambda c:-cnt[c])
    fig,(a1,a2)=plt.subplots(1,2,figsize=(12.4,4.6))

    # counts
    v=[cnt[c] for c in cities]
    cols=[S8 if c=='Pune' else GRAY for c in cities]
    b=a1.barh(cities[::-1], v[::-1], color=cols[::-1], height=0.66, zorder=3)
    for bar,val in zip(b,v[::-1]):
        a1.text(val+4, bar.get_y()+bar.get_height()/2, str(val), va='center',
                fontsize=10.5, color=INK2)
    a1.set_title('COUNT: number of orders', fontsize=13, fontweight='bold',
                 color=INK, loc='left', pad=10)
    a1.set_xlim(0,430); nospine_x(a1); softgrid(a1,'x')
    a1.tick_params(axis='y', labelsize=10.5, left=False)
    a1.text(215,-1.25,'Pune books the most orders',fontsize=11,color=S1,ha='center',fontweight='bold')

    # rate
    byavg=sorted(cities, key=lambda c: rev[c]/cnt[c])
    v2=[rev[c]/cnt[c]/1e5 for c in byavg]
    cols2=[S8 if c=='Pune' else GRAY for c in byavg]
    b2=a2.barh(byavg, v2, color=cols2, height=0.66, zorder=3)
    for bar,val in zip(b2,v2):
        a2.text(val+0.04, bar.get_y()+bar.get_height()/2, f'{val:.2f}', va='center',
                fontsize=10.5, color=INK2)
    a2.set_title('RATE: revenue per order (₹ lakh)', fontsize=13, fontweight='bold',
                 color=INK, loc='left', pad=10)
    a2.set_xlim(0,3.0); nospine_x(a2); softgrid(a2,'x')
    a2.tick_params(axis='y', labelsize=10.5, left=False)
    a2.text(1.5,-1.25,'Pune is 7th of 8 on value per order',fontsize=11,color=S1,ha='center',fontweight='bold')

    fig.suptitle('Pune tops one list and sits second-from-bottom on the other',
                 fontsize=15, fontweight='bold', color=INK, x=0.02, ha='left', y=1.04)
    plt.tight_layout(w_pad=4)
    return finish(fig,'s_rate_vs_count')

# ============================================================
# STATS — SEASONALITY
# ============================================================
def s_seasonality():
    d=defaultdict(lambda: defaultdict(float))
    for r in CONF:
        d[r['booking_date'][:4]][int(r['booking_date'][5:7])]+=n(r,'net_amount')
    months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    fig,ax=plt.subplots(figsize=(9.6,4.8))
    ax.axvspan(8.5,10.5,color=S4,alpha=0.10,zorder=1)
    ax.axvspan(5.5,7.5,color=S8,alpha=0.08,zorder=1)
    ax.text(9.5,0.13,'Festive peak',ha='center',fontsize=10.5,
            color='#8a6000',fontweight='bold')
    ax.text(6.5,0.13,'Monsoon trough',ha='center',fontsize=10.5,
            color='#9b2f2e',fontweight='bold')

    ends=[]
    for y,c in zip(['2022','2023','2024'],[GRAY,GRAY_D,S1]):
        v=[d[y][m]/1e7 for m in range(1,13)]
        ax.plot(months, v, color=c, linewidth=2.8 if y=='2024' else 1.8,
                marker='o' if y=='2024' else None, markersize=5,
                markeredgecolor=SURFACE, markeredgewidth=1.4,
                zorder=4 if y=='2024' else 3)
        ends.append([v[-1], y, c])
    # de-collide the year labels
    ends.sort(key=lambda e:-e[0])
    for i in range(1,len(ends)):
        if ends[i-1][0]-ends[i][0] < 0.17:
            ends[i][0]=ends[i-1][0]-0.17
    for yv,y,c in ends:
        ax.text(11.25, yv, f'  {y}', color=INK if y=='2024' else MUTED,
                fontsize=10.5, fontweight='bold' if y=='2024' else 'normal',
                va='center')
    title(ax,'October runs three times July, all three years',
          'Monthly net revenue · ₹ crore')
    ax.set_ylim(0,2.9); ax.set_xlim(-0.4,12.4); softgrid(ax)
    ax.tick_params(axis='x', labelsize=10.5, bottom=False)
    ax.set_ylabel('₹ crore', fontsize=10.5, color=MUTED)
    return finish(fig,'s_seasonality')

# ============================================================
# STATS — SMALL N
# ============================================================
def s_small_n():
    cats=['Matrimonial','Healthcare','Government','Tech','Retail','Real Estate']
    pct=[240,150,68,22,14,9]; nn=[3,6,14,58,140,260]
    cols=[S1 if k<10 else (WARNING if k<30 else GOOD) for k in nn]
    fig,ax=plt.subplots(figsize=(9.4,4.6))
    b=ax.barh(cats[::-1], pct[::-1], color=cols[::-1], height=0.64, zorder=3)
    for bar,p,k in zip(b,pct[::-1],nn[::-1]):
        ax.text(p+6, bar.get_y()+bar.get_height()/2, f'+{p}%   n={k}',
                va='center', fontsize=11, fontweight='bold',
                color=S1 if k<10 else INK2)
    title(ax,'"Matrimonial up 240%" means 3 deals became 10',
          'Year-on-year growth with the sample size beside it · illustrative cut')
    ax.set_xlim(0,330); nospine_x(ax); softgrid(ax,'x')
    ax.tick_params(axis='y', labelsize=11, left=False)
    for x,c,t in [(10,S1,'n under 10: noise'),(120,WARNING,'n under 30: fragile'),(235,GOOD,'n of 30 or more: usable')]:
        ax.text(x,-1.15,t,fontsize=10.5,color=c,fontweight='bold')
    return finish(fig,'s_small_n')

# ============================================================
# STATS — DATA QUALITY
# ============================================================
def s_quality():
    fig,ax=plt.subplots(figsize=(9.6,4.4))
    ax.axis('off')
    issues=[('13 spellings of 8 city names','"Mumbai", "mumbai", "MUMBAI", "Mumabi", " Delhi", "Delhi "',CRITICAL),
            ('10 rows with blank revenue','Every SUM you run drops them without saying so',CRITICAL),
            ('5 bookings at 95% discount','A typing error, or a deal somebody needs to explain',WARNING),
            ('589 non-confirmed rows','Cancelled and Pending. Leave them in and every total is inflated.',WARNING)]
    for i,(h,d,c) in enumerate(issues):
        y=0.80-i*0.235
        ax.add_patch(plt.Rectangle((0.005,y-0.075),0.99,0.175,facecolor=SURFACE,
                     edgecolor=GRID,linewidth=1.2,transform=ax.transAxes,zorder=2))
        ax.add_patch(plt.Rectangle((0.005,y-0.075),0.006,0.175,facecolor=c,
                     transform=ax.transAxes,zorder=3))
        ax.text(0.03,y+0.045,h,transform=ax.transAxes,fontsize=12.5,fontweight='bold',color=INK,va='center')
        ax.text(0.03,y-0.025,d,transform=ax.transAxes,fontsize=10.5,color=INK2,va='center')
    ax.text(0,1.0,'What Step 2 turned up in 3,079 rows',transform=ax.transAxes,
            fontsize=15,fontweight='bold',color=INK,va='bottom')
    return finish(fig,'s_quality')

# ============================================================
# DIAGRAM — 7-step process ladder
# ============================================================
def d_process():
    steps=[('1','CONTEXT','Whose decision, and when do they need it?'),
           ('2','SHAPE','Rows, columns, date range, what is broken.'),
           ('3','TOTAL','Start at the biggest number.'),
           ('4','BREAK DOWN','One dimension at a time.'),
           ('5','COMPARE','Against last year, the plan, or a peer.'),
           ('6','DRIVERS','Why it moved. The parts have to add up.'),
           ('7','VALIDATE','Would I put my name on this?')]
    fig,ax=plt.subplots(figsize=(10.4,5.8))
    ax.set_xlim(0,10); ax.set_ylim(0,7.6); ax.axis('off')
    for i,(num_,name,desc) in enumerate(steps):
        y=6.9-i*0.95
        w=3.1+i*0.86
        ax.add_patch(plt.Rectangle((0.55,y-0.34),w,0.68,facecolor=S1,
                     alpha=0.14+i*0.028,edgecolor='none',zorder=2))
        ax.add_patch(plt.Circle((0.55,y),0.235,color=S1,zorder=4))
        ax.text(0.55,y,num_,ha='center',va='center',fontsize=11.5,
                fontweight='bold',color='white',zorder=5)
        ax.text(1.0,y,name,fontsize=12.5,fontweight='bold',color=INK,va='center')
        ax.text(3.35,y,desc,fontsize=10.5,color=INK2,va='center')
    ax.annotate('', xy=(0.16,0.55), xytext=(0.16,6.9),
                arrowprops=dict(arrowstyle='-|>',color=BASELINE,lw=1.6))
    ax.text(0.0,3.7,'W I D E   t o   N A R R O W',rotation=90,fontsize=9.5,
            color=MUTED,va='center',ha='center',fontweight='bold')
    ax.text(0.55,7.42,'Seven steps, in this order',fontsize=15,
            fontweight='bold',color=INK,va='bottom')
    return finish(fig,'d_process')

# ============================================================
# DIAGRAM — chart decision tree
# ============================================================
def d_chart_tree():
    rows=[('How things compare','BAR — horizontal, sorted',S1),
          ("Who's best and worst",'BAR — sorted, ends highlighted',S1),
          ('How it moved over time','LINE',S3),
          ('What makes up the total','STACKED BAR  (pie only if ≤ 4 parts)',S2),
          ('How values are spread','HISTOGRAM',S4),
          ('Whether X and Y relate','SCATTER',S7),
          ('What drove the change','WATERFALL',S5),
          ('Patterns across two things','HEATMAP',S6),
          ('Exact numbers, few rows','TABLE — not a chart',MUTED)]
    fig,ax=plt.subplots(figsize=(10.6,5.8))
    ax.set_xlim(0,10); ax.set_ylim(0,10); ax.axis('off')
    ax.text(0,9.75,'What are you trying to show?',fontsize=15,fontweight='bold',color=INK,va='bottom')
    for i,(q,chart,c) in enumerate(rows):
        y=8.75-i*0.95
        ax.text(0.12,y,'"'+q+'"',fontsize=11.5,color=INK,va='center')
        ax.annotate('', xy=(5.28,y), xytext=(4.55,y),
                    arrowprops=dict(arrowstyle='-|>',color=BASELINE,lw=1.3))
        ax.add_patch(plt.Rectangle((5.4,y-0.28),4.5,0.56,facecolor=c,alpha=0.16,
                     edgecolor='none',zorder=2))
        ax.add_patch(plt.Rectangle((5.4,y-0.28),0.075,0.56,facecolor=c,
                     edgecolor='none',zorder=3))
        ax.text(5.62,y,chart,fontsize=11.5,fontweight='bold',color=INK,va='center')
    ax.text(0.12,0.05,'Stuck? Use a horizontal bar chart. It is never the wrong answer.',
            fontsize=11.5,color=MUTED,style='italic')
    return finish(fig,'d_chart_tree')

# ============================================================
# DIAGRAM — 8 types map
# ============================================================
def d_eight_types():
    ROT=[S1,S2,S3,S4]   # red, teal, gold, blue in fixed order, repeating
    types=[('1','COMPARISON','This against that',ROT[0]),
           ('2','RANKING','Who is on top',ROT[1]),
           ('3','TREND','What changed over time',ROT[2]),
           ('4','COMPOSITION','What makes up the whole',ROT[3]),
           ('5','DISTRIBUTION','How the values spread',ROT[0]),
           ('6','CORRELATION','Whether they move together',ROT[1]),
           ('7','OUTLIERS','What looks wrong',ROT[2]),
           ('8','DECOMPOSITION','Why it moved',ROT[3])]
    fig,ax=plt.subplots(figsize=(11.6,5.4))
    ax.set_xlim(0,12); ax.set_ylim(0.9,6.35); ax.axis('off')
    for i,(num_,name,desc,c) in enumerate(types):
        col=i%4; row=i//4
        x=0.1+col*2.95; y=3.25-row*2.15
        ax.add_patch(plt.Rectangle((x,y),2.72,1.72,facecolor=c,alpha=0.11,
                     edgecolor='none',zorder=2))
        ax.add_patch(plt.Rectangle((x,y),2.72,0.055,facecolor=c,zorder=3))
        ax.text(x+0.18,y+1.32,num_,fontsize=21,fontweight='bold',color=c,va='center')
        ax.text(x+0.62,y+1.33,name,fontsize=12,fontweight='bold',color=INK,va='center')
        ax.text(x+0.18,y+0.62,desc,fontsize=10.5,color=INK2,va='center')
    ax.text(0.1,6.05,'Eight ways to ask a dataset something',fontsize=15,
            fontweight='bold',color=INK,va='bottom')
    ax.text(0.1,5.62,'Types 1 to 3 cover most of what you get asked. 6 to 8 are the ones people skip.',
            fontsize=10.5,color=MUTED,va='bottom')
    return finish(fig,'d_eight_types')

# ============================================================
# WRONG vs RIGHT chart
# ============================================================
def d_wrong_right():
    d=defaultdict(float)
    for r in CONF: d[r['ad_type']]+=n(r,'net_amount')
    labels=list(d.keys()); vals=[v/1e7 for v in d.values()]
    fig,(a1,a2)=plt.subplots(1,2,figsize=(12.6,5))

    # WRONG: 3D-ish pie, rainbow, legend
    a1.pie(vals, labels=None, autopct='%1.1f%%',
           colors=['#e74c3c','#3498db','#2ecc71','#9b59b6','#f1c40f'],
           startangle=15, textprops={'fontsize':9},
           wedgeprops={'edgecolor':'black','linewidth':1.4})
    a1.legend(labels, loc='center left', bbox_to_anchor=(-0.28,0.5),
              fontsize=8.5, frameon=True, shadow=True)
    a1.set_title('Revenue Split by Ad Type', fontsize=13, color=INK, pad=12)
    a1.text(0,-1.42,'A topic for a title, five colours, a legend to decode, no sort order',
            ha='center',fontsize=10.5,color=CRITICAL)

    # RIGHT: sorted bar, emphasis
    order=sorted(zip(labels,vals), key=lambda x:x[1])
    nm=[k for k,_ in order]; vv=[v for _,v in order]
    cols=[S1 if k=='Display' else GRAY for k in nm]
    b=a2.barh(nm, vv, color=cols, height=0.62, zorder=3)
    for bar,v in zip(b,vv):
        a2.text(v+0.35, bar.get_y()+bar.get_height()/2, f'₹{v:.1f} Cr',
                va='center', fontsize=11, color=INK2)
    a2.set_title('Display alone is 63% of all ad revenue', fontsize=13,
                 fontweight='bold', color=INK, loc='left', pad=12)
    a2.set_xlim(0,34); nospine_x(a2); softgrid(a2,'x')
    a2.tick_params(axis='y', labelsize=11, left=False)
    a2.text(17,-1.30,'The finding as the title, one colour, sorted, labels on the bars',
            ha='center',fontsize=10.5,color=S1)
    plt.tight_layout(w_pad=5)
    return finish(fig,'d_wrong_right')

# ============================================================
if __name__=='__main__':
    fns=[t1_comparison,t2_ranking,t3_trend,t4_composition,t5_distribution,
         t6_correlation,t7_outliers,t8_decomposition,s_rate_vs_count,
         s_seasonality,s_small_n,s_quality,d_process,d_chart_tree,
         d_eight_types,d_wrong_right]
    for f in fns:
        print(f'  {f.__name__:22s} -> {os.path.basename(f())}')
    print(f'\n{len(fns)} images in {IMG}')
