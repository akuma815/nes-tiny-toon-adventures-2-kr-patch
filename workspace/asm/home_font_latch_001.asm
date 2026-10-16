; OriginFB0D, whole original39bytes. C7 remains source profile-derived.
; 06F3 XOR5A encodes selected font; RAM clear0 safely decodes native90.
; EOR2+NOP2 replace redundant2002 read4 cycles; prior2006/2005 pairs
; have restored the PPU address latch. Real IRQ/PPU evidence still required.
    LDA $06EA
    ASL A
    TAY
    LDA $06F3
    EOR #$5A
    STA $C6
    LDA $FB35,Y
    STA $C7
    NOP
    LDX $C6
    STX $A000
    INX
    STX $A008
    LDX $C7
    STX $B000
    INX
    STX $B008
    JMP $FD13
