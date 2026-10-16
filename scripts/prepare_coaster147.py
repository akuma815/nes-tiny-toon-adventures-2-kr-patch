from pathlib import Path
R=Path(__file__).resolve().parents[1]
def main():
 p=R/'scripts/run_coaster147.py';assert not p.exists()
 s=(R/'scripts/run_train142.py').read_text('utf-8').replace('142','147').replace('train','coaster')
 s=s.replace('scripts/trace_coaster_reader147.lua','scripts/trace_train_reader142.lua')
 p.write_text(s,'utf-8');(R/'work/coaster147').mkdir(exist_ok=False);print('prepared no-seed coaster147 reader route')
if __name__=='__main__':main()
