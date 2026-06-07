import streamlit as st
import itertools
import random
import math
import pandas as pd

st.set_page_config(page_title="Pick 3 & Pick 4 Rundown Systems", page_icon="🎰", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
.mh{background:linear-gradient(135deg,#1a1a2e,#0f3460);padding:2rem;border-radius:12px;margin-bottom:1.5rem;text-align:center;}
.mh h1{font-size:2.2rem;margin:0;color:#f0c040;}
.mh p{font-size:1rem;margin:0.4rem 0 0;color:#a0c4ff;}
.card{background:#1e2a3a;border:1px solid #2e4060;border-radius:10px;padding:1rem 1.2rem;margin-bottom:0.8rem;color:#dce6f0;}
.card h4{color:#f0c040;margin-top:0;}
.tb{display:inline-block;background:#0f3460;border:1px solid #f0c040;border-radius:6px;padding:0.3rem 0.7rem;margin:0.2rem;font-family:monospace;font-size:1.05rem;font-weight:bold;color:#f0c040;letter-spacing:0.12em;}
.sr{background:#0f3460;border:2px solid #f0c040;border-radius:10px;padding:1rem 1.2rem;margin:0.8rem 0;color:white;}
.sr h3{color:#f0c040;margin-top:0;}
.mc{background:#1e2a3a;border-radius:10px;padding:0.9rem;text-align:center;border:1px solid #2e4060;}
.mc .v{font-size:1.7rem;font-weight:bold;color:#f0c040;}
.mc .l{font-size:0.82rem;color:#a0c4ff;margin-top:0.15rem;}
.ne{color:#e17055!important;}
.pe{color:#00b894!important;}
.wb{background:#2d1a0e;border-left:4px solid #e17055;padding:0.8rem 1rem;border-radius:0 8px 8px 0;margin:0.8rem 0;color:#ffeaa7;}
.ib{background:#0d2137;border-left:4px solid #74b9ff;padding:0.8rem 1rem;border-radius:0 8px 8px 0;margin:0.8rem 0;color:#dce6f0;}
</style>
""", unsafe_allow_html=True)

def dchk(s):
    d=[int(x) for x in s]; sm=sum(d)
    od=sum(1 for x in d if x%2!=0); ev=len(d)-od
    c={}
    for x in d: c[x]=c.get(x,0)+1
    return d,sm,od,ev,len(set(d)),sorted(c.values(),reverse=True)

def oe_lbl(od,ev):
    if ev==0: return "All Odd"
    if od==0: return "All Even"
    return "Mixed"

def fp(digs):
    return sorted(set("".join(p) for p in itertools.permutations([str(d) for d in digs])))

def r123(digs):
    base=fp(digs); ex=[]
    for d in digs:
        for d2 in digs:
            if d!=d2: ex+=[str(d)+str(d)+str(d2),str(d)+str(d2)+str(d),str(d2)+str(d)+str(d)]
    return sorted(set(base+ex))

def r317(digs):
    tix=[]; mid=digs[len(digs)//2]; oth=[d for d in digs if d!=mid]
    for a in oth:
        for b in oth: tix.append(str(a)+str(mid)+str(b))
    for p in itertools.permutations([str(d) for d in digs]): tix.append("".join(p))
    return sorted(set(tix))

def r238(digs):
    base=fp(digs)
    r=[t for t in base if sum(int(d) for d in t)<=20]
    return r if r else base

def rwhl(digs):
    k=min(3,len(digs)); tix=[]
    for combo in itertools.combinations(digs,k):
        for p in itertools.permutations(combo): tix.append("".join(str(d) for d in p))
    return sorted(set(tix))[:20]

def gen(method,digs,game):
    n=3 if game=="Pick 3" else 4
    d=digs[:n] if len(digs)>=n else digs
    if method=="Full Permutation": return fp(d)
    if method=="123 Simple Rundown": return r123(d) if game=="Pick 3" else fp(d)
    if method=="317 Pattern-Based": return r317(d)
    if method=="238 Reduction Rundown": return r238(d)
    if method=="Condensed Wheel": return rwhl(d)
    return fp(d)

def s3(s):
    d,sm,od,ev,u,fr=dchk(s); oe=oe_lbl(od,ev)
    cons=len(d)>1 and all(abs(d[i+1]-d[i])==1 for i in range(len(d)-1))
    if fr[0]==3: return "Straight Play Only","Triple digits - only 1 combination.","🔴"
    if fr[0]==2:
        if sm<=13: return "317 Pattern-Based","Double digits, low sum - pattern covers key combos cheaply.","🟡"
        return "Box-Weighted Rundown","High-sum doubles hit boxed plays frequently.","🟠"
    if cons: return "238 Reduction Rundown","Consecutive digits - reduction targets skewed positions.","🟢"
    if oe=="All Odd": return "238 Reduction Rundown","All-odd - reduction prunes low-prob combos.","🟢"
    if oe=="All Even": return "238 Reduction Rundown","All-even - reduction is most cost-effective.","🟢"
    if sm<=13: return "123 Simple Rundown","All-different, low sum - 6 permutations at low cost.","🟢"
    return "Full Permutation","High-sum mixed - play all permutations.","🔵"

def s4(s):
    d,sm,od,ev,u,fr=dchk(s); oe=oe_lbl(od,ev)
    if fr[0]==4: return "Straight Play Only","Quad digits - only 1 combination.","🔴"
    if fr[0]==3: return "317 Pattern-Based","Triple+1 - pattern isolates key position combos.","🟡"
    if fr[0]==2 and len(fr)>1 and fr[1]==2: return "238 Reduction Rundown","Two pairs - reduction eliminates redundant combos.","🟢"
    if fr[0]==2: return "Condensed Wheel","One pair+2 different - wheel guarantees partial hits.","🔵"
    if 0 in d: return "Condensed Wheel","Contains 0 - wheel covers zero-position combos.","🔵"
    if oe=="All Odd": return "238 Reduction Rundown","All-odd - reduction to highest-value combos.","🟢"
    if oe=="All Even": return "238 Reduction Rundown","All-even - reduction most cost-effective.","🟢"
    if sm<=18: return "123 Simple Rundown","All-unique, low sum - covers max combos at low cost.","🟢"
    return "Full Permutation","High-sum all-different - full permutation.","🔵"

METHS=["Full Permutation","123 Simple Rundown","317 Pattern-Based","238 Reduction Rundown","Condensed Wheel","Box-Weighted Rundown"]

st.sidebar.markdown("## 🎰 Navigation")
page=st.sidebar.radio("Go to",["🏠 Overview","🎯 Live Play Selector","🧮 Rundown Calculator","📊 EV & Probability","🎲 Monte Carlo Simulator","📚 Methods Reference","✅ Checklist"])
st.sidebar.markdown("---")
st.sidebar.markdown("<div class='wb' style='font-size:0.8rem;'>⚠️ <b>Disclaimer</b><br>For research use only. Lottery play carries negative EV. No system eliminates house edge.</div>",unsafe_allow_html=True)
st.sidebar.caption("Prepared for Hass · May 2026 · v1.0")

if page=="🏠 Overview":
    st.markdown("<div class='mh'><h1>🎰 Pick 3 & Pick 4 Rundown Systems</h1><p>A Structured Examination of Methods, Mathematics, and Practical Guidance</p><p style='color:#74b9ff;font-size:0.85rem;'>Prepared for Hass · Research Report v1.0 · May 2026 · Newark, NJ</p></div>",unsafe_allow_html=True)
    c1,c2,c3,c4=st.columns(4)
    with c1: st.markdown("<div class='mc'><div class='v'>6</div><div class='l'>Rundown Methods</div></div>",unsafe_allow_html=True)
    with c2: st.markdown("<div class='mc'><div class='v'>1,000</div><div class='l'>Pick 3 Outcomes</div></div>",unsafe_allow_html=True)
    with c3: st.markdown("<div class='mc'><div class='v'>10,000</div><div class='l'>Py</p></div>",unsafe_allow_html=True)
    st.markdown("<div class='ib'>After any Pick 3 or Pick 4 number is drawn, use the selector to instantly know which rundown to run.</div>",unsafe_allow_html=True)
    gs=st.selectbox("Select Game",["Pick 3","Pick 4"],key="lg")
    dn=3 if gs=="Pick 3" else 4
    drw=st.text_input(f"Enter the Drawn Number ({dn} digits, 0-9)",max_chars=dn)
    if drw:
        drw=drw.strip()
        if not drw.isdigit() or len(drw)!=dn:
            st.error(f"Please enter exactly {dn} digits.")
        else:
            digs,dsum,odds,evens,uniq,freq=dchk(drw); oe=oe_lbl(odds,evens)
            st.markdown("---"); st.subheader("Digit Analysis")
            p1,p2,p3,p4=st.columns(4)
            pat="All Same" if freq[0]==dn else ("Has Repeats" if freq[0]>1 else "All Different")
            with p1: st.markdown(f"<div class='mc'><div class='v'>{drw}</div><div class='l'>Drawn</div></div>",unsafe_allow_html=True)
            with p2: st.markdown(f"<div class='mc'><div class='v'>{dsum}</div><div class='l'>Sum</div></div>",unsafe_allow_html=True)
            with p3: st.markdown(f"<div class='mc'><div class='v'>{oe}</div><div class='l'>Odd/Even</div></div>",unsafe_allow_html=True)
            with p4: st.markdown(f"<div class='mc'><div class='v'>{pat}</div><div class='l'>Pattern</div></div>",unsafe_allow_html=True)
            st.markdown("---"); st.subheader("Recommended Rundown")
            meth,reason,dot=s3(drw) if gs=="Pick 3" else s4(drw)
            st.markdown(f"<div class='sr'><h3>{dot} {meth}</h3><p style='margin:0;color:#a0c4ff;'>{reason}</p></div>",unsafe_allow_html=True)
            if meth!="Straight Play Only":
                bd=list(dict.fromkeys(digs))
                m=meth.replace(" (Extended)","").replace(" + Boxed","")
                tix=gen(m if m in METHS else "Full Permutation",bd,gs)
                st.markdown("".join(f"<span class='tb'>{t}</span>" for t in tix),unsafe_allow_html=True)
                st.markdown(f"**{len(tix)} tickets**")
            st.markdown("---"); st.subheader("Three Quick Checks")
            thr="<=13 Low/>=14 High" if gs=="Pick 3" else "<=18 Low/>=19 High"
            is_low=(dsum<=13) if gs=="Pick 3" else (dsum<=18)
            st.dataframe(pd.DataFrame({"Check":["1. Digit Type","2. Sum","3. Odd/Even"],"Result":[pat,f"{dsum} ({'Low' if is_low else 'High'})",oe]}),use_container_width=True,hide_index=True)
    with st.expander("Pick 3 Selector Reference"):
        st.dataframe(pd.DataFrame({"Pattern":["Triple","Double Low","Double High","All Odd","All Even","Mixed Low","Mixed High","Consecutive"],"Method":["Straight only","317 Pattern","Box-Weighted","238 Reduction","238 Reduction","123 Simple","Full Perm","238 Reduction"]}),use_container_width=True,hide_index=True)
    with st.expander("Pick 4 Selector Reference"):
        st.dataframe(pd.DataFrame({"Pattern":["Quad","Triple+1","Two Pairs","One Pair+2","All Diff Low","All Diff High","All Odd","All Even","Has 0"],"Method":["Straight only","317 Pattern","238 Reduction","Condensed Wheel","123 Simple","Full Perm","238 Reduction","238 Reduction","Condensed Wheel"]}),use_container_width=True,hide_index=True)

elif page=="🧮 Rundown Calculator":
    st.markdown("<div class='mh'><h1>🧮 Rundown Calculator</h1><p>Enter base digits and select a method to generate your complete ticket list</p></div>",unsafe_allow_html=True)
    cl,cr=st.columns([1,1.5])
    with cl:
        game=st.selectbox("Game",["Pick 3","Pick 4"])
        meth=st.selectbox("Method",METHS)
        nb=3 if game=="Pick 3" else 4
        bc=st.columns(nb); bd=[]
        for i,col in enumerate(bc):
            with col:
                d=st.number_input(f"D{i+1}",min_value=0,max_value=9,value=min(i+1,9),step=1,key=f"b{i}")
                bd.append(int(d))
        wager=st.number_input("Wager/ticket ($)",min_value=0.50,max_value=5.0,value=1.0,step=0.50)
    with cr:
        tix=gen(meth,bd,game); tot=1000 if game=="Pick 3" else 10000
        pstr=len(tix)/tot; pay=500 if game=="Pick 3" else 5000
        evstr=pstr*pay-len(tix)*wager
        m1,m2,m3,m4=st.columns(4)
        with m1: st.markdown(f"<div class='mc'><div class='v'>{len(tix)}</div><div class='l'>Tickets</div></div>",unsafe_allow_html=True)
        with m2: st.markdown(f"<div class='mc'><div class='v'>${len(tix)*wager:.2f}</div><div class='l'>Cost</div></div>",unsafe_allow_html=True)
        with m3: st.markdown(f"<div class='mc'><div class='v'>{pstr*100:.2f}%</div><div class='l'>Coverage</div></div>",unsafe_allow_html=True)
        with m4:
            cls="ne" if evstr<0 else "pe"
            st.markdown(f"<div class='mc'><div class='v {cls}'>${evstr:.2f}</div><div class='l'>EV</div></div>",unsafe_allow_html=True)
        st.markdown("".join(f"<span class='tb'>{t}</span>" for t in tix),unsafe_allow_html=True)

elif page=="📊 EV & Probability":
    st.markdown("<div class='mh'><h1>📊 EV & Probability</h1><p>Mathematical basis of rundown coverage and expected returns</p></div>",unsafe_allow_html=True)
    st.subheader("Single-Ticket Probabilities")
    st.dataframe(pd.DataFrame({"Game":["Pick 3","Pick 3","Pick 4","Pick 4"],"Play":["Straight","Boxed 3-distinct","Straight","Boxed 4-distinct"],"Outcomes":["1,000","1,000","10,000","10,000"],"P(Win)":["0.1%","0.6%","0.01%","0.24%"]}),use_container_width=True,hide_index=True)
    st.markdown("---"); st.subheader("Expected Value Calculator")
    st.markdown("<div class='ib'><b>EV = (n/total) x Payout - (n x cost)</b><br>Negative EV confirms house edge is preserved regardless of rundown strategy.</div>",unsafe_allow_html=True)
    col1,col2=st.columns(2)
    with col1:
        eg=st.selectbox("Game",["Pick 3","Pick 4"],key="eg")
        nt=st.slider("Tickets",1,24,6)
        we=st.number_input("Wager ($)",0.50,5.0,1.0,0.50,key="we")
    with col2:
        to=1000 if eg=="Pick 3" else 10000
        sp=st.number_input("Straight Payout ($)",value=500 if eg=="Pick 3" else 5000)
        bp=st.number_input("Boxed Payout ($)",value=80 if eg=="Pick 3" else 200)
    ps=nt/to; tc=nt*we; evs=ps*sp-tc
    m1,m2,m3=st.columns(3)
    with m1: st.markdown(f"<div class='mc'><div class='v'>{ps*100:.3f}%</div><div class='l'>P(Straight)</div></div>",unsafe_allow_html=True)
    with m2: st.markdown(f"<div class='mc'><div class='v'>${tc:.2f}</div><div class='l'>Total Cost</div></div>",unsafe_allow_html=True)
    with m3:="sm")
        sdr=st.text_input("Base Digits (comma separated)",value="1,2,3" if sg=="Pick 3" else "1,2,3,4")
    with c2:
        nt2=st.select_slider("Simulated Draws",[10000,50000,100000,250000,500000],value=100000)
        sw=st.number_input("Wager ($)",0.50,5.0,1.0,0.50,key="sw")
        run=st.button("Run Simulation",type="primary",use_container_width=True)
    if run:
        try:
            sd=[int(x.strip()) for x in sdr.split(",")]
            assert all(0<=x<=9 for x in sd)
        except: st.error("Please enter valid digits 0-9."); st.stop()
        with st.spinner(f"Running {nt2:,} simulated draws..."):
            tix=gen(sm,sd,sg); ts=set(tix)
            pay=500 if sg=="Pick 3" else 5000; bpay=80 if sg=="Pick 3" else 200
            sh=bh=0; tp=0.0; dl=3 if sg=="Pick 3" else 4
            for _ in range(nt2):
                draw="".join(str(random.randint(0,9)) for _ in range(dl))
                if draw in ts: sh+=1; tp+=pay
                elif sorted(draw) in [sorted(t) for t in tix[:10]]: bh+=1; tp+=bpay
            tc2=nt2*len(tix)*sw; nr=tp-tc2; roi=tp/tc2*100 if tc2>0 else 0
        r1,r2,r3,r4=st.columns(4)
        with r1: st.markdown(f"<div class='mc'><div class='v'>{sh:,}</div><div class='l'>Straight Hits</div></div>",unsafe_allow_html=True)
        with r2: st.markdown(f"<div class='mc'><div class='v'>{bh:,}</div><div class='l'>Boxed Hits</div></div>",unsafe_allow_html=True)
        with r3:
            nc="ne" if nr<0 else "pe"
            st.markdown(f"<div class='mc'><div class='v {nc}'>${nr:,.2f}</div><div class='l'>Net Return</div></div>",unsafe_allow_html=True)
        with r4:
            rc="ne" if roi<100 else "pe"
            st.markdown(f"<div class='mc'><div class='v {rc}'>{roi:.1f}%</div><div class='l'>ROI</div></div>",unsafe_allow_html=True)
        st.markdown("".join(f"<span class='tb'>{t}</span>" for t in tix),unsafe_allow_html=True)
        st.markdown(f"<div class='wb'>After {nt2:,} draws: net return <b>${nr:,.2f}</b> ({roi:.1f}% ROI). House margin is preserved regardless of coverage strategy.</div>",unsafe_allow_html=True)

elif page=="📚 Methods Reference":
    st.markdown("<div class='mh'><h1>📚 Methods Reference</h1><p>Complete guide to all rundown methods with worked examples</p></div>",unsafe_allow_html=True)
    mdata=[("Full Permutation","Low","All permutations of chosen distinct digits played as straight tickets.","1,2,3 -> 123,132,213,231,312,321",["Max coverage","Simple"],["Higher cost"]),("123 Simple Rundown","Low","All permutations of 3 distinct digits, optionally augmented with repeats.","Base 1,2,3 -> all 6 perms",["Low cost","Good for low-sum mixed draws"],["No edge over randomness"]),("317 Pattern-Based","Medium","Fixes the middle digit; varies first and last positions.","Fix 1, vary 3 and 7",["Targeted coverage","Lower cost"],["Pattern assumptions statistically unfounded"]),("238 Reduction Rundown","Medium","Full permutation base with reduction rules applied.","Base 2,3,8 drop combos with sum>20",["Better cost control"],["Reduction rules are heuristic"]),("Condensed Wheel","High","Guarantees every 3-element subset covered in at least one ticket.","5 digits -> wheel ensuring partial match",["Conditional partial-hit guarantee"],["Guarantee is conditional on digit set"]),("Box-Weighted Rundown","Low-Med","Combinations played exclusively as boxed tickets.","Play all perms boxed only",["Higher hit frequency"],["Lower payout per win"])]
    for name,cx,desc,ex,pros,cons in mdata:
        with st.expander(f"{name} - Complexity: {cx}"):
            a,b=st.columns([2,1])
            with a:
                st.markdown(f"**Description:** {desc}")
                st.markdown(f"**Example:** `{ex}`")
            with b:
                st.markdown("**Pros:**")
                for p in pros: st.markdown(f"- {p}")
                st.markdown("**Cons:**")
                for c in cons: st.markdown(f"- {c}")
    st.markdown("---"); st.subheader("Section 5 - Criticisms & Limitations")
    for title,desc in [("No Edge Over Randomness","Rundowns cannot alter the random nature of lottery draws. Each draw is independent."),("Negative Expected Value","All state lotteries return less to players than is wagered. Rundowns inherit the same negative EV."),("Gambler Fallacy Risk","Hot/cold digit analysis rests on the gambler's fallacy. Prior draws are statistically irrelevant."),("Cost vs Payout Tradeoff","Systems can create a psychological impression of profit even when costs exceed payouts."),("Regulatory Notes","Misrepresenting systems as guaranteed profit may constitute deceptive advertising."),("Problem Gambling Risk","Frequent small wins can reinforce gambling behavior. Always include responsible gambling disclosures.")]:
        st.markdown(f"<div class='card'><h4>{title}</h4><p style='margin:0;color:#a0c4ff;'>{desc}</p></div>",unsafe_allow_html=True)

elif page=="✅ Checklist":
    st.markdown("<div class='mh'><h1>✅ Rundown Report Checklist</h1><p>Quick checklist for building a complete and responsibly presented rundown report</p></div>",unsafe_allow_html=True)
    items=[("Define game rules and payout table","Specify Pick 3/4, play types, and exact payouts."),("List base digits and generation rules","Document the digit set and wheel/permutation/reduction logic."),("Show exact ticket list or algorithm","Enumerate every ticket or provide a deterministic algorithm."),("Compute coverage and expected value","Calculate coverage fraction and EV for each prize tier."),("Simulate draws and report hit rates","Run 100k+ simulated draws. Report hit frequency and ROI."),("Include responsible gambling disclosure","State clearly that no system eliminates negative EV."),("Cite the payout table source","Reference the specific payout table version and date.")]
    checks={}
    for i,(item,guide) in enumerate(items):
        a,b=st.columns([0.05,0.95])
        with a: checks[i]=st.checkbox("",key=f"chk{i}")
        with b:
            col="#00b894" if checks.get(i) else "#dce6f0"
            st.markdown(f"<div style='padding:0.5rem 0;border-bottom:1px solid #2e4060;'><span style='font-weight:bold;color:{col};'>{item}</span><br><span style='color:#a0c4ff;font-size:0.85rem;'>{guide}</span></div>",unsafe_allow_html=True)
    done=sum(checks.values()); total=len(items)
    st.markdown("---")
    st.subheader(f"Progress: {done}/{total} ({int(done/total*100) if total else 0}%)")
    st.progress(done/total if total else 0)
    st.markdown("---"); st.subheader("Section 6 - Recommendations")
    for i,(title,rec) in enumerate([("Be explicit about assumptions","State play type, wager, payout table, and any reduction rules used."),("Include EV calculations","Compute expected monetary return for best-case and typical-case."),("Provide reproducible examples","Share the complete ticket list or the algorithm used."),("Warn about limitations prominently","Emphasize that no system improves long-term expected returns."),("Add simulation if building software","Implement simulation showing empirical hit frequency and variance."),("Cite the payout table source","Payout tables change - always reference the specific version.")],1):
        st.markdown(f"<div class='card'><h4>{i}. {title}</h4><p style='margin:0;color:#a0c4ff;'>{rec}</p></div>",unsafe_allow_html=True)
    st.markdown("<div class='wb'><b>Important Disclaimer</b><br>No rundown system can change the fundamental mathematics of a lottery. This tool is for research and analytical purposes only.<br><br>Problem Gambling Helpline: <b>1-800-522-4700</b></div>",unsafe_allow_html=True)

        ec="ne" if evs<0 else "pe"
        st.markdown(f"<div class='mc'><div class='v {ec}'>${evs:.2f}</div><div class='l'>EV (Straight)</div></div>",unsafe_allow_html=True)
    st.markdown(f"<div class='wb'>EV=({nt}/{to:,})x${sp:,}-${tc:.2f}=<b>${evs:.2f}</b>. Rundowns reduce variance but do not improve long-run returns.</div>",unsafe_allow_html=True)
    st.markdown("---"); st.subheader("Coverage vs EV")
    rows=[{"Tickets":n,"P3 Coverage":f"{n/1000*100:.1f}%","P3 EV":f"${(n/1000)*500-n:.2f}","P4 Coverage":f"{n/10000*100:.3f}%","P4 EV":f"${(n/10000)*5000-n:.2f}"} for n in [1,2,3,4,6,8,12,24]]
    st.dataframe(pd.DataFrame(rows),use_container_width=True,hide_index=True)

elif page=="🎲 Monte Carlo Simulator":
    st.markdown("<div class='mh'><h1>🎲 Monte Carlo Simulator</h1><p>Run virtual draws to see empirical hit frequency</p></div>",unsafe_allow_html=True)
    c1,c2=st.columns(2)
    with c1:
        sg=st.selectbox("Game",["Pick 3","Pick 4"],key="sg")
        sm=st.selectbox("Method",METHS,keyick 4 Outcomes</div></div>",unsafe_allow_html=True)
    with c4: st.markdown("<div class='mc'><div class='v ne'>−$3</div><div class='l'>EV per $6 Rundown</div></div>",unsafe_allow_html=True)
    st.markdown("---")
    st.subheader("📋 Executive Summary")
    st.markdown("A **rundown system** for Pick 3 and Pick 4 is a structured method players use to cover many number combinations efficiently while reducing cost and increasing the chance of a partial win. This interactive tool covers all 6 methods with worked examples, probability calculations, EV analysis, and Monte Carlo simulation.")
    st.markdown("### 🔑 Key Findings")
    for icon,title,desc in [("🎯","Coverage Tools Only","Rundowns do not alter the underlying probability of any individual draw outcome."),("📐","Method Differences","Common methods differ primarily in coverage breadth, ticket count, and target hit profile."),("📉","Negative EV","Expected value for lottery play is negative in virtually all jurisdictions; rundowns do not improve long-run returns."),("📝","Research Best Practice","Always pair rundown descriptions with explicit EV calculations, reproducible ticket lists, and limitation disclosures.")]:
        st.markdown(f"<div class='card'><h4>{icon} {title}</h4><p style='margin:0;'>{desc}</p></div>",unsafe_allow_html=True)
    st.markdown("---")
    st.subheader("📖 Key Term Definitions")
    terms={"Base Set":"The small group of digits selected by the player from which all rundown combinations are derived.","Coverage":"The proportion of all possible draw outcomes represented within the rundown ticket list.","Hit Profile":"The set of prize types the rundown is capable of producing - straight wins, boxed wins, two-digit matches.","Wheel":"A combinatorial construction guaranteeing a partial match if winning digits include a minimum subset of chosen digits.","Reduction Rule":"A filter applied to a larger candidate set to remove lower-priority combinations.","Cost":"Total monetary stake required to play every ticket at the chosen wager amount."}
    cols=st.columns(2)
    for i,(term,dfn) in enumerate(terms.items()):
        with cols[i%2]: st.markdown(f"<div class='card'><h4>{term}</h4><p style='margin:0;color:#a0c4ff;'>{dfn}</p></div>",unsafe_allow_html=True)
