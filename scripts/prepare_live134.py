from pathlib import Path
R=Path(__file__).resolve().parents[1]
p=R/'scripts/run_live134.py';assert not p.exists()
s=(R/'scripts/run_branch_seed_qa.py').read_text('utf-8').replace("('trace_branch_seed_v1.lua','trace_branch_seed_irq_v1.lua')","('trace_live_page134.lua',)")
s=s.replace("'scope':'Controlled ticket/point branch QA. Numerical state intentionally seeded; direct visual review separate; no full playthrough.'","'scope':'Read-only live page/IRQ timing and RAM1B/RAM22 telemetry apart from declared initial ticket seed. No screenshots, ROM/state edits, fullplay or global equivalence.'")
p.write_text(s,'utf-8')
