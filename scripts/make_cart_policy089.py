"""Work89 native-vector-gated2F push controller variant, original ROM untouched."""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def main():
 p=R/'scripts/trace_cart_rounds_v6.lua';runner=R/'scripts/run_cart_rounds_qa_v6.py';assert not p.exists()and not runner.exists()
 s=(R/'scripts/trace_cart_rounds_v5.lua').read_text('utf-8')
 changes=[
 ("local route0=", "local burst_until=0\nlocal release_log=assert(io.open(out..'/cart2F_release_policy.csv','wb'));release_log:write('frame,target,mode,eligible,base_vx,base_vy,alignment,charge,burst_until,A,heading\\n')\nlocal route0="),
 ("if dist<56 and behind then ax,ay=tx+ex*6,ty+ey*6;mode='push'", "if dist<56 and behind and (level==0 or targettype~=0x2f or ((px-tx)*dx+(py-ty)*dy)/(math.max(1,dist)*len)>0.65)then ax,ay=tx+ex*6,ty+ey*6;mode='push'"),
 ("local dx,dy=ax-px,ay-py\n  if frame>=4200 then dx=dx*0.08-vx*0.60;dy=dy*0.08-vy*0.60 end", "local dx,dy=ax-px,ay-py\n  local push2F=frame>=4200 and level>=1 and targettype==0x2f and mode=='push'\n  if push2F then local p=assert(pits[level][1]);dx=(p[1]+p[3])/2-tx;dy=(p[2]+p[4])/2-ty end\n  if frame>=4200 and not push2F then dx=dx*0.08-vx*0.60;dy=dy*0.08-vy*0.60 end"),
 ("else input.a=frame%48<40;if mode~='push'", "else input.a=frame%48<40\n   if level>=1 and targettype==0x2f then\n    local bx,by=signed(0x9d,0x9e),signed(0x9b,0x9c);local p=assert(pits[level][1]);local hx,hy=(p[1]+p[3])/2,(p[2]+p[4])/2\n    local lx,ly=hx-tx,hy-ty;local den=math.sqrt((bx*bx+by*by)*(lx*lx+ly*ly));local alignment=den>0 and (bx*lx+by*ly)/den or 0\n    local charge=r(0xa9)+256*r(0xaa);local dist=math.sqrt((px-tx)^2+(py-ty)^2);local eligible=push2F and alignment>0.80 and dist<48 and charge>=512\n    if eligible and frame>=burst_until then burst_until=frame+16 end\n    if frame<burst_until then input.a=false elseif push2F then input.a=true end\n    release_log:write(string.format('%d,%d,%s,%s,%d,%d,%.6f,%d,%d,%s,%d\\n',frame,target,mode,tostring(eligible),bx,by,alignment,charge,burst_until,tostring(input.a),r(0x510)))\n   end\n   if mode~='push'"),
 ("if frame==limit then log:close()end end,emu.eventType.endFrame)", "if frame==limit then log:close();release_log:close()end end,emu.eventType.endFrame)")]
 for a,b in changes:assert s.count(a)==1,(a,s.count(a));s=s.replace(a,b)
 s=s.replace('Work87: only2F intercept automaticB disabled; pitB retained.', 'Work89:2F strictapproach, nativebasevector alignment-gatedA release16frames; V5 pitB retained.')
 p.write_text(s,'utf-8')
 runner.write_text((R/'scripts/run_cart_rounds_qa_v5.py').read_text('utf-8').replace('trace_cart_rounds_v5.lua','trace_cart_rounds_v6.lua').replace('fullcharge40/48','fullcharge40/48 except2F push nativevector-aligned release16frames andstrictapproach'),'utf-8')
if __name__=='__main__':main()