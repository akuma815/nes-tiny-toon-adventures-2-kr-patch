from pathlib import Path
R=Path(__file__).resolve().parents[1]
def main():
 p=R/'scripts/run_cart146.py';assert not p.exists()
 s=(R/'scripts/run_train142.py').read_text('utf-8').replace('142','146').replace('train','cart')
 s=s.replace('scripts/trace_cart_reader146.lua','scripts/trace_train_reader142.lua')
 p.write_text(s,'utf-8');(R/'work/cart146').mkdir(exist_ok=False)
 print('prepared short native cart146; no winningbot or course-completion variant')
if __name__=='__main__':main()
