"""
READING DATA — enterprise course build
Aurex brand. Named frameworks, credential bar, module wayfinding,
practitioner war stories, reference-artefact density.
"""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from PIL import Image
import os

IMG='/private/tmp/claude-502/-Users-dishantsingla-Downloads-projects-aurex-backend/affd460f-5448-4470-a3bb-58de722ad050/scratchpad/img'
OUT='/Users/dishantsingla/Downloads/Reading-Data-Masterclass.pptx'

# ---- Aurex tokens ----
RED   =RGBColor(0xE0,0x1E,0x29); RED_D=RGBColor(0xB5,0x1D,0x2A)
MAROON=RGBColor(0x8F,0x00,0x13); TEAL =RGBColor(0x0E,0x8F,0x7A)
GOLD  =RGBColor(0xC7,0x9A,0x2F); BLUE =RGBColor(0x4E,0x79,0xCF)
INK   =RGBColor(0x12,0x11,0x11); INK2 =RGBColor(0x4A,0x48,0x47)
BODY  =RGBColor(0x5F,0x5D,0x5C); MUTED=RGBColor(0x8A,0x85,0x7F)
FAINT =RGBColor(0xB0,0xAA,0xA4)
GRID  =RGBColor(0xE4,0xE0,0xDB); HAIR =RGBColor(0xD6,0xD1,0xCA)
SURF  =RGBColor(0xFB,0xF9,0xF8); PLANE=RGBColor(0xF4,0xF0,0xEB)
CARD  =RGBColor(0xFF,0xFF,0xFF); TINT =RGBColor(0xFD,0xEC,0xEC)
TEAL_T=RGBColor(0xE6,0xF2,0xEF); GOLD_T=RGBColor(0xFA,0xF3,0xE4)
BLUE_T=RGBColor(0xEF,0xF3,0xFC)
DARK  =RGBColor(0x1A,0x18,0x18); DARK2=RGBColor(0x26,0x23,0x22)
WHITE =RGBColor(0xFF,0xFF,0xFF)
F='Helvetica Neue'
W=13.333; H=7.5

prs=Presentation(); prs.slide_width=Inches(W); prs.slide_height=Inches(H)

MODULES=['THE SEVEN-STEP READ','THE EIGHT LENSES','THE CHART SELECTOR',
         'THE SIX DISTORTIONS','THE FIVE-CHECK GATE']
_state={'mod':0,'n':0}

# ---------------- primitives ----------------
def _noshadow(sh):
    spPr=sh._element.spPr
    for t in ('a:effectLst','a:effectDag'):
        for e in spPr.findall(qn(t)): spPr.remove(e)
    spPr.append(spPr.makeelement(qn('a:effectLst'),{}))
    st=sh._element.find(qn('p:style'))
    if st is not None:
        r=st.find(qn('a:effectRef'))
        if r is not None: r.set('idx','0')

def rect(s,l,t,w,h,fill,line=None,lw=0.75):
    sh=s.shapes.add_shape(MSO_SHAPE.RECTANGLE,Inches(l),Inches(t),Inches(w),Inches(h))
    sh.fill.solid(); sh.fill.fore_color.rgb=fill
    if line: sh.line.color.rgb=line; sh.line.width=Pt(lw)
    else: sh.line.fill.background()
    sh.shadow.inherit=False; _noshadow(sh); return sh

def oval(s,l,t,d,fill):
    sh=s.shapes.add_shape(MSO_SHAPE.OVAL,Inches(l),Inches(t),Inches(d),Inches(d))
    sh.fill.solid(); sh.fill.fore_color.rgb=fill; sh.line.fill.background()
    sh.shadow.inherit=False; _noshadow(sh); return sh

def tx(s,l,t,w,h,text,size=18,bold=False,color=INK,align=PP_ALIGN.LEFT,
       space=1.24,track=None,caps=False,font=F):
    b=s.shapes.add_textbox(Inches(l),Inches(t),Inches(w),Inches(h))
    tf=b.text_frame; tf.word_wrap=True
    for i,line in enumerate(str(text).split('\n')):
        p=tf.paragraphs[0] if i==0 else tf.add_paragraph()
        p.text=line; p.alignment=align; p.line_spacing=space
        p.space_after=Pt(size*0.28)
        f_=p.font; f_.size=Pt(size); f_.bold=bold; f_.color.rgb=color; f_.name=font
        if track is not None:
            for r in p.runs: r.font._rPr.set('spc',str(int(track*100)))
        if caps:
            for r in p.runs: r.font._rPr.set('cap','all')
    return b

def kicker(s,l,t,text,color=RED,size=10.5):
    return tx(s,l,t,9,0.32,text,size,True,color,track=1.4)

def slide(bg=SURF,chrome=True,mod=None):
    s=prs.slides.add_slide(prs.slide_layouts[6])
    s.background.fill.solid(); s.background.fill.fore_color.rgb=bg
    _state['n']+=1
    if chrome:
        dark = bg in (DARK,DARK2)
        m=_state['mod'] if mod is None else mod
        if m:
            lab=f'MODULE {m}   ·   {MODULES[m-1]}'
            tx(s,7.55,0.30,5.15,0.3,lab,9,True,
               FAINT if dark else MUTED,align=PP_ALIGN.RIGHT,track=1.2)
        tx(s,12.05,H-0.52,0.68,0.3,f'{_state["n"]:02d}',9,True,
           FAINT if dark else MUTED,align=PP_ALIGN.RIGHT)
    return s

def rule(s,l,t,w,color=RED,h=0.045): return rect(s,l,t,w,h,color)
def hair(s,l,t,w): return rect(s,l,t,w,0.012,GRID)

def fit(name,mw,mh):
    with Image.open(f'{IMG}/{name}.png') as im: pw,ph=im.size
    r=min(mw/pw,mh/ph); return pw*r,ph*r

def img_fit(s,name,mw,mh,top,cx=None):
    w,h=fit(name,mw,mh); left=(W-w)/2 if cx is None else cx-w/2
    s.shapes.add_picture(f'{IMG}/{name}.png',Inches(left),Inches(top),
                         width=Inches(w),height=Inches(h))
    return w,h

# ---------------- templates ----------------
def cover():
    s=slide(SURF,chrome=False)
    rect(s,0,0,W,0.22,RED)
    kicker(s,0.95,1.02,'AUREX  ·  BCCL’S SECURE AI WORKSPACE',RED,11)
    tx(s,0.92,1.62,11.8,1.7,'Reading data',66,True,INK,track=-1.6)
    tx(s,0.95,3.42,10.2,1.1,
       'A working method for getting from a spreadsheet you did not build\nto a number you would defend in front of your MD.',
       21,False,BODY,space=1.34)
    rule(s,0.95,4.82,2.2,RED,0.05)
    # credential strip
    rect(s,0.95,5.22,11.45,1.16,PLANE)
    rect(s,0.95,5.22,0.06,1.16,RED)
    tx(s,1.28,5.42,5.4,0.34,'DISHANT SINGLA',13,True,INK,track=0.9)
    tx(s,1.28,5.76,5.6,0.5,'B.Tech, IIT Roorkee 2015  ·  Founder, Base42 Systems',
       11.5,False,BODY)
    creds=[('₹110 Cr','ad business on the\nplatform I built'),
           ('1 Bn+','ad impressions\na month'),
           ('200 M','monthly active\nusers'),
           ('120 M','Ola customer\nprofiles built')]
    x=6.62
    for i,(n_,l_) in enumerate(creds):
        if i: rect(s,x-0.20,5.42,0.008,0.76,HAIR)
        tx(s,x,5.40,1.5,0.4,n_,17,True,RED,track=-0.3)
        tx(s,x,5.78,1.55,0.5,l_,8.5,False,MUTED,space=1.16)
        x+=1.46
    tx(s,0.95,6.66,11.5,0.4,
       'Tuesday 4 August 2026   ·   2:30–4:30 PM IST   ·   Live, hands-on   ·   Bring a laptop',
       11.5,False,MUTED,track=0.4)
    return s

def divider(num,title_,sub,accent=RED,lead=None):
    _state['mod']=num
    s=slide(DARK,mod=num)
    rect(s,0,0,W,0.22,accent)
    tx(s,0.95,1.42,6,0.4,f'MODULE {num} OF 5',10,True,accent,track=1.6)
    tx(s,0.92,2.02,3,1.6,f'{num:02d}',78,True,DARK2 if False else RGBColor(0x3A,0x35,0x33),
       track=-2.0)
    tx(s,0.95,3.42,11.2,1.2,title_,40,True,WHITE,track=-0.9)
    rule(s,0.95,4.86,2.0,accent,0.05)
    tx(s,0.95,5.20,10.4,1.3,sub,18,False,RGBColor(0xBC,0xB6,0xB0),space=1.32)
    if lead:
        tx(s,0.95,6.52,11.2,0.4,lead,11,True,accent,track=1.1)
    return s

def _wrapped(text,size,box_w):
    """Rough rendered line count: source breaks plus wrapping."""
    cpl=max(8,int(box_w*72/(size*0.495)))
    n=0
    for ln in text.split('\n'):
        n+=max(1,-(-len(ln)//cpl))
    return n

def statement(head,sub=None,accent=RED):
    s=slide(SURF)
    rect(s,0,0,W,0.22,accent)
    BW=11.55
    # pick the largest size that still renders in <=3 lines, then measure it
    for size in (46,40,34,30):
        lines=_wrapped(head,size,BW)
        if lines<=(1 if size==46 else 2 if size==40 else 3): break
    hh=lines*(size*1.20+size*0.28)/72.0
    top=(H-hh-(0.95 if sub else 0))/2
    tx(s,0.95,top,BW,hh+0.35,head,size,True,INK,space=1.20,track=-0.7)
    if sub:
        rule(s,0.95,top+hh+0.28,1.5,accent,0.035)
        tx(s,0.95,top+hh+0.55,10.9,0.9,sub,18,False,BODY,space=1.34)
    return s

def titled(head,sub=None,accent=RED,bg=SURF):
    """Standard content slide header. Returns (slide, content_top)."""
    s=slide(bg)
    rect(s,0,0,W,0.22,accent)
    tx(s,0.95,0.72,11.4,0.6,head,27,True,INK,track=-0.5)
    y=1.46
    if sub:
        tx(s,0.95,1.34,11.4,0.5,sub,13.5,False,MUTED); y=1.92
    hair(s,0.95,y-0.20,11.45)
    return s,y

def chart_slide(name,lens,finding,note,accent=RED):
    s=slide(SURF)
    rect(s,0,0,W,0.22,accent)
    kicker(s,0.95,0.34,lens,accent,10)
    top=0.92
    nh=0.34 if len(note)<100 else 0.62
    w,h=img_fit(s,name,11.9,H-top-nh-0.86,top)
    yb=top+h+0.24
    hair(s,0.95,yb,11.45)
    tx(s,0.95,yb+0.16,11.4,nh,note,13.5,False,BODY,space=1.30)
    return s

def full_img(name,lens=None,accent=RED):
    s=slide(SURF)
    rect(s,0,0,W,0.22,accent)
    if lens: kicker(s,0.95,0.34,lens,accent,10)
    img_fit(s,name,12.2,H-0.92-0.62,0.92)
    return s

def lens_card(num,name,question,onfile,trap,accent):
    s=slide(SURF)
    rect(s,0,0,W,0.22,accent)
    kicker(s,0.95,0.34,f'LENS {num} OF 8',accent,10)
    tx(s,0.92,0.86,1.5,1.2,f'{num}',72,True,accent,track=-2.0)
    tx(s,2.05,1.16,10.4,0.8,name,34,True,INK,track=-0.7)
    hair(s,0.95,2.36,11.45)
    cols=[('THE QUESTION IT ANSWERS',question,accent,PLANE),
          ('ON TODAY’S FILE',onfile,MUTED,PLANE),
          ('THE TRAP IT HIDES',trap,RED_D,TINT)]
    x=0.95
    for k,body,c,bg in cols:
        rect(s,x,2.72,3.63,2.34,bg)
        rect(s,x,2.72,0.055,2.34,c)
        tx(s,x+0.28,2.92,3.1,0.3,k,9.5,True,c,track=1.1)
        tx(s,x+0.28,3.30,3.15,1.6,body,15.5,False,INK,space=1.30)
        x+=3.91
    tx(s,0.95,5.42,11.4,0.4,'Next: the same lens run on 2,490 confirmed bookings.',
       13,False,MUTED)
    return s

def war_story(tag,head,body,pull,pulllabel,lesson):
    s=slide(DARK2)
    rect(s,0,0,W,0.22,GOLD)
    tx(s,0.95,0.60,6,0.34,tag,10,True,GOLD,track=1.5)
    tx(s,0.95,1.06,7.3,1.5,head,29,True,WHITE,space=1.20,track=-0.6)
    tx(s,0.95,2.72,7.3,2.5,body,15.5,False,RGBColor(0xC4,0xBE,0xB8),space=1.42)
    # pull-out
    rect(s,8.85,1.06,3.55,2.9,RGBColor(0x33,0x2F,0x2E))
    rect(s,8.85,1.06,0.055,2.9,GOLD)
    tx(s,9.18,1.42,3.0,1.0,pull,50,True,GOLD,track=-1.6)
    tx(s,9.18,2.52,3.0,1.2,pulllabel,12.5,False,RGBColor(0xB0,0xA9,0xA2),space=1.30)
    rule(s,0.95,5.62,1.6,GOLD,0.04)
    tx(s,0.95,5.90,11.4,0.8,lesson,17,True,WHITE,space=1.28)
    return s

def prompt_slide(head,prompt,expect,accent=RED):
    s=slide(PLANE)
    rect(s,0,0,W,0.22,accent)
    tx(s,0.95,0.66,11.4,0.55,head,25,True,INK,track=-0.5)
    tx(s,0.95,1.24,11.4,0.4,'Paste this, do not type it. The wording is the lesson.',
       12.5,False,MUTED)
    box=rect(s,0.95,1.82,7.35,4.86,CARD,GRID,1.0)
    tf=box.text_frame; tf.word_wrap=True
    tf.margin_left=Inches(0.32); tf.margin_right=Inches(0.20)
    tf.margin_top=Inches(0.26); tf.margin_bottom=Inches(0.12)
    for i,l in enumerate(prompt.split('\n')):
        p=tf.paragraphs[0] if i==0 else tf.add_paragraph()
        p.text=l; p.alignment=PP_ALIGN.LEFT; p.line_spacing=1.34
        p.font.size=Pt(11.5); p.font.name='Courier New'; p.font.color.rgb=INK2
    rect(s,8.62,1.82,3.78,4.86,CARD,GRID,1.0)
    rect(s,8.62,1.82,0.055,4.86,accent)
    tx(s,8.95,2.10,3.2,0.3,'WHAT COMES BACK',9.5,True,accent,track=1.1)
    y=2.56
    for e in expect:
        oval(s,8.95,y+0.09,0.10,accent)
        tx(s,9.22,y,2.95,0.9,e,13.5,False,INK,space=1.28)
        y+=0.86
    return s

def handson(minutes,task,chat,accent=TEAL):
    s=slide(TEAL_T)
    rect(s,0,0,W,0.22,accent)
    rect(s,0.95,0.62,2.55,0.42,accent)
    tx(s,1.12,0.68,2.3,0.32,f'HANDS-ON · {minutes} MIN',10,True,WHITE,track=0.9)
    y=1.62
    for i,t in enumerate(task):
        tx(s,1.32,y,10.9,0.7,t,22,False,INK,space=1.26)
        oval(s,0.95,y+0.14,0.22,accent)
        y+=0.86
    rule(s,0.95,y+0.42,11.45,accent,0.035)
    tx(s,0.95,y+0.72,11.4,0.6,f'Post in chat:  “{chat}”',19,True,RGBColor(0x0A,0x6B,0x5B))
    return s

def numbered(head,items,sub=None,accent=RED,bg=SURF):
    s,y=titled(head,sub,accent,bg)
    n=len(items); gap=min(1.02,(H-y-0.72)/n)
    y+=(H-y-0.62-n*gap)/2
    for i,it in enumerate(items):
        c=oval(s,0.98,y+0.08,0.44,accent)
        p=c.text_frame.paragraphs[0]; p.text=str(i+1); p.alignment=PP_ALIGN.CENTER
        p.font.size=Pt(13.5); p.font.bold=True; p.font.color.rgb=WHITE; p.font.name=F
        if isinstance(it,tuple):
            tx(s,1.66,y-0.02,10.9,0.42,it[0],18.5,True,INK)
            tx(s,1.66,y+0.36,10.9,0.5,it[1],14,False,BODY)
        else:
            tx(s,1.66,y+0.04,10.9,gap,it,18.5,False,INK,space=1.26)
        y+=gap
    return s

def table(head,sub,cols,rows,widths,accent=RED,rowh=0.62,fs=12.5):
    s,y=titled(head,sub,accent)
    xs=[0.95]
    for w in widths[:-1]: xs.append(xs[-1]+w)
    # header
    for x,w,c in zip(xs,widths,cols):
        tx(s,x,y,w-0.16,0.3,c,9.5,True,accent,track=1.1)
    y+=0.42; rect(s,0.95,y-0.10,11.45,0.018,HAIR)
    for r in rows:
        for i,(x,w,cell) in enumerate(zip(xs,widths,r)):
            bold=(i==0)
            tx(s,x,y+0.06,w-0.18,rowh,cell,fs,bold,
               INK if bold else BODY,space=1.22)
        y+=rowh; hair(s,0.95,y-0.06,11.45)
    return s

# ================= BUILD =================
cover()

# ---- 01 credentials / the buzz ----
s=slide(DARK,chrome=True)
rect(s,0,0,W,0.22,RED)
tx(s,0.95,0.72,6,0.34,'WHO IS RUNNING THIS SESSION',10,True,RED,track=1.5)
tx(s,0.92,1.20,7.6,1.4,'I have spent eight years building\nthe systems these numbers come out of.',
   28,True,WHITE,space=1.22,track=-0.6)
tx(s,0.95,2.92,7.4,1.6,
   'Ola, Koo, Khatabook, Wealthy, HT Media. Customer data platforms, identity '
   'resolution, recommendation systems, ad targeting. Most recently the central '
   'data platform at HT Digital Streams, sitting under a ₹110 crore a year '
   'ad business.',15.5,False,RGBColor(0xC4,0xBE,0xB8),space=1.44)
tx(s,0.95,4.62,7.4,0.9,
   'Every trap in this session is one I have shipped, been burned by, or caught '
   'in review. That is the only reason it is in here.',14.5,False,GOLD,space=1.38)
rect(s,8.72,1.20,3.68,5.16,DARK2)
rect(s,8.72,1.20,0.055,5.16,RED)
tx(s,9.06,1.48,3.1,0.3,'AT SCALE',9.5,True,RED,track=1.2)
mets=[('₹110 Cr','ad revenue running on the platform'),
      ('1 Bn+','ad impressions a month'),
      ('200 M','monthly active users'),
      ('120 M','Ola customer profiles built'),
      ('₹2.5 Cr','a year in retired tooling'),
      ('60%','duplicate IDs eliminated')]
yy=1.88
for n_,l_ in mets:
    tx(s,9.06,yy,3.1,0.36,n_,19.5,True,WHITE,track=-0.5)
    tx(s,9.06,yy+0.40,3.1,0.3,l_,10.5,False,RGBColor(0xA8,0xA1,0x9A))
    yy+=0.755

# ---- 02 the stakes ----
s,y=titled('Why a company pays for this',
           'The gap between a number that survives scrutiny and one that does not')
left=[('The number nobody checked','A board pack goes out with a metric computed on the wrong '
       'date column. Three months of decisions get anchored to it.'),
      ('The definition nobody agreed','Two teams present revenue in the same meeting, ₹40 Cr apart. '
       'Both are right. Nobody knows that yet.'),
      ('The trend that was three accounts','A segment is declared a growth engine. One client churns '
       'and the growth engine goes with it.')]
yy=y+0.12
for h_,b_ in left:
    rect(s,0.95,yy,5.55,1.42,TINT)
    rect(s,0.95,yy,0.055,1.42,RED_D)
    tx(s,1.28,yy+0.18,4.95,0.34,h_,15.5,True,INK)
    tx(s,1.28,yy+0.58,4.95,0.8,b_,12.5,False,BODY,space=1.26)
    yy+=1.60
rect(s,7.05,y+0.12,5.35,4.58,PLANE)
rect(s,7.05,y+0.12,0.055,4.58,TEAL)
tx(s,7.40,y+0.34,4.6,0.3,'WHAT CHANGES AFTER TODAY',9.5,True,TEAL,track=1.1)
tx(s,7.40,y+0.76,4.62,2.9,
   'Open a file you have never seen. Work out what it actually contains. '
   'Ask it eight questions that surface something. Then put a number in front '
   'of a decision-maker with the caveat already attached.\n\n'
   'None of that needs Excel skill or statistics training. It needs the '
   'sequence, and it needs to know where numbers go wrong.',
   14,False,INK,space=1.42)
rect(s,7.40,y+3.58,4.62,0.014,HAIR)
tx(s,7.40,y+3.78,4.62,0.5,'Aurex does the execution.\nYou do the judgement.',
   15.5,True,TEAL,space=1.26)

# ---- 03 what you leave with ----
s,y=titled('Five frameworks, one file, and the cards to run them again',
           'Everything in this session is designed to be reusable on Monday')
fw=[('01','THE SEVEN-STEP READ','The sequence for any unfamiliar file',RED),
    ('02','THE EIGHT LENSES','Every question a dataset can answer',TEAL),
    ('03','THE CHART SELECTOR','Say the comparison, get the chart',GOLD),
    ('04','THE SIX DISTORTIONS','Where confident numbers go wrong',BLUE),
    ('05','THE FIVE-CHECK GATE','What to verify before you send',RED_D)]
x=0.95
for n_,t_,d_,c in fw:
    rect(s,x,y+0.30,2.16,2.5,PLANE)
    rect(s,x,y+0.30,2.16,0.055,c)
    tx(s,x+0.24,y+0.56,1.7,0.4,n_,22,True,c,track=-0.6)
    tx(s,x+0.24,y+1.06,1.75,0.9,t_,12.5,True,INK,space=1.20)
    tx(s,x+0.24,y+2.00,1.75,0.7,d_,10.5,False,BODY,space=1.22)
    x+=2.30
hair(s,0.95,y+3.14,11.45)
tx(s,0.95,y+3.36,11.4,0.4,'YOU ALSO LEAVE WITH',9.5,True,RED,track=1.1)
take=[('The practice file','3,079 rows of real-shaped ad bookings, traps included'),
      ('Eight prompts','One per lens, written to force checkable output'),
      ('The gate card','Five checks, one page, stick it on your monitor')]
x=0.95
for t_,d_ in take:
    tx(s,x,y+3.74,3.5,0.32,t_,15,True,INK)
    tx(s,x,y+4.08,3.5,0.5,d_,12,False,BODY,space=1.24)
    x+=3.85

# ---- 04 the file ----
s,y=titled('One file. Every framework runs on it.',
           'ad-sales-data.csv  ·  three years of advertising bookings, 2022 to 2024')
kpis=[('3,079','rows'),('14','columns'),('8','cities'),
      ('2,490','confirmed bookings'),('₹44.8 Cr','net revenue')]
x=0.95
for n_,l_ in kpis:
    rect(s,x,y+0.10,2.16,1.24,PLANE)
    rect(s,x,y+0.10,0.055,1.24,RED)
    tx(s,x+0.26,y+0.30,1.8,0.44,n_,23,True,INK,track=-0.5)
    tx(s,x+0.26,y+0.80,1.8,0.3,l_,11,False,MUTED)
    x+=2.30
tx(s,0.95,y+1.72,11.4,0.4,'WHAT IS IN IT',9.5,True,RED,track=1.1)
grid=[('Dates','booked and published'),('Cities','8 Indian metros'),
      ('Editions','4 publications'),('Ad types','Display, Digital, Classified, and two more'),
      ('Categories','10 advertiser sectors'),('Reps','30 salespeople'),
      ('Money','rate, discount, gross, net'),('Status','confirmed, cancelled, pending')]
for i,(k,v) in enumerate(grid):
    col=i%2; row=i//2
    xx=0.95+col*5.85; yy=y+2.14+row*0.62
    tx(s,xx,yy,1.5,0.34,k,14,True,INK)
    tx(s,xx+1.55,yy,4.1,0.34,v,14,False,BODY)
hair(s,0.95,y+4.72,11.45)
tx(s,0.95,y+4.92,11.4,0.4,
   'It carries four planted data-quality faults. Finding them is Step 2.',
   14,True,RED_D)

# =========== MODULE 1 ===========
divider(1,'The Seven-Step Read',
        'Analysts do not start with the numbers. They start with the decision,\n'
        'then the shape of the file, and only then the arithmetic.',
        RED,'STEPS 1 TO 7  ·  25 MINUTES')

full_img('d_process','THE FRAMEWORK',RED)

numbered('Step 1 — CONTEXT: three questions before the file opens',
         [('Who decides, and when?','If you cannot name the person and the date, you are producing trivia.'),
          ('Which answer would change the decision?','If every possible finding leads to the same action, do not run the analysis.'),
          ('What is the smallest version you could answer today?','One metric, one dimension, one period. Widen later if it earns it.')],
         sub='Most weak analysis is a correct answer to a question nobody had.')

s,y=titled('What Step 1 sounds like in practice',
           'Same file, same tool, two different opening moves')
rect(s,0.95,y+0.10,5.55,4.5,TINT)
rect(s,0.95,y+0.10,0.055,4.5,RED_D)
tx(s,1.28,y+0.34,4.9,0.3,'WITHOUT A FRAME',9.5,True,RED_D,track=1.1)
tx(s,1.28,y+0.74,4.9,0.5,'“Analyse this file.”',21,True,INK)
tx(s,1.28,y+1.48,4.9,2.4,'Revenue rose 4.3%\n8 cities represented\n3,079 rows\n'
   'Q3 shows a dip\nAverage deal ₹1.8 lakh',14.5,False,BODY,space=1.52)
hair(s,1.28,y+3.72,4.9)
tx(s,1.28,y+3.92,4.9,0.5,'All of it true. None of it usable.',14,True,RED_D)
rect(s,6.85,y+0.10,5.55,4.5,TEAL_T)
rect(s,6.85,y+0.10,0.055,4.5,TEAL)
tx(s,7.18,y+0.34,4.9,0.3,'WITH A FRAME',9.5,True,TEAL,track=1.1)
tx(s,7.18,y+0.74,4.9,0.8,'“Which two cities should lose\nheadcount next quarter?”',
   19,True,INK,space=1.22)
tx(s,7.18,y+1.78,4.9,2.1,'One table\nRevenue per rep, by city\n'
   'Two cities named\nA caveat about deal mix',14.5,False,BODY,space=1.52)
hair(s,7.18,y+3.72,4.9)
tx(s,7.18,y+3.92,4.9,0.5,'One question, and the file has a job.',14,True,TEAL)

full_img('s_quality','STEP 2 — SHAPE: WHAT DID THE FILE ACTUALLY ARRIVE AS',RED)

war_story('WAR STORY · HT DIGITAL STREAMS  ·  IDENTITY RESOLUTION',
 'We were counting the same person up to four times.',
 'Three sites and a set of APIs, each minting its own user ID. Every audience '
 'number the business planned against was inflated, and nobody could see it, '
 'because each system was internally consistent.\n\n'
 'The fix was not analytical. It was going back to what one row meant, across '
 'four systems that had each quietly decided for themselves.',
 '60%','of duplicate IDs eliminated once the grain was defined once, centrally',
 'Step 2 exists because “what is one row?” is the question that was never asked.')

statement('Spend the first two minutes\non what the file is.',
          'Somebody filtered it, named the columns and decided what to leave out before it '
          'reached you. Those decisions are now your assumptions, whether you look at them or not.',
          RED)

# =========== MODULE 2 ===========
divider(2,'The Eight Lenses',
        'Almost every question you will be handed is one of these eight.\n'
        'Naming the lens tells you the cut, the chart, and the trap to check.',
        TEAL,'LENSES 1 TO 8  ·  40 MINUTES')

table('The Eight Lenses, on one page',
      'The reference artefact for this module. Photograph this slide.',
      ['LENS','THE QUESTION','THE CUT','THE TRAP IT HIDES'],
      [['1  Comparison','How does this stack up against that?','Total by dimension, sorted','Counts where rates belong'],
       ['2  Ranking','Who is on top, who is at the bottom?','Sort both ends, not just the top','A top-10 list with no bottom'],
       ['3  Trend','What changed, and when exactly?','Index to a common base','Two scales on one chart'],
       ['4  Composition','What makes up the whole?','Share of total, by period','Mix shift read as performance'],
       ['5  Distribution','What does a typical one look like?','Histogram, plus the median','The mean quoted as typical'],
       ['6  Correlation','Do these move together?','Scatter, then a coefficient','Correlation stated as cause'],
       ['7  Outliers','What looks wrong?','Flag against the median','Concentration read as a trend'],
       ['8  Decomposition','Why did the number move?','Bridge that sums to the total','A residual nobody names']],
      [2.06,3.55,2.98,2.86],TEAL,rowh=0.545,fs=12)

LENS=[(1,'COMPARISON','How does this one stack up against that one?',
       'Which city bills the most ad revenue?','Mumbai is biggest at everything. Biggest is not the same as best.',RED,
       't1_comparison','Sorted, one colour on the point, numbers on the bars. You will reach for this shape more than any other.'),
      (2,'RANKING','Who is on top, and who is at the bottom?',
       'Which reps carry the business, and which coast?','A top-10 list flatters. The bottom is where the recoverable money sits.',TEAL,
       't2_ranking','Show both ends. A top-5 on its own hides the gap you can actually do something about.'),
      (3,'TREND','What changed over time, and when exactly?',
       'Is digital really growing, or does it just feel that way?','Raw lines let the biggest series bury every other story.',GOLD,
       't3_trend','Indexed to 2022 = 100. When one series is 40× another, plotting raw values shows you the big line and nothing else.'),
      (4,'COMPOSITION','What makes up the total, and is the mix moving?',
       'Print is shrinking. By how much, and into what?','Volume can rise while revenue stalls. That is mix, not performance.',BLUE,
       't4_composition','Mix shift lives here. More of what sold was the cheap thing, so pages went up and money did not.'),
      (5,'DISTRIBUTION','What does a typical one actually look like?',
       'What is a normal deal size here?','A handful of whales drag the average away from reality.',RED,
       't5_distribution','Mean ₹1.80L, median ₹0.79L. Call the mean “typical” in a meeting and you are overstating by 2.3×.'),
      (6,'CORRELATION','Do these two things move together?',
       'Do bigger discounts actually win bigger deals?','Two things moving together is not one causing the other.',TEAL,
       't6_correlation','r = −0.05, so there is nothing here. That is still a result, and it is the one that settles a discount argument.'),
      (7,'OUTLIERS','What looks wrong, and is it real or a data error?',
       'Are a handful of deals carrying the whole year?','A few large deals can manufacture a trend that does not exist.',GOLD,
       't7_outliers','80 deals out of 2,490 carry 22% of revenue. Lose two of them and the trend you were describing goes away.'),
      (8,'DECOMPOSITION','Why did the number move?',
       'Revenue grew 21%. More deals, or bigger ones?','“It went up” is not a driver. Parts that do not sum are not an answer.',BLUE,
       't8_decomposition','The parts have to sum to the whole. An unexplained residual means you do not understand the movement yet.')]

for i,(n_,nm,q,onf,trap,c,img,note) in enumerate(LENS):
    lens_card(n_,nm,q,onf,trap,c)
    chart_slide(img,f'LENS {n_} · {nm}',None,note,c)
    if n_==1:
        prompt_slide('The prompt behind Lens 1',
 'Using the code interpreter on ad-sales-data.csv:\n\n'
 'Filter to status = Confirmed and drop rows\n'
 'where net_amount is blank. Tell me how many\n'
 'rows you dropped.\n\n'
 'The city column has spelling variants. Show me\n'
 'the mapping you intend to apply before you\n'
 'apply it.\n\n'
 'Then total net_amount by city, sorted high\n'
 'to low. Give me the gap between top and\n'
 'bottom as a multiple, not just two numbers.\n\n'
 'Return a horizontal bar chart, sorted, one\n'
 'accent colour, values on the bars, titled with\n'
 'the finding as a sentence.',
 ['A sorted bar chart, titled with the finding',
  'A cleaning log: 13 city strings collapsed to 8',
  'The row count it dropped, stated up front',
  'The gap as “2.1×”, not as two raw numbers'],RED)
    if n_==8:
        prompt_slide('The prompt behind Lens 8',
 'Net revenue moved from ₹12.81 Cr in 2023 to\n'
 '₹15.54 Cr in 2024. Find out why, with code.\n\n'
 '1  Confirm the total change, absolute and %.\n\n'
 '2  Split it into two effects:\n'
 '     volume    = (orders24 − orders23) × avg23\n'
 '     deal size = (avg24 − avg23) × orders24\n\n'
 '3  The two must sum to the total change.\n'
 '   Print the reconciliation and the residual.\n'
 '   If the residual is not about zero, stop and\n'
 '   tell me what is unexplained.\n\n'
 '4  Label every driver OBSERVED or INFERRED.',
 ['A bridge where the parts tie to the total',
  '20% from more orders, 80% from bigger ones',
  'The residual, printed, at about zero',
  'An honest label on anything it assumed'],BLUE)

war_story('WAR STORY · HT DIGITAL STREAMS  ·  CONTEXTUAL TARGETING',
 'The lift was real. The first number we ran was not.',
 'We moved from broad targeting to in-page semantics with brand-safety '
 'controls. The early read looked enormous, because the two groups were not '
 'comparable. Different placements, different weeks, different mix.\n\n'
 'Once it was cut properly against a like-for-like baseline, the gain held up. '
 'Smaller than the first number, and defensible in front of a client.',
 '+25%','CTR and conversion against vanilla targeting, on a like-for-like cut',
 'Lens 1 is the whole discipline: a number means nothing until you name what it is compared to.')

statement('Most people stop at\n“revenue went up.”',
          'Lenses 6 to 8 are the ones that get skipped, and the ones that get you invited '
          'back into the room.',MAROON)

handson(12,['Open ad-sales-data.csv in Aurex.',
            'Pick any two lenses and run them properly.',
            'Write down which trap you checked for.'],
        'The one thing that surprised you most')

# =========== MODULE 3 ===========
divider(3,'The Chart Selector',
        'Nine comparisons, nine answers. Name the comparison out loud\n'
        'and the chart stops being a matter of taste.',
        GOLD,'15 MINUTES')

full_img('d_chart_tree','THE SELECTOR',GOLD)
full_img('d_wrong_right','THE SAME NUMBERS, TWICE',GOLD)

numbered('Three rules that fix almost every chart',
         [('Put the finding in the title','“Display is 63% of revenue”, never “Revenue by Ad Type”.'),
          ('One colour carries the point','Everything else goes grey. Colour is an argument, not decoration.'),
          ('Label the bars, delete the furniture','Legend, gridlines, border, markers. All of it competes with the data.')],
         sub='Then point at anything still on the chart and ask what it proves. '
             'If it does not support the title, take it off.',accent=GOLD)

# =========== MODULE 4 ===========
divider(4,'The Six Distortions',
        'No formulas. Six ways a technically correct number\n'
        'ends up telling a room the wrong thing.',
        BLUE,'20 MINUTES')

full_img('s_rate_vs_count','DISTORTION 1 — COUNTS WHERE RATES BELONG',BLUE)
statement('Always ask “per what?”',
          'Counts reward whoever is biggest. Divide by something and you find out who is '
          'actually good at it. Per order, per rep, per rupee spent, per head.',BLUE)

full_img('t5_distribution','DISTORTION 2 — THE MEAN QUOTED AS TYPICAL',BLUE)
table('Mean, median, and the gap between them','Read the gap before you quote either',
      ['','WHAT IT IS','WHEN TO USE IT'],
      [['Mean','Add everything up, divide by the count','Values cluster together with no long tail'],
       ['Median','Line them up, take the one in the middle','A few large values are pulling the average'],
       ['The gap','₹1.80L mean against ₹0.79L median','At 2.3× apart, quoting the mean overstates']],
      [1.9,4.6,4.95],BLUE,rowh=0.86,fs=14)

full_img('s_seasonality','DISTORTION 3 — CALENDAR READ AS PERFORMANCE',BLUE)
numbered('Which growth comparison to use',
         [('Year on year','This January against last January. Cancels seasonality. Your default.'),
          ('Month on month','Fast signal, very noisy. Never multiply it by 12 to get an annual rate.'),
          ('A part-finished month','Exclude it, or put the day count right next to the number.')],
         sub='This file swings threefold between July and October, so a month-on-month '
             'number here is mostly calendar.',accent=BLUE)

full_img('s_small_n','DISTORTION 4 — PERCENTAGES ON TINY SAMPLES',BLUE)

s,y=titled('Distortion 5 — correlation reported as cause',
           'Two series moving together is the beginning of the work, not the end',accent=BLUE)
tx(s,0.95,y+0.20,11.4,1.0,'Ice cream sales and drowning deaths rise together.\nSummer drives both.',
   26,True,INK,space=1.26,track=-0.5)
hair(s,0.95,y+1.72,11.45)
tx(s,0.95,y+1.96,11.4,0.34,'SO WHEN YOU FIND A RELATIONSHIP',9.5,True,BLUE,track=1.1)
steps=[('Ask what else changed in the same window','Campaigns, pricing, seasonality, a tracking change.'),
       ('Say out loud whether you observed it or inferred it','Two words. It changes how the room treats the claim.'),
       ('Go looking for the third thing driving both','That is usually where the actual explanation is.')]
yy=y+2.40
for h_,b_ in steps:
    tx(s,0.95,yy,11.2,0.36,h_,17,True,INK)
    tx(s,0.95,yy+0.38,11.2,0.36,b_,13.5,False,BODY)
    yy+=1.00

war_story('WAR STORY · HT DIGITAL STREAMS  ·  PLATFORM CONSOLIDATION',
 'Three tools, three versions of the same metric.',
 'Mixpanel, Redshift and Elasticsearch each held a version of the truth, and '
 'teams quoted whichever one they had access to. Meetings were spent '
 'reconciling numbers rather than deciding anything.\n\n'
 'Consolidating onto one modelled layer with agreed definitions took most of '
 'six months. The reporting improvement was almost a side effect.',
 '₹2.5 Cr','a year in run-rate savings once the duplicate stack was retired',
 'Distortion 6 is the undefined metric. It is the cheapest one to fix and the one nobody owns.')

# =========== MODULE 5 ===========
divider(5,'The Five-Check Gate',
        'Aurex will run your code perfectly and still answer\n'
        'the wrong question. This is the gate before you send.',
        RED_D,'15 MINUTES')

s,y=titled('A groupby on the wrong column runs perfectly',
           'Nothing in the output tells you the column was wrong',accent=RED_D)
tx(s,0.95,y+0.14,11.4,0.9,
   'You get a clean table, a tidy chart and a confident summary. The failure '
   'mode moved from arithmetic to aim.',18,False,BODY,space=1.34)
tx(s,0.95,y+1.28,11.4,0.34,'MEASURED ACCURACY ON REAL SPREADSHEETS',9.5,True,RED_D,track=1.1)
acc=[('Looking things up','89%',TEAL),('Filtering rows','71%',TEAL),
     ('Adding things up','54%',GOLD),('Counting','42%',RED),
     ('Sorting','38%',RED),('Medians','20%',RED)]
for i,(k,v,c) in enumerate(acc):
    x=0.95+(i%3)*3.85; yy=y+1.76+(i//3)*1.28
    rect(s,x,yy,3.62,1.06,PLANE)
    rect(s,x,yy,0.055,1.06,c)
    tx(s,x+0.28,yy+0.14,2.6,0.32,k,13,False,BODY)
    tx(s,x+0.28,yy+0.50,2.6,0.44,v,23,True,c,track=-0.5)
hair(s,0.95,y+4.34,11.45)
tx(s,0.95,y+4.54,11.4,0.5,
   'Lookups come back right. Anything that needs arithmetic across rows, check it yourself.',
   14.5,True,RED_D)

numbered('The Five-Check Gate',
         [('Row accounting','Ask how many rows it used, then compare that to how many are in the file.'),
          ('Spot-verify the headline','Pick the number that matters most and check that one against the source.'),
          ('Ask it a second way','Different phrasing, same question. Two answers means you have none.'),
          ('Open what it made you','Look at the axis. Read the labels. Generated files look finished early.'),
          ('Sign it','Would you put your name on this? You are about to.')],
         sub='94% of working spreadsheets already carry a human error. '
             'The bar here is checkability, not perfection.',accent=RED_D)

handson(10,['Take the finding you produced earlier.',
            'Run all five checks against it.',
            'Rewrite it as one sentence your manager could act on.'],
        'Your one sentence',accent=RED_D)

# =========== CLOSE ===========
_state['mod']=0
s,y=titled('The five cards you are leaving with',
           'Each one works on any file, in any tool, in any department')
fw2=[('01','THE SEVEN-STEP READ','Context · Shape · Total · Break down · Compare · Drivers · Validate',RED),
     ('02','THE EIGHT LENSES','Comparison · Ranking · Trend · Composition · Distribution · Correlation · Outliers · Decomposition',TEAL),
     ('03','THE CHART SELECTOR','Name the comparison, take the chart it gives you',GOLD),
     ('04','THE SIX DISTORTIONS','Rates · Mean · Calendar · Sample size · Cause · Definitions',BLUE),
     ('05','THE FIVE-CHECK GATE','Rows · Headline · Second phrasing · Open the file · Sign it',RED_D)]
yy=y+0.10
for n_,t_,d_,c in fw2:
    rect(s,0.95,yy,11.45,0.92,PLANE)
    rect(s,0.95,yy,0.055,0.92,c)
    tx(s,1.30,yy+0.20,0.7,0.4,n_,17,True,c,track=-0.4)
    tx(s,2.10,yy+0.16,3.5,0.4,t_,14.5,True,INK)
    tx(s,5.75,yy+0.20,6.4,0.5,d_,12.5,False,BODY,space=1.20)
    yy+=1.04

s=slide(DARK,chrome=True)
rect(s,0,0,W,0.22,RED)
tx(s,0.95,1.62,10.8,2.0,
   'Somebody sends you a spreadsheet you did not build,\n'
   'about a part of the business you half-know,\n'
   'and wants your read on it by tomorrow morning.',
   23,False,RGBColor(0xB0,0xAA,0xA4),space=1.42)
rule(s,0.95,4.28,2.0,RED,0.05)
tx(s,0.92,4.62,11.4,1.0,'You now have a sequence for that.',40,True,WHITE,track=-1.0)
tx(s,0.95,5.86,11.4,0.5,
   'Dishant Singla  ·  Base42 Systems  ·  run on Aurex, inside BCCL',
   12.5,False,MUTED,track=0.5)

prs.save(OUT)
print(OUT); print(len(prs.slides._sldIdLst),'slides')
