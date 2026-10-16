from pathlib import Path
R=Path(__file__).resolve().parents[1]
def main():
 p=R/'scripts/run_water143.py';assert not p.exists()
 s=(R/'scripts/run_train142.py').read_text('utf-8').replace('142','143').replace('train','water')
 s=s.replace('scripts/trace_water_reader143.lua','scripts/trace_train_reader142.lua')
 p.write_text(s,'utf-8');(R/'work/water143').mkdir(exist_ok=False)
 print('prepared water143; exact frozen142 reader observer reused')
if __name__=='__main__':main()
