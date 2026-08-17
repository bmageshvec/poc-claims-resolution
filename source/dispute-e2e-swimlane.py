# -*- coding: utf-8 -*-
import os
import html, os

C = {"flow":"#334155","sync":"#1061B0","poll":"#C1440E","asyn":"#7B2CBF",
     "ink":"#0F172A","sub":"#475569","line":"#94A3B8"}

# ---------------------------------------------------------------- geometry
GUT = 212                              # left lane-label gutter
PH  = [("1","CAPTURE","Cardholder raises it; the platform proves it is a real, in-window, non-duplicate claim",212,566),
       ("2","AUTO-RESOLVE & TRIAGE","Rules decide: settle it now, credit provisionally, or send it to an analyst",566,920),
       ("3","PRE-DISPUTE","Try to close it without a chargeback — alerts, deflection, merchant inquiry",920,1300),
       ("4","DISPUTE — FILE","Build the evidence pack, route to the right scheme, file it, poll for the answer",1300,1650),
       ("5","RECOVER","Pre-arbitration, arbitration, appeal — executed in VROL/MCOM, orchestrated here",1650,2050)]
W = 2062
TOP_TITLE = 74
HDR_H = 66
LANE_Y0 = TOP_TITLE + HDR_H

LANES = [("Cardholder & Channels","app · web · IVR · branch · CSR",104),
         ("Core Issuer Platform","auth · posting · GL · fraud · CRM",116),
         ("DRS · Intake & Triage","the record of the claim",116),
         ("DRS · Orchestration","every decision is made here",178),
         ("DRS · Scheme Adapters","file · poll · fan-out · reconcile",116),
         ("Deflection Networks","Ethoca · RDR / Verifi",104),
         ("Scheme Platforms","VROL (Visa) · MCOM (Mastercard)",150),
         ("Acquirer & Merchant","reached only through the scheme",104)]
LT = []
_y = LANE_Y0
for _n,_s,_h in LANES:
    LT.append(_y); _y += _h
LANE_Y1 = _y
LEG_Y = LANE_Y1 + 16
H = LEG_Y + 78

def lane_row(i, row=None, bh=56):
    """top-y of a box in lane i"""
    h = LANES[i][2]
    if row is None: return LT[i] + (h-bh)/2.0
    if i == 3:  return LT[i] + (16 if row=="A" else 96)
    if i == 6:  return LT[i] + (14 if row=="A" else 80)
    return LT[i] + (h-bh)/2.0

N = {}
def n(nid, lane, x, w, kind, label, row=None, bh=56):
    y = lane_row(lane, row, bh)
    N[nid] = (x, y, w, bh, kind, label)

# ---------------------------------------------------------------- nodes
# lane 0 — cardholder & channels
n("a1",0,228,153,"actor","Claim raised|app · web · IVR|branch · CSR")
n("a2",0,397,153,"actor","ID&V + consent|captured at the channel")
n("a3",0,582,322,"actor","Acknowledgement + case reference sent|email · SMS · push")
n("a4",0,936,348,"actor","Cardholder supplies extra evidence|receipts · merchant comms — optional")
n("a5",0,1316,318,"actor","Status update: filed with the scheme")
n("a6",0,1666,368,"actor","Outcome letter — final credit or debit explained")
# lane 1 — core issuer platform
n("b1",1,228,153,"core","Card auth & posting|transaction lookup")
n("b2",1,397,153,"core","Customer master|contact · KYC · card")
n("b3",1,751,153,"core","Fraud & scoring|risk signal")
n("b4",1,582,153,"core","GL / ledger|provisional credit posted")
n("b5",1,936,348,"core","Ledger hold maintained|merchant refund posted if deflected")
n("b6",1,1316,318,"core","Ledger position held|Visa Allocation — funds never move")
n("b7",1,1666,368,"core","GL — final settlement write-back, reversal or confirmation")
# lane 2 — intake / triage / case data
n("c1",2,228,153,"step","Claim captured|reason · amount|free-text narrative")
n("c2",2,397,153,"step","Duplicate &|prior-claim check")
n("c3",2,582,153,"step","Reason code derived|+ eligibility rules run")
n("c4",2,751,153,"step","Evidence checklist|raised to analyst")
n("c5",2,936,348,"step","Pre-dispute case opened · deflection window tracked")
n("c6",2,1316,318,"step","Evidence pack assembled, validated, versioned")
n("c7",2,1666,176,"step","Recovery case|tracking")
n("c8",2,1858,176,"step","Reconciliation & assurance|never mutates the case")
# lane 3 — orchestration & decisions
n("d1",3,228,322,"dec","Claim valid?|transaction found · within window · not a duplicate","A",66)
n("d2",3,228,322,"note","Reg E clock starts — 10 / 45 / 90 business days","B",66)
n("d3",3,582,322,"dec","Auto-resolve eligible?|low value · clear liability · written-off","A",66)
n("d4",3,582,153,"dec","Provisional|credit due?","B",66)
n("d5",3,751,153,"step","Route to|analyst queue","B",66)
n("d6",3,936,348,"dec","Deflect before filing?|alert match · RDR rule · merchant inquiry answered","A",66)
n("d7",3,936,170,"dec","Merchant refunded|→ close claim","B",66)
n("d8",3,1114,170,"step","Proceed to file","B",66)
n("d9",3,1316,318,"dec","Scheme route|VISA → VROL · MASTERCARD → MCOM","A",66)
n("d10",3,1316,318,"dec","Acquirer re-presented?|accept liability vs carry on","B",66)
n("d11",3,1666,368,"dec","Who files pre-arbitration?|Allocation → acquirer · Collaboration & MDR → issuer","A",66)
n("d12",3,1666,368,"dec","Ruling ≥ USD 5,000 → appeal?|otherwise the ruling is final","B",66)
# lane 4 — adapters
n("e1",4,582,322,"step","Case events published to subscribers")
n("e2",4,936,348,"step","Deflection adapter — alert out, status polled back")
n("e3",4,1316,153,"step","Filer|synchronous submit")
n("e4",4,1481,153,"step","Poller|status & event feed")
n("e5",4,1666,176,"step","Pre-arb / arbitration|filer + poller")
n("e6",4,1858,176,"step","Reconciliation poller|independent of the case")
# lane 5 — deflection networks
n("f1",5,936,170,"ext","Ethoca|fraud & dispute alerts")
n("f2",5,1114,170,"ext","RDR / Verifi|rules-based deflection")
# lane 6 — scheme platforms
n("g1",6,936,170,"ext","VROL|Merchant Purchase Inquiry","A")
n("g2",6,1114,170,"ext","MCOM|Collaboration request","A")
n("g3",6,1316,153,"ext","VROL — Allocation|or Collaboration","A")
n("g4",6,1481,153,"ext","MCOM — first|chargeback (cycle 1)","A")
n("g6",6,1666,112,"ext","Pre-arbitration","A")
n("g7",6,1794,112,"ext","Arbitration|ruling","A")
n("g8",6,1922,112,"ext","Appeal /|compliance","A")
n("g9",6,1666,368,"ext","Settlement & clearing advice","B")
# lane 7 — acquirer / merchant
n("h1",7,936,348,"ext","Merchant reviews the inquiry — refunds or defends")
n("h2",7,1316,318,"ext","Acquirer accepts or re-presents with evidence")
n("h3",7,1666,368,"ext","Acquirer accepts the ruling or escalates")

# ---------------------------------------------------------------- edges
# (src, dst, kind, via_x, chan, dxa, dxb)
E = [
 # phase 1
 ("a1","c1","flow",None,0,-30,-30), ("a1","a2","flow",None,0,0,0),
 ("b2","a2","sync",None,0,30,30),   ("b1","c1","sync",None,0,30,30),
 ("c1","c2","flow",None,0,0,0),     ("c2","d1","flow",None,0,0,120),
 ("d1","d2","flow",None,0,0,0),
 # phase 1 -> 2
 ("d2","c3","flow",558,0,0,0),   ("c3","c4","flow",None,0,0,0),
 ("c3","d3","flow",None,0,-40,-120),("b3","d3","sync",None,0,0,-40),
 ("d3","d4","flow",None,0,-80,0),   ("d3","d5","flow",None,0,80,0),
 ("d4","b4","sync",574,0,0,0),     ("c4","e1","async",None,0,60,60),
 ("e1","a3","async",912,0,0,0),
 # phase 2 -> 3
 ("d5","c5","flow",None,0,0,-120),  ("c5","e2","flow",None,0,-120,-120),
 ("e2","f1","async",None,-8,-120,-30),("e2","f2","async",None,-8,60,20),
 ("f1","e2","poll",None,10,30,-60), ("f2","e2","poll",None,10,-20,110),
 ("e2","g1","sync",None,10,-150,-60),("e2","g2","sync",None,10,150,60),
 ("g1","h1","flow",None,0,-40,-100),("g2","h1","flow",None,0,40,100),
 ("h1","e2","poll",1292,0,0,0),     ("e2","d6","flow",None,0,120,120),
 ("d6","d7","flow",None,0,-80,0),   ("d6","d8","flow",None,0,80,0),
 ("d7","b5","sync",None,0,0,-120),  ("c5","a4","flow",1288,0,0,0),
 # phase 3 -> 4
 ("d8","c6","flow",None,0,0,-100),  ("c6","d9","flow",None,0,0,0),
 ("d9","e3","flow",None,0,-60,0),   ("e3","g3","sync",None,0,-30,0),
 ("e3","g4","sync",None,8,40,-30),  ("g3","h2","flow",None,0,-40,-90), ("g4","h2","flow",None,0,40,90),
 ("h2","g4","flow",None,0,-120,0),  ("g3","e4","poll",None,-16,50,-40),
 ("g4","e4","poll",None,-16,50,40),  ("e4","d10","flow",None,0,0,100),
 ("d9","a5","async",1308,0,0,0),    ("d9","b6","flow",None,0,110,110),
 # phase 4 -> 5
 ("d10","d11","flow",None,0,140,-150),("d11","e5","flow",None,0,-120,0),
 ("e5","g6","sync",None,0,0,0),     ("g6","g7","flow",None,0,0,0),
 ("g7","e5","poll",None,-14,0,50),  ("e5","d12","flow",None,0,50,-120),
 ("d12","g8","sync",None,0,0,0),    ("g7","g9","flow",None,0,0,-140),
 ("g8","g9","flow",None,8,0,140),   ("g9","e6","poll",2042,0,0,0),
 ("e6","c8","flow",None,0,0,0),     ("c8","b7","sync",None,0,0,120),
 ("d12","c7","flow",None,0,-150,0), ("b7","a6","async",None,0,-140,-140),
 ("g6","h3","flow",1658,0,0,0),
]


# ---------------------------------------------------------------- auto router
def _segs(pts): return [(pts[i],pts[i+1]) for i in range(len(pts)-1)]
def _hit(seg, box, pad=4):
    (x1,y1),(x2,y2)=seg; bx,by,bw,bh=box
    bx-=pad; by-=pad; bw+=2*pad; bh+=2*pad
    return min(x1,x2) < bx+bw and bx < max(x1,x2) and min(y1,y2) < by+bh and by < max(y1,y2)
def _cross(pts, a, b):
    c=0
    for sg in _segs(pts):
        for nid,v in N.items():
            if nid in (a,b): continue
            if _hit(sg, v[:4]): c+=1
    return c
def _free_x(y0,y1):
    iv=[]
    for nid,(x,y,w,h,k,l) in N.items():
        if y < y1 and y0 < y+h: iv.append((x-6,x+w+6))
    iv.sort(); free=[]; cur=200.0
    for a0,a1 in iv:
        if a0 > cur: free.append((cur,a0))
        cur=max(cur,a1)
    if cur < 2050: free.append((cur,2050.0))
    return [f for f in free if f[1]-f[0] >= 9]
def autoroute(aid,bid):
    a=N[aid]; b=N[bid]
    acy=a[1]+a[3]/2.0; bcy=b[1]+b[3]/2.0
    acx=a[0]+a[2]/2.0; bcx=b[0]+b[2]/2.0
    y0,y1=min(acy,bcy),max(acy,bcy)
    cands=[]
    for f0,f1 in _free_x(y0,y1):
        for t in (0.5,0.25,0.75):
            cands.append(f0+(f1-f0)*t)
    best=None
    for vx in cands:
        pts=route(aid,bid,vx,0,0,0)
        c=_cross(pts,aid,bid)
        sc=(c, abs(vx-acx)+abs(vx-bcx))
        if best is None or sc<best[0]: best=(sc,vx)
    return best[1] if best else None

ST = {"flow":(C["flow"],"","af",1.8),
      "sync":(C["sync"],"","as",2.0),
      "poll":(C["poll"],' stroke-dasharray="2 4"',"ap",2.4),
      "async":(C["asyn"],' stroke-dasharray="9 5"',"ay",2.2)}

def route(aid,bid,via_x,chan,dxa,dxb):
    ax,ay,aw,ah = N[aid][:4]; bx,by,bw,bh = N[bid][:4]
    acx,acy = ax+aw/2.0, ay+ah/2.0
    bcx,bcy = bx+bw/2.0, by+bh/2.0
    if abs(acy-bcy) < 2:
        if bx >= ax+aw: return [(ax+aw,acy),(bx,bcy)]
        return [(ax,acy),(bx+bw,bcy)]
    if via_x is not None:
        down = bcy > acy
        ina = ax+10 <= via_x <= ax+aw-10
        inb = bx+10 <= via_x <= bx+bw-10
        pts=[]
        if ina: pts.append((via_x, ay+ah if down else ay))
        else:   pts += [(ax+aw if via_x > acx else ax, acy),(via_x,acy)]
        if inb: pts.append((via_x, by if down else by+bh))
        else:   pts += [(via_x,bcy),(bx+bw if via_x > bcx else bx, bcy)]
        return pts
    down = bcy > acy
    sy = ay+ah if down else ay
    ey = by if down else by+bh
    my = (sy+ey)/2.0 + chan
    p0=(acx+dxa,sy); p1=(acx+dxa,my); p2=(bcx+dxb,my); p3=(bcx+dxb,ey)
    if abs(p0[0]-p3[0])<1: return [p0,p3]
    return [p0,p1,p2,p3]

RES={}
for _e in E:
    _a,_b,_k,_vx,_ch,_da,_db=_e
    _p=route(_a,_b,_vx,_ch,_da,_db)
    if _cross(_p,_a,_b):
        _v=autoroute(_a,_b)
        if _v is not None:
            _p2=route(_a,_b,_v,0,0,0)
            if _cross(_p2,_a,_b) < _cross(_p,_a,_b): _p=_p2
    RES[(_a,_b)]=_p

def esc(s): return html.escape(s,quote=False)

# ---------------------------------------------------------------- render
o=[]
o.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Segoe UI, Inter, Helvetica, Arial, sans-serif">')
o.append('<defs>')
for k,(col,dash,mid,sw) in ST.items():
    o.append(f'<marker id="{mid}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{col}"/></marker>')
o.append('</defs>')
o.append(f'<rect width="{W}" height="{H}" fill="#FFFFFF"/>')

# title
o.append(f'<text x="24" y="34" font-size="21" font-weight="700" fill="{C["ink"]}">Dispute Claims Resolution — end-to-end swimlane, Capture through Recover</text>')
o.append(f'<text x="24" y="56" font-size="12.5" fill="{C["sub"]}">One flow, eight lanes, five phases. The platform orchestrates every decision; the scheme platforms execute recovery. Nothing reaches the acquirer except through a scheme.</text>')

# lane bands
for i,(nm,sub,h) in enumerate(LANES):
    y=LT[i]
    o.append(f'<rect x="0" y="{y}" width="{W}" height="{h}" fill="{"#FFFFFF" if i%2 else "#F8FAFC"}"/>')
    o.append(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="#CBD5E1" stroke-width="1"/>')
    o.append(f'<rect x="0" y="{y}" width="{GUT}" height="{h}" fill="#E8EDF3"/>')
    o.append(f'<text x="16" y="{y+h/2-3}" font-size="12.5" font-weight="700" fill="{C["ink"]}">{esc(nm)}</text>')
    o.append(f'<text x="16" y="{y+h/2+14}" font-size="10.5" fill="{C["sub"]}">{esc(sub)}</text>')
o.append(f'<line x1="0" y1="{LANE_Y1}" x2="{W}" y2="{LANE_Y1}" stroke="#CBD5E1" stroke-width="1"/>')
o.append(f'<line x1="{GUT}" y1="{LANE_Y0}" x2="{GUT}" y2="{LANE_Y1}" stroke="#94A3B8" stroke-width="1.4"/>')

# phase headers + separators
PC = ["#0E7490","#0F766E","#B45309","#1061B0","#7B2CBF"]
for i,(num,nm,desc,x0,x1) in enumerate(PH):
    o.append(f'<rect x="{x0}" y="{TOP_TITLE}" width="{x1-x0-2}" height="{HDR_H-8}" rx="6" fill="{PC[i]}" opacity="0.10"/>')
    o.append(f'<rect x="{x0}" y="{TOP_TITLE}" width="4" height="{HDR_H-8}" rx="2" fill="{PC[i]}"/>')
    o.append(f'<text x="{x0+14}" y="{TOP_TITLE+21}" font-size="13" font-weight="700" fill="{PC[i]}">PHASE {num} · {esc(nm)}</text>')
    words=desc.split(); ln=[""]; lim=int((x1-x0-26)/5.05)
    for wd in words:
        if len(ln[-1])+len(wd)+1>lim: ln.append(wd)
        else: ln[-1]=(ln[-1]+" "+wd).strip()
    for j,l in enumerate(ln[:2]):
        o.append(f'<text x="{x0+14}" y="{TOP_TITLE+37+j*12}" font-size="10" fill="{C["sub"]}">{esc(l)}</text>')
    if i:
        o.append(f'<line x1="{x0}" y1="{LANE_Y0}" x2="{x0}" y2="{LANE_Y1}" stroke="#94A3B8" stroke-width="1" stroke-dasharray="5 5"/>')

# edges first (under boxes)
for (a,b,k,vx,ch,da,db) in E:
    col,dash,mid,sw = ST[k]
    pts = RES[(a,b)]
    d = "M " + " L ".join(f"{p[0]:.1f},{p[1]:.1f}" for p in pts)
    o.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{sw}"{dash} stroke-linejoin="round" marker-end="url(#{mid})" opacity="0.92"/>')

# nodes
FILL={"step":("#FFFFFF","#94A3B8",1.3),"dec":("#FEF6E7","#B45309",1.7),
      "core":("#EEF2F7","#64748B",1.3),"ext":("#EAF2FB","#1061B0",1.5),
      "actor":("#F2FBF6","#0E7490",1.4),"note":("#F8FAFC","#94A3B8",1.1)}
for nid,(x,y,w,h,kind,label) in N.items():
    fill,stroke,sw = FILL[kind]
    extra = ' stroke-dasharray="4 3"' if kind=="note" else ""
    o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{extra}/>')
    if kind=="dec":
        o.append(f'<rect x="{x}" y="{y}" width="4" height="{h}" rx="2" fill="#B45309"/>')
    lines=label.split("|"); cx=x+w/2.0
    th = 14 + (len(lines)-1)*12.5
    ty = y+h/2.0 - th/2.0 + 11
    o.append(f'<text x="{cx}" y="{ty}" text-anchor="middle" font-size="11.6" font-weight="600" fill="{C["ink"]}">{esc(lines[0])}</text>')
    for j,l in enumerate(lines[1:]):
        o.append(f'<text x="{cx}" y="{ty+14+j*12.5}" text-anchor="middle" font-size="10.2" fill="{C["sub"]}">{esc(l)}</text>')

# legend
ly=LEG_Y+8
o.append(f'<rect x="16" y="{LEG_Y}" width="{W-32}" height="62" rx="6" fill="#F8FAFC" stroke="#CBD5E1"/>')
o.append(f'<text x="30" y="{ly+16}" font-size="11.5" font-weight="700" fill="{C["ink"]}">LINE STYLE</text>')
items=[("flow","internal flow / hand-off"),("sync","synchronous call"),("poll","poll (scheme or partner is asked, repeatedly)"),("async","asynchronous / event")]
lx=140
for k,lab in items:
    col,dash,mid,sw=ST[k]
    o.append(f'<line x1="{lx}" y1="{ly+12}" x2="{lx+44}" y2="{ly+12}" stroke="{col}" stroke-width="{sw}"{dash} marker-end="url(#{mid})"/>')
    o.append(f'<text x="{lx+52}" y="{ly+16}" font-size="11" fill="{C["sub"]}">{esc(lab)}</text>')
    lx += 60 + len(lab)*5.9 + 30
o.append(f'<text x="30" y="{ly+42}" font-size="11.5" font-weight="700" fill="{C["ink"]}">BOX</text>')
bx=140
for kind,lab in [("actor","cardholder / channel"),("core","core issuer platform"),("step","platform step"),("dec","DECISION POINT"),("ext","external — scheme, partner, acquirer"),("note","regulatory clock / note")]:
    fill,stroke,sw=FILL[kind]
    extra=' stroke-dasharray="4 3"' if kind=="note" else ""
    o.append(f'<rect x="{bx}" y="{ly+30}" width="26" height="15" rx="3" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{extra}/>')
    o.append(f'<text x="{bx+33}" y="{ly+42}" font-size="11" fill="{C["sub"]}">{esc(lab)}</text>')
    bx += 40 + len(lab)*5.9 + 26
o.append('</svg>')

OUT="/sessions/relaxed-intelligent-feynman/mnt/cpoc-claims-resolution/diagrams/dispute-e2e-swimlane.svg"
open(OUT,"w",encoding="utf-8").write("\n".join(o))

# ---- checks
ov=0
ids=list(N)
for i in range(len(ids)):
    for j in range(i+1,len(ids)):
        x1,y1,w1,h1=N[ids[i]][:4]; x2,y2,w2,h2=N[ids[j]][:4]
        if x1<x2+w2 and x2<x1+w1 and y1<y2+h2 and y2<y1+h1:
            print("OVERLAP",ids[i],ids[j]); ov+=1
tight=0
for nid,(x,y,w,h,kind,label) in N.items():
    for j,l in enumerate(label.split("|")):
        px = len(l)*(6.1 if j==0 else 5.3)
        if px > w-14: print("TIGHT",nid,repr(l),round(px),w); tight+=1
print("nodes",len(N),"edges",len(E),"overlaps",ov,"tight",tight,"size",W,"x",H)

# ---------------------------------------------------------------- edge/box collision check
def segs(pts):
    return [(pts[i],pts[i+1]) for i in range(len(pts)-1)]
def hits(seg, box, pad=3):
    (x1,y1),(x2,y2)=seg; bx,by,bw,bh=box
    bx-=pad; by-=pad; bw+=2*pad; bh+=2*pad
    lo_x,hi_x=min(x1,x2),max(x1,x2); lo_y,hi_y=min(y1,y2),max(y1,y2)
    return lo_x < bx+bw and bx < hi_x and lo_y < by+bh and by < hi_y
bad=0
for (a,b,k,vx,ch,da,db) in E:
    pts=RES[(a,b)]
    for sg in segs(pts):
        for nid,v in N.items():
            if nid in (a,b): continue
            if hits(sg, v[:4]):
                print("CROSS  %-4s -> %-4s  through %s" % (a,b,nid)); bad+=1
print("edge/box crossings:", bad)

# ================================================================ draw.io emitter
# Same node/edge model, same routed polylines. Emits an editable .drawio master so
# the diagram can be nudged in the GUI without re-running this script.
# NOTE: <b>/<font> are legal here because draw.io cells set html=1 and render them.
# That is NOT true of Mermaid labels — see prompts/mermaid-diagram-rules.md rule 9.

def _x(s): return (s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
                    .replace('"',"&quot;").replace("'","&#39;"))
def _tint(hexc, f=0.10):
    r,g,b = int(hexc[1:3],16),int(hexc[3:5],16),int(hexc[5:7],16)
    return "#%02X%02X%02X" % tuple(round(255+(v-255)*f) for v in (r,g,b))

DSTYLE = {
 "step" :"fillColor=#FFFFFF;strokeColor=#94A3B8;strokeWidth=1.3;",
 "dec"  :"fillColor=#FEF6E7;strokeColor=#B45309;strokeWidth=1.7;",
 "core" :"fillColor=#EEF2F7;strokeColor=#64748B;strokeWidth=1.3;",
 "ext"  :"fillColor=#EAF2FB;strokeColor=#1061B0;strokeWidth=1.5;",
 "actor":"fillColor=#F2FBF6;strokeColor=#0E7490;strokeWidth=1.4;",
 "note" :"fillColor=#F8FAFC;strokeColor=#94A3B8;strokeWidth=1.1;dashed=1;dashPattern=4 3;",
}
DEDGE = {
 "flow" :"strokeColor=#334155;strokeWidth=1.8;",
 "sync" :"strokeColor=#1061B0;strokeWidth=2;",
 "poll" :"strokeColor=#C1440E;strokeWidth=2.4;dashed=1;dashPattern=1 3;",
 "async":"strokeColor=#7B2CBF;strokeWidth=2.2;dashed=1;dashPattern=8 4;",
}
VBASE = "rounded=1;arcSize=12;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;fontSize=11;fontColor=#0F172A;fontStyle=0;"
EBASE = ("edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=blockThin;endFill=1;"
         "exitDx=0;exitDy=0;entryDx=0;entryDy=0;exitPerimeter=0;entryPerimeter=0;jettySize=auto;")

def _label(lines):
    out = "<b>%s</b>" % _x(lines[0])
    for l in lines[1:]:
        out += "<br><font style=\"font-size:9.5px\" color=\"#475569\">%s</font>" % _x(l)
    return out

d=[]
d.append('<mxfile host="app.diagrams.net" agent="dispute-e2e-swimlane.py" version="24.0.0">')
d.append('  <diagram id="e2e-swimlane" name="E2E Swimlane">')
d.append('    <mxGraphModel dx="1600" dy="900" grid="1" gridSize="10" guides="1" tooltips="1" '
         'connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="%d" pageHeight="%d" math="0" shadow="0">' % (W,H))
d.append('      <root>')
d.append('        <mxCell id="0" />')
d.append('        <mxCell id="L0" value="Frame" parent="0" style="locked=1;" />')
d.append('        <mxCell id="L1" value="Diagram" parent="0" />')

def V(cid, x, y, w, h, style, value="", parent="L1"):
    value = _x(value)          # draw.io stores HTML labels XML-escaped inside the attribute
    d.append('        <mxCell id="%s" value="%s" style="%s" vertex="1" parent="%s">'
             '<mxGeometry x="%.1f" y="%.1f" width="%.1f" height="%.1f" as="geometry"/></mxCell>'
             % (cid, value, style, parent, x, y, w, h))

# --- frame layer: title, lane bands, gutter labels, phase headers
V("t1",24,14,1600,28,"text;html=1;align=left;verticalAlign=middle;fontSize=21;fontStyle=1;fontColor=#0F172A;",
  "Dispute Claims Resolution — end-to-end swimlane, Capture through Recover","L0")
V("t2",24,44,1900,20,"text;html=1;align=left;verticalAlign=middle;fontSize=12;fontColor=#475569;",
  "One flow, eight lanes, five phases. The platform orchestrates every decision; the scheme platforms execute recovery. "
  "Nothing reaches the acquirer except through a scheme.","L0")
for i,(nm,sub,h) in enumerate(LANES):
    V("lane%d"%i,0,LT[i],W,h,"rounded=0;whiteSpace=wrap;html=1;fillColor=%s;strokeColor=#CBD5E1;"
      % ("#FFFFFF" if i%2 else "#F8FAFC"),"","L0")
    V("gut%d"%i,0,LT[i],GUT,h,"rounded=0;whiteSpace=wrap;html=1;fillColor=#E8EDF3;strokeColor=#CBD5E1;"
      "align=left;verticalAlign=middle;spacingLeft=14;fontSize=11.5;fontColor=#0F172A;",
      "<b>%s</b><br><font style=\"font-size:9.5px\" color=\"#475569\">%s</font>" % (_x(nm),_x(sub)),"L0")
PCD = ["#0E7490","#0F766E","#B45309","#1061B0","#7B2CBF"]
for i,(num,nm,desc,x0,x1) in enumerate(PH):
    V("ph%d"%i,x0,TOP_TITLE,x1-x0-2,HDR_H-8,
      "rounded=1;arcSize=8;whiteSpace=wrap;html=1;fillColor=%s;strokeColor=%s;align=left;verticalAlign=top;"
      "spacingLeft=12;spacingTop=6;fontSize=12.5;fontColor=%s;" % (_tint(PCD[i]),PCD[i],PCD[i]),
      "<b>PHASE %s · %s</b><br><font style=\"font-size:9.5px\" color=\"#475569\">%s</font>" % (num,_x(nm),_x(desc)),"L0")
    if i:
        d.append('        <mxCell id="sep%d" style="endArrow=none;html=1;strokeColor=#94A3B8;dashed=1;dashPattern=5 5;" '
                 'edge="1" parent="L0"><mxGeometry relative="1" as="geometry">'
                 '<mxPoint x="%d" y="%d" as="sourcePoint"/><mxPoint x="%d" y="%d" as="targetPoint"/>'
                 '</mxGeometry></mxCell>' % (i,x0,LANE_Y0,x0,LANE_Y1))

# --- diagram layer: nodes
for nid,(x,y,w,h,kind,label) in N.items():
    V("n_"+nid, x, y, w, h, VBASE+DSTYLE[kind], _label(label.split("|")))

# --- diagram layer: edges, carrying the verified waypoints
for k,(a,b,kind,vx,ch,da,db) in enumerate(E):
    pts = RES[(a,b)]
    ax,ay,aw,ah = N[a][:4]; bx,by,bw,bh = N[b][:4]
    ex_,ey_ = (pts[0][0]-ax)/aw, (pts[0][1]-ay)/ah
    nx_,ny_ = (pts[-1][0]-bx)/bw, (pts[-1][1]-by)/bh
    st = (EBASE + DEDGE[kind] + "exitX=%.4f;exitY=%.4f;entryX=%.4f;entryY=%.4f;" % (ex_,ey_,nx_,ny_))
    d.append('        <mxCell id="e_%d" style="%s" edge="1" parent="L1" source="n_%s" target="n_%s">' % (k,st,a,b))
    d.append('          <mxGeometry relative="1" as="geometry"><Array as="points">')
    for px,py in pts[1:-1]:
        d.append('            <mxPoint x="%.1f" y="%.1f"/>' % (px,py))
    d.append('          </Array></mxGeometry>')
    d.append('        </mxCell>')

# --- legend
V("lgbox",16,LEG_Y,W-32,62,"rounded=1;arcSize=6;whiteSpace=wrap;html=1;fillColor=#F8FAFC;strokeColor=#CBD5E1;","","L0")
V("lgt1",30,LEG_Y+8,100,20,"text;html=1;align=left;verticalAlign=middle;fontSize=11.5;fontStyle=1;fontColor=#0F172A;","LINE STYLE","L0")
lx=140
for j,(k,lab) in enumerate([("flow","internal flow / hand-off"),("sync","synchronous call"),
                            ("poll","poll (scheme or partner is asked, repeatedly)"),("async","asynchronous / event")]):
    d.append('        <mxCell id="lge%d" style="endArrow=blockThin;endFill=1;html=1;%s" edge="1" parent="L0">'
             '<mxGeometry relative="1" as="geometry"><mxPoint x="%d" y="%d" as="sourcePoint"/>'
             '<mxPoint x="%d" y="%d" as="targetPoint"/></mxGeometry></mxCell>'
             % (j, DEDGE[k], lx, LEG_Y+20, lx+44, LEG_Y+20))
    V("lgl%d"%j, lx+50, LEG_Y+10, len(lab)*6.2, 20,
      "text;html=1;align=left;verticalAlign=middle;fontSize=11;fontColor=#475569;", lab, "L0")
    lx += 60 + len(lab)*5.9 + 30
V("lgt2",30,LEG_Y+38,100,20,"text;html=1;align=left;verticalAlign=middle;fontSize=11.5;fontStyle=1;fontColor=#0F172A;","BOX","L0")
bx2=140
for j,(kind,lab) in enumerate([("actor","cardholder / channel"),("core","core issuer platform"),("step","platform step"),
                               ("dec","DECISION POINT"),("ext","external — scheme, partner, acquirer"),("note","regulatory clock / note")]):
    V("lgb%d"%j, bx2, LEG_Y+40, 26, 15, "rounded=1;arcSize=20;html=1;"+DSTYLE[kind], "", "L0")
    V("lgbl%d"%j, bx2+31, LEG_Y+38, len(lab)*6.2, 20,
      "text;html=1;align=left;verticalAlign=middle;fontSize=11;fontColor=#475569;", lab, "L0")
    bx2 += 40 + len(lab)*5.9 + 26

d.append('      </root>')
d.append('    </mxGraphModel>')
d.append('  </diagram>')
d.append('</mxfile>')

DOUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dispute-e2e-swimlane.drawio")
open(DOUT,"w",encoding="utf-8").write("\n".join(d))

from xml.parsers import expat as _expat
_p=_expat.ParserCreate(); _p.Parse(open(DOUT,"rb").read(),True)
_ncell = "\n".join(d).count("<mxCell")
print("drawio: well-formed, %d cells -> %s" % (_ncell, os.path.basename(DOUT)))
