; Preserve every native PPU/CHR write offset, as well as total IRQ cycles.
; Y is already zero after delay1: NOP retains LDY #0's two cycles.
; Eight DEC iterations plus PHA/PLA take70cycles (native nine take71).
; LDX zp adds one cycle. PHA/PLA preserves A and balances the IRQ stack.
; The later redundant status read becomes two NOPs: same four cycles.
; The PPU latch is zero after paired2006/2005 writes; scan94 has no vblank.
    STA $F008
    LDA #$01
    STA $F000
    LDY #$0C
    JSR $FC98
    LDA #$08
    STA $47
    LDY #$10
delay1:
    DEY
    BNE @delay1
    LDA $2002
    LDA #$A8
    STA $2000
    LDA #$21
    LDX #$80
    NOP
    STA $2006
    STX $2006
    STY $2005
    STY $2005
delay2:
    DEC $47
    BNE @delay2
    PHA
    PLA
    NOP
    NOP
    LDX $C6
    STX $A000
    INX
    STX $A008
    LDX #$60
    STX $B000
    INX
    STX $B008
    JMP $FD13
