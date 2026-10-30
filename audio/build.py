import json,glob,os,csv,collections,zipfile,numpy as np,soundfile as sf,sys
D='/tmp/claude-0/dl'; OUT=sys.argv[1]; os.makedirs(OUT,exist_ok=True)
FS=16000; rng=np.random.default_rng(252)
# LibriSpeech
tr={}
for f in glob.glob(f'{D}/LibriSpeech/test-clean/*/*/*.trans.txt'):
    for l in open(f): k,t=l.strip().split(' ',1); tr[k]=t
def ls(k):
    s,c,_=k.split('-'); return f'{D}/LibriSpeech/test-clean/{s}/{c}/{k}.flac'
male=['7176-88083-0002','1089-134686-0000','61-70968-0014','7176-88083-0003','1089-134686-0006','61-70968-0011',
      '7176-88083-0004','1089-134686-0008','61-70968-0024','7176-88083-0010','1089-134686-0013','61-70968-0030']
female=['4446-2271-0001','1580-141083-0002','8463-287645-0006','4446-2271-0020','1580-141083-0003','8463-287645-0011',
        '4446-2273-0003','1580-141083-0009','8463-294825-0001','4446-2273-0008','1580-141083-0012','8463-287645-0013']
# speechocean762 children
SO=f'{D}/speechocean762'; age={};gen={};text={};spk={}
for s in ['train','test']:
    for l in open(f'{SO}/{s}/spk2age'): a,b=l.split(); age[a]=int(b)
    for l in open(f'{SO}/{s}/spk2gender'): a,b=l.split(); gen[a]=b
    for l in open(f'{SO}/{s}/text'): a,b=l.strip().split(None,1); text[a]=b
    for l in open(f'{SO}/{s}/utt2spk'): a,b=l.split(); spk[a]=b
sc=json.load(open(f'{SO}/resource/scores.json'))
by=collections.defaultdict(list)
for u in sorted(text):
    s=spk[u]
    if 9<=age[s]<=12 and sc[u]['accuracy']>=9 and sc[u]['fluency']>=9 and sc[u]['prosodic']>=8 and len(text[u].split())>=6:
        by[s].append(u)
kids=['6121','5195','2179','6504','5072','3208']
want={'6121':6,'5195':6,'2179':6,'6504':2,'5072':2,'3208':2}
child=[]
for s in kids:
    us=by[s][:want[s]]
    for i in range(0,len(us),2): child.append((s,us[i],us[i+1]))
assert len(child)==12, len(child)
child=[child[k] for k in [0,3,6,9,1,4,7,10,2,5,8,11]]
def so(u): return f'{SO}/WAVE/SPEAKER{int(spk[u]):04d}/{u}.WAV'
# noise
import io
noise={}
for e,ch in [('PCAFETER','ch01'),('STRAFFIC','ch01')]:
    z=zipfile.ZipFile(f'{D}/{e}.zip'); n=[x for x in z.namelist() if x.endswith(f'{ch}.wav')][0]
    x,fs=sf.read(io.BytesIO(z.read(n))); assert fs==FS; noise[e]=x
def mono(x): return x.mean(1) if x.ndim>1 else x
def rms(x): return np.sqrt(np.mean(x**2))
rows=[]
cats={'M':[(ls(k),k,tr[k],'LibriSpeech test-clean',k.split('-')[0]) for k in male],
      'F':[(ls(k),k,tr[k],'LibriSpeech test-clean',k.split('-')[0]) for k in female],
      'C':[(None,(a,b),text[a]+' / '+text[b],'speechocean762',s) for s,a,b in child]}
idx=0
for cat,items in cats.items():
    for i,it in enumerate(items):
        path,key,txt,src,sp=it
        if cat=='C':
            a,b=key; xa,_=sf.read(so(a)); xb,_=sf.read(so(b))
            x=np.concatenate([mono(xa),np.zeros(int(.6*FS)),mono(xb)]); srcid=f'{a}+{b}'
            note=f'child age {age[sp]}, {"girl" if gen[sp]=="f" else "boy"}'
        else:
            x,fs=sf.read(path); assert fs==FS; x=mono(x); srcid=key; note=''
        design='ABC'[i//4]; cond='quiet' if i%4<2 else 'noisy'
        nz=''; snr=''
        if cond=='noisy':
            e='PCAFETER' if i%4==2 else 'STRAFFIC'
            n=noise[e]; st=rng.integers(0,len(n)-len(x)); n=n[st:st+len(x)]
            n=n*rms(x)/rms(n)/10**(5/20); x=x+n; nz=e; snr='+5 dB'
        x=0.9*x/np.max(np.abs(x))
        name=f'set{design}_{cat}_{cond}_{sum(1 for r in rows if r["set"]==design and r["speaker"]==cat and r["condition"]==cond)+1}.wav'
        sf.write(f'{OUT}/{name}',x,FS,subtype='PCM_16')
        rows.append(dict(file=name,set=design,speaker=cat,condition=cond,noise=nz,snr=snr,duration_s=round(len(x)/FS,1),
                         source=src,source_id=srcid,speaker_id=sp,note=note,transcript=txt))
with open(f'{OUT}/manifest.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(sorted(rows,key=lambda r:r['file']))
for r in sorted(rows,key=lambda r:r['file']): print(r['file'],r['duration_s'],r['source_id'],r['noise'],r['transcript'][:60])
