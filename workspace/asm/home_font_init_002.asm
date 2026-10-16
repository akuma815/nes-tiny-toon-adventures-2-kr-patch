; Helper bank2 identity02 permits CBF0 to return here after native bank32 call.
; Original home initialization followed by default native font90; original92/2B restored.
LDA #$00
JSR $8DFD
LDA #$32
STA $92
LDA #$5A
STA $06F3
LDA #$04
JSR $F99A
NOP
NOP
JMP $FDDB
