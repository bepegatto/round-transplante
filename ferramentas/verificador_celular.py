import yaml,glob,re,sys
src=sys.argv[1]
W=360  # largura útil típica de celular
res={}
for f in sorted(glob.glob(src+'/Src/scr*.pa.yaml')):
    d=yaml.safe_load(open(f)); scr=list(d['Screens'])[0]
    out=[]
    def walk(ch,par):
        for c in ch:
            n=list(c)[0]; v=c[n]; p=v.get('Properties',{}); ctl=v['Control']
            if n.startswith(('ctnSug','recSug','lblSug','txtSug','btnSug')): continue
            w=str(p.get('Width','')); t=str(p.get('Text',''))
            if 'App.Width < 600' not in w:
                m=re.search(r'(Parent\.(?:Template)?Width)\s*-\s*(\d+)',w)
                if m and int(m.group(2))>=150: out.append((n,'largura encolhe demais',w))
                m2=re.fullmatch(r'=(\d+)',w)
                if m2 and int(m2.group(1))>=300: out.append((n,'largura fixa grande',w))
            if ctl.startswith('Label') and 'AutoHeight' not in p:
                dyn=bool(re.search(r'ThisItem|\bg[A-Z]|&',t))
                h=re.fullmatch(r'=(\d+)',str(p.get('Height','=40')))
                if dyn and h and int(h.group(1))<=40 and not str(p.get('Width','')).startswith('=') is False:
                    out.append((n,'texto variável em altura fixa',p.get('Height','(padrão)')))
            walk(v.get('Children',[]),n)
    walk(d['Screens'][scr]['Children'],scr)
    res[scr]=out
for s,o in res.items():
    from collections import Counter
    print(s,len(o),dict(Counter(x[1] for x in o)))
