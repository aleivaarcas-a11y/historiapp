import re,sys
ABBR=re.compile(r"(\b(p|pp|c|ca|a|C|cf|vol|vols|no|n\.º|fig|figs|cap|ch|ed|eds|Eds|trad|trans|Trad|Trans|St|Mr|Dr|fís|lib|vv|v|ss|s|f|ff|al|op|cit|ibid|etc|approx|aprox|núm)\.|\b[A-Z]\.|\d\.)$")
def sents(p):
    parts=re.split(r"(?<=[.;?!])\s+",p); out=[]
    for x in parts:
        if out and (ABBR.search(out[-1]) or not re.match(r"[A-ZÁÉÍÓÚÑ¿«\"'(“‘0-9]",x)):
            out[-1]+=' '+x
        else: out.append(x)
    return out
def run(path,pat,outpath):
    R=re.compile(pat)
    t=open(path,encoding='utf-8').read(); res=[]; removed=0
    for line in t.split('\n'):
        if line.startswith('> ') and not line.startswith('> No procede'):
            ss=sents(line[2:]); keep=[s for s in ss if not R.search(s)]; removed+=len(ss)-len(keep)
            if not keep: res.append('>'); continue
            k=' '.join(keep)
            if k.endswith(';'): k=k[:-1]+'.'
            res.append('> '+k)
        else: res.append(line)
    txt='\n'.join(res); txt=re.sub(r"(\n>\n)(>\n)+",r"\1",txt)
    open(outpath,'w',encoding='utf-8').write(txt); print(path,'removed',removed)
ES=r"\bAlex\b|[Pp]antalla|[Ll]a diapositiva (siguiente|anterior|ofrece|compara)|[Ee]sta diapositiva|[Ll]a frase de la diapositiva|pendientes? de (comprobar|cotejo|fuente)|queda pendiente|no se localiza en la biblioteca|[Ss]e corrige|frase funcional|[Ss]e retira|Comprobar edición|comprobar páginas|remisión de la"
EN=r"\bAlex\b|[Oo]n (the )?screen|[Tt]he screen|[Tt]he slide|[Tt]his slide|slide's|following ones need|remains? to be checked|remains pending|remain to be checked|cannot be located in the library|not found in the library|is corrected|are corrected|functional sentence|is withdrawn|withdrawn as a criterion|have left the slide|Check the edition|check the pages"
if sys.argv[1]=='es': run(sys.argv[2],ES,sys.argv[3])
else: run(sys.argv[2],EN,sys.argv[3])
